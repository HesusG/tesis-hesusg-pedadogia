"""Run the full analysis pipeline: preprocess → ingest → similarity → analysis → export."""
import json
import sys
import click
import numpy as np

from .config import METADATA_FILE, PROCESSED_DIR, CHROMA_DIR, WEB_DATA_DIR
from .preprocess import preprocess_all
from .ingest import load_metadata, chunk_text, get_or_create_collection
from .embeddings import get_embedding_function
from .similarity import get_collection, compute_similarity_matrix, compute_dimension_scores
from .analysis import hierarchical_clustering, compute_tsne, validate_clusters
from .export import export_results


@click.command()
@click.option("--skip-preprocess", is_flag=True, help="Skip PDF extraction step")
@click.option("--skip-ingest", is_flag=True, help="Skip ChromaDB ingestion step")
@click.option("--force", is_flag=True, help="Force reprocessing of all steps")
@click.option("--no-cloud", is_flag=True, help="Skip Chroma Cloud sync")
def main(skip_preprocess: bool, skip_ingest: bool, force: bool, no_cloud: bool):
    """Run the full analysis pipeline."""

    # ── Step 1: Preprocess PDFs ──
    if not skip_preprocess:
        click.echo("\n" + "=" * 50)
        click.echo("STEP 1: PDF TEXT EXTRACTION")
        click.echo("=" * 50)
        results = preprocess_all(force=force)
        total = len(results["processed"]) + len(results["skipped"])
        click.echo(f"  Ready: {total} documents")
        if results["failed"]:
            click.echo(f"  Failed: {len(results['failed'])}")
    else:
        click.echo("\n  [Skipping preprocessing]")

    # ── Step 2: Ingest into ChromaDB ──
    if not skip_ingest:
        click.echo("\n" + "=" * 50)
        click.echo("STEP 2: CHROMADB INGESTION")
        click.echo("=" * 50)

        metadata = load_metadata()
        if not metadata["policies"]:
            click.echo("  No policies in metadata.json!")
            sys.exit(1)

        collection = get_or_create_collection()

        if force:
            # Delete existing collection and recreate
            import chromadb
            client = chromadb.PersistentClient(path=str(CHROMA_DIR))
            try:
                client.delete_collection("politicas_ia_educacion")
            except Exception:
                pass
            collection = get_or_create_collection()

        ingested = 0
        for p in metadata["policies"]:
            pid = p["policy_id"]
            txt_path = PROCESSED_DIR / f"{pid}.txt"
            if not txt_path.exists():
                click.echo(f"  SKIP  {pid} (no processed file)")
                continue

            # Check if already ingested
            existing = collection.get(where={"policy_id": pid})
            if existing["ids"] and not force:
                click.echo(f"  SKIP  {pid} (already in ChromaDB)")
                continue

            text = txt_path.read_text(encoding="utf-8")
            chunks = chunk_text(text)
            ids = [f"{pid}_chunk_{i:04d}" for i in range(len(chunks))]
            metadatas = [
                {
                    "policy_id": pid,
                    "country": p["country"],
                    "region": p["region"],
                    "year": p.get("year", 0),
                    "language": p.get("language", ""),
                    "chunk_index": i,
                }
                for i in range(len(chunks))
            ]
            collection.add(documents=chunks, ids=ids, metadatas=metadatas)
            click.echo(f"  OK    {pid}: {len(chunks)} chunks")
            ingested += 1

        click.echo(f"  Total ingested: {ingested}")
        click.echo(f"  Collection size: {collection.count()} chunks")
    else:
        click.echo("\n  [Skipping ingestion]")

    # ── Step 3: Similarity analysis ──
    click.echo("\n" + "=" * 50)
    click.echo("STEP 3: SIMILARITY ANALYSIS")
    click.echo("=" * 50)

    metadata = load_metadata()
    policy_ids = [p["policy_id"] for p in metadata["policies"]
                  if (PROCESSED_DIR / f"{p['policy_id']}.txt").exists()]

    if len(policy_ids) < 2:
        click.echo("  Need at least 2 policies for similarity analysis!")
        sys.exit(1)

    collection = get_collection()
    click.echo(f"  Computing similarity matrix for {len(policy_ids)} policies...")
    sim_matrix, valid_ids = compute_similarity_matrix(collection, policy_ids)
    click.echo(f"  Matrix shape: {sim_matrix.shape}")

    click.echo(f"  Computing dimension scores (7 dimensions)...")
    dim_scores = compute_dimension_scores(collection, valid_ids)
    click.echo(f"  Scores computed for {len(dim_scores)} policies")

    # ── Step 4: Clustering ──
    click.echo("\n" + "=" * 50)
    click.echo("STEP 4: CLUSTERING & VISUALIZATION")
    click.echo("=" * 50)

    clusters, linkage_matrix = hierarchical_clustering(sim_matrix, valid_ids)
    click.echo(f"  Found {len(clusters)} clusters")
    for cid, members in clusters.items():
        click.echo(f"    Cluster {cid}: {', '.join(members)}")

    validation = validate_clusters(clusters, valid_ids)
    for cid, info in validation.items():
        coherent = "coherent" if info["region_coherence"] else "mixed"
        click.echo(f"    Cluster {cid}: {coherent} ({', '.join(set(info['regions']))})")

    tsne_coords = None
    if len(valid_ids) >= 4:
        tsne_coords = compute_tsne(sim_matrix, perplexity=min(5, len(valid_ids) - 1))
        click.echo(f"  t-SNE projection computed")

    # ── Step 5: Export ──
    click.echo("\n" + "=" * 50)
    click.echo("STEP 5: EXPORT RESULTS")
    click.echo("=" * 50)

    output_file = export_results(
        similarity_matrix=sim_matrix,
        policy_ids=valid_ids,
        dimension_scores=dim_scores,
        clusters=clusters,
        tsne_coords=tsne_coords,
    )

    click.echo(f"\n{'=' * 50}")
    click.echo("PIPELINE COMPLETE")
    click.echo(f"{'=' * 50}")
    click.echo(f"  Policies analyzed: {len(valid_ids)}")
    click.echo(f"  Results: {output_file}")


if __name__ == "__main__":
    main()
