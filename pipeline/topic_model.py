"""Unsupervised topic modeling with BERTopic.

This module runs BEFORE any supervised dimension analysis.
Results should be committed to git before applying the pre-registered
dimension framework, to maintain the unsupervised-first principle.

Usage:
    python -m pipeline.topic_model [--nr-topics auto] [--min-topic-size 5]
"""
import json
import logging
from pathlib import Path

import numpy as np

from pipeline.config import (
    BERTOPIC_MIN_TOPIC_SIZE,
    BERTOPIC_NR_TOPICS,
    CHROMA_DIR,
    COLLECTION_NAME,
    FIGURES_DIR,
    WEB_DATA_DIR,
)

logger = logging.getLogger(__name__)


def load_chunks_from_chroma():
    """Load all chunks and their embeddings from ChromaDB."""
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.get(include=["documents", "metadatas", "embeddings"])
    documents = results["documents"]
    metadatas = results["metadatas"]
    embeddings = np.array(results["embeddings"])

    logger.info(f"Loaded {len(documents)} chunks from ChromaDB")
    return documents, metadatas, embeddings


def run_bertopic(
    documents,
    embeddings,
    nr_topics=BERTOPIC_NR_TOPICS,
    min_topic_size=BERTOPIC_MIN_TOPIC_SIZE,
):
    """Run BERTopic on the corpus chunks.

    Returns the fitted model, topics, and probabilities.
    """
    from bertopic import BERTopic
    from umap import UMAP

    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )

    topic_model = BERTopic(
        umap_model=umap_model,
        nr_topics=nr_topics if nr_topics != "auto" else None,
        min_topic_size=min_topic_size,
        verbose=True,
    )

    topics, probs = topic_model.fit_transform(documents, embeddings)

    topic_info = topic_model.get_topic_info()
    logger.info(f"Found {len(topic_info) - 1} topics (excluding outlier topic -1)")
    logger.info(f"Topic distribution: {topic_info[['Topic', 'Count']].to_string()}")

    return topic_model, topics, probs


def compute_topic_distribution_per_document(topics, metadatas):
    """Compute topic distribution per policy document.

    Returns a dict: {policy_id: {topic_id: count}}.
    """
    doc_topics = {}
    for topic, meta in zip(topics, metadatas):
        policy_id = meta.get("policy_id", "unknown")
        if policy_id not in doc_topics:
            doc_topics[policy_id] = {}
        doc_topics[policy_id][topic] = doc_topics[policy_id].get(topic, 0) + 1

    return doc_topics


def export_results(topic_model, topics, probs, metadatas, output_dir=None):
    """Export topic model results as JSON for the web visualization."""
    if output_dir is None:
        output_dir = WEB_DATA_DIR

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Topic info
    topic_info = topic_model.get_topic_info()
    topic_data = []
    for _, row in topic_info.iterrows():
        if row["Topic"] == -1:
            continue
        topic_words = topic_model.get_topic(row["Topic"])
        topic_data.append({
            "topic_id": int(row["Topic"]),
            "count": int(row["Count"]),
            "name": row.get("Name", f"Topic_{row['Topic']}"),
            "top_words": [{"word": w, "weight": float(s)} for w, s in topic_words[:10]],
        })

    # Per-document distribution
    doc_topics = compute_topic_distribution_per_document(topics, metadatas)

    results = {
        "model": "BERTopic",
        "n_topics": len(topic_data),
        "n_chunks": len(topics),
        "topics": topic_data,
        "document_distributions": doc_topics,
    }

    output_file = output_dir / "topic_model_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info(f"Topic model results exported to {output_file}")
    return results


def main():
    """Run the full unsupervised topic modeling pipeline."""
    logging.basicConfig(level=logging.INFO)

    logger.info("=== UNSUPERVISED TOPIC MODELING (Phase 1) ===")
    logger.info("Loading chunks from ChromaDB...")
    documents, metadatas, embeddings = load_chunks_from_chroma()

    logger.info("Running BERTopic...")
    topic_model, topics, probs = run_bertopic(documents, embeddings)

    logger.info("Exporting results...")
    results = export_results(topic_model, topics, probs, metadatas)

    logger.info(f"Done. Found {results['n_topics']} topics across {results['n_chunks']} chunks.")
    return topic_model, topics, probs


if __name__ == "__main__":
    main()
