"""Export top chunk pairs between similar policies for the explorer visualization."""
import json
import numpy as np
from pathlib import Path
from scipy.spatial.distance import cosine

from .config import (
    DIMENSIONS, WEB_DATA_DIR, PROCESSED_DIR,
    CHUNK_SIZE, CHUNK_OVERLAP,
)
from .similarity import get_collection
from .embeddings import get_embedding_function


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


def get_dominant_dimension(embedding, dim_embeddings: dict) -> str:
    """Find which dimension an embedding is most similar to."""
    best_dim = "gobernanza"
    best_score = -1
    for dim_key, dim_emb in dim_embeddings.items():
        sim = 1 - cosine(embedding, dim_emb)
        if sim > best_score:
            best_score = sim
            best_dim = dim_key
    return best_dim


def export_chunk_pairs(similarity_threshold: float = 0.70, top_k: int = 5):
    """Export top-k most similar chunk pairs for each policy pair above threshold."""
    # Load results.json to get similarity matrix and policy ids
    results_path = WEB_DATA_DIR / "results.json"
    if not results_path.exists():
        print("ERROR: results.json not found. Run 'make export' first.")
        return

    with open(results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    policy_ids = [p["id"] for p in results["policies"]]
    sim_matrix = results["similarity_matrix"]
    n = len(policy_ids)

    # Find pairs above threshold
    pairs_above = []
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i][j] >= similarity_threshold:
                pairs_above.append((i, j, sim_matrix[i][j]))

    print(f"Found {len(pairs_above)} pairs above threshold {similarity_threshold}")

    if not pairs_above:
        print("No pairs above threshold. Exporting empty file.")
        output = {"pairs": [], "metadata": {"threshold": similarity_threshold, "top_k": top_k}}
        WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(WEB_DATA_DIR / "chunk_pairs.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False)
        return

    # Get ChromaDB collection
    collection = get_collection()
    embedding_fn = get_embedding_function()

    # Compute dimension embeddings
    dim_embeddings = {}
    for dim_key, dim_info in DIMENSIONS.items():
        dim_embeddings[dim_key] = np.array(embedding_fn([dim_info["query"]])[0])

    # Cache: policy_id -> list of (chunk_text, embedding)
    chunk_cache = {}

    def get_chunks_with_embeddings(policy_id: str):
        if policy_id in chunk_cache:
            return chunk_cache[policy_id]

        # Read processed text
        txt_path = PROCESSED_DIR / f"{policy_id}.txt"
        if not txt_path.exists():
            print(f"  WARNING: {txt_path} not found, skipping")
            chunk_cache[policy_id] = []
            return []

        text = txt_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        # Get embeddings from ChromaDB
        results_db = collection.get(
            where={"policy_id": policy_id},
            include=["embeddings", "documents"],
        )

        if not results_db["embeddings"] or len(results_db["embeddings"]) == 0:
            # Fall back to computing embeddings from chunks
            print(f"  Computing embeddings for {policy_id} ({len(chunks)} chunks)...")
            embeddings = embedding_fn(chunks[:200])  # limit to 200 chunks
            chunk_data = list(zip(chunks[:200], embeddings))
        else:
            # Use stored chunks and embeddings
            chunk_data = list(zip(
                results_db["documents"],
                results_db["embeddings"],
            ))

        chunk_cache[policy_id] = chunk_data
        return chunk_data

    # Process each pair
    output_pairs = []
    for idx, (i, j, pair_sim) in enumerate(pairs_above):
        pid_a = policy_ids[i]
        pid_b = policy_ids[j]
        print(f"  [{idx+1}/{len(pairs_above)}] {pid_a} <-> {pid_b} (sim={pair_sim:.3f})")

        chunks_a = get_chunks_with_embeddings(pid_a)
        chunks_b = get_chunks_with_embeddings(pid_b)

        if not chunks_a or not chunks_b:
            continue

        # Compute cross-similarity between all chunk pairs
        # Use numpy for efficiency
        embs_a = np.array([e for _, e in chunks_a])
        embs_b = np.array([e for _, e in chunks_b])

        # Normalize for cosine similarity
        norms_a = np.linalg.norm(embs_a, axis=1, keepdims=True)
        norms_b = np.linalg.norm(embs_b, axis=1, keepdims=True)
        norms_a[norms_a == 0] = 1
        norms_b[norms_b == 0] = 1
        embs_a_norm = embs_a / norms_a
        embs_b_norm = embs_b / norms_b

        sim_cross = embs_a_norm @ embs_b_norm.T  # shape: (len_a, len_b)

        # Get top-k pairs
        flat_indices = np.argsort(sim_cross.ravel())[::-1][:top_k]
        top_chunks = []
        for flat_idx in flat_indices:
            ci = int(flat_idx // sim_cross.shape[1])
            cj = int(flat_idx % sim_cross.shape[1])
            chunk_sim = float(sim_cross[ci, cj])

            text_a = chunks_a[ci][0][:500]  # truncate for JSON size
            text_b = chunks_b[cj][0][:500]

            dim_a = get_dominant_dimension(chunks_a[ci][1], dim_embeddings)
            dim_b = get_dominant_dimension(chunks_b[cj][1], dim_embeddings)

            top_chunks.append({
                "chunk_a": {"text": text_a, "index": ci, "dimension": dim_a},
                "chunk_b": {"text": text_b, "index": cj, "dimension": dim_b},
                "similarity": round(chunk_sim, 4),
            })

        output_pairs.append({
            "doc_a": pid_a,
            "doc_b": pid_b,
            "similarity": round(pair_sim, 4),
            "top_chunks": top_chunks,
        })

    # Write output
    output = {
        "pairs": output_pairs,
        "metadata": {
            "threshold": similarity_threshold,
            "top_k": top_k,
            "num_pairs": len(output_pairs),
        },
    }

    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_path = WEB_DATA_DIR / "chunk_pairs.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nExported {len(output_pairs)} pairs to {out_path}")
    total_chunks = sum(len(p["top_chunks"]) for p in output_pairs)
    print(f"Total chunk entries: {total_chunks}")


if __name__ == "__main__":
    export_chunk_pairs()
