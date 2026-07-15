"""SPIKE Fase 2e — ingesta del corpus China 2025-2026 a `politicas_v3`.

chunk 500/50 → embed multilingüe (lee chino nativo) → ChromaDB con metadata Tier A.
NOTA (flagged): el blurb de contexto (Anthropic) y la traducción ZH→EN para el
clasificador son mejoras posteriores; el embedding multilingüe no las necesita
para almacenar/recuperar. Se guarda el texto ORIGINAL (consistente con los demás
países, que también están en su idioma).

Uso: python -m pipeline_v3.ingest
"""
import json
import chromadb

from .config import (CHROMA_DIR, COLLECTION_V3, CHUNK_SIZE, CHUNK_OVERLAP,
                     EMBEDDING_MODEL, PROJECT_ROOT)
from pipeline.embeddings import get_embedding_function
from pipeline.ingest import chunk_text

REGISTRY = PROJECT_ROOT / "pipeline_v3" / "china_2026_registry.json"
RAW_DIR = PROJECT_ROOT / "policies" / "raw" / "china_2026"

# Campos Tier A que van a cada chunk (denormalizados). Sin None (ChromaDB no acepta None).
TIER_A = ["country", "region", "genre", "language", "year",
          "adopting_body", "doc_type_official", "source_uri", "ingest_version"]


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_V3, embedding_function=get_embedding_function())


def main():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    docs = [d for d in reg if d.get("status") == "ok"]
    col = get_collection()
    print(f"Colección '{COLLECTION_V3}' (emb={EMBEDDING_MODEL}) — {col.count()} chunks previos")

    total = 0
    for d in docs:
        pid = d["doc_id"]
        # re-ingesta idempotente
        try:
            col.delete(where={"policy_id": pid})
        except Exception:
            pass
        text = (RAW_DIR / f"{pid}_zh.txt").read_text(encoding="utf-8")
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        base = {"policy_id": pid, **{k: d.get(k) for k in TIER_A}}
        base = {k: v for k, v in base.items() if v is not None}
        ids = [f"{pid}_chunk_{i:04d}" for i in range(len(chunks))]
        metas = [{**base, "parent_doc_id": pid, "chunk_index": i} for i in range(len(chunks))]
        for s in range(0, len(chunks), 500):
            e = min(s + 500, len(chunks))
            col.add(documents=chunks[s:e], ids=ids[s:e], metadatas=metas[s:e])
        total += len(chunks)
        print(f"  [+] {pid:32s} {len(chunks):>3} chunks | {d['genre']:11s} {d['year']}")

    print(f"\n  Ingestados {len(docs)} docs, {total} chunks. Colección total: {col.count()}")
    # verificación: retrieval de gobernanza
    fn = get_embedding_function()
    r = col.query(query_texts=["el papel del Estado en dirigir y cultivar la educación en IA"],
                  n_results=3, include=["metadatas", "distances"])
    print("\n  Sanity retrieval ('rol del Estado'):")
    for m, dist in zip(r["metadatas"][0], r["distances"][0]):
        print(f"    {m['policy_id']:32s} (dist {dist:.2f})")


if __name__ == "__main__":
    main()
