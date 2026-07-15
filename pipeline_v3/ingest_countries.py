"""SPIKE Fase 2f — ingesta de los otros 6 países a `politicas_v3`.

China ya está (8 docs 2025-2026). Aquí entran EUA, Canadá, Colombia, Alemania,
Sudáfrica, Australia (texto ya procesado en policies/processed/, en su idioma
original — el embedding multilingüe lo maneja). Metadata Tier A con `genre`
(control del confusor) asignado a mano.

Uso: python -m pipeline_v3.ingest_countries
"""
from collections import Counter

from .config import (CHUNK_SIZE, CHUNK_OVERLAP, INGEST_VERSION, PROJECT_ROOT, GENRE_VOCAB)
from .ingest import get_collection, TIER_A
from pipeline.ingest import chunk_text

PROC = PROJECT_ROOT / "policies" / "processed"

COUNTRIES = [
    {"doc_id": "canada_pan_canadian_ai_strategy_2017", "country": "canada", "region": "norteamerica",
     "genre": "strategy", "language": "en", "year": 2017,
     "adopting_body": "CIFAR / Gov of Canada", "doc_type_official": "National AI Strategy",
     "file": "canada_pan_canadian_ai_strategy_2017.txt"},
    {"doc_id": "colombia_conpes_3975_2019", "country": "colombia", "region": "latinoamerica",
     "genre": "strategy", "language": "es", "year": 2019,
     "adopting_body": "DNP / CONPES", "doc_type_official": "Documento CONPES",
     "file": "colombia_conpes_3975_2019.txt"},
    {"doc_id": "eeuu_eo14110_2023", "country": "eeuu", "region": "norteamerica",
     "genre": "law", "language": "en", "year": 2023,
     "adopting_body": "White House (Executive Office)", "doc_type_official": "Executive Order",
     "file": "eeuu_eo14110_2023.txt"},
    {"doc_id": "alemania_ki_strategie_2020", "country": "alemania", "region": "europa",
     "genre": "strategy", "language": "de", "year": 2020,
     "adopting_body": "Bundesregierung", "doc_type_official": "KI-Strategie",
     "file": "alemania_ki_strategie_2020.txt"},
    {"doc_id": "sudafrica_4ir_2020", "country": "sudafrica", "region": "africa",
     "genre": "report", "language": "en", "year": 2020,
     "adopting_body": "Presidential Commission 4IR", "doc_type_official": "PC4IR Report",
     "file": "sudafrica_4ir_2020.txt"},
    {"doc_id": "australia_ai_action_plan_2021", "country": "australia", "region": "oceania",
     "genre": "action_plan", "language": "en", "year": 2021,
     "adopting_body": "Australian Government", "doc_type_official": "AI Action Plan",
     "file": "australia_ai_action_plan_2021.txt"},
]


def main():
    assert all(d["genre"] in GENRE_VOCAB for d in COUNTRIES), "genre fuera del vocab"
    col = get_collection()
    print(f"politicas_v3 — {col.count()} chunks previos (China ya ingerida)")
    total = 0
    for d in COUNTRIES:
        pid = d["doc_id"]
        try:
            col.delete(where={"policy_id": pid})
        except Exception:
            pass
        text = (PROC / d["file"]).read_text(encoding="utf-8")
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        rec = {**d, "source_uri": f"policies/processed/{d['file']}", "ingest_version": INGEST_VERSION}
        base = {"policy_id": pid, **{k: rec.get(k) for k in TIER_A}}
        base = {k: v for k, v in base.items() if v is not None}
        ids = [f"{pid}_chunk_{i:04d}" for i in range(len(chunks))]
        metas = [{**base, "parent_doc_id": pid, "chunk_index": i} for i in range(len(chunks))]
        for s in range(0, len(chunks), 500):
            e = min(s + 500, len(chunks))
            col.add(documents=chunks[s:e], ids=ids[s:e], metadatas=metas[s:e])
        total += len(chunks)
        print(f"  [+] {pid:36s} {len(chunks):>3} chunks | {d['country']:10s} {d['genre']:11s} {d['language']}")

    md = col.get(include=["metadatas"])["metadatas"]
    print(f"\n  +{len(COUNTRIES)} países, {total} chunks. politicas_v3 total: {col.count()}")
    by_country = Counter(m["country"] for m in md)
    print("  Corpus v3 por país:", dict(by_country))
    by_genre = Counter(m["genre"] for m in md)
    print("  Por género (control):", dict(by_genre))


if __name__ == "__main__":
    main()
