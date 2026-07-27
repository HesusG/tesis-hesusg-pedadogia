"""SPIKE Fase 6 — ¿el +0.94 de China mide al PAÍS o al GÉNERO DOCUMENTAL?

La Fase 5 midió a China con 8 documentos de IA-**en-educación** (2025-2026) y a los
otros 6 países con **estrategias generales de IA** (2017-2023). El eje dézhì mide
"el Estado cultiva y forma personas", y la política educativa trata por definición
de formar personas. Explicación alternativa obvia:

    China no sale alta por ser China, sino porque le medimos documentos de educación.

Este spike la somete a prueba con un diseño 2×2 más un tercer brazo:

  ┌──────────────┬─────────────────────────┬──────────────────────────┐
  │              │ documento educativo     │ estrategia general de IA │
  ├──────────────┼─────────────────────────┼──────────────────────────┤
  │ China        │ corpus v3 (Fase 5)      │ NGAIDP 2017      ← nuevo │
  │ no China     │ India NEP, UNESCO ←nuevo│ corpus v3 (Fase 5)       │
  └──────────────┴─────────────────────────┴──────────────────────────┘

  + brazo "vecindario confuciano": Corea, Japón, Singapur (IA general). Separa
    "es China" de "es la región de herencia confuciana" — que es, literalmente,
    lo que la tesis afirma medir.

Predicciones (pre-registradas al commitear este archivo):
  P1. Si el efecto es del PAÍS: NGAIDP (China, IA general) ≈ +1, alto como el
      corpus educativo chino.
  P2. Si el efecto es del GÉNERO: India NEP y UNESCO (educación, no China) suben
      por encima de 0, y NGAIDP baja hacia 0.
  P3. Si el efecto es REGIONAL: Corea/Japón/Singapur también suben.

Los documentos de control van a una colección APARTE (`politicas_v3_control`) para
no contaminar el corpus pre-registrado. Todo lo demás — chunking 500/50, query de
gobernanza, K=10, panel de 7 jueces, códebook — es idéntico a la Fase 5, que es lo
que hace comparables los números.

Uso: python -m pipeline_v3.confound_test
"""
import json
import random
import statistics as stats
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import chromadb

from .config import (CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, INGEST_VERSION,
                     PROJECT_ROOT, PANEL, WEB_DATA_DIR, CACHE_DIR, K_PASSAGES,
                     GENRE_VOCAB, load_codebook)
from .judges import classify, codebook_hash
from .compare_countries import GOV_QUERY, MAX_WORKERS, to_en
from pipeline.ingest import chunk_text
from pipeline.embeddings import get_embedding_function

CONTROL_COLLECTION = "politicas_v3_control"
PROC = PROJECT_ROOT / "policies" / "processed"
RAW = PROJECT_ROOT / "policies" / "raw"
OUT_FILE = WEB_DATA_DIR / "dezhi_confound_test.json"
RECORDS_FILE = CACHE_DIR / "dezhi_confound_records.jsonl"
SEED, N_BOOT = 42, 5000

