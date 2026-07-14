"""Confucian concept-axes MVP — Kozlowski-style bipolar projection.

Measures how strongly each of 3 AI-education policies expresses six Confucian
values, by projecting their per-chunk embeddings onto six BIPOLAR axes built
from pre-registered anchor pairs (config.CONFUCIAN_AXES):

    axis = normalize( mean(pos_anchors) - mean(neg_anchors) )
    raw  = normalize(chunk_vector) . axis          # cosine in [-1, 1]
    z    = (raw - mu_bg) / sigma_bg                 # vs. the policy-corpus background

Unit of analysis is the CHUNK: we report distributions per (document, axis),
never a significance test across few documents. A construct-validity check
verifies the Analects (Confucian-positive control) separates from the EU AI Act
(legalistic negative control) before any substantive reading.

Writes web/data/confucian_mvp.json.

Usage:
    python -m pipeline.confucian_axes
"""
import json
import click
import numpy as np

from .config import (
    CHROMA_DIR, WEB_DATA_DIR, CONFUCIAN_MVP_JSON,
    POLICY_READ_COLLECTION_NAME, ANALECTS_COLLECTION_NAME,
    CONFUCIAN_AXES, MVP_POLICY_IDS, MVP_CONTROL_NEG_POLICY_ID,
    CHINA_MVP_POLICY, CHUNK_SIZE, CHUNK_OVERLAP,
    EMBEDDING_MODEL_LOCAL,
)
from .preprocess import clean_text
from .ingest import chunk_text
from .embeddings import get_embedding_function
from .export import NumpyEncoder

# Display names for the MVP documents.
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
    """L2-normalize each row; zero rows are left as zero."""
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
    """Return L2-normalized chunk vectors for a document (or the whole collection)."""
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
        return  # already present
    raw_file = CHINA_MVP_POLICY["raw_file"]
    click.echo(f"  China policy '{pid}' not found in collection — ingesting from {raw_file.name}")
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


def build_axes(embedding_fn) -> dict:
    """Build one unit direction vector per Confucian axis (bipolar subtraction)."""
    axes = {}
    for key, ax in CONFUCIAN_AXES.items():
        pos = embedding_fn(ax["pos_anchors_en"] + ax["pos_anchors_es"])
        neg = embedding_fn(ax["neg_anchors_en"] + ax["neg_anchors_es"])
        direction = np.mean(np.array(pos), axis=0) - np.mean(np.array(neg), axis=0)
        norm = np.linalg.norm(direction)
        axes[key] = direction / norm if norm else direction
    return axes


def background_stats(bg_vecs: np.ndarray, axes: dict) -> dict:
    """Mean/std of raw projections over the policy-corpus background, per axis."""
    stats = {}
    for key, axis_unit in axes.items():
        proj = bg_vecs @ axis_unit
        stats[key] = (float(np.mean(proj)), float(np.std(proj) or 1.0))
    return stats


def score_document(vecs: np.ndarray, axes: dict, bg: dict) -> dict:
    """Per-chunk z-scored projection distribution for one document, per axis."""
    out = {}
    for key, axis_unit in axes.items():
        raw = vecs @ axis_unit
        mu, sigma = bg[key]
        z = (raw - mu) / sigma
        median_z = float(np.median(z))
        out[key] = {
            "median_z": median_z,
            "mean_z": float(np.mean(z)),
            "std_z": float(np.std(z)),
            "p25": float(np.percentile(z, 25)),
            "p75": float(np.percentile(z, 75)),
            "n_chunks": int(len(z)),
            # display transform only: ±3 SD -> 0..100
            "display_0_100": float(np.clip((median_z + 3) / 6, 0, 1) * 100),
        }
    return out


def run_construct_validity(scores: dict) -> dict:
    """Analects (positive) must separate from EU AI Act (legalistic negative)."""
    pos = scores["analects"]
    neg = scores[MVP_CONTROL_NEG_POLICY_ID]
    per_axis = {k: {"analects": pos[k]["median_z"], "control": neg[k]["median_z"],
                    "ordered": pos[k]["median_z"] > neg[k]["median_z"]}
                for k in CONFUCIAN_AXES}
    axes_ordered = sum(1 for v in per_axis.values() if v["ordered"])
    antipole = (pos["dezhi_fa"]["median_z"] > 0 > neg["dezhi_fa"]["median_z"])
    self_anchor_fail = [k for k in CONFUCIAN_AXES if pos[k]["median_z"] <= 0]
    return {
        "ordering_pass": axes_ordered >= 5,
        "axes_ordered": f"{axes_ordered}/6",
        "antipole_pass": bool(antipole),
        "self_anchor_pass": len(self_anchor_fail) == 0,
        "self_anchor_axes": f"{6 - len(self_anchor_fail)}/6",
        "self_anchor_failing": self_anchor_fail,
        "per_axis": per_axis,
    }


