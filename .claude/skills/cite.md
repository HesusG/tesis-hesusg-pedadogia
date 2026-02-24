# /cite — Gestionar Citas

## Trigger
User invokes `/cite <search query or DOI>`

## Behavior
1. Search for the reference by query or DOI
2. Check if already exists in `document/referencias.bib`
3. If not found:
   - Generate BibTeX entry
   - Suggest BibTeX key: `apellido2024keyword`
   - Add to `document/referencias.bib`
4. If found:
   - Show existing entry and its key
5. Show usage example: `\citep{key}` or `\citet{key}`

## Key Format
- Single author: `garcia2024inteligencia`
- Two authors: `garcialopez2024`
- Three+: `garcia_etal2024`
- Organization: `unesco2024ai`

## Guidelines
- Always use Spanish field names where applicable
- Include DOI when available
- For web documents, include `url` and `urldate` fields
- For government documents, use `@techreport` or `@misc`
