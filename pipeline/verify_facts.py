"""Hybrid fact-checker: semantic retrieval + regex number comparison.

Embeddings locate the relevant passage; regex extracts and compares numbers.

Usage:
    python -m pipeline.verify_facts --chapter cap01
    python -m pipeline.verify_facts --chapter cap01 --n-results 15
"""
import argparse
import re
import sys
import textwrap
from pathlib import Path

from pipeline.config import PROJECT_ROOT
from pipeline.ingest_bibliography import get_or_create_bib_collection
from pipeline.verify_chapter import strip_latex

TEX_DIR = PROJECT_ROOT / "document" / "chapters"
N_RESULTS = 10

# ── Number extraction patterns ──────────────────────────────────────

NUMBER_PATTERNS = {
    "percentage": re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:%|\\%|por\s*ciento)", re.IGNORECASE
    ),
    "currency_billions": re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:mil\s*millones|billion|billones|miles?\s*de\s*millones)",
        re.IGNORECASE,
    ),
    "currency_millions": re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:millones|million)", re.IGNORECASE
    ),
    "count_with_unit": re.compile(
        r"(\d{1,3}(?:[,.\s]\d{3})*|\d+)\s+"
        r"(?:países|countries|estudios|escuelas|schools|docentes|"
        r"profesores|teachers|estudiantes|students|universidades|"
        r"instituciones|empresas|organizations|empleos|jobs|"
        r"personas|people|millones|programas|centros|"
        r"horas|hours|semanas|weeks|meses|months|años|years)",
        re.IGNORECASE,
    ),
    "ranking": re.compile(
        r"(?:lugar|rank|puesto|posición|position)\s+(\d+)", re.IGNORECASE
    ),
    "score": re.compile(
        r"(?:puntaje|score|índice|index)\s+(?:de\s+)?(\d+(?:[.,]\d+)?)",
        re.IGNORECASE,
    ),
    "year_data": re.compile(
        r"(?:en|desde|para|by|since|in)\s+(2\d{3})", re.IGNORECASE
    ),
    "plain_number": re.compile(
        r"(?<!\d)(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?!\d)"
    ),
}


def normalize_number(s: str) -> float:
    """Normalize a number string to float. Handles '1,234' and '1.234' (thousands)."""
    s = s.strip().replace(" ", "")
    # If comma-separated thousands (e.g., '1,234')
    if re.match(r"\d{1,3}(,\d{3})+$", s):
        return float(s.replace(",", ""))
    # If dot-separated thousands with no decimal (e.g., '1.234' meaning 1234)
    # Ambiguous — but in Spanish context dots can be thousands separators
    # Prefer treating as decimal if single group after dot
    s = s.replace(",", ".")
    return float(s)


def extract_numbers(text: str) -> list[dict]:
    """Extract all numbers with their type and context from text."""
    found = []
    for ntype, pattern in NUMBER_PATTERNS.items():
        if ntype == "plain_number":
            continue  # use as fallback only
        for m in pattern.finditer(text):
            try:
                value = normalize_number(m.group(1))
            except (ValueError, IndexError):
                continue
            found.append({
                "type": ntype,
                "value": value,
                "raw": m.group(0),
                "span": m.span(),
            })
    return found


# ── Claim extraction from LaTeX ──────────────────────────────────────


def extract_numeric_claims(tex_path: Path) -> list[dict]:
    """Extract sentences with citations AND numbers from a .tex file."""
    content = tex_path.read_text(encoding="utf-8")

    # Remove comments
    content = re.sub(r"%.*$", "", content, flags=re.MULTILINE)

    # Split into paragraphs
    blocks = re.split(r"\n\s*\n|\n\\(?:section|subsection)", content)

    claims = []
    claim_id = 0

    for block in blocks:
        block = block.strip()
        if not block or "\\cite" not in block:
            continue

        # Split into sentences
        plain = strip_latex(block)
        sentences = re.split(r"(?<=[.!?])\s+", plain)

        for sent in sentences:
            sent = sent.strip()
            if len(sent) < 30:
                continue

            # Extract cite keys from this sentence
            cite_markers = re.findall(r"\[CITE:([^\]]+)\]", sent)
            cite_keys = []
            for marker in cite_markers:
                cite_keys.extend(k.strip() for k in marker.split(","))

            # Clean sentence (remove CITE markers)
            clean_sent = re.sub(r"\s*\[CITE:[^\]]+\]", "", sent).strip()
            if len(clean_sent) < 30:
                continue

            # Extract numbers
            numbers = extract_numbers(clean_sent)
            if not numbers and not cite_keys:
                continue

            claim_id += 1
            claims.append({
                "id": claim_id,
                "text": clean_sent,
                "cite_keys": cite_keys,
                "numbers": numbers,
                "has_numbers": len(numbers) > 0,
            })

    return claims


# ── ChromaDB retrieval filtered by bibkey ─────────────────────────────


