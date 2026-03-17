# /wrap-up — Cierre de Sesión

## Trigger
User invokes `/wrap-up`

## Behavior
1. **Resumen de trabajo**: Listar archivos creados, modificados y commits hechos en esta sesión usando `git diff --stat` y `git log` del periodo de la sesión.
2. **Aprendizajes**: Identificar convenciones nuevas, errores descubiertos, o decisiones tomadas durante la sesión que deban persistir.
3. **Actualizar MEMORY.md**: Actualizar `memory/MEMORY.md` con:
   - Progreso de capítulos (conteos de palabras actualizados)
   - Nuevas decisiones o herramientas introducidas
   - Estado de fases del proyecto
4. **Sugerir ediciones a CLAUDE.md**: Si se descubrieron nuevas convenciones de workflow, proponer cambios concretos a `CLAUDE.md` (mostrar diff, no aplicar sin confirmación).
5. **Advertir pendientes**: Si hay archivos sin commitear (`git status`), listarlos y preguntar si se quiere hacer commit antes de cerrar.

## Output Format
```
═══ Resumen de Sesión ═══

Trabajo realizado:
  - [archivo] — descripción del cambio
  - ...

Commits:
  - abc1234 tipo(ámbito): mensaje
  - ...

Aprendizajes:
  - [convención/decisión descubierta]

MEMORY.md actualizado: ✓/✗
CLAUDE.md sugerencias: [ninguna | lista de cambios propuestos]

Pendientes sin commitear: [ninguno | lista]
```
