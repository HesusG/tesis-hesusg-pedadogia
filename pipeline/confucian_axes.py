"""Confucian concept-axes MVP — Analects-grounded bipolar projection + A/B test.

Each axis is a BIPOLAR direction in embedding space:

    positive pole = centroid of the actual Analects passages about the value
                    (retrieved from the indexed 'analectas_confucio' collection
                    using the concept's anchor phrases as queries — Confucius's
                    own words, not paraphrases)
    negative pole = centroid of constructed modern-policy contrast phrases
    axis          = normalize(pos_centroid - neg_centroid)

A document's score on an axis is the per-chunk projection, z-scored against the
policy-corpus background. We A/B THREE candidate axis sets (config.AXIS_SETS) and
pick the one that best (a) separates the Analects from a legalistic control and
(b) discriminates among real policies. Writes web/data/confucian_mvp.json.

Usage:
    python -m pipeline.confucian_axes
"""
import json
import click
import numpy as np

from .config import (
    CHROMA_DIR, WEB_DATA_DIR, CONFUCIAN_MVP_JSON,
    POLICY_READ_COLLECTION_NAME, ANALECTS_COLLECTION_NAME,
    CONFUCIAN_AXES, AXIS_SETS, MVP_POLICY_IDS, MVP_CONTROL_NEG_POLICY_ID,
    CHINA_MVP_POLICY, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_LOCAL,
)
from .preprocess import clean_text
from .ingest import chunk_text
from .embeddings import get_embedding_function
from .export import NumpyEncoder

DOC_LABELS = {
    "china_ngaidp_2017": {"label": "China · New Gen AI Development Plan 2017",
                          "country": "china", "region": "asia"},
    "colombia_conpes_3975_2019": {"label": "Colombia · CONPES 3975",
                                  "country": "colombia", "region": "latinoamerica"},
    "canada_pan_canadian_ai_strategy_2017": {"label": "Canadá · Pan-Canadian AI Strategy",
                                             "country": "canada", "region": "norteamerica"},
    "eu_ai_act_2024": {"label": "UE · AI Act 2024 (control legal)",
                       "country": "ue", "region": "europa"},
    "analects": {"label": "Analectas de Confucio (control confuciano)",
                 "country": "china", "region": "asia"},
}


def l2norm(mat: np.ndarray) -> np.ndarray:
    mat = np.asarray(mat, dtype=float)
    if mat.ndim == 1:
        mat = mat.reshape(1, -1)
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return mat / norms


def get_client():
    import chromadb
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_vectors(collection, policy_id: str | None = None) -> np.ndarray:
    """L2-normalized chunk vectors for a document (or the whole collection)."""
    kwargs = {"include": ["embeddings"]}
    if policy_id is not None:
        kwargs["where"] = {"policy_id": policy_id}
    res = collection.get(**kwargs)
    embs = res["embeddings"]
    if embs is None or len(embs) == 0:
        raise ValueError(f"No embeddings for policy_id={policy_id!r}")
    return l2norm(np.array(embs))


def ensure_china_doc(policy_col):
    """The China policy is absent from the stored v1 collection; ingest on demand."""
    pid = CHINA_MVP_POLICY["policy_id"]
    if policy_col.get(where={"policy_id": pid}, include=[])["ids"]:
        return
    raw_file = CHINA_MVP_POLICY["raw_file"]
    click.echo(f"  China policy '{pid}' not found — ingesting from {raw_file.name}")
    cleaned = clean_text(raw_file.read_text(encoding="utf-8"))
    chunks = chunk_text(cleaned, CHUNK_SIZE, CHUNK_OVERLAP)
    ids = [f"{pid}_chunk_{i:04d}" for i in range(len(chunks))]
    metadatas = [
        {"policy_id": pid, "country": CHINA_MVP_POLICY["country"],
         "region": CHINA_MVP_POLICY["region"], "year": CHINA_MVP_POLICY["year"],
         "language": CHINA_MVP_POLICY["language"], "chunk_index": i}
        for i in range(len(chunks))
    ]
    for start in range(0, len(chunks), 500):
        end = min(start + 500, len(chunks))
        policy_col.add(documents=chunks[start:end], ids=ids[start:end],
                       metadatas=metadatas[start:end])
    click.echo(f"  Ingested {len(chunks)} China chunks")


