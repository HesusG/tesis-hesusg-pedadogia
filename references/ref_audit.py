"""Audit bibliography references against local PDFs.

Usage:
    python ref_audit.py                    # Full audit
    python ref_audit.py --chapter cap01    # Only citations in cap01
    python ref_audit.py --check            # Exit 1 if gaps exist
    python ref_audit.py --unpaywall        # Try downloading missing via Unpaywall
"""
import argparse
import json
import os
import re
import ssl
import sys
import urllib.request
import urllib.error

REFS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(REFS_DIR)
BIB_PATH = os.path.join(PROJECT_DIR, "document", "referencias.bib")
CHAPTERS_DIR = os.path.join(PROJECT_DIR, "document", "chapters")

# SSL context (some sites have cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def parse_bib(path):
    """Extract bibkeys and DOIs from a .bib file.

    Returns dict: {bibkey: {"doi": str|None, "title": str|None, "type": str}}
    """
    entries = {}
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Match each entry: @type{key, ... }
    entry_re = re.compile(
        r"@(\w+)\{([^,]+),\s*(.*?)\n\}",
        re.DOTALL,
    )
    doi_re = re.compile(r"doi\s*=\s*\{([^}]+)\}", re.IGNORECASE)
    title_re = re.compile(r"title\s*=\s*\{(.+?)\}(?:\s*,|\s*$)", re.IGNORECASE)

    for match in entry_re.finditer(text):
        entry_type = match.group(1).lower()
        bibkey = match.group(2).strip()
        body = match.group(3)

        doi_match = doi_re.search(body)
        title_match = title_re.search(body)

        entries[bibkey] = {
            "doi": doi_match.group(1).strip() if doi_match else None,
            "title": title_match.group(1).strip() if title_match else None,
            "type": entry_type,
        }

    return entries


