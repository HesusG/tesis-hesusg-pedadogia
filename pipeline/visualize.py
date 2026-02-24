"""Generate figures for the LaTeX thesis."""
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from .config import FIGURES_DIR, WEB_DATA_DIR, DIMENSIONS, REGION_COLORS


def setup_style():
    """Configure matplotlib for thesis-quality figures."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def plot_similarity_heatmap(results: dict, output_path: Path):
    """Generate similarity matrix heatmap."""
    matrix = np.array(results["similarity_matrix"])
    labels = [p["country"] for p in results["policies"]]

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        matrix,
        xticklabels=labels,
        yticklabels=labels,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd",
        vmin=0,
        vmax=1,
        ax=ax,
    )
    ax.set_title("Matriz de Similitud Semántica entre Políticas")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    fig.savefig(output_path / "heatmap_similitud.pdf")
    plt.close()


def plot_dimension_radar(results: dict, policy_ids: list[str], output_path: Path):
    """Generate radar chart comparing policies across dimensions."""
    dim_labels = list(results["dimension_labels"].values())
    n_dims = len(dim_labels)
    angles = np.linspace(0, 2 * np.pi, n_dims, endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for pid in policy_ids:
        if pid in results["dimension_scores"]:
            values = [results["dimension_scores"][pid].get(k, 0) for k in results["dimension_labels"].keys()]
            values += values[:1]
            policy_name = next(
                (p["country"] for p in results["policies"] if p["id"] == pid),
                pid,
            )
            ax.plot(angles, values, "o-", label=policy_name)
            ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_labels, size=9)
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    ax.set_title("Comparación por Dimensiones de Análisis")
    fig.savefig(output_path / "radar_dimensiones.pdf")
    plt.close()


def generate_all_figures():
    """Generate all thesis figures from results data."""
    setup_style()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    results_file = WEB_DATA_DIR / "results.json"
    if not results_file.exists():
        print("✗ No results.json found. Run pipeline first.")
        return

    with open(results_file, "r", encoding="utf-8") as f:
        results = json.load(f)

    plot_similarity_heatmap(results, FIGURES_DIR)
    print("  ✓ Heatmap de similitud")

    # Radar for a selection of policies
    if results["policies"]:
        sample_ids = [p["id"] for p in results["policies"][:4]]
        plot_dimension_radar(results, sample_ids, FIGURES_DIR)
        print("  ✓ Radar de dimensiones")

    print(f"✓ Figuras generadas en {FIGURES_DIR}")


if __name__ == "__main__":
    generate_all_figures()
