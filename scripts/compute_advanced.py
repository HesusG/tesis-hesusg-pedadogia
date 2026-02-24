#!/usr/bin/env python3
"""
compute_advanced.py — Compute UMAP, dendrogram, correlations,
network edges, and Sankey data from existing results.json.

Merges new keys back into results.json for the web visualization.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

# Optional: UMAP (falls back to t-SNE coords if unavailable)
try:
    from umap import UMAP

    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False
    print("⚠ umap-learn not installed. Skipping UMAP computation.")

# ── Paths ──
PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_FILE = PROJECT_ROOT / "web" / "data" / "results.json"


def load_results():
    """Load the existing results.json."""
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_results(data):
    """Save enriched results.json."""
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Results saved to {RESULTS_FILE}")


def compute_umap(similarity_matrix):
    """Compute 2D UMAP from the similarity matrix."""
    if not HAS_UMAP:
        return None

    sim = np.array(similarity_matrix)
    # Convert similarity to distance
    dist = 1.0 - sim
    np.fill_diagonal(dist, 0)
    # Ensure symmetry
    dist = (dist + dist.T) / 2

    reducer = UMAP(
        n_components=2,
        n_neighbors=5,
        min_dist=0.3,
        metric="precomputed",
        random_state=42,
    )
    coords = reducer.fit_transform(dist)
    return coords.tolist()


def compute_dendrogram(similarity_matrix, policy_ids):
    """Compute scipy linkage matrix for D3 dendrogram."""
    sim = np.array(similarity_matrix)
    dist = 1.0 - sim
    np.fill_diagonal(dist, 0)
    dist = (dist + dist.T) / 2

    # Convert to condensed form for scipy
    condensed = squareform(dist, checks=False)
    Z = linkage(condensed, method="ward")

    return {
        "linkage_matrix": Z.tolist(),
        "labels": policy_ids,
    }


def compute_dimension_correlations(dimension_scores, dimension_labels):
    """Compute Pearson correlation matrix between the 7 dimensions."""
    dim_keys = list(dimension_labels.keys())
    policy_ids = list(dimension_scores.keys())
    n_dims = len(dim_keys)

    # Build matrix: rows = dimensions, cols = policies
    matrix = np.zeros((n_dims, len(policy_ids)))
    for j, pid in enumerate(policy_ids):
        scores = dimension_scores.get(pid, {})
        for i, dk in enumerate(dim_keys):
            matrix[i, j] = scores.get(dk, 0)

    # Pearson correlation between dimensions
    corr = np.corrcoef(matrix)

    return {
        "matrix": np.round(corr, 4).tolist(),
        "labels": [dimension_labels[k] for k in dim_keys],
    }


def compute_network_edges(similarity_matrix, policy_ids, threshold=0.70):
    """Extract edges with similarity above threshold."""
    n = len(policy_ids)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            w = similarity_matrix[i][j]
            if w >= threshold:
                edges.append(
                    {
                        "source": policy_ids[i],
                        "target": policy_ids[j],
                        "weight": round(w, 4),
                    }
                )
    edges.sort(key=lambda e: e["weight"], reverse=True)
    return edges


def compute_sankey(policies, clusters):
    """Build Sankey nodes and links: region → cluster flows."""
    region_names = {
        "europa": "Europa",
        "americas": "Américas",
        "asia_pacifico": "Asia-Pacífico",
        "internacional": "Internacional",
    }
    cluster_names = {
        "1": "Cluster 1: Tecnológico",
        "2": "Cluster 2: Integral",
        "3": "Cluster 3: Regulación",
    }

    # Build policy → cluster map
    policy_cluster = {}
    for cid, members in clusters.items():
        for pid in members:
            policy_cluster[pid] = cid

    # Build policy → region map
    policy_region = {}
    for p in policies:
        policy_region[p["id"]] = p["region"]

    # Collect unique regions and clusters used
    regions_used = sorted(set(policy_region.values()))
    clusters_used = sorted(clusters.keys())

    # Build node list: regions first, then clusters
    nodes = []
    for r in regions_used:
        nodes.append({"id": r, "label": region_names.get(r, r)})
    for c in clusters_used:
        nodes.append({"id": f"cluster_{c}", "label": cluster_names.get(c, f"Cluster {c}")})

    # Build links: region → cluster with policy details
    link_map = {}
    for p in policies:
        r = p["region"]
        c = policy_cluster.get(p["id"])
        if c is None:
            continue
        key = (r, f"cluster_{c}")
        if key not in link_map:
            link_map[key] = {"source": r, "target": f"cluster_{c}", "value": 0, "policies": []}
        link_map[key]["value"] += 1
        link_map[key]["policies"].append(p["country"])

    links = list(link_map.values())

    return {"nodes": nodes, "links": links}


def main():
    print("Loading results.json...")
    data = load_results()

    sim_matrix = data["similarity_matrix"]
    policy_ids = data["policy_ids"]
    policies = data["policies"]
    clusters = data["clusters"]
    dim_scores = data["dimension_scores"]
    dim_labels = data["dimension_labels"]

    # 1. UMAP
    print("Computing UMAP 2D projection...")
    umap_coords = compute_umap(sim_matrix)
    if umap_coords is not None:
        data["umap"] = umap_coords
        print(f"  ✓ UMAP: {len(umap_coords)} points")
    else:
        print("  ⚠ UMAP skipped (no umap-learn)")

    # 2. Dendrogram
    print("Computing dendrogram linkage...")
    dendro = compute_dendrogram(sim_matrix, policy_ids)
    data["dendrogram"] = dendro
    print(f"  ✓ Dendrogram: {len(dendro['linkage_matrix'])} merges")

    # 3. Dimension correlations
    print("Computing dimension correlations...")
    dim_corr = compute_dimension_correlations(dim_scores, dim_labels)
    data["dimension_correlations"] = dim_corr
    print(f"  ✓ Correlations: {len(dim_corr['labels'])}×{len(dim_corr['labels'])} matrix")

    # 4. Network edges
    print("Computing network edges (threshold=0.70)...")
    edges = compute_network_edges(sim_matrix, policy_ids, threshold=0.70)
    data["network_edges"] = edges
    print(f"  ✓ Network: {len(edges)} edges above threshold")

    # 5. Sankey
    print("Computing Sankey data...")
    sankey = compute_sankey(policies, clusters)
    data["sankey"] = sankey
    print(f"  ✓ Sankey: {len(sankey['nodes'])} nodes, {len(sankey['links'])} links")

    # Save
    save_results(data)
    print("\n✓ All advanced computations complete.")


if __name__ == "__main__":
    main()
