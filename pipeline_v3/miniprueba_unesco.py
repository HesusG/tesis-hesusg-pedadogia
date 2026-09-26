"""Small-scale pilot of the UNESCO-grid pipeline (thesis design v4, exploratory).

One chain, end to end, on a deliberately small sample:
  1. retrieve, per country and per target UNESCO category, the k fragments closest
     to the category description (local multilingual embeddings, politicas_v3);
  2. give each fragment, with its previous and next fragment as context, to the
     7-model panel, which assigns one of the 7 UNESCO categories (or none) and the
     Schiff label (education for AI / AI for education);
  3. keep fragments with a panel majority for the target category -> per-category
     vector stores split by country;
  4. country-to-country cosine distance between centroids, per category;
  5. language control: re-embed accepted fragments translated to English and compare;
  6. agreement: Fleiss kappa (nominal) for the whole panel and by model origin.

Everything is cached on disk; re-running replays instead of re-calling.
Usage: .venv/bin/python -m pipeline_v3.miniprueba_unesco
"""
import json
import hashlib
import statistics as stats
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

from . import agreement
from .config import (CHROMA_DIR, COLLECTION_V3, CACHE_DIR, PANEL, DEEP_DIVE_DOCS,
                     EMBEDDING_MODEL, CLASSIFIER_MAX_RETRIES, CLASSIFIER_MAX_TOKENS,
                     TRANSLATION_MODEL, PROJECT_ROOT)
from .judges import client, _parse

K_PER_CELL = 5
TARGETS = ["6.3", "6.4", "6.5"]
COUNTRIES = ["alemania", "australia", "canada", "china", "colombia", "eeuu", "mexico", "sudafrica"]
MAJORITY = 4  # of 7 judges

CODEBOOK_FILE = PROJECT_ROOT / "pipeline_v3" / "unesco_codebook.json"
PILOT_CACHE = CACHE_DIR / "miniprueba"
OUT_FILE = PROJECT_ROOT / "web" / "data" / "miniprueba_unesco.json"
SCHIFF = ["education_for_ai", "ai_for_education", "both", "neither"]


def load_cb() -> dict:
    return json.loads(CODEBOOK_FILE.read_text(encoding="utf-8"))


def cb_hash(cb: dict) -> str:
    return hashlib.sha256(json.dumps(cb, sort_keys=True, ensure_ascii=False)
                          .encode("utf-8")).hexdigest()[:12]


def system_prompt(cb: dict) -> str:
    cats = "\n".join(f"  {c['id']} {c['name']}: {c['definition']}" for c in cb["categories"])
    return (
        "<role>You are an expert coder of public education policy. You apply a fixed "
        "codebook rigorously, not your opinion.</role>\n"
        "<task>Read the TARGET fragment (the surrounding fragments are only context) and "
        "assign (a) the single UNESCO policy category it mainly addresses, or \"none\", "
        "and (b) the Schiff label.</task>\n"
        f"<categories>\n{cats}\n  none: the fragment does not address AI and education "
        "policy in any of these senses.\n</categories>\n"
        f"<schiff>{cb['schiff']}</schiff>\n"
        f"<rules>{' '.join(cb['decision_rules'])}</rules>\n"
        '<output>Return ONLY JSON: {"category": "6.1".."6.7" or "none", "schiff": '
        '"education_for_ai"|"ai_for_education"|"both"|"neither", "rationale": "<one '
        'sentence>"}</output>'
    )


def classify(model: str, prev: str, target: str, nxt: str, cb: dict) -> dict:
    key = hashlib.sha256(f"{model}|{cb_hash(cb)}|{prev}|{target}|{nxt}".encode()).hexdigest()[:24]
    f = PILOT_CACHE / "classifications" / f"{key}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    user = (f"CONTEXT BEFORE:\n{prev or '(start of document)'}\n\n"
            f"TARGET FRAGMENT:\n{target}\n\n"
            f"CONTEXT AFTER:\n{nxt or '(end of document)'}\n\nRespond ONLY with the JSON.")
    msgs = [{"role": "system", "content": system_prompt(cb)}, {"role": "user", "content": user}]
    last = None
    for _ in range(CLASSIFIER_MAX_RETRIES):
        for rf in ({"type": "json_object"}, None):
            try:
                kw = dict(model=model, temperature=0.0, messages=msgs,
                          max_tokens=CLASSIFIER_MAX_TOKENS)
                if rf:
                    kw["response_format"] = rf
                r = client().chat.completions.create(**kw)
                out = _parse(r.choices[0].message.content)
                cat = str(out.get("category", "none")).strip().lower()
                cat = cat if cat in {c["id"] for c in cb["categories"]} else "none"
                sch = str(out.get("schiff", "neither")).strip().lower()
                sch = sch if sch in SCHIFF else "neither"
                res = {"category": cat, "schiff": sch,
                       "rationale": out.get("rationale", ""), "model": model,
                       "ts": datetime.now(timezone.utc).isoformat()}
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
                return res
            except Exception as e:  # noqa: BLE001
                last = e
    return {"error": str(last), "model": model}


