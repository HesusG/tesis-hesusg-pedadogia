# /fact-check — Pipeline Híbrido de Verificación

## Trigger
User invokes `/fact-check [capítulo]` (default: cap01)

## Behavior
1. **Verificar colección**: Comprobar que la colección `bibliografia_referencias` existe en ChromaDB y tiene chunks. Si está vacía o no existe:
   - Ejecutar `make ingest-refs` primero
   - Verificar que los PDFs de referencias están en `references/`
   - Reportar cuántos PDFs se ingirieron y cuántos chunks se crearon
2. **Ejecutar fact-check**: Correr `make factcheck-cap01` (o el target del capítulo indicado).
3. **Interpretar resultados**: Parsear la salida y resumir:
   - **EXACT_MATCH**: Claims verificados correctamente (listar conteo)
   - **DIFFERENT**: Claims con datos que no coinciden (mostrar cada uno con corrección sugerida)
   - **NOT_FOUND**: Claims donde no se encontró respaldo (advertir que puede ser PDF stub o claim sin fuente)
4. **Reporte**: Mostrar resumen con porcentajes y acciones sugeridas.

## Prerequisitos
- PDFs de bibliografía en `references/` (ver `references/MANIFEST.md`)
- ChromaDB disponible (local `.chroma_db/` o cloud)
- Módulos: `pipeline/ingest_bibliography.py`, `pipeline/verify_facts.py`

## Output Format
```
═══ Fact-Check: Cap 01 ═══

Colección: bibliografia_referencias (N chunks de M PDFs)

Resultados:
  ✓ EXACT_MATCH:  15/25 claims (60%)
  ⚠ DIFFERENT:     7/25 claims (28%)
  ✗ NOT_FOUND:     3/25 claims (12%)

Claims a corregir:
  1. [claim original] → [dato correcto] (fuente: ref.pdf)
  2. ...

Claims sin respaldo:
  1. [claim] — posible PDF stub o claim sin fuente local
```