def retrieve_for_claim(claim: dict, collection, n_results: int) -> list[dict]:
    """Query ChromaDB bibliography collection filtered by cited bibkeys.

    Returns list of retrieval results, one per bibkey cited.
    """
    results = []
    query_text = claim["text"][:500]

    bibkeys = claim["cite_keys"]
    if not bibkeys:
        bibkeys = ["__no_cite__"]

    for bibkey in bibkeys:
        try:
            where_filter = {"bibkey": bibkey}
            response = collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            # bibkey not in collection — try without filter as fallback
            results.append({
                "bibkey": bibkey,
                "chunks": [],
                "error": f"bibkey '{bibkey}' not found in collection",
            })
            continue

        chunks = []
        distances = response["distances"][0] if response["distances"] else []
        documents = response["documents"][0] if response["documents"] else []
        metadatas = response["metadatas"][0] if response["metadatas"] else []

        for dist, doc, meta in zip(distances, documents, metadatas):
            similarity = max(0.0, 1.0 - dist / 2.0)
            chunks.append({
                "text": doc,
                "similarity": round(similarity, 3),
                "chunk_index": meta.get("chunk_index", -1),
                "numbers": extract_numbers(doc),
            })

        results.append({
            "bibkey": bibkey,
            "chunks": chunks,
            "error": None,
        })

    return results


# ── Number comparison ─────────────────────────────────────────────────


def compare_numbers(claim_numbers: list[dict], retrieval_results: list[dict]) -> list[dict]:
    """Compare each number in the claim against numbers found in source chunks.

    Returns a verdict for each claim number.
    """
    verdicts = []

    for cn in claim_numbers:
        claim_val = cn["value"]
        claim_type = cn["type"]
        best_verdict = "NOT_FOUND"
        best_source = None
        best_similarity = 0.0

        for rr in retrieval_results:
            for chunk in rr.get("chunks", []):
                for sn in chunk["numbers"]:
                    # Prefer matching same type
                    if sn["type"] != claim_type and claim_type != "plain_number":
                        continue

                    source_val = sn["value"]
                    if source_val == 0:
                        continue

                    # Exact match
                    if claim_val == source_val:
                        verdict = "EXACT_MATCH"
                    elif abs(claim_val - source_val) / max(abs(source_val), 1e-9) < 0.05:
                        verdict = "APPROXIMATE"
                    else:
                        verdict = "DIFFERENT"

                    # Keep the best verdict found
                    priority = {"EXACT_MATCH": 3, "APPROXIMATE": 2, "DIFFERENT": 1, "NOT_FOUND": 0}
                    if priority.get(verdict, 0) > priority.get(best_verdict, 0):
                        best_verdict = verdict
                        best_source = {
                            "value": source_val,
                            "raw": sn["raw"],
                            "bibkey": rr["bibkey"],
                            "chunk_index": chunk["chunk_index"],
                            "similarity": chunk["similarity"],
                        }
                        best_similarity = chunk["similarity"]
                    elif (verdict == best_verdict and
                          chunk["similarity"] > best_similarity):
                        best_source = {
                            "value": source_val,
                            "raw": sn["raw"],
                            "bibkey": rr["bibkey"],
                            "chunk_index": chunk["chunk_index"],
                            "similarity": chunk["similarity"],
                        }
                        best_similarity = chunk["similarity"]

        verdicts.append({
            "claim_value": claim_val,
            "claim_raw": cn["raw"],
            "claim_type": claim_type,
            "verdict": best_verdict,
            "source": best_source,
        })

    return verdicts


# ── Main pipeline ─────────────────────────────────────────────────────


def run_factcheck(tex_path: Path, collection, n_results: int) -> list[dict]:
    """Run the full fact-check pipeline on a chapter."""
    claims = extract_numeric_claims(tex_path)

    results = []
    for claim in claims:
        retrieval = retrieve_for_claim(claim, collection, n_results)

        # Check if any bibkey had chunks
        has_source = any(
            len(rr.get("chunks", [])) > 0 for rr in retrieval
        )

        if claim["has_numbers"]:
            verdicts = compare_numbers(claim["numbers"], retrieval)
        else:
            verdicts = []

        # Top retrieval snippet for context
        top_snippet = None
        top_sim = 0.0
        for rr in retrieval:
            for chunk in rr.get("chunks", []):
                if chunk["similarity"] > top_sim:
                    top_sim = chunk["similarity"]
                    top_snippet = chunk["text"][:150]

        results.append({
            **claim,
            "retrieval": retrieval,
            "has_source": has_source,
            "verdicts": verdicts,
            "top_similarity": top_sim,
            "top_snippet": top_snippet,
        })

    return results


# ── Report ────────────────────────────────────────────────────────────