def translate(text: str) -> str:
    key = hashlib.sha256(f"{TRANSLATION_MODEL}|{text}".encode()).hexdigest()[:24]
    f = PILOT_CACHE / "translations" / f"{key}.txt"
    if f.exists():
        return f.read_text(encoding="utf-8")
    r = client().chat.completions.create(
        model=TRANSLATION_MODEL, temperature=0, max_tokens=900,
        messages=[{"role": "system", "content": "Translate this public-policy text to English, "
                   "faithfully and completely. Output ONLY the translation."},
                  {"role": "user", "content": text}])
    out = r.choices[0].message.content.strip()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(out, encoding="utf-8")
    return out


def cosine_dist(a: np.ndarray, b: np.ndarray) -> float:
    return float(1 - a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def dist_matrix(vecs_by_country: dict) -> dict:
    cs = [c for c in COUNTRIES if vecs_by_country.get(c)]
    cent = {c: np.mean(vecs_by_country[c], axis=0) for c in cs}
    return {"countries": cs,
            "matrix": [[round(cosine_dist(cent[a], cent[b]), 4) for b in cs] for a in cs]}


def upper(m: dict, order: list) -> list:
    idx = {c: i for i, c in enumerate(m["countries"])}
    return [m["matrix"][idx[a]][idx[b]] for i, a in enumerate(order) for b in order[i + 1:]]


def pca2(X: np.ndarray) -> np.ndarray:
    Xc = X - X.mean(axis=0)
    _, _, vt = np.linalg.svd(Xc, full_matrices=False)
    return Xc @ vt[:2].T


def main():
    cb = load_cb()
    model = SentenceTransformer(EMBEDDING_MODEL)
    col = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(COLLECTION_V3)
    catdef = {c["id"]: c for c in cb["categories"]}

    # 1. retrieval per (country, target category)
    frags = {}
    for cat in TARGETS:
        qv = model.encode(catdef[cat]["retrieval_query"]).tolist()
        for country in COUNTRIES:
            where = {"country": country}
            if country == "china":
                where = {"$and": [{"country": "china"},
                                  {"policy_id": {"$nin": DEEP_DIVE_DOCS}}]}
            r = col.query(query_embeddings=[qv], n_results=K_PER_CELL, where=where,
                          include=["documents", "metadatas", "embeddings", "distances"])
            for i, d, m, e, dist in zip(r["ids"][0], r["documents"][0], r["metadatas"][0],
                                        r["embeddings"][0], r["distances"][0]):
                fr = frags.setdefault(i, {"id": i, "text": d, "country": country,
                                          "policy_id": m["policy_id"], "language": m["language"],
                                          "chunk_index": m["chunk_index"],
                                          "emb": list(map(float, e)), "retrieved_for": []})
                fr["retrieved_for"].append({"category": cat, "distance": round(float(dist), 4)})
    print(f"retrieved {len(frags)} unique fragments")

    # context: previous and next fragment of the same document
    for fr in frags.values():
        for off, k in ((-1, "prev"), (1, "next")):
            g = col.get(where={"$and": [{"policy_id": fr["policy_id"]},
                                        {"chunk_index": fr["chunk_index"] + off}]},
                        include=["documents"])
            fr[k] = g["documents"][0] if g["documents"] else ""

    # 2. panel classification
    jobs = [(fr["id"], j) for fr in frags.values() for j in PANEL]
    def run(job):
        fid, j = job
        fr = frags[fid]
        return fid, j.key, j.origin, classify(j.model, fr["prev"], fr["text"], fr["next"], cb)
    with ThreadPoolExecutor(max_workers=16) as ex:
        for n, (fid, name, origin, res) in enumerate(ex.map(run, jobs), 1):
            frags[fid].setdefault("votes", {})[name] = {**res, "origin": origin}
            if n % 70 == 0:
                print(f"  {n}/{len(jobs)} classifications")

    # 3. majority label
    for fr in frags.values():
        cats = [v["category"] for v in fr["votes"].values() if "category" in v]
        schs = [v["schiff"] for v in fr["votes"].values() if "schiff" in v]
        top, n = Counter(cats).most_common(1)[0] if cats else ("none", 0)
        fr["majority"] = top if n >= MAJORITY else "no_consensus"
        fr["majority_n"] = n
        fr["n_votes"] = len(cats)
        st, sn = Counter(schs).most_common(1)[0] if schs else ("neither", 0)
        fr["schiff_majority"] = st if sn >= MAJORITY else "no_consensus"

    # 6. agreement (nominal) — reuse pipeline_v3.agreement with categorical codes
    labels = [c["id"] for c in cb["categories"]] + ["none"]
    agreement.CATEGORIES = list(range(len(labels)))
    code = {l: i for i, l in enumerate(labels)}
    def units(origin=None):
        return [[code[v["category"]] for v in fr["votes"].values()
                 if "category" in v and (origin is None or v["origin"] == origin)]
                for fr in frags.values()]
    agr = {}
    for key, origin in (("panel", None), ("western", "western"), ("chinese", "chinese")):
        u = units(origin)
        agr[key] = {"fleiss_kappa": round(agreement.fleiss_kappa(u), 3),
                    "alpha_nominal": round(agreement.krippendorff_alpha(u, "nominal"), 3),
                    "pct_exact": round(agreement.percent_agreement(u)["exact"], 3)}
    per_model = {}
    for j in PANEL:
        hits = [fr["votes"][j.key]["category"] == fr["majority"]
                for fr in frags.values()
                if fr["majority"] not in ("no_consensus",) and "category" in fr["votes"].get(j.key, {})]
        per_model[j.key] = {"origin": j.origin, "agree_with_majority": round(sum(hits) / len(hits), 3) if hits else None}

    # 4. per-category stores and distances (original language)
    results = {"categories": {}}
    trans_needed = [fr for fr in frags.values()
                    if fr["majority"] in TARGETS and fr["language"] != "en"]
    with ThreadPoolExecutor(max_workers=8) as ex:
        tr = dict(zip([f["id"] for f in trans_needed], ex.map(lambda f: translate(f["text"]), trans_needed)))
    for fr in frags.values():
        if fr["majority"] in TARGETS:
            fr["text_en"] = tr.get(fr["id"], fr["text"])
    en_emb = {fid: model.encode(fr["text_en"]).tolist() for fid, fr in frags.items() if "text_en" in fr}

    for cat in TARGETS:
        acc = [fr for fr in frags.values() if fr["majority"] == cat]
        orig = defaultdict(list); en = defaultdict(list)
        for fr in acc:
            orig[fr["country"]].append(fr["emb"])
            en[fr["country"]].append(en_emb[fr["id"]])
        m_orig, m_en = dist_matrix(orig), dist_matrix(en)
        common = [c for c in m_orig["countries"] if len(orig[c]) >= 1]
        rho = (agreement.spearman(upper(m_orig, common), upper(m_en, common))
               if len(common) >= 4 else None)
        pts = []
        if len(acc) >= 3:
            P = pca2(np.array([fr["emb"] for fr in acc]))
            pts = [{"x": round(float(p[0]), 4), "y": round(float(p[1]), 4),
                    "country": fr["country"], "id": fr["id"]} for p, fr in zip(P, acc)]
        results["categories"][cat] = {
            "name": catdef[cat]["name_es"],
            "n_accepted": {c: len(orig.get(c, [])) for c in COUNTRIES},
            "dist_original": m_orig, "dist_english": m_en,
            "spearman_original_vs_english": None if rho is None else round(rho, 3),
            "pca": pts,
        }

    # 1'. coverage (P1): what the panel says about every retrieved fragment, per country
    coverage = {c: Counter() for c in COUNTRIES}
    schiff_cov = {c: Counter() for c in COUNTRIES}
    for fr in frags.values():
        coverage[fr["country"]][fr["majority"]] += 1
        schiff_cov[fr["country"]][fr["schiff_majority"]] += 1

    out = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "params": {"k_per_cell": K_PER_CELL, "targets": TARGETS, "majority": MAJORITY,
                   "embedding_model": EMBEDDING_MODEL, "collection": COLLECTION_V3,
                   "excluded_docs": DEEP_DIVE_DOCS, "codebook_hash": cb_hash(cb),
                   "panel": [{"name": j.key, "model": j.model, "origin": j.origin} for j in PANEL],
                   "translation_model": TRANSLATION_MODEL},
        "codebook": cb,
        "n_fragments": len(frags),
        "n_classifications": sum(fr["n_votes"] for fr in frags.values()),
        "agreement": agr, "per_model": per_model,
        "coverage": {c: dict(v) for c, v in coverage.items()},
        "schiff": {c: dict(v) for c, v in schiff_cov.items()},
        "results": results,
        "fragments": [{k: v for k, v in fr.items() if k not in ("emb",)} for fr in frags.values()],
    }
    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT_FILE}  fragments={len(frags)}  agreement={agr['panel']}")


if __name__ == "__main__":
    main()