def parse_tex_citations(path):
    """Extract all citation keys from a .tex file.

    Handles \\cite{}, \\citep{}, \\citet{}, and multi-key citations.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove comments
    text = re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)

    cite_re = re.compile(r"\\cite[tp]?\*?\{([^}]+)\}")
    keys = set()
    for match in cite_re.finditer(text):
        raw = match.group(1)
        for key in raw.split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def find_chapter_file(chapter_name):
    """Find the .tex file for a chapter name like 'cap01'."""
    patterns = [
        os.path.join(CHAPTERS_DIR, f"{chapter_name}*.tex"),
        os.path.join(CHAPTERS_DIR, f"{chapter_name}.tex"),
    ]
    import glob as g
    for pat in patterns:
        matches = g.glob(pat)
        if matches:
            return matches[0]
    return None


def scan_local_pdfs():
    """Scan references/ for PDF files and extract bibkeys from filenames.

    Naming convention: bibkey_short-title.pdf
    Returns dict: {bibkey: filename}
    """
    pdfs = {}
    for fname in os.listdir(REFS_DIR):
        if not fname.endswith(".pdf"):
            continue
        # Extract bibkey: everything before the first underscore-separated description
        # Pattern: author2024keyword_description.pdf -> bibkey = author2024keyword
        parts = fname.rsplit(".pdf", 1)[0]
        # bibkey is the part before the first underscore that follows the year+keyword
        bibkey_match = re.match(r"([a-z]+\d{4}[a-z0-9]*)", parts)
        if bibkey_match:
            pdfs[bibkey_match.group(1)] = fname
    return pdfs


def try_unpaywall(doi, bibkey):
    """Check Unpaywall for an OA PDF URL."""
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email=thesis@upaep.mx"
        req = urllib.request.Request(url, headers={"User-Agent": "Academic-Research/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read())
            if data.get("best_oa_location") and data["best_oa_location"].get("url_for_pdf"):
                return data["best_oa_location"]["url_for_pdf"]
            elif data.get("best_oa_location") and data["best_oa_location"].get("url"):
                return f"OA page (no direct PDF): {data['best_oa_location']['url']}"
    except Exception as e:
        return f"API error: {e}"
    return None


def download_pdf(url, filename):
    """Download a PDF to references/."""
    path = os.path.join(REFS_DIR, filename)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return True
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Academic-Research/1.0"
        })
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = resp.read()
            if len(data) < 500:
                return False
            with open(path, "wb") as f:
                f.write(data)
            return True
    except Exception:
        return False


def run_audit(chapter=None, check=False, unpaywall=False):
    """Run the audit and print results."""
    # Parse .bib
    bib_entries = parse_bib(BIB_PATH)

    # Determine which citations to audit
    if chapter:
        tex_path = find_chapter_file(chapter)
        if not tex_path:
            print(f"ERROR: No se encontro archivo .tex para '{chapter}'")
            print(f"  Buscando en: {CHAPTERS_DIR}")
            sys.exit(1)
        cited_keys = parse_tex_citations(tex_path)
        scope_label = os.path.basename(tex_path).replace(".tex", "")
    else:
        # All bib entries
        cited_keys = set(bib_entries.keys())
        scope_label = "todas las referencias"

    # Scan local PDFs
    local_pdfs = scan_local_pdfs()

    # Cross-reference
    with_pdf = []
    without_pdf = []
    orphan_pdfs = []

    for key in sorted(cited_keys):
        if key in local_pdfs:
            with_pdf.append((key, local_pdfs[key]))
        else:
            doi = bib_entries.get(key, {}).get("doi")
            entry_type = bib_entries.get(key, {}).get("type", "unknown")
            without_pdf.append((key, doi, entry_type))

    # Find orphan PDFs (PDFs without bib entry)
    bib_keys_set = set(bib_entries.keys())
    for bibkey, fname in local_pdfs.items():
        if bibkey not in bib_keys_set:
            orphan_pdfs.append((bibkey, fname))

    # Classify missing: books vs downloadable
    books = []
    downloadable = []
    for key, doi, entry_type in without_pdf:
        if entry_type in ("book", "incollection"):
            books.append((key, doi, entry_type))
        else:
            downloadable.append((key, doi, entry_type))

    # Print report
    print()
    print(f"{'=' * 60}")
    print(f"  Auditoria de Referencias: {scope_label}")
    print(f"{'=' * 60}")
    print()

    total = len(cited_keys)
    n_with = len(with_pdf)
    n_without = len(without_pdf)
    n_books = len(books)
    n_downloadable = len(downloadable)

    print(f"  Citas encontradas:    {total}")
    print(f"  Con PDF local:        {n_with} OK")
    print(f"  Sin PDF local:        {n_without} FALTANTES")
    if n_without > 0:
        print(f"    - Libros/capitulos: {n_books} (descarga manual)")
        print(f"    - Descargables:     {n_downloadable}")
    print()

    if chapter:
        # Check for citations not in .bib
        unknown = [k for k in cited_keys if k not in bib_entries]
        if unknown:
            print(f"  ADVERTENCIA: {len(unknown)} citas NO estan en referencias.bib:")
            for k in sorted(unknown):
                print(f"    ? {k}")
            print()

    if with_pdf:
        print(f"  CON PDF LOCAL ({n_with}):")
        for key, fname in with_pdf:
            print(f"    OK {key}")
        print()

    if downloadable:
        print(f"  FALTANTES — descargables ({n_downloadable}):")
        for key, doi, entry_type in downloadable:
            doi_str = f"DOI: {doi}" if doi else "sin DOI"
            print(f"    X  {key} — {doi_str}")
            if unpaywall and doi:
                result = try_unpaywall(doi, key)
                if result and result.startswith("http"):
                    print(f"       Unpaywall: {result}")
                    # Try downloading
                    title = bib_entries.get(key, {}).get("title", "ref")
                    short = re.sub(r'[^a-z0-9]+', '-', title.lower())[:40]
                    fname = f"{key}_{short}.pdf"
                    if download_pdf(result, fname):
                        print(f"       DESCARGADO: {fname}")
                    else:
                        print(f"       Descarga fallida")
                elif result:
                    print(f"       Unpaywall: {result}")
                else:
                    print(f"       Unpaywall: sin version OA")
        print()

    if books:
        print(f"  LIBROS/CAPITULOS — descarga manual ({n_books}):")
        for key, doi, entry_type in books:
            title = bib_entries.get(key, {}).get("title", "")
            print(f"    B  {key} — {title[:60]}")
        print()

    if orphan_pdfs:
        print(f"  PDFs HUERFANOS (sin entrada en .bib): {len(orphan_pdfs)}")
        for bibkey, fname in orphan_pdfs:
            print(f"    ?  {fname}")
        print()

    # Summary line
    coverage = (n_with / total * 100) if total > 0 else 0
    print(f"  Cobertura: {n_with}/{total} ({coverage:.0f}%)")
    print()

    # --check mode: exit 1 if there are downloadable gaps
    if check and n_downloadable > 0:
        print(f"CHECK FAILED: {n_downloadable} referencias descargables sin PDF local")
        sys.exit(1)
    elif check:
        print(f"CHECK OK: todas las referencias descargables tienen PDF local")

    return {
        "total": total,
        "with_pdf": n_with,
        "without_pdf": n_without,
        "books": n_books,
        "downloadable": n_downloadable,
        "orphans": len(orphan_pdfs),
    }


def main():
    parser = argparse.ArgumentParser(description="Auditar referencias .bib vs PDFs locales")
    parser.add_argument("--chapter", type=str, help="Filtrar por capitulo (e.g., cap01)")
    parser.add_argument("--check", action="store_true", help="Exit 1 si hay referencias descargables sin PDF")
    parser.add_argument("--unpaywall", action="store_true", help="Intentar descargar faltantes via Unpaywall")
    args = parser.parse_args()

    run_audit(chapter=args.chapter, check=args.check, unpaywall=args.unpaywall)


if __name__ == "__main__":
    main()