def print_report(results: list[dict], chapter: str):
    """Print the fact-check report."""
    numeric_claims = [r for r in results if r["has_numbers"]]
    qual_claims = [r for r in results if not r["has_numbers"]]

    total_verdicts = []
    for r in numeric_claims:
        total_verdicts.extend(r["verdicts"])

    exact = sum(1 for v in total_verdicts if v["verdict"] == "EXACT_MATCH")
    approx = sum(1 for v in total_verdicts if v["verdict"] == "APPROXIMATE")
    diff = sum(1 for v in total_verdicts if v["verdict"] == "DIFFERENT")
    notfound = sum(1 for v in total_verdicts if v["verdict"] == "NOT_FOUND")
    no_source = sum(1 for r in results if not r["has_source"])

    print(f"\n{'=' * 70}")
    print(f"  FACT-CHECK: {chapter}")
    print(f"{'=' * 70}")
    print(f"  Total claims: {len(results)} "
          f"({len(numeric_claims)} numeric, {len(qual_claims)} qualitative)")
    print(f"  Claims sin source en colección: {no_source}")
    print(f"\n  Numeric verdicts ({len(total_verdicts)} numbers checked):")
    print(f"    EXACT_MATCH : {exact}")
    print(f"    APPROXIMATE : {approx}")
    print(f"    DIFFERENT   : {diff}")
    print(f"    NOT_FOUND   : {notfound}")
    print(f"{'=' * 70}\n")

    # Print numeric claims
    if numeric_claims:
        print("─── NUMERIC CLAIMS ───\n")

    for r in numeric_claims:
        text_short = textwrap.shorten(r["text"], width=90, placeholder="...")
        cite_str = ", ".join(r["cite_keys"]) if r["cite_keys"] else "(sin cita)"

        # Determine overall icon for this claim
        verdict_set = {v["verdict"] for v in r["verdicts"]}
        if "DIFFERENT" in verdict_set:
            icon = "X"
        elif "NOT_FOUND" in verdict_set and "EXACT_MATCH" not in verdict_set:
            icon = "?"
        elif "EXACT_MATCH" in verdict_set:
            icon = "+"
        elif "APPROXIMATE" in verdict_set:
            icon = "~"
        else:
            icon = "?"

        print(f"[{icon}] #{r['id']}: {text_short}")
        print(f"    Citas: [{cite_str}]")

        for v in r["verdicts"]:
            vicon = {"EXACT_MATCH": "+", "APPROXIMATE": "~",
                     "DIFFERENT": "X", "NOT_FOUND": "?"}[v["verdict"]]
            line = f"    [{vicon}] {v['claim_raw']} → {v['verdict']}"
            if v["source"]:
                s = v["source"]
                line += (f"  (source: {s['raw']} in {s['bibkey']} "
                         f"chunk {s['chunk_index']}, sim={s['similarity']:.2f})")
            print(line)

        if not r["has_source"]:
            print("    ! bibkey not found in bibliography collection")

        print()

    # Print qualitative claims without source
    no_src_qual = [r for r in qual_claims if not r["has_source"]]
    if no_src_qual:
        print("─── QUALITATIVE CLAIMS (no source in collection) ───\n")
        for r in no_src_qual:
            text_short = textwrap.shorten(r["text"], width=90, placeholder="...")
            cite_str = ", ".join(r["cite_keys"]) if r["cite_keys"] else "(sin cita)"
            print(f"  [?] #{r['id']}: {text_short}")
            print(f"      Citas: [{cite_str}]")
        print()

    # Summary of problems
    problems = [
        r for r in numeric_claims
        if any(v["verdict"] in ("DIFFERENT", "NOT_FOUND") for v in r["verdicts"])
    ]
    if problems:
        print(f"\n{'=' * 70}")
        print(f"  CLAIMS REQUIRING ATTENTION ({len(problems)})")
        print(f"{'=' * 70}")
        for r in problems:
            text_short = textwrap.shorten(r["text"], width=80, placeholder="...")
            cite_str = ", ".join(r["cite_keys"]) if r["cite_keys"] else "(sin cita)"
            verdicts_str = ", ".join(
                f"{v['claim_raw']}={v['verdict']}" for v in r["verdicts"]
            )
            print(f"  #{r['id']}: {text_short}")
            print(f"         [{cite_str}] → {verdicts_str}")
    else:
        print("\n  + All numeric claims verified successfully.")


def main():
    parser = argparse.ArgumentParser(
        description="Fact-check thesis chapter: hybrid semantic + regex verification"
    )
    parser.add_argument(
        "--chapter", required=True,
        help="Chapter identifier (e.g., cap01, cap02)",
    )
    parser.add_argument(
        "--n-results", type=int, default=N_RESULTS,
        help=f"Number of chunks to retrieve per bibkey (default: {N_RESULTS})",
    )
    args = parser.parse_args()

    # Find tex file
    tex_file = TEX_DIR / f"{args.chapter}-planteamiento.tex"
    if not tex_file.exists():
        candidates = list(TEX_DIR.glob(f"{args.chapter}*.tex"))
        if candidates:
            tex_file = candidates[0]
        else:
            print(f"ERROR: No .tex file found for chapter '{args.chapter}'")
            sys.exit(1)

    print(f"Reading: {tex_file.name}")
    collection = get_or_create_bib_collection()
    count = collection.count()
    print(f"Bibliography collection: {count} chunks")

    if count == 0:
        print("ERROR: Bibliography collection is empty. "
              "Run 'make ingest-refs' first.")
        sys.exit(1)

    results = run_factcheck(tex_file, collection, args.n_results)
    print_report(results, args.chapter)


if __name__ == "__main__":
    main()