# `topic` y `arm` son Tier A: asignados a mano, NUNCA por LLM (igual que `genre`).
CONTROLS = [
    # ── Celda: China × IA general. El test decisivo de P1 vs P2. ──
    {"doc_id": "china_ngaidp_2017", "country": "china", "region": "asia",
     "genre": "strategy", "language": "en", "year": 2017, "topic": "general_ai",
     "arm": "china_general", "adopting_body": "State Council of the PRC",
     "doc_type_official": "New Generation AI Development Plan",
     "path": RAW / "china" / "3_new_gen_ai_development_plan_2017_en.txt"},

    # ── Celda: no China × educación. Si el género infla el eje, estos suben. ──
    {"doc_id": "india_nep_2020", "country": "india", "region": "asia",
     "genre": "strategy", "language": "en", "year": 2020, "topic": "education",
     "arm": "noncn_education", "adopting_body": "Ministry of Education, India",
     "doc_type_official": "National Education Policy 2020",
     "path": PROC / "india_nep_2020.txt"},
    {"doc_id": "unesco_genai_guidance_2023", "country": "unesco", "region": "internacional",
     "genre": "guidance", "language": "en", "year": 2023, "topic": "education",
     "arm": "noncn_education", "adopting_body": "UNESCO",
     "doc_type_official": "Guidance for generative AI in education and research",
     "path": PROC / "unesco_genai_guidance_2023.txt"},

    # ── Brazo: vecindario confuciano × IA general. ¿China o la región? ──
    {"doc_id": "corea_ai_strategy_2019", "country": "corea", "region": "asia",
     "genre": "strategy", "language": "en", "year": 2019, "topic": "general_ai",
     "arm": "confucian_neighborhood", "adopting_body": "Government of the Republic of Korea",
     "doc_type_official": "National Strategy for AI",
     "path": PROC / "corea_ai_strategy_2019.txt"},
    {"doc_id": "japon_ai_strategy_2019", "country": "japon", "region": "asia",
     "genre": "strategy", "language": "en", "year": 2019, "topic": "general_ai",
     "arm": "confucian_neighborhood", "adopting_body": "Government of Japan",
     "doc_type_official": "AI Strategy 2019",
     "path": PROC / "japon_ai_strategy_2019.txt"},
    {"doc_id": "singapur_nais_2019", "country": "singapur", "region": "asia",
     "genre": "strategy", "language": "en", "year": 2019, "topic": "general_ai",
     "arm": "confucian_neighborhood", "adopting_body": "Smart Nation Singapore",
     "doc_type_official": "National AI Strategy",
     "path": PROC / "singapur_nais_2019.txt"},
]

TIER_A = ["country", "region", "genre", "language", "year", "topic", "arm",
          "adopting_body", "doc_type_official", "source_uri", "ingest_version"]


def ingest():
    """Chunking y embedding IDÉNTICOS a la Fase 5 — si difirieran, los números no
    serían comparables y el control no probaría nada."""
    assert all(d["genre"] in GENRE_VOCAB for d in CONTROLS), "genre fuera del vocab"
    missing = [d["doc_id"] for d in CONTROLS if not d["path"].exists()]
    if missing:
        raise SystemExit(f"Faltan textos fuente: {missing}")

    col = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_or_create_collection(
        name=CONTROL_COLLECTION, embedding_function=get_embedding_function())
    for d in CONTROLS:
        pid = d["doc_id"]
        try:
            col.delete(where={"policy_id": pid})
        except Exception:
            pass
        chunks = chunk_text(d["path"].read_text(encoding="utf-8"), CHUNK_SIZE, CHUNK_OVERLAP)
        rec = {**d, "source_uri": str(d["path"].relative_to(PROJECT_ROOT)),
               "ingest_version": INGEST_VERSION}
        base = {"policy_id": pid, **{k: rec.get(k) for k in TIER_A}}
        base = {k: v for k, v in base.items() if v is not None}
        ids = [f"{pid}_chunk_{i:04d}" for i in range(len(chunks))]
        metas = [{**base, "parent_doc_id": pid, "chunk_index": i} for i in range(len(chunks))]
        for s in range(0, len(chunks), 500):
            col.add(documents=chunks[s:s + 500], ids=ids[s:s + 500], metadatas=metas[s:s + 500])
        print(f"  [+] {pid:28s} {len(chunks):>4} chunks | {d['arm']:22s} {d['topic']}")
    return col


def boot_ci(vals, seed=SEED):
    rng = random.Random(seed)
    n = len(vals)
    bs = sorted(stats.mean([vals[rng.randrange(n)] for _ in range(n)]) for _ in range(N_BOOT))
    return [bs[int(0.025 * N_BOOT)], bs[int(0.975 * N_BOOT)]]


