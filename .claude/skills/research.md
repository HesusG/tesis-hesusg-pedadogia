# /research — Buscar y Validar Fuentes

## Trigger
User invokes `/research <topic or query>`

## Behavior
1. Search for academic papers, policy documents, and institutional reports related to the query
2. Search in BOTH English and Spanish — this thesis covers international policies
3. For each source found:
   - Verify it's from a reputable source (peer-reviewed journal, government agency, international org)
   - Check if open access or available through common academic databases
   - Extract: author, year, title, journal/publisher, DOI/URL
4. Format as BibTeX entry ready for `document/referencias.bib`
5. Suggest where in the thesis this source is most relevant (chapter + section)
6. Flag if a similar source already exists in `document/referencias.bib` to avoid duplicates

## Output Format
```
### [Title]
- **Authors**: ...
- **Year**: ...
- **Source**: ...
- **Relevance**: Cap X, Section Y.Z
- **Open Access**: Yes/No
- **BibTeX key**: `author2024keyword`

@article{author2024keyword,
  author = {...},
  title = {...},
  ...
}
```

## Guidelines
- Prefer sources from 2019-2025 for AI education policies
- Prioritize: UNESCO, OECD, WEF, World Bank publications for international frameworks
- Include Latin American sources when available (CEPAL, OEI, BID)
- For country-specific policies, look for official government documents first
