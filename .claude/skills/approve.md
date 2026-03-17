# /approve — Revisar, Commit y Push

## Trigger
User invokes `/approve [mensaje opcional]`

## Behavior
1. **Mostrar cambios**: Ejecutar `git status` y `git diff --stat` para presentar un resumen de todos los cambios pendientes.
2. **Agrupar por ámbito**: Clasificar archivos modificados por tipo:
   - `document/` → tesis
   - `pipeline/` → pipeline
   - `web/` → web
   - `slides/` → slides
   - Otros → config
3. **Proponer commit**: Generar mensaje de commit en formato del proyecto (`tipo(ámbito): descripción`). Si hay múltiples ámbitos, usar el dominante o `chore(config)` si es mixto.
4. **Detectar convenciones**: Si los cambios revelan nuevas convenciones (nuevo target de Makefile, nuevo script, nuevo patrón), proponer actualizar CLAUDE.md.
5. **Seguridad**: Verificar que NO se incluyan:
   - `.env`, credenciales, API keys
   - Archivos binarios grandes (>1MB)
   - Archivos que deberían estar en `.gitignore`
   Si se detectan, advertir y excluirlos.
6. **Confirmar**: Mostrar el plan al usuario y esperar confirmación explícita antes de ejecutar.
7. **Ejecutar**: `git add` (archivos específicos, nunca `-A`) → `git commit` → `git push`.
8. **Reportar**: Mostrar el commit hash y confirmar push exitoso.

## Output Format
```
═══ Cambios Pendientes ═══

tesis (3 archivos):
  M document/chapters/cap01-planteamiento.tex
  M document/referencias.bib
  A document/chapters/conclusiones.tex

pipeline (1 archivo):
  M pipeline/config.py

Mensaje propuesto: fix(tesis): corregir datos numéricos en cap01

¿Proceder con commit + push? (sí/no)
```
