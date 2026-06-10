"""Retrieval engine for the UNESCO-derived evaluation rubric.

For every rubric criterion (policies/eval/rubrica.json) and every policy in the
corpus, retrieves the top-k most similar chunks from ChromaDB and writes one
auditable scoring sheet per document to policies/eval/sheets/. The researcher
scores each criterion (0-3) reading the retrieved passages; scores live in
policies/eval/scores.json, which starts as a blank template generated here.

Scale (defined in cap04): 0 = ausente, 1 = mencionado, 2 = especificado con
instrumentos, 3 = especificado con metas SMART.

Run: USE_LOCAL_EMBEDDINGS=1 python3 -m pipeline.rubric
"""
import json
from pathlib import Path

from .config import METADATA_FILE, POLICIES_DIR
from .similarity import get_collection

RUBRIC_FILE = POLICIES_DIR / "eval" / "rubrica.json"
SHEETS_DIR = POLICIES_DIR / "eval" / "sheets"
SCORES_FILE = POLICIES_DIR / "eval" / "scores.json"
TOP_K = 6


def load_rubric() -> list[dict]:
    with open(RUBRIC_FILE, encoding="utf-8") as f:
        return json.load(f)


def retrieve_for_criterion(collection, query: str, policy_id: str, k: int = TOP_K):
    """Top-k chunks of one policy for one criterion query."""
    results = collection.query(
        query_texts=[query],
        n_results=k,
        where={"policy_id": policy_id},
        include=["documents", "distances", "metadatas"],
    )
    chunks = []
    for doc, dist, meta in zip(
        results["documents"][0], results["distances"][0], results["metadatas"][0]
    ):
        chunks.append({
            "chunk_index": meta.get("chunk_index"),
            "similarity": round(1 - dist, 4),
            "text": doc,
        })
    return chunks


def build_sheets():
    rubric = load_rubric()
    collection = get_collection()
    with open(METADATA_FILE, encoding="utf-8") as f:
        metadata = json.load(f)

    SHEETS_DIR.mkdir(parents=True, exist_ok=True)
    policy_ids = [p["policy_id"] for p in metadata["policies"]]

    for pid in policy_ids:
        sheet_lines = [f"# Hoja de puntuación — {pid}", ""]
        sheet_lines.append("Escala: 0=ausente · 1=mencionado · 2=con instrumentos · 3=con metas SMART")
        sheet_lines.append("")
        for crit in rubric:
            sheet_lines.append(f"## [{crit['id']}] ({crit['bloque']})")
            sheet_lines.append(f"**Criterio**: {crit['criterio']}")
            sheet_lines.append(f"**Fuente UNESCO**: “{crit['fuente']}”")
            sheet_lines.append("")
            chunks = retrieve_for_criterion(collection, crit["consulta"], pid)
            for c in chunks:
                sheet_lines.append(
                    f"- (sim {c['similarity']:.3f}, chunk {c['chunk_index']}) {c['text'][:600]}"
                )
            sheet_lines.append("")
            sheet_lines.append("**Puntuación**: _pendiente_  |  **Justificación**: _pendiente_")
            sheet_lines.append("")
        sheet_path = SHEETS_DIR / f"{pid}.md"
        sheet_path.write_text("\n".join(sheet_lines), encoding="utf-8")
        print(f"  ✓ {sheet_path.name} ({len(rubric)} criterios × top-{TOP_K})")

    # blank score template (only created if absent — never overwrite scoring work)
    if not SCORES_FILE.exists():
        template = {
            pid: {crit["id"]: {"score": None, "justificacion": "", "instrumento": ""}
                  for crit in rubric}
            for pid in policy_ids
        }
        SCORES_FILE.write_text(
            json.dumps(template, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  ✓ Plantilla de puntuaciones → {SCORES_FILE}")


def main():
    if not RUBRIC_FILE.exists():
        raise SystemExit(f"Falta {RUBRIC_FILE}; genera la rúbrica primero.")
    build_sheets()
    print("✓ Hojas de puntuación generadas")


if __name__ == "__main__":
    main()
