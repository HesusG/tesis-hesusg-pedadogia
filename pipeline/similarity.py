"""Similarity analysis between policy documents."""
import json
import numpy as np
from scipy.spatial.distance import cosine
from collections import defaultdict

from .config import (
    DIMENSIONS, COUNTRIES, COLLECTION_NAME, CHROMA_DIR,
    CHROMA_CLOUD_API_KEY, CHROMA_CLOUD_TENANT, CHROMA_CLOUD_DATABASE,
)
from .embeddings import get_embedding_function


def get_collection():
    """Get the ChromaDB collection (local primary, cloud fallback)."""
    import chromadb

    embedding_fn = get_embedding_function()

    # Try local first
    try:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn,
        )
        if collection.count() > 0:
            return collection
    except Exception:
        pass

    # Fall back to cloud if local is empty/missing
    if CHROMA_CLOUD_API_KEY:
        try:
            client = chromadb.CloudClient(
                api_key=CHROMA_CLOUD_API_KEY,
                tenant=CHROMA_CLOUD_TENANT,
                database=CHROMA_CLOUD_DATABASE,
            )
            return client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=embedding_fn,
            )
        except Exception:
            pass

    # Last resort: return local even if empty
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )


def get_policy_embedding(collection, policy_id: str) -> np.ndarray:
    """Get average embedding for a policy (across all its chunks)."""
    results = collection.get(
        where={"policy_id": policy_id},
        include=["embeddings"],
    )
    if results["embeddings"] is None or len(results["embeddings"]) == 0:
        raise ValueError(f"No embeddings found for {policy_id}")
    return np.mean(results["embeddings"], axis=0)


def compute_similarity_matrix(collection, policy_ids: list[str]) -> np.ndarray:
    """Compute pairwise cosine similarity matrix."""
    embeddings = {}
    for pid in policy_ids:
        try:
            embeddings[pid] = get_policy_embedding(collection, pid)
        except ValueError:
            continue

    n = len(embeddings)
    ids = list(embeddings.keys())
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1.0
            elif j > i:
                sim = 1 - cosine(embeddings[ids[i]], embeddings[ids[j]])
                matrix[i][j] = sim
                matrix[j][i] = sim

    return matrix, ids


def compute_dimension_scores(collection, policy_ids: list[str]) -> dict:
    """Score each policy on each analytical dimension using query similarity."""
    embedding_fn = get_embedding_function()
    scores = {}

    for dim_key, dim_info in DIMENSIONS.items():
        # Get embedding for the dimension query
        dim_embedding = embedding_fn([dim_info["query"]])[0]

        for pid in policy_ids:
            try:
                policy_emb = get_policy_embedding(collection, pid)
                sim = 1 - cosine(policy_emb, dim_embedding)
                if pid not in scores:
                    scores[pid] = {}
                scores[pid][dim_key] = float(sim)
            except ValueError:
                continue

    return scores


if __name__ == "__main__":
    collection = get_collection()
    # Get all policy IDs from metadata
    from .config import METADATA_FILE
    import json

    with open(METADATA_FILE) as f:
        metadata = json.load(f)
    policy_ids = [p["policy_id"] for p in metadata["policies"]]

    matrix, ids = compute_similarity_matrix(collection, policy_ids)
    print(f"Similarity matrix computed: {matrix.shape}")

    scores = compute_dimension_scores(collection, policy_ids)
    print(f"Dimension scores computed for {len(scores)} policies")
