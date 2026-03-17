# /build-thesis — Compilar Tesis

## Trigger
User invokes `/build-thesis [--format pdf|docx|both]`

## Behavior
1. Default format: PDF
2. Run `make pdf`:
   - pdflatex → bibtex → pdflatex × 2
   - Copy to output/tesis.pdf
3. If `--format docx` or `--format both`:
   - Run `make docx`
   - Uses pandoc with citeproc
   - Copy to output/tesis.docx
4. Report any LaTeX warnings or errors
5. Show page count and word count estimate

## Error Handling
- If compilation fails, identify the problematic line and suggest fix
- Common issues: missing `\end{}`, undefined references, missing bib entries
- For docx: if pandoc not installed, provide installation command

## Pandoc Compatibility (WSL)
The docx export uses pandoc with citation processing. Compatibility varies by version:
- **pandoc >= 2.11**: Use `--citeproc` (built-in filter, preferred)
- **pandoc < 2.11**: Use `--filter pandoc-citeproc` (external filter)
- **If neither works**: Export without citation processing (`pandoc` without cite flags) — citations will appear as raw `\citep{}` keys but the document structure will be intact. The user can process citations manually in Word or via Zotero plugin.

Check pandoc version with `pandoc --version` before choosing the method.
