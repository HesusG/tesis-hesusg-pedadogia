"""Ingesta de documentos de política al ChromaDB."""
import json
import click
from pathlib import Path
from tqdm import tqdm

from .config import (
    RAW_DIR, PROCESSED_DIR, METADATA_FILE, CHROMA_DIR,
    COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP,
    OPENAI_API_KEY, USE_LOCAL_EMBEDDINGS,
    EMBEDDING_MODEL_OPENAI, EMBEDDING_MODEL_LOCAL,
    CHROMA_CLOUD_API_KEY, CHROMA_CLOUD_TENANT, CHROMA_CLOUD_DATABASE,
)
from .embeddings import get_embedding_function


def load_metadata():
    """Load policy metadata from JSON."""
    if METADATA_FILE.exists():
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"policies": []}


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


def read_processed_file(policy_id: str) -> str:
    """Read a processed text file for a policy."""
    # Search in processed directory
    for txt_file in PROCESSED_DIR.rglob(f"{policy_id}*.txt"):
        return txt_file.read_text(encoding="utf-8")
    raise FileNotFoundError(f"No processed file found for {policy_id}")


def ingest_policy(policy_id: str, collection):
    """Ingest a single policy into ChromaDB."""
    metadata = load_metadata()
    policy = next((p for p in metadata["policies"] if p["policy_id"] == policy_id), None)
    if not policy:
        raise ValueError(f"Policy {policy_id} not found in metadata.json")

    text = read_processed_file(policy_id)
    chunks = chunk_text(text)

    ids = [f"{policy_id}_chunk_{i:04d}" for i in range(len(chunks))]
    metadatas = [
        {
            "policy_id": policy_id,
            "country": policy["country"],
            "region": policy["region"],
            "year": policy.get("year", 0),
            "language": policy.get("language", ""),
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ]

    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    return len(chunks)


def get_or_create_collection():
    """Get or create the local ChromaDB collection."""
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedding_fn = get_embedding_function()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )
    return collection


def get_or_create_cloud_collection():
    """Get or create the Chroma Cloud collection for redundancy."""
    if not CHROMA_CLOUD_API_KEY:
        return None
    import chromadb

    try:
        client = chromadb.CloudClient(
            api_key=CHROMA_CLOUD_API_KEY,
            tenant=CHROMA_CLOUD_TENANT,
            database=CHROMA_CLOUD_DATABASE,
        )
        embedding_fn = get_embedding_function()
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn,
        )
        return collection
    except Exception as e:
        click.echo(f"  ⚠ Chroma Cloud unavailable: {e}")
        return None


def sync_to_cloud(policy_id: str, chunks: list[str], ids: list[str], metadatas: list[dict], cloud_collection):
    """Sync ingested chunks to Chroma Cloud."""
    if cloud_collection is None:
        return
    try:
        cloud_collection.upsert(documents=chunks, ids=ids, metadatas=metadatas)
    except Exception as e:
        click.echo(f"  ⚠ Cloud sync failed for {policy_id}: {e}")


@click.command()
@click.option("--all", "ingest_all", is_flag=True, help="Ingest all policies")
@click.option("--policy", help="Ingest a specific policy by ID")
@click.option("--no-cloud", is_flag=True, help="Skip Chroma Cloud sync")
def main(ingest_all: bool, policy: str, no_cloud: bool):
    """Ingest policy documents into ChromaDB (local + cloud)."""
    collection = get_or_create_collection()
    cloud_collection = None if no_cloud else get_or_create_cloud_collection()
    metadata = load_metadata()

    if cloud_collection:
        click.echo("☁ Chroma Cloud connected — syncing enabled")

    if policy:
        n = ingest_policy(policy, collection)
        click.echo(f"✓ {policy}: {n} chunks ingested (local)")
        # Sync to cloud
        text = read_processed_file(policy)
        chunks = chunk_text(text)
        p_meta = next((p for p in metadata["policies"] if p["policy_id"] == policy), {})
        ids = [f"{policy}_chunk_{i:04d}" for i in range(len(chunks))]
        metadatas = [{"policy_id": policy, "country": p_meta.get("country", ""), "region": p_meta.get("region", ""), "year": p_meta.get("year", 0), "language": p_meta.get("language", ""), "chunk_index": i} for i in range(len(chunks))]
        sync_to_cloud(policy, chunks, ids, metadatas, cloud_collection)
    elif ingest_all:
        for p in tqdm(metadata["policies"], desc="Ingesting policies"):
            try:
                text = read_processed_file(p["policy_id"])
                chunks = chunk_text(text)
                ids = [f"{p['policy_id']}_chunk_{i:04d}" for i in range(len(chunks))]
                metadatas = [{"policy_id": p["policy_id"], "country": p["country"], "region": p["region"], "year": p.get("year", 0), "language": p.get("language", ""), "chunk_index": i} for i in range(len(chunks))]
                collection.add(documents=chunks, ids=ids, metadatas=metadatas)
                click.echo(f"  ✓ {p['policy_id']}: {len(chunks)} chunks (local)")
                sync_to_cloud(p["policy_id"], chunks, ids, metadatas, cloud_collection)
            except FileNotFoundError:
                click.echo(f"  ✗ {p['policy_id']}: no processed file found")
    else:
        click.echo("Use --all or --policy <id>")


if __name__ == "__main__":
    main()