def analects_centroid(analects_col, queries, k=3) -> np.ndarray:
    """Positive pole = mean embedding of the top Analects passages for the concept."""
    vecs = []
    for q in queries:
        r = analects_col.query(query_texts=[q], n_results=k, include=["embeddings"])
        vecs.extend(r["embeddings"][0])
    return np.mean(np.array(vecs), axis=0)


def build_axis(mode, embedding_fn, analects_col, ax) -> np.ndarray:
    """Bipolar axis under one anchor strategy.

    theory   : positive pole = modern paraphrases (my phrases)
    grounded : positive pole = centroid of retrieved Analects passages
    hybrid   : positive pole = average of the two (classical + policy register)
    The negative pole is always the constructed modern-policy contrast.
    """
    para = np.array(embedding_fn(ax["pos_anchors_en"] + ax["pos_anchors_es"]))
    neg = np.mean(np.array(embedding_fn(ax["neg_anchors_en"] + ax["neg_anchors_es"])), axis=0)
    if mode == "theory":
        pos = para.mean(axis=0)
    elif mode == "grounded":
        pos = analects_centroid(analects_col, ax["pos_anchors_en"] + ax["pos_anchors_es"])
    else:  # hybrid
        gc = analects_centroid(analects_col, ax["pos_anchors_en"] + ax["pos_anchors_es"])
        pos = np.mean(np.vstack([gc, para.mean(axis=0)]), axis=0)
    direction = pos - neg
    norm = np.linalg.norm(direction)
    return direction / norm if norm else direction


def bg_stats(bg_vecs: np.ndarray, axis_unit: np.ndarray):
    proj = bg_vecs @ axis_unit
    return float(np.mean(proj)), float(np.std(proj) or 1.0)


def axis_stats(vecs: np.ndarray, axis_unit: np.ndarray, mu: float, sigma: float) -> dict:
    z = (vecs @ axis_unit - mu) / sigma
    median_z = float(np.median(z))
    return {
        "median_z": median_z,
        "p25": float(np.percentile(z, 25)),
        "p75": float(np.percentile(z, 75)),
        "n_chunks": int(len(z)),
        "display_0_100": float(np.clip((median_z + 3) / 6, 0, 1) * 100),
    }


ANCHOR_MODES = ["theory", "grounded", "hybrid"]


def evaluate_set(scores, keys):
    """Metrics for one axis set. self_anchor is CIRCULAR under grounded/hybrid."""
    a, e = scores["analects"], scores[MVP_CONTROL_NEG_POLICY_ID]
    ordering = float(np.mean([a[k]["median_z"] > e[k]["median_z"] for k in keys]))
    gap = float(np.mean([a[k]["median_z"] - e[k]["median_z"] for k in keys]))
    disc = float(np.mean([np.std([scores[p][k]["median_z"] for p in MVP_POLICY_IDS]) for k in keys]))
    self_anchor = float(np.mean([a[k]["median_z"] > 0 for k in keys]))
    gov = None
    if "dezhi_fa" in keys:
        ch = scores["china_ngaidp_2017"]["dezhi_fa"]["median_z"]
        ca = scores["canada_pan_canadian_ai_strategy_2017"]["dezhi_fa"]["median_z"]
        eu = e["dezhi_fa"]["median_z"]
        gov = {"china": ch, "canada": ca, "eu": eu,
               "china_gt_canada": bool(ch > ca), "eu_is_law_pole": bool(eu < 0),
               "ok": bool(ch > ca and eu < 0)}
    return {"n_axes": len(keys), "ordering_frac": ordering, "control_gap": gap,
            "discrimination": disc, "self_anchor_frac": self_anchor, "governance_face": gov}