@click.command()
def main():
    """Compute Confucian concept-axis fingerprints for the MVP policies."""
    click.echo("=" * 60)
    click.echo("  CONFUCIAN CONCEPT AXES — MVP")
    click.echo("=" * 60)

    embedding_fn = get_embedding_function()
    client = get_client()
    policy_col = client.get_collection(POLICY_READ_COLLECTION_NAME,
                                       embedding_function=embedding_fn)
    analects_col = client.get_collection(ANALECTS_COLLECTION_NAME,
                                         embedding_function=embedding_fn)

    ensure_china_doc(policy_col)

    click.echo("Building 6 bipolar axes from pre-registered anchors...")
    axes = build_axes(embedding_fn)

    click.echo("Computing background distribution (policy corpus)...")
    bg_vecs = get_vectors(policy_col)  # all policy chunks
    bg = background_stats(bg_vecs, axes)

    # Score the 3 MVP policies + the two controls.
    scores, n_chunks = {}, {}
    for pid in MVP_POLICY_IDS + [MVP_CONTROL_NEG_POLICY_ID]:
        vecs = get_vectors(policy_col, pid)
        scores[pid] = score_document(vecs, axes, bg)
        n_chunks[pid] = len(vecs)
    analects_vecs = get_vectors(analects_col)
    scores["analects"] = score_document(analects_vecs, axes, bg)
    n_chunks["analects"] = len(analects_vecs)

    validity = run_construct_validity(scores)

    # Face validity: China should lean more to dézhì than Canada.
    face = {
        "china_dezhi_median_z": scores["china_ngaidp_2017"]["dezhi_fa"]["median_z"],
        "canada_dezhi_median_z": scores["canada_pan_canadian_ai_strategy_2017"]["dezhi_fa"]["median_z"],
    }
    face["china_gt_canada_on_dezhi"] = face["china_dezhi_median_z"] > face["canada_dezhi_median_z"]

    # ── Assemble output ──
    def doc_block(pid):
        meta = DOC_LABELS.get(pid, {"label": pid, "country": "", "region": ""})
        return {"label": meta["label"], "country": meta["country"],
                "region": meta["region"], "n_chunks": n_chunks[pid],
                "axes": scores[pid]}

    output = {
        "axes": [{"key": k, "zh": ax["zh"], "pinyin": ax["pinyin"],
                  "label": ax["label"], "pos_pole": ax["pos_pole"],
                  "neg_pole": ax["neg_pole"]}
                 for k, ax in CONFUCIAN_AXES.items()],
        "documents": {pid: doc_block(pid) for pid in MVP_POLICY_IDS},
        "controls": {"analects": doc_block("analects"),
                     MVP_CONTROL_NEG_POLICY_ID: doc_block(MVP_CONTROL_NEG_POLICY_ID)},
        "construct_validity": validity,
        "face_validity": face,
        "metadata": {
            "embedding_model": EMBEDDING_MODEL_LOCAL,
            "standardization": "z-score vs policy-corpus background",
            "unit_of_analysis": "chunk (800 chars, 200 overlap)",
            "background_n_chunks": int(len(bg_vecs)),
            "status": "PRELIMINAR / MVP — solo validez de constructo",
        },
    }

    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFUCIAN_MVP_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, cls=NumpyEncoder, ensure_ascii=False, indent=2)

    # ── Console report ──
    click.echo("\n  Fingerprints (median z per axis):")
    header = "  " + " " * 40 + "".join(f"{k[:8]:>9}" for k in CONFUCIAN_AXES)
    click.echo(header)
    for pid in MVP_POLICY_IDS + [MVP_CONTROL_NEG_POLICY_ID, "analects"]:
        row = "".join(f"{scores[pid][k]['median_z']:>9.2f}" for k in CONFUCIAN_AXES)
        click.echo(f"  {DOC_LABELS.get(pid, {}).get('label', pid)[:40]:40s}{row}")

    click.echo("\n  Construct validity:")
    click.echo(f"    ordering (>=5/6): {validity['ordering_pass']}  ({validity['axes_ordered']})")
    click.echo(f"    antipole (Analects>0>EU on dézhì↔fǎ): {validity['antipole_pass']}")
    click.echo(f"    self-anchor (Analects>0 per axis): {validity['self_anchor_axes']}"
               f"  failing: {validity['self_anchor_failing'] or 'none'}")
    click.echo(f"  Face validity — China>Canada on dézhì: {face['china_gt_canada_on_dezhi']}")
    click.echo(f"\n  Wrote {CONFUCIAN_MVP_JSON}")


if __name__ == "__main__":
    main()
