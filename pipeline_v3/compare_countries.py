"""SPIKE Fase 4/5 — comparación cross-country en dézhì (China vs liberales).

Para cada país: recupera top-K pasajes de gobernanza de `politicas_v3`, traduce a
EN (EN primario por la Fase 3), clasifica con el panel de 7 jueces, y agrega la
mediana dézhì por país. Reporta el ranking + el desglose por origen (sidequest).

Fase 5 sube K de 3 a 10, cachea las traducciones, registra **cada clasificación
cruda** en `dezhi_records.jsonl` (insumo de `agreement.py`) y reporta la cobertura
por juez para que un modelo caído no se confunda con un score bajo.

Uso: python -m pipeline_v3.compare_countries
"""
import json
import hashlib
import statistics as stats
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import chromadb

from .config import (CHROMA_DIR, COLLECTION_V3, PANEL, WEB_DATA_DIR, CACHE_DIR,
                     K_PASSAGES, TRANSLATION_MODEL, load_codebook)
from .judges import classify, client, codebook_hash
from pipeline.embeddings import get_embedding_function

GOV_QUERY = ("the role of the state and government in guiding, cultivating, directing or "
             "regulating AI in education and society; governance, state leadership, "
             "individual rights, rule of law, national planning")
COUNTRIES = ["china", "eeuu", "canada", "colombia", "alemania", "sudafrica", "australia"]
K = K_PASSAGES
RECORDS_FILE = CACHE_DIR / "dezhi_records.jsonl"
TRANSLATION_CACHE = CACHE_DIR / "translations"
MAX_WORKERS = 12   # los jueces son I/O sobre OpenRouter; en serie son horas


def to_en(text: str, lang: str) -> str:
    """Traduce a inglés (Vía B: todos los jueces leen el MISMO idioma). Cacheado en disco."""
    if lang == "en":
        return text
    TRANSLATION_CACHE.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(f"{TRANSLATION_MODEL}|{lang}|{text}".encode("utf-8")).hexdigest()[:24]
    cf = TRANSLATION_CACHE / f"{key}.txt"
    if cf.exists():
        return cf.read_text(encoding="utf-8")
    r = client().chat.completions.create(
        model=TRANSLATION_MODEL, temperature=0, max_tokens=700,
        messages=[{"role": "system", "content": "Translate the following public-policy text to English faithfully. Output ONLY the translation."},
                  {"role": "user", "content": text}])
    out = r.choices[0].message.content.strip()
    cf.write_text(out, encoding="utf-8")
    return out


def main():
    cb = load_codebook()
    cbh = codebook_hash(cb)
    col = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(
        COLLECTION_V3, embedding_function=get_embedding_function())

    # ── 1. Retrieval uniforme + traducción a EN (cacheada) ──
    jobs = []       # (country, passage_idx, meta, passage_en, judge)
    for c in COUNTRIES:
        q = col.query(query_texts=[GOV_QUERY], n_results=K, where={"country": c},
                      include=["documents", "metadatas"])
        docs, metas = q["documents"][0], q["metadatas"][0]
        for i, (d, m) in enumerate(zip(docs, metas)):
            passage = to_en(d, m["language"])
            for j in PANEL:
                jobs.append((c, i, m, passage, j))
        print(f"  {c:12s} recuperado y traducido ({len(docs)} pasajes)")

    # ── 2. Clasificación en paralelo (I/O sobre OpenRouter; la caché hace esto reanudable) ──
    print(f"\n  Clasificando {len(jobs)} pares (pasaje × juez) con {MAX_WORKERS} hilos...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        outs = list(ex.map(lambda t: classify(t[4].model, t[3], cb=cb), jobs))

    recs = []       # una fila por (pasaje × juez)
    errors = defaultdict(int)
    for (c, i, m, _passage, j), out in zip(jobs, outs):
        s = out.get("score")
        if s is None:
            errors[j.key] += 1
            continue
        recs.append({"country": c, "passage_idx": i,
                     # La ingesta escribió `policy_id`/`parent_doc_id`; el esquema
                     # Tier A lo llama `doc_id`. Se leen los campos REALES (leer
                     # `doc_id` devolvía null y vaciaba la provenance).
                     "doc_id": m.get("policy_id") or m.get("parent_doc_id"),
                     "chunk_index": m.get("chunk_index"), "year": m.get("year"),
                     "genre": m.get("genre"), "src_language": m.get("language"),
                     "judge": j.key, "origin": j.origin, "model": j.model,
                     "score": s, "confidence": out.get("confidence"),
                     # El rationale se consolida aquí para que este archivo sea la
                     # provenance ÚNICA y versionada: el caché por llamada es
                     # regenerable y no se comitea.
                     "rationale": out.get("rationale")})

    # ── registro crudo (insumo de agreement.py + provenance de la tesis) ──
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with RECORDS_FILE.open("w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    by_c = defaultdict(list)
    for r in recs:
        by_c[r["country"]].append(r["score"])
    ranking = sorted((c for c in COUNTRIES if by_c[c]),
                     key=lambda c: (-stats.median(by_c[c]), -stats.mean(by_c[c])))

    print("\n  ══ Ranking dézhì por país (mediana; +2 = Estado-dirige, -2 = derechos limitan) ══")
    for c in ranking:
        v = by_c[c]
        print(f"    {c:12s} {stats.median(v):+.2f}  (media {stats.mean(v):+.2f}, n={len(v)})")

    print("\n  Sidequest — por origen del modelo:")
    origin_med, origin_mean = {}, {}
    for origin in ("western", "chinese"):
        v = [r["score"] for r in recs if r["origin"] == origin]
        origin_med[origin], origin_mean[origin] = stats.median(v), stats.mean(v)
        print(f"    {origin:10s} mediana {stats.median(v):+.2f}  media {stats.mean(v):+.2f}  (n={len(v)})")

    print("\n  Cobertura por juez (clasificaciones válidas / esperadas):")
    expected = len(COUNTRIES) * K
    coverage = {}
    for j in PANEL:
        got = sum(1 for r in recs if r["judge"] == j.key)
        coverage[j.key] = {"valid": got, "expected": expected, "errors": errors[j.key]}
        flag = "✓" if got == expected else "⚠"
        print(f"    [{flag}] {j.key:9s} {got:3d}/{expected}  (errores: {errors[j.key]})")

    out = {
        "axis": "dezhi_governance", "k_passages": K, "n_classifications": len(recs),
        "codebook_hash": cbh,
        "country_dezhi": {c: {"median": stats.median(by_c[c]), "mean": stats.mean(by_c[c]),
                              "n": len(by_c[c])} for c in COUNTRIES if by_c[c]},
        "ranking": ranking,
        "origin_median": origin_med,
        "origin_mean": origin_mean,
        "judge_coverage": coverage,
        "status": f"PRELIMINAR / MVP — panel EN, K={K} pasajes de gobernanza/país, "
                  f"{len(PANEL)} jueces (4 origen chino / 3 occidental)",
    }
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_DATA_DIR / "dezhi_country_comparison.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Wrote {WEB_DATA_DIR / 'dezhi_country_comparison.json'}")
    print(f"  Wrote {RECORDS_FILE} ({len(recs)} registros crudos)")


if __name__ == "__main__":
    main()
