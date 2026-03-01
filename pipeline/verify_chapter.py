"""Semantic verification of thesis chapter claims against ChromaDB policy corpus.

Usage:
    python -m pipeline.verify_chapter --chapter cap01
    python -m pipeline.verify_chapter --chapter cap01 --threshold 0.35
"""
import argparse
import re
import sys
import textwrap
from pathlib import Path

from pipeline.config import PROJECT_ROOT
from pipeline.ingest import get_or_create_collection


TEX_DIR = PROJECT_ROOT / "document" / "chapters"

# Threshold below which a claim is flagged as weakly supported
DEFAULT_THRESHOLD = 0.35
N_RESULTS = 5


def strip_latex(text: str) -> str:
    """Remove LaTeX commands, keeping readable text."""
    # Remove comments
    text = re.sub(r"%.*$", "", text, flags=re.MULTILINE)
    # Remove common environments
    text = re.sub(r"\\begin\{[^}]+\}", "", text)
    text = re.sub(r"\\end\{[^}]+\}", "", text)
    # Preserve text inside \textit, \textbf, etc.
    text = re.sub(r"\\text(?:it|bf|tt|sc)\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"\1", text)
    # Remove citations but keep a marker
    text = re.sub(r"~?\\cite[pt]?\{([^}]*)\}", r" [CITE:\1]", text)
    # Remove labels, refs, sections
    text = re.sub(r"\\(?:label|ref|section|subsection|chapter|footnote)\{[^}]*\}", "", text)
    text = re.sub(r"\\item\[?[^\]]*\]?", "", text)
    # Remove remaining commands
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    # Clean up braces and whitespace
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"``|''", '"', text)
    text = re.sub(r"~", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_claims(tex_path: Path) -> list[dict]:
    """Extract substantive claims (paragraphs with citations) from .tex file."""
    content = tex_path.read_text(encoding="utf-8")

    # Split into paragraphs (double newline or section boundaries)
    blocks = re.split(r"\n\s*\n|\n\\(?:section|subsection)", content)

    claims = []
    for i, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue
        # Skip pure structure (labels, begin/end, comments-only)
        if re.match(r"^[%\\]*(label|begin|end|chapter|section)", block):
            if "\\cite" not in block:
                continue

        # Extract cited keys
        cite_keys = re.findall(r"\\cite[pt]?\{([^}]*)\}", block)
        all_keys = []
        for ck in cite_keys:
            all_keys.extend(k.strip() for k in ck.split(","))

        plain = strip_latex(block)

        # Only keep substantive text (>40 chars and contains actual content)
        if len(plain) < 40:
            continue

        # Split long paragraphs into sentences for more precise matching
        sentences = re.split(r"(?<=[.!?])\s+", plain)
        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 30:
                continue
            # Find which cite keys this sentence references
            sent_keys = re.findall(r"\[CITE:([^\]]+)\]", sent)
            sent_cite_keys = []
            for sk in sent_keys:
                sent_cite_keys.extend(k.strip() for k in sk.split(","))
            # Clean the cite markers for the query
            clean_sent = re.sub(r"\s*\[CITE:[^\]]+\]", "", sent).strip()
            if len(clean_sent) < 30:
                continue

            claims.append({
                "text": clean_sent,
                "cite_keys": sent_cite_keys if sent_cite_keys else all_keys,
                "paragraph_idx": i,
            })

    return claims


def verify_claims(claims: list[dict], collection, threshold: float, n_results: int):
    """Query ChromaDB for each claim and assess support level."""
    results = []

    for claim in claims:
        query_text = claim["text"]
        # Truncate very long claims to avoid embedding issues
        if len(query_text) > 500:
            query_text = query_text[:500]

        try:
            response = collection.query(
                query_texts=[query_text],
                n_results=n_results,
                include=["documents", "metadatas", "distances"],
            )
        except Exception as e:
            results.append({
                **claim,
                "error": str(e),
                "matches": [],
                "best_score": 0.0,
                "support": "ERROR",
            })
            continue

        matches = []
        distances = response["distances"][0] if response["distances"] else []
        documents = response["documents"][0] if response["documents"] else []
        metadatas = response["metadatas"][0] if response["metadatas"] else []

        for dist, doc, meta in zip(distances, documents, metadatas):
            # ChromaDB returns L2 distances; convert to similarity
            # For normalized embeddings: similarity ≈ 1 - dist/2
            similarity = max(0.0, 1.0 - dist / 2.0)
            matches.append({
                "policy_id": meta.get("policy_id", "unknown"),
                "country": meta.get("country", "unknown"),
                "chunk_index": meta.get("chunk_index", -1),
                "similarity": round(similarity, 3),
                "snippet": (doc[:120] + "...") if doc and len(doc) > 120 else (doc or ""),
            })

        best_score = matches[0]["similarity"] if matches else 0.0

        if best_score >= 0.5:
            support = "STRONG"
        elif best_score >= threshold:
            support = "MODERATE"
        else:
            support = "WEAK"

        results.append({
            **claim,
            "matches": matches,
            "best_score": best_score,
            "support": support,
        })

    return results


def print_report(results: list[dict], chapter: str, threshold: float):
    """Print formatted verification report."""
    strong = sum(1 for r in results if r.get("support") == "STRONG")
    moderate = sum(1 for r in results if r.get("support") == "MODERATE")
    weak = sum(1 for r in results if r.get("support") == "WEAK")
    errors = sum(1 for r in results if r.get("support") == "ERROR")

    print(f"\n{'=' * 70}")
    print(f"  VERIFICACIÓN SEMÁNTICA: {chapter}")
    print(f"{'=' * 70}")
    print(f"  Claims analizados: {len(results)}")
    print(f"  Respaldo FUERTE (≥0.50): {strong}")
    print(f"  Respaldo MODERADO (≥{threshold:.2f}): {moderate}")
    print(f"  Respaldo DÉBIL (<{threshold:.2f}): {weak}")
    if errors:
        print(f"  Errores: {errors}")
    print(f"{'=' * 70}\n")

    for i, r in enumerate(results, 1):
        text_short = textwrap.shorten(r["text"], width=90, placeholder="...")
        cite_str = ", ".join(r["cite_keys"]) if r["cite_keys"] else "(sin cita)"

        icon = {"STRONG": "+", "MODERATE": "~", "WEAK": "!", "ERROR": "X"}
        mark = icon.get(r.get("support", "?"), "?")

        print(f"[{mark}] #{i}: {text_short}")
        print(f"    Citas: {cite_str}")
        print(f"    Score: {r.get('best_score', 0):.3f} — {r.get('support', '?')}")

        if r.get("matches"):
            top = r["matches"][0]
            print(f"    → {top['policy_id']} (chunk {top['chunk_index']}): "
                  f"{top['similarity']:.3f}")
            snippet = textwrap.shorten(top["snippet"], width=80, placeholder="...")
            print(f"      \"{snippet}\"")

        if r.get("support") == "WEAK":
            print(f"    ⚠ ATENCIÓN: respaldo semántico débil — verificar fuente")

        print()

    # Summary of weak claims
    weak_claims = [r for r in results if r.get("support") == "WEAK"]
    if weak_claims:
        print(f"\n{'=' * 70}")
        print(f"  CLAIMS CON RESPALDO DÉBIL ({len(weak_claims)})")
        print(f"{'=' * 70}")
        for i, r in enumerate(weak_claims, 1):
            text_short = textwrap.shorten(r["text"], width=80, placeholder="...")
            cite_str = ", ".join(r["cite_keys"]) if r["cite_keys"] else "(sin cita)"
            print(f"  {i}. {text_short}")
            print(f"     Citas: {cite_str} | Score: {r.get('best_score', 0):.3f}")
    else:
        print("\n  ✓ Todos los claims tienen respaldo semántico aceptable.")


def main():
    parser = argparse.ArgumentParser(
        description="Verificar claims de un capítulo contra ChromaDB"
    )
    parser.add_argument(
        "--chapter", required=True,
        help="Chapter identifier (e.g., cap01, cap02)"
    )
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"Minimum similarity for moderate support (default: {DEFAULT_THRESHOLD})"
    )
    parser.add_argument(
        "--n-results", type=int, default=N_RESULTS,
        help=f"Number of results per query (default: {N_RESULTS})"
    )
    args = parser.parse_args()

    # Find tex file
    tex_file = TEX_DIR / f"{args.chapter}-planteamiento.tex"
    if not tex_file.exists():
        # Try generic pattern
        candidates = list(TEX_DIR.glob(f"{args.chapter}*.tex"))
        if candidates:
            tex_file = candidates[0]
        else:
            print(f"ERROR: No .tex file found for chapter '{args.chapter}'")
            sys.exit(1)

    print(f"Leyendo: {tex_file.name}")
    claims = extract_claims(tex_file)
    print(f"Claims extraídos: {len(claims)}")

    print("Conectando a ChromaDB...")
    collection = get_or_create_collection()
    count = collection.count()
    print(f"Chunks en colección: {count}")

    if count == 0:
        print("ERROR: La colección ChromaDB está vacía. Ejecute 'make ingest' primero.")
        sys.exit(1)

    print(f"Verificando {len(claims)} claims (threshold={args.threshold})...")
    results = verify_claims(claims, collection, args.threshold, args.n_results)

    print_report(results, args.chapter, args.threshold)


if __name__ == "__main__":
    main()