@click.command()
def main():
    """A/B three axis sets × three anchor strategies; pick by governance face + discrimination."""
    click.echo("=" * 68)
    click.echo("  CONFUCIAN CONCEPT AXES — A/B (3 sets × 3 anchor strategies)")
    click.echo("=" * 68)

    embedding_fn = get_embedding_function()
    client = get_client()
    policy_col = client.get_collection(POLICY_READ_COLLECTION_NAME, embedding_function=embedding_fn)
    analects_col = client.get_collection(ANALECTS_COLLECTION_NAME, embedding_function=embedding_fn)
    ensure_china_doc(policy_col)

    concepts = sorted(set(k for keys in AXIS_SETS.values() for k in keys))
    bg_vecs = get_vectors(policy_col)
    docvecs = {pid: get_vectors(policy_col, pid) for pid in MVP_POLICY_IDS + [MVP_CONTROL_NEG_POLICY_ID]}
    docvecs["analects"] = get_vectors(analects_col)

    # scores_by_mode[mode][doc][concept], metrics_by_mode[mode][set]
    scores_by_mode, metrics = {}, {}
    for mode in ANCHOR_MODES:
        axes = {c: build_axis(mode, embedding_fn, analects_col, CONFUCIAN_AXES[c]) for c in concepts}
        bg = {c: bg_stats(bg_vecs, axes[c]) for c in concepts}
        sc = {doc: {c: axis_stats(vecs, axes[c], *bg[c]) for c in concepts}
              for doc, vecs in docvecs.items()}
        scores_by_mode[mode] = sc
        metrics[mode] = {name: evaluate_set(sc, keys) for name, keys in AXIS_SETS.items()}

    # ── Pick winner (mode, set): governance face first, then discrimination ──
    # Prefer sets that pass governance face validity; among those, prefer anchors
    # grounded in the actual text (hybrid > theory) for provenance defensibility.
    # grounded-alone is de facto excluded because it fails governance (it measures
    # resemblance to Confucius's virtue-prose, not the governance model).
    mode_pref = {"hybrid": 2, "theory": 1, "grounded": 0}
    def rank_key(mode, name):
        m = metrics[mode][name]
        gov_ok = 1 if (m["governance_face"] and m["governance_face"]["ok"]) else 0
        return (gov_ok, mode_pref[mode], m["discrimination"])
    win_mode, win_set = max(((mo, s) for mo in ANCHOR_MODES for s in AXIS_SETS), key=lambda t: rank_key(*t))
    win_keys = AXIS_SETS[win_set]
    scores = scores_by_mode[win_mode]

    a, e = scores["analects"], scores[MVP_CONTROL_NEG_POLICY_ID]
    ordered = sum(a[k]["median_z"] > e[k]["median_z"] for k in win_keys)
    self_fail = [k for k in win_keys if a[k]["median_z"] <= 0]
    antipole = bool(a["dezhi_fa"]["median_z"] > 0 > e["dezhi_fa"]["median_z"]) if "dezhi_fa" in win_keys else None
    cv = {"axes_ordered": f"{ordered}/{len(win_keys)}", "ordering_pass": ordered >= len(win_keys) - 1,
          "antipole_pass": antipole, "self_anchor_axes": f"{len(win_keys) - len(self_fail)}/{len(win_keys)}",
          "self_anchor_failing": self_fail,
          "self_anchor_note": "circular bajo grounded/hybrid (el polo positivo es texto de las Analectas)"}

    def doc_block(pid, keys):
        meta = DOC_LABELS.get(pid, {"label": pid, "country": "", "region": ""})
        return {"label": meta["label"], "country": meta["country"], "region": meta["region"],
                "n_chunks": scores[pid][keys[0]]["n_chunks"], "axes": {k: scores[pid][k] for k in keys}}

    output = {
        "winner": {"anchor_mode": win_mode, "axis_set": win_set},
        "ab_test": {
            "criterion": "validez de gobernanza (China>Canadá en dézhì y UE en polo de ley), luego discriminación",
            "matrix": {mode: {name: {"axes": AXIS_SETS[name], **metrics[mode][name]}
                              for name in AXIS_SETS} for mode in ANCHOR_MODES},
        },
        "axes": [{"key": k, "zh": CONFUCIAN_AXES[k]["zh"], "pinyin": CONFUCIAN_AXES[k]["pinyin"],
                  "label": CONFUCIAN_AXES[k]["label"], "pos_pole": CONFUCIAN_AXES[k]["pos_pole"],
                  "neg_pole": CONFUCIAN_AXES[k]["neg_pole"]} for k in win_keys],
        "documents": {pid: doc_block(pid, win_keys) for pid in MVP_POLICY_IDS},
        "controls": {"analects": doc_block("analects", win_keys),
                     MVP_CONTROL_NEG_POLICY_ID: doc_block(MVP_CONTROL_NEG_POLICY_ID, win_keys)},
        "construct_validity": cv,
        "face_validity": metrics[win_mode][win_set]["governance_face"],
        "metadata": {
            "embedding_model": EMBEDDING_MODEL_LOCAL,
            "anchor_mode": win_mode,
            "anchor_note": {"theory": "polo positivo = paráfrasis modernas",
                            "grounded": "polo positivo = pasajes reales de las Analectas",
                            "hybrid": "polo positivo = Analectas + paráfrasis"}[win_mode],
            "standardization": "z-score vs policy-corpus background",
            "unit_of_analysis": "chunk (800 chars, 200 overlap)",
            "background_n_chunks": int(len(bg_vecs)),
            "status": "PRELIMINAR / MVP",
        },
    }

    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFUCIAN_MVP_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, cls=NumpyEncoder, ensure_ascii=False, indent=2)

    # ── Console matrix ──
    click.echo(f"\n  {'mode':9s}{'set':8s}{'discrim↑':>9}{'gap↑':>7}{'orden':>7}{'gov.face':>10}")
    for mode in ANCHOR_MODES:
        for name in AXIS_SETS:
            m = metrics[mode][name]
            g = m["governance_face"]
            gv = ("ok" if g["ok"] else "China<Can" if not g["china_gt_canada"] else "EU!<0") if g else "n/a"
            mk = "  <--" if (mode, name) == (win_mode, win_set) else ""
            click.echo(f"  {mode:9s}{name:8s}{m['discrimination']:>9.2f}{m['control_gap']:>7.2f}"
                       f"{m['ordering_frac']:>7.2f}{gv:>10}{mk}")
    click.echo(f"\n  GANADOR: anchor={win_mode}  set={win_set}  ({', '.join(win_keys)})")
    click.echo("\n  Fingerprints (median z):")
    click.echo("  " + " " * 40 + "".join(f"{k[:8]:>9}" for k in win_keys))
    for pid in MVP_POLICY_IDS + [MVP_CONTROL_NEG_POLICY_ID, "analects"]:
        row = "".join(f"{scores[pid][k]['median_z']:>9.2f}" for k in win_keys)
        click.echo(f"  {DOC_LABELS.get(pid, {}).get('label', pid)[:40]:40s}{row}")
    g = metrics[win_mode][win_set]["governance_face"]
    click.echo(f"\n  Gobernanza: China {g['china']:.2f} vs Canadá {g['canada']:.2f} (China>Can={g['china_gt_canada']}), "
               f"UE {g['eu']:.2f} (polo ley={g['eu_is_law_pole']})")
    click.echo(f"  Wrote {CONFUCIAN_MVP_JSON}")


if __name__ == "__main__":
    main()
