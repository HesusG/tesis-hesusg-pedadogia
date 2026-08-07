"""Pre-registration validation: compare unsupervised topics to pre-registered dimensions.

This module compares the output of BERTopic (unsupervised Phase 1) against
the pre-registered 7-dimension framework (supervised Phase 2) to assess:

1. Which pre-registered dimensions emerge naturally in the unsupervised analysis?
2. Which BERTopic topics do NOT map to any pre-registered dimension? (blind spots)
3. Which pre-registered dimensions do NOT appear in BERTopic? (imposed structure)

The comparison is the core methodological contribution of v2: demonstrating
whether analyst-defined frameworks capture the actual structure of the data.

Usage:
    python -m pipeline.validation
"""
import json
import logging
from pathlib import Path

import numpy as np

from pipeline.config import DIMENSIONS, WEB_DATA_DIR

logger = logging.getLogger(__name__)


def load_topic_results(path=None):
    """Load BERTopic results from JSON."""
    if path is None:
        path = WEB_DATA_DIR / "topic_model_results.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_dimension_scores(path=None):
    """Load supervised dimension scores from results.json."""
    if path is None:
        path = WEB_DATA_DIR / "results.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("dimension_scores", {})


def compute_topic_dimension_overlap(topic_results, embedding_model=None):
    """Compute semantic overlap between BERTopic topics and pre-registered dimensions.

    For each BERTopic topic, compute cosine similarity of its top words
    against each dimension query. High similarity = the topic maps to
    that dimension. Low similarity across all dimensions = a "blind spot"
    that the pre-registered framework misses.
    """
    if embedding_model is None:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    # Embed dimension queries
    dim_queries = {
        key: dim["query"] for key, dim in DIMENSIONS.items()
    }
    dim_keys = list(dim_queries.keys())
    dim_embeddings = embedding_model.encode(list(dim_queries.values()))

    # For each topic, create a text representation from top words
    topic_texts = []
    topic_ids = []
    for topic in topic_results.get("topics", []):
        words = " ".join([w["word"] for w in topic.get("top_words", [])])
        topic_texts.append(words)
        topic_ids.append(topic["topic_id"])

    if not topic_texts:
        logger.warning("No topics found in results")
        return {}

    topic_embeddings = embedding_model.encode(topic_texts)

    # Compute cosine similarity matrix (topics × dimensions)
    from numpy.linalg import norm

    overlap_matrix = []
    for t_emb in topic_embeddings:
        row = []
        for d_emb in dim_embeddings:
            sim = float(np.dot(t_emb, d_emb) / (norm(t_emb) * norm(d_emb)))
            row.append(sim)
        overlap_matrix.append(row)

    overlap_matrix = np.array(overlap_matrix)

    # Analyze results
    results = {
        "topic_dimension_similarities": {},
        "unmapped_topics": [],
        "unmapped_dimensions": [],
        "coverage_summary": {},
    }

    # For each topic: which dimension is closest?
    MAPPING_THRESHOLD = 0.5
    mapped_dimensions = set()

    for i, topic_id in enumerate(topic_ids):
        best_dim_idx = int(np.argmax(overlap_matrix[i]))
        best_dim = dim_keys[best_dim_idx]
        best_sim = float(overlap_matrix[i][best_dim_idx])

        topic_name = topic_results["topics"][i].get("name", f"Topic_{topic_id}")
        entry = {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "best_dimension": best_dim,
            "best_similarity": best_sim,
            "all_similarities": {
                dim_keys[j]: float(overlap_matrix[i][j])
                for j in range(len(dim_keys))
            },
        }

        results["topic_dimension_similarities"][str(topic_id)] = entry

        if best_sim >= MAPPING_THRESHOLD:
            mapped_dimensions.add(best_dim)
        else:
            results["unmapped_topics"].append({
                "topic_id": topic_id,
                "topic_name": topic_name,
                "top_words": [w["word"] for w in topic_results["topics"][i].get("top_words", [])[:5]],
                "best_dimension": best_dim,
                "best_similarity": best_sim,
                "interpretation": (
                    f"This topic does not clearly map to any pre-registered dimension "
                    f"(max similarity: {best_sim:.3f} with {best_dim}). "
                    f"This may represent a blind spot in the analytical framework."
                ),
            })

    # Which dimensions have no matching topic?
    for dim_key in dim_keys:
        if dim_key not in mapped_dimensions:
            results["unmapped_dimensions"].append({
                "dimension": dim_key,
                "label": DIMENSIONS[dim_key]["label"],
                "interpretation": (
                    f"No BERTopic cluster strongly maps to '{DIMENSIONS[dim_key]['label']}'. "
                    f"This dimension may be imposed by the framework rather than "
                    f"emerging naturally from the corpus."
                ),
            })

    results["coverage_summary"] = {
        "total_topics": len(topic_ids),
        "mapped_topics": len(topic_ids) - len(results["unmapped_topics"]),
        "unmapped_topics": len(results["unmapped_topics"]),
        "total_dimensions": len(dim_keys),
        "covered_dimensions": len(mapped_dimensions),
        "uncovered_dimensions": len(dim_keys) - len(mapped_dimensions),
        "mapping_threshold": MAPPING_THRESHOLD,
    }

    return results


def export_validation_results(results, output_dir=None):
    """Export validation results as JSON."""
    if output_dir is None:
        output_dir = WEB_DATA_DIR

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "validation_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info(f"Validation results exported to {output_file}")


def main():
    """Run the pre-registration validation pipeline."""
    logging.basicConfig(level=logging.INFO)

    logger.info("=== PRE-REGISTRATION VALIDATION ===")
    logger.info("Comparing unsupervised topics to pre-registered dimensions...")

    topic_results = load_topic_results()
    logger.info(f"Loaded {topic_results['n_topics']} BERTopic topics")

    results = compute_topic_dimension_overlap(topic_results)

    summary = results.get("coverage_summary", {})
    logger.info(f"Mapped topics: {summary.get('mapped_topics')}/{summary.get('total_topics')}")
    logger.info(f"Covered dimensions: {summary.get('covered_dimensions')}/{summary.get('total_dimensions')}")

    if results.get("unmapped_topics"):
        logger.info("=== BLIND SPOTS (topics not in framework) ===")
        for t in results["unmapped_topics"]:
            logger.info(f"  Topic {t['topic_id']}: {t['top_words']}")

    if results.get("unmapped_dimensions"):
        logger.info("=== IMPOSED STRUCTURE (dimensions not in data) ===")
        for d in results["unmapped_dimensions"]:
            logger.info(f"  {d['dimension']}: {d['label']}")

    export_validation_results(results)
    logger.info("Done.")


if __name__ == "__main__":
    main()
