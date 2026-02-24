"""Export analysis results for web visualization."""
import json
import numpy as np
from datetime import datetime

from .config import (
    WEB_DATA_DIR, METADATA_FILE, DIMENSIONS, COUNTRIES, REGION_COLORS,
    EMBEDDING_MODEL_OPENAI, USE_LOCAL_EMBEDDINGS, EMBEDDING_MODEL_LOCAL,
)


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def export_results(
    similarity_matrix: np.ndarray,
    policy_ids: list[str],
    dimension_scores: dict,
    clusters: dict,
    tsne_coords: np.ndarray = None,
):
    """Export all analysis results to JSON for web visualization."""
    # Load metadata
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Build policy list with metadata
    # Detect countries with multiple policies for disambiguation
    country_counts = {}
    for pid in policy_ids:
        pm = next((p for p in metadata["policies"] if p["policy_id"] == pid), {})
        cid = pm.get("country", pid.split("_")[0])
        country_counts[cid] = country_counts.get(cid, 0) + 1

    policies = []
    for pid in policy_ids:
        policy_meta = next(
            (p for p in metadata["policies"] if p["policy_id"] == pid), {}
        )
        country_id = policy_meta.get("country", pid.split("_")[0])
        country_info = COUNTRIES.get(country_id, {})
        display_name = country_info.get("name", country_id)
        # Disambiguate when a country has multiple policies
        if country_counts.get(country_id, 1) > 1:
            short_title = policy_meta.get("title", pid).split("—")[0].split(":")[0].strip()
            # Use a short label from the policy title
            if "NEP" in pid.upper() or "nep" in pid:
                display_name += " (NEP)"
            elif "NITI" in pid.upper() or "aiforall" in pid:
                display_name += " (NITI)"
            else:
                display_name += f" ({short_title[:20]})"
        extra = {k: v for k, v in policy_meta.items()
                 if k not in ("policy_id", "country", "region")}
        policies.append({
            "id": pid,
            "country_id": country_id,
            "country": display_name,
            "region": country_info.get("region", ""),
            "region_color": REGION_COLORS.get(country_info.get("region", ""), "#666"),
            **extra,
        })

    # Build results object
    results = {
        "policies": policies,
        "similarity_matrix": similarity_matrix.tolist(),
        "policy_ids": policy_ids,
        "dimension_scores": dimension_scores,
        "dimension_labels": {k: v["label"] for k, v in DIMENSIONS.items()},
        "clusters": clusters,
        "region_colors": REGION_COLORS,
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "embedding_model": EMBEDDING_MODEL_LOCAL if USE_LOCAL_EMBEDDINGS else EMBEDDING_MODEL_OPENAI,
            "num_policies": len(policy_ids),
        },
    }

    if tsne_coords is not None:
        results["tsne"] = tsne_coords.tolist()

    # Write to web data directory
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = WEB_DATA_DIR / "results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, cls=NumpyEncoder, indent=2, ensure_ascii=False)

    print(f"✓ Results exported to {output_file}")
    return output_file


if __name__ == "__main__":
    print("Run via: python3 -m pipeline.export")
    print("Requires similarity analysis to be completed first.")