def main():
    print(f"── Ingesta del brazo de control → {CONTROL_COLLECTION} ──")
    col = ingest()

    cb = load_codebook()
    jobs = []
    for d in CONTROLS:
        q = col.query(query_texts=[GOV_QUERY], n_results=K_PASSAGES,
                      where={"policy_id": d["doc_id"]}, include=["documents", "metadatas"])
        for i, (doc, m) in enumerate(zip(q["documents"][0], q["metadatas"][0])):
            passage = to_en(doc, m["language"])
            for j in PANEL:
                jobs.append((d, i, passage, j))

    print(f"\n── Clasificando {len(jobs)} pares (pasaje × juez) ──")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        outs = list(ex.map(lambda t: classify(t[3].model, t[2], cb=cb), jobs))

    recs, errors = [], defaultdict(int)
    for (d, i, _p, j), out in zip(jobs, outs):
        s = out.get("score")
        if s is None:
            errors[j.key] += 1
            continue
        recs.append({"doc_id": d["doc_id"], "country": d["country"], "topic": d["topic"],
                     "arm": d["arm"], "genre": d["genre"], "year": d["year"],
                     "passage_idx": i, "judge": j.key, "origin": j.origin,
                     "score": s, "confidence": out.get("confidence"),
                     "rationale": out.get("rationale")})
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with RECORDS_FILE.open("w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if errors:
        print(f"  ⚠ errores por juez: {dict(errors)}")

    # ── Agregado por documento (bootstrap sobre pasajes, como en la Fase 5) ──
    by_doc_pass = defaultdict(lambda: defaultdict(list))
    for r in recs:
        by_doc_pass[r["doc_id"]][r["passage_idx"]].append(r["score"])
    doc_stats = {}
    for pid, passages in by_doc_pass.items():
        pmeans = [stats.mean(v) for v in passages.values()]
        doc_stats[pid] = {"mean": stats.mean(pmeans), "n_passages": len(pmeans),
                          "ci95": boot_ci(pmeans)}

    meta = {d["doc_id"]: d for d in CONTROLS}
    print("\n  ══ Resultado por documento de control ══")
    for pid, v in sorted(doc_stats.items(), key=lambda kv: -kv[1]["mean"]):
        d = meta[pid]
        lo, hi = v["ci95"]
        print(f"    {pid:28s} {v['mean']:+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  "
              f"{d['country']:9s} {d['topic']:11s} {d['arm']}")

    # ── Veredicto sobre las tres predicciones ──
    ng = doc_stats.get("china_ngaidp_2017")
    edu = [doc_stats[d["doc_id"]] for d in CONTROLS
           if d["arm"] == "noncn_education" and d["doc_id"] in doc_stats]
    neigh = [doc_stats[d["doc_id"]] for d in CONTROLS
             if d["arm"] == "confucian_neighborhood" and d["doc_id"] in doc_stats]

    CHINA_V3 = 0.943   # Fase 5, corpus educativo chino (referencia)
    LIBERAL_V3 = 0.0   # Fase 5, los otros 6 países
    verdict = {}
    print("\n  ══ Veredicto ══")
    if ng:
        verdict["p1_china_general_high"] = ng["ci95"][0] > 0.25
        print(f"    P1 país: NGAIDP (China, IA general) = {ng['mean']:+.3f} "
              f"IC95 [{ng['ci95'][0]:+.2f}, {ng['ci95'][1]:+.2f}] vs China-educación {CHINA_V3:+.2f} "
              f"→ {'ALTO, el efecto sobrevive sin educación' if verdict['p1_china_general_high'] else 'BAJO, el efecto dependía del género educativo'}")
    if edu:
        m = stats.mean(x["mean"] for x in edu)
        verdict["p2_education_inflates"] = any(x["ci95"][0] > 0.25 for x in edu)
        print(f"    P2 género: educación no-china = {m:+.3f} vs liberales-IA-general {LIBERAL_V3:+.2f} "
              f"→ {'SUBE, el género infla el eje' if verdict['p2_education_inflates'] else 'NO sube, el género no explica el resultado'}")
    if neigh:
        m = stats.mean(x["mean"] for x in neigh)
        verdict["p3_regional"] = any(x["ci95"][0] > 0.25 for x in neigh)
        print(f"    P3 región: Corea/Japón/Singapur = {m:+.3f} "
              f"→ {'SUBEN, el efecto es regional confuciano' if verdict['p3_regional'] else 'NO suben, el efecto es específico de China'}")

    payload = {"design": "2x2 tema × país + brazo vecindario confuciano",
               "k_passages": K_PASSAGES, "codebook_hash": codebook_hash(cb),
               "n_classifications": len(recs),
               "reference_fase5": {"china_education": CHINA_V3, "liberal_general_ai": LIBERAL_V3},
               "doc_stats": doc_stats,
               "doc_meta": {pid: {k: v for k, v in meta[pid].items() if k != "path"}
                            for pid in doc_stats},
               "verdict": verdict}
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Wrote {OUT_FILE}")
    print(f"  Wrote {RECORDS_FILE} ({len(recs)} registros)")


if __name__ == "__main__":
    main()
