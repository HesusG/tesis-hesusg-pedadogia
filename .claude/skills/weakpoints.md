# /weakpoints — Análisis de Puntos Débiles

## Trigger
User invokes `/weakpoints [chapter or section]`

## Behavior
1. Read the specified content carefully
2. Identify weaknesses in these categories:
   - **Lógica**: argumentos circulares, non sequiturs, saltos lógicos
   - **Evidencia**: afirmaciones sin respaldo, generalización excesiva, datos desactualizados
   - **Alcance**: scope creep (se sale del tema), promesas no cumplidas en la estructura
   - **Metodología**: debilidades en el diseño, amenazas a la validez, limitaciones no reconocidas
   - **Coherencia**: contradicciones internas, terminología inconsistente
3. Rate each weakness:
   - **CRÍTICO**: Compromete la validez del argumento
   - **IMPORTANTE**: Debilita significativamente la sección
   - **MENOR**: Mejora deseable pero no esencial
4. Suggest specific fixes for each weakness

## Output Format
```
## Puntos Débiles: [sección]

### CRÍTICO
1. **[Problema]**: [Descripción]
   - Ubicación: [línea/párrafo]
   - Sugerencia: [cómo resolver]

### IMPORTANTE
...

### MENOR
...

### Fortalezas
- [Lo que está bien hecho — siempre incluir al menos una]
```
