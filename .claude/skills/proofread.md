# /proofread — Revisión de Texto Académico

## Trigger
User invokes `/proofread [chapter or file path]`

## Behavior
1. Read the specified chapter or file
2. Check for:
   - **Gramática española**: concordancia, tildes, puntuación, uso de subjuntivo
   - **Tono académico**: evitar coloquialismos, mantener registro formal sin ser pomposo
   - **Formato LaTeX**: comandos correctos, entornos bien cerrados, referencias cruzadas
   - **Citas**: toda afirmación sustantiva tiene `\citep{}` o `\citet{}`, no hay citas huérfanas
   - **Coherencia**: los párrafos fluyen lógicamente, las transiciones son claras
   - **Consistencia terminológica**: los mismos conceptos usan los mismos términos
3. Apply the /writing skill anti-AI patterns check
4. Report issues grouped by severity

## Output Format
```
## Revisión: [capítulo]

### Errores (corregir)
1. Línea X: [problema] → [corrección]

### Sugerencias (mejorar)
1. Línea X: [observación]

### Estadísticas
- Palabras: N
- Citas: N
- TODOs pendientes: N
```

## Guidelines
- Never add unnecessary complexity or flowery language
- Preserve the author's voice — correct errors, don't rewrite style
- Flag any paragraph longer than 200 words as potentially needing splitting
