"""Cluster analysis and pattern identification."""
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import squareform
from sklearn.manifold import TSNE

from .config import COUNTRIES, REGION_COLORS


def hierarchical_clustering(similarity_matrix: np.ndarray, policy_ids: list[str], threshold: float = 0.5):
    """Perform hierarchical clustering on the similarity matrix."""
    # Convert similarity to distance
    distance_matrix = 1 - similarity_matrix
    np.fill_diagonal(distance_matrix, 0)

    # Condensed distance matrix
    condensed = squareform(distance_matrix)

    # Hierarchical clustering
    Z = linkage(condensed, method="ward")

    # Cut tree at threshold
    clusters = fcluster(Z, t=threshold, criterion="distance")

    # Group policies by cluster
    cluster_groups = {}
    for pid, cluster_id in zip(policy_ids, clusters):
        cluster_id = int(cluster_id)
        if cluster_id not in cluster_groups:
            cluster_groups[cluster_id] = []
        cluster_groups[cluster_id].append(pid)

    return cluster_groups, Z


def compute_tsne(similarity_matrix: np.ndarray, perplexity: int = 5) -> np.ndarray:
    """Compute t-SNE projection for visualization."""
    distance_matrix = 1 - similarity_matrix
    np.fill_diagonal(distance_matrix, 0)

    tsne = TSNE(
        n_components=2,
        perplexity=min(perplexity, len(similarity_matrix) - 1),
        metric="precomputed",
        init="random",
        random_state=42,
    )
    return tsne.fit_transform(distance_matrix)


def validate_clusters(cluster_groups: dict, policy_ids: list[str]) -> dict:
    """Compare clusters against known geopolitical groupings."""
    validation = {}
    for cluster_id, members in cluster_groups.items():
        regions = []
        for pid in members:
            for country_id, info in COUNTRIES.items():
                if pid.startswith(country_id):
                    regions.append(info["region"])
                    break
        validation[cluster_id] = {
            "members": members,
            "regions": regions,
            "region_coherence": len(set(regions)) == 1 if regions else False,
        }
    return validation
