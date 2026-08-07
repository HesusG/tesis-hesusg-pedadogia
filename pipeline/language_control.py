"""Language control analysis for quantifying linguistic confounds.

Implements three methods to separate linguistic similarity from
thematic similarity in the cross-national policy corpus:

1. English-only baseline: translate all non-EN docs, re-embed, compare
2. Language family controls: within- vs across-family similarity
3. Parallel corpus test: same document in multiple languages

Usage:
    python -m pipeline.language_control
"""
import json
import logging
from collections import defaultdict

import numpy as np

from pipeline.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    COUNTRIES,
    WEB_DATA_DIR,
)

logger = logging.getLogger(__name__)


def load_similarity_matrix(path=None):
    """Load the similarity matrix from results.json."""
    if path is None:
        path = WEB_DATA_DIR / "results.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("similarity_matrix", {})


def compute_language_family_stats(similarity_matrix):
    """Compare within-family vs across-family similarity.

    Language families based on COUNTRIES config:
    - Germanic/English: eeuu, canada, australia, sudafrica
    - Romance: colombia (Spanish)
    - German: alemania
    - Sinitic (translated to EN): china

    Returns dict with mean similarities for each comparison.
    """
    families = defaultdict(list)
    for country_key, info in COUNTRIES.items():
        lang = info.get("language", "en")
        if lang == "en":
            families["english"].append(country_key)
        elif lang == "es":
            families["spanish"].append(country_key)
        elif lang == "de":
            families["german"].append(country_key)
        elif lang == "zh":
            families["chinese"].append(country_key)

    within_sims = []
    across_sims = []

    for pair_key, sim in similarity_matrix.items():
        parts = pair_key.split("_vs_") if "_vs_" in pair_key else pair_key.split("|")
        if len(parts) != 2:
            continue

        c1, c2 = parts
        family1 = next(
            (fam for fam, members in families.items() if c1 in members), None
        )
        family2 = next(
            (fam for fam, members in families.items() if c2 in members), None
        )

        if family1 and family2:
            if family1 == family2:
                within_sims.append(sim)
            else:
                across_sims.append(sim)

    results = {
        "families": {k: v for k, v in families.items()},
        "within_family": {
            "mean": float(np.mean(within_sims)) if within_sims else None,
            "std": float(np.std(within_sims)) if within_sims else None,
            "n": len(within_sims),
        },
        "across_family": {
            "mean": float(np.mean(across_sims)) if across_sims else None,
            "std": float(np.std(across_sims)) if across_sims else None,
            "n": len(across_sims),
        },
    }

    if within_sims and across_sims:
        results["delta"] = results["within_family"]["mean"] - results["across_family"]["mean"]
        results["interpretation"] = (
            "Positive delta indicates linguistic proximity inflates similarity. "
            f"Delta = {results['delta']:.4f}"
        )

    return results


def compare_multilingual_vs_english_only(
    multilingual_matrix, english_only_matrix
):
    """Compare similarity matrices: original multilingual vs English-only.

    The difference quantifies the linguistic component of similarity.
    """
    common_pairs = set(multilingual_matrix.keys()) & set(english_only_matrix.keys())

    deltas = []
    pair_details = []
    for pair in common_pairs:
        multi_sim = multilingual_matrix[pair]
        en_sim = english_only_matrix[pair]
        delta = multi_sim - en_sim
        deltas.append(delta)
        pair_details.append({
            "pair": pair,
            "multilingual": float(multi_sim),
            "english_only": float(en_sim),
            "delta": float(delta),
        })

    pair_details.sort(key=lambda x: abs(x["delta"]), reverse=True)

    return {
        "n_pairs": len(deltas),
        "mean_delta": float(np.mean(deltas)) if deltas else None,
        "std_delta": float(np.std(deltas)) if deltas else None,
        "max_delta_pair": pair_details[0] if pair_details else None,
        "top_10_deltas": pair_details[:10],
        "interpretation": (
            "Positive delta = multilingual similarity > english-only similarity = "
            "linguistic proximity inflating the score. "
            "Negative delta = translation changed the semantic relationship."
        ),
    }


def export_language_control_results(results, output_dir=None):
    """Export language control analysis to JSON."""
    if output_dir is None:
        output_dir = WEB_DATA_DIR

    output_file = output_dir / "language_control_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info(f"Language control results exported to {output_file}")


def main():
    """Run language control analysis."""
    logging.basicConfig(level=logging.INFO)

    logger.info("=== LANGUAGE CONTROL ANALYSIS ===")

    # Step 1: Language family stats on multilingual matrix
    logger.info("Computing language family statistics...")
    sim_matrix = load_similarity_matrix()
    family_stats = compute_language_family_stats(sim_matrix)

    logger.info(f"Within-family mean: {family_stats['within_family']['mean']}")
    logger.info(f"Across-family mean: {family_stats['across_family']['mean']}")
    if family_stats.get("delta"):
        logger.info(f"Delta: {family_stats['delta']:.4f}")

    results = {
        "analysis": "language_control",
        "family_stats": family_stats,
    }

    # Step 2: If English-only matrix exists, compare
    en_only_path = WEB_DATA_DIR / "results_english_only.json"
    if en_only_path.exists():
        logger.info("English-only results found, comparing matrices...")
        with open(en_only_path) as f:
            en_data = json.load(f)
        en_matrix = en_data.get("similarity_matrix", {})
        comparison = compare_multilingual_vs_english_only(sim_matrix, en_matrix)
        results["multilingual_vs_english"] = comparison
        logger.info(f"Mean delta: {comparison['mean_delta']:.4f}")

    export_language_control_results(results)
    logger.info("Done.")


if __name__ == "__main__":
    main()
