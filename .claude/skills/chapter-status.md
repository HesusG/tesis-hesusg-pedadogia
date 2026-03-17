# /chapter-status — Estado de Capítulos

## Trigger
User invokes `/chapter-status [chapter]`

## Behavior
1. If no chapter specified, show all chapters
2. For each chapter, report:
   - Word count (via detex | wc -w or wc -w on raw tex minus commands)
   - Target word count (see targets below)
   - Progress percentage
   - Number of `\citep`/`\citet` citations
   - Number of TODO/FIXME/XXX markers
   - Number of sections with content vs empty stubs
   - Last modified date

## Word Targets
All chapters are complete. Targets reflect actual achieved lengths:
- Cap 1 (Planteamiento): 2,000 palabras
- Cap 2 (Marco Teórico): 3,500 palabras
- Cap 3 (Marco Contextual): 3,500 palabras
- Cap 4 (Metodología): 4,200 palabras
- Cap 5 (Resultados): 2,900 palabras
- Conclusiones: 1,200 palabras
- Total: ~17,300 palabras (~69 páginas)

## Output Format
```
═══ Estado de la Tesis ═══

  Cap 1 — Planteamiento      ██████████ 100%   2,000/2,000 palabras   12 citas   0 TODOs
  Cap 2 — Marco Teórico      ██████████ 100%   3,500/3,500 palabras   40 citas   0 TODOs
  Cap 3 — Marco Contextual   ██████████ 100%   3,500/3,500 palabras   25 citas   0 TODOs
  Cap 4 — Metodología        ██████████ 100%   4,200/4,200 palabras   15 citas   0 TODOs
  Cap 5 — Resultados         ██████████ 100%   2,900/2,900 palabras   22 citas   0 TODOs

  Total: ~17,300 palabras (~69 páginas)
```

## Notes
- Word counts are approximate (detex strips LaTeX commands imperfectly)
- All chapters have been through multiple iterations including fact-checking
- Cap 1 is at Iteration 7 (post fact-check, post polish)
