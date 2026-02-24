"""Extract text from raw PDF policy documents."""
import re
import sys
import click
from pathlib import Path

from pypdf import PdfReader

from .config import RAW_DIR, PROCESSED_DIR, METADATA_FILE

# Map raw directory names to config.py country keys
DIR_TO_COUNTRY = {
    "australia": "australia",
    "brazil": "brasil",
    "canada": "canada",
    "chile": "chile",
    "china": "china",
    "colombia": "colombia",
    "estonia": "estonia",
    "eu": "eu",
    "finland": "finlandia",
    "france": "francia",
    "germany": "alemania",
    "india": "india",
    "japan": "japon",
    "korea": "corea",
    "mexico": "mexico",
    "oecd": "ocde",
    "singapore": "singapur",
    "spain": "espana",
    "unesco": "unesco",
    "usa": "eeuu",
    "wef": "wef",
    "worldbank": "banco_mundial",
}


def clean_text(text: str) -> str:
    """Clean extracted PDF text for embedding."""
    # Collapse multiple whitespace/newlines into single spaces
    text = re.sub(r"\s+", " ", text)
    # Remove isolated page numbers (common PDF artifact)
    text = re.sub(r"\b\d{1,3}\s*\|\s*", "", text)
    # Remove common header/footer patterns
    text = re.sub(r"Page \d+ of \d+", "", text, flags=re.IGNORECASE)
    # Remove excessive dots (table of contents leaders)
    text = re.sub(r"\.{4,}", " ", text)
    # Remove null bytes and control characters
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text.strip()


def extract_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pypdf."""
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)
    return "\n\n".join(pages)


def build_policy_id(country_key: str, filename: str) -> str:
    """Build a policy_id from country key and filename.

    E.g., ('australia', 'ai_action_plan_2021.pdf') -> 'australia_ai_action_plan_2021'
    """
    stem = Path(filename).stem  # remove .pdf
    return f"{country_key}_{stem}"


def preprocess_all(force: bool = False):
    """Extract text from all available PDFs in policies/raw/."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    results = {"processed": [], "skipped": [], "failed": []}

    for pdf_path in sorted(RAW_DIR.rglob("*.pdf")):
        dir_name = pdf_path.parent.name
        country_key = DIR_TO_COUNTRY.get(dir_name, dir_name)
        policy_id = build_policy_id(country_key, pdf_path.name)
        output_path = PROCESSED_DIR / f"{policy_id}.txt"

        if output_path.exists() and not force:
            click.echo(f"  SKIP  {policy_id} (already processed)")
            results["skipped"].append(policy_id)
            continue

        click.echo(f"  GET   {policy_id}...", nl=False)
        try:
            raw_text = extract_pdf(pdf_path)
            cleaned = clean_text(raw_text)

            if len(cleaned) < 500:
                click.echo(f" FAIL (too short: {len(cleaned)} chars)")
                results["failed"].append((policy_id, "Extracted text too short"))
                continue

            output_path.write_text(cleaned, encoding="utf-8")
            click.echo(f" OK ({len(cleaned):,} chars)")
            results["processed"].append(policy_id)
        except Exception as e:
            click.echo(f" FAIL ({e})")
            results["failed"].append((policy_id, str(e)))

    return results


@click.command()
@click.option("--force", is_flag=True, help="Reprocess even if output exists")
@click.option("--policy", help="Process a single policy by its raw dir/filename")
def main(force: bool, policy: str):
    """Extract text from raw PDF policy documents."""
    click.echo("=" * 50)
    click.echo("PDF TEXT EXTRACTION")
    click.echo("=" * 50)

    if policy:
        # Single policy mode
        pdf_path = RAW_DIR / policy
        if not pdf_path.exists():
            click.echo(f"File not found: {pdf_path}")
            sys.exit(1)
        dir_name = pdf_path.parent.name
        country_key = DIR_TO_COUNTRY.get(dir_name, dir_name)
        policy_id = build_policy_id(country_key, pdf_path.name)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

        raw_text = extract_pdf(pdf_path)
        cleaned = clean_text(raw_text)
        output_path = PROCESSED_DIR / f"{policy_id}.txt"
        output_path.write_text(cleaned, encoding="utf-8")
        click.echo(f"  OK {policy_id}: {len(cleaned):,} chars -> {output_path}")
    else:
        results = preprocess_all(force=force)
        click.echo()
        click.echo("=" * 50)
        click.echo("SUMMARY")
        click.echo("=" * 50)
        click.echo(f"  Processed: {len(results['processed'])}")
        click.echo(f"  Skipped:   {len(results['skipped'])}")
        click.echo(f"  Failed:    {len(results['failed'])}")
        if results["failed"]:
            click.echo()
            click.echo("FAILURES:")
            for pid, err in results["failed"]:
                click.echo(f"  {pid}: {err}")


if __name__ == "__main__":
    main()
