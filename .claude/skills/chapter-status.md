# /chapter-status — Estado de Capítulos

## Trigger
User invokes `/chapter-status [chapter]`

## Behavior
1. If no chapter specified, show all chapters
2. For each chapter, report:
   - Word count (via detex | wc -w or wc -w on raw tex minus commands)
   - Target word count (Cap1: 3750, Cap2: 6250, Cap3: 5000, Cap4: 5000, Cap5: 6250)
   - Progress percentage
   - Number of `\citep`/`\citet` citations
   - Number of TODO/FIXME/XXX markers
   - Number of sections with content vs empty stubs
   - Last modified date

## Output Format
```
═══ Estado de la Tesis ═══

  Cap 1 — Planteamiento      ████████░░  80%   3,000/3,750 palabras   12 citas   2 TODOs
  Cap 2 — Marco Teórico      ██░░░░░░░░  20%   1,250/6,250 palabras    8 citas   5 TODOs
  Cap 3 — Marco Contextual   ░░░░░░░░░░   0%       0/5,000 palabras    0 citas   0 TODOs
  Cap 4 — Metodología        ░░░░░░░░░░   0%       0/5,000 palabras    0 citas   0 TODOs
  Cap 5 — Resultados         ░░░░░░░░░░   0%       0/6,250 palabras    0 citas   0 TODOs

  Total: 4,250/26,250 palabras (~17 páginas de ~105)
```
