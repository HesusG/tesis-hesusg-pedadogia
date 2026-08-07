"""Ingest the Analects of Confucius into a dedicated ChromaDB collection.

Public-domain James Legge English translation (Project Gutenberg #3330),
stored at corpus/analects/analects_legge_en.txt. Serves as the
Confucian-positive control corpus for the concept-axes MVP
(pipeline/confucian_axes.py). Reuses the same chunker and embedding
function as the policy pipeline so the vectors live in the same space.

Usage:
    python -m pipeline.ingest_analects [--force]
"""
import click

from .config import (
    CHROMA_DIR, ANALECTS_COLLECTION_NAME, ANALECTS_SOURCE_FILE,
    CHUNK_SIZE, CHUNK_OVERLAP,
)
from .preprocess import clean_text
from .ingest import chunk_text
from .embeddings import get_embedding_function


def get_or_create_analects_collection():
    """Get or create the Analects ChromaDB collection."""
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=ANALECTS_COLLECTION_NAME,
        embedding_function=get_embedding_function(),
    )


@click.command()
@click.option("--force", is_flag=True, help="Re-ingest even if already present")
def main(force: bool):
    """Ingest the Analects into ChromaDB for the Confucian-axes MVP."""
    click.echo("=" * 60)
    click.echo("  ANALECTS INGESTION — Confucian concept-axes MVP")
    click.echo("=" * 60)

    if not ANALECTS_SOURCE_FILE.exists():
        click.echo(f"Source not found: {ANALECTS_SOURCE_FILE}")
        raise SystemExit(1)

    collection = get_or_create_analects_collection()
    click.echo(f"Collection '{ANALECTS_COLLECTION_NAME}' — "
               f"{collection.count()} existing chunks")

    if collection.count() > 0 and not force:
        click.echo("Already ingested (use --force to re-ingest). Nothing to do.")
        return

    if force and collection.count() > 0:
        existing = collection.get(include=[])["ids"]
        if existing:
            collection.delete(ids=existing)
        click.echo(f"  Cleared {len(existing)} existing chunks")

    cleaned = clean_text(ANALECTS_SOURCE_FILE.read_text(encoding="utf-8"))
    chunks = chunk_text(cleaned, CHUNK_SIZE, CHUNK_OVERLAP)
    ids = [f"analects_chunk_{i:04d}" for i in range(len(chunks))]
    metadatas = [
        {"source": "analects_legge_en", "language": "en", "chunk_index": i}
        for i in range(len(chunks))
    ]

    batch_size = 500
    for start in range(0, len(chunks), batch_size):
        end = min(start + batch_size, len(chunks))
        collection.add(
            documents=chunks[start:end],
            ids=ids[start:end],
            metadatas=metadatas[start:end],
        )

    click.echo(f"  Ingested {len(chunks)} chunks ({len(cleaned):,} chars)")
    click.echo(f"  Collection total: {collection.count()}")


if __name__ == "__main__":
    main()
