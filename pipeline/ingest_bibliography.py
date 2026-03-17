"""Ingest reference PDFs (bibliography) into a separate ChromaDB collection.

This populates the 'bibliografia_referencias' collection used by verify_facts.py
to fact-check numerical claims in thesis chapters.

Usage:
    python -m pipeline.ingest_bibliography [--force]
"""
import re
import click
from pathlib import Path

from .config import (
    REFERENCES_DIR, CHROMA_DIR, BIBLIOGRAPHY_COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP,
)
from .preprocess import extract_pdf, clean_text
from .ingest import chunk_text
from .embeddings import get_embedding_function

# PDFs smaller than this are likely stubs or HTML saves
MIN_TEXT_LENGTH = 500
# Skip PDFs larger than this to avoid memory issues during embedding
MAX_CHUNKS_PER_PDF = 2000


def extract_bibkey(filename: str) -> str | None:
    """Extract bibkey from reference filename.

    'maslej2024aiindex_ai-index-2024.pdf' -> 'maslej2024aiindex'
    """
    m = re.match(r"([a-z]+\d{4}[a-z0-9]*)", filename)
    return m.group(1) if m else None


def get_or_create_bib_collection():
    """Get or create the bibliography ChromaDB collection."""
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedding_fn = get_embedding_function()
    return client.get_or_create_collection(
        name=BIBLIOGRAPHY_COLLECTION_NAME,
        embedding_function=embedding_fn,
    )


def ingest_pdf(pdf_path: Path, collection, force: bool = False) -> dict:
    """Ingest a single reference PDF into the bibliography collection.

    Returns dict with keys: bibkey, status, chunks, message.
    """
    bibkey = extract_bibkey(pdf_path.name)
    if not bibkey:
        return {"bibkey": None, "status": "skip", "chunks": 0,
                "message": f"Cannot parse bibkey from {pdf_path.name}"}

    # Check if already ingested (by querying for first chunk ID)
    if not force:
        existing = collection.get(ids=[f"{bibkey}_chunk_0000"], include=[])
        if existing["ids"]:
            return {"bibkey": bibkey, "status": "skip", "chunks": 0,
                    "message": "already ingested"}

    # Extract and clean text
    try:
        raw_text = extract_pdf(pdf_path)
    except Exception as e:
        return {"bibkey": bibkey, "status": "fail", "chunks": 0,
                "message": f"PDF extraction failed: {e}"}

    cleaned = clean_text(raw_text)

    if len(cleaned) < MIN_TEXT_LENGTH:
        return {"bibkey": bibkey, "status": "warn", "chunks": 0,
                "message": f"too short ({len(cleaned)} chars) — possible stub"}

    # Chunk
    chunks = chunk_text(cleaned, CHUNK_SIZE, CHUNK_OVERLAP)
    if len(chunks) > MAX_CHUNKS_PER_PDF:
        return {"bibkey": bibkey, "status": "warn", "chunks": 0,
                "message": f"too large ({len(chunks)} chunks > {MAX_CHUNKS_PER_PDF}) — skipped"}

    # Build IDs and metadata
    ids = [f"{bibkey}_chunk_{i:04d}" for i in range(len(chunks))]
    # Extract year from bibkey (e.g., 'maslej2024aiindex' -> 2024)
    year_match = re.search(r"(\d{4})", bibkey)
    year = int(year_match.group(1)) if year_match else 0

    metadatas = [
        {
            "bibkey": bibkey,
            "title": pdf_path.stem,
            "year": year,
            "source_type": "reference",
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]

    # Delete existing chunks if force re-ingesting
    if force:
        try:
            collection.delete(where={"bibkey": bibkey})
        except Exception:
            pass

    # Add to collection in batches (ChromaDB has limits)
    batch_size = 500
    for start in range(0, len(chunks), batch_size):
        end = min(start + batch_size, len(chunks))
        collection.add(
            documents=chunks[start:end],
            ids=ids[start:end],
            metadatas=metadatas[start:end],
        )

    return {"bibkey": bibkey, "status": "ok", "chunks": len(chunks),
            "message": f"{len(chunks)} chunks ({len(cleaned):,} chars)"}


@click.command()
@click.option("--force", is_flag=True, help="Re-ingest even if already present")
def main(force: bool):
    """Ingest reference PDFs into ChromaDB for fact-checking."""
    click.echo("=" * 60)
    click.echo("  BIBLIOGRAPHY INGESTION — fact-check corpus")
    click.echo("=" * 60)

    pdf_files = sorted(REFERENCES_DIR.glob("*.pdf"))
    if not pdf_files:
        click.echo(f"No PDFs found in {REFERENCES_DIR}")
        return

    click.echo(f"Found {len(pdf_files)} PDFs in {REFERENCES_DIR}")
    collection = get_or_create_bib_collection()
    click.echo(f"Collection '{BIBLIOGRAPHY_COLLECTION_NAME}' — "
               f"{collection.count()} existing chunks\n")

    stats = {"ok": 0, "skip": 0, "warn": 0, "fail": 0}
    total_chunks = 0

    for pdf_path in pdf_files:
        result = ingest_pdf(pdf_path, collection, force=force)
        status = result["status"]
        stats[status] = stats.get(status, 0) + 1
        total_chunks += result["chunks"]

        icon = {"ok": "+", "skip": "-", "warn": "!", "fail": "X"}[status]
        bibkey = result["bibkey"] or pdf_path.name
        click.echo(f"  [{icon}] {bibkey:40s} {result['message']}")

    click.echo(f"\n{'=' * 60}")
    click.echo(f"  Ingested: {stats['ok']}  Skipped: {stats['skip']}  "
               f"Warnings: {stats['warn']}  Failed: {stats['fail']}")
    click.echo(f"  Total new chunks: {total_chunks}")
    click.echo(f"  Collection total: {collection.count()}")
    click.echo(f"{'=' * 60}")


if __name__ == "__main__":
    main()
