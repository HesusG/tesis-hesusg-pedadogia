# /housekeep — Limpieza y Salud del Repo

## Trigger
User invokes `/housekeep`

## Behavior
1. **Estado git**: Ejecutar `git status` y clasificar archivos en untracked, modified, staged.
2. **Archivos temporales**: Detectar archivos `*_temp*`, `*.bak`, `*.orig`, build artifacts (`*.aux`, `*.log`, etc.) fuera de `.gitignore`.
3. **Verificar .gitignore**: Comprobar que las reglas cubren:
   - LaTeX auxiliares
   - Python cache
   - ChromaDB local
   - Entornos virtuales
   - PDFs de políticas y referencias
   - Output generado
   Si falta algo, proponer adición.
4. **Dead code**: Buscar archivos `.py` en `scripts/` y `pipeline/` que no estén importados ni referenciados en el `Makefile`. Reportar como candidatos a revisión (no borrar automáticamente).
5. **Tamaño del repo**: Mostrar tamaño total del directorio y los 5 archivos más grandes.
6. **Sugerir acciones**: Para cada hallazgo, proponer:
   - `rm` para archivos temp
   - `make clean` para build artifacts
   - `.gitignore` para archivos que no deberían trackearse
   - `git add` para trabajo pendiente legítimo

## Output Format
```
═══ Salud del Repo ═══

Estado git:
  Untracked: N archivos
  Modified:  N archivos
  Staged:    N archivos

Archivos temporales encontrados:
  - path/to/file_temp.ext → sugerir: rm

.gitignore: ✓ al día / ⚠ falta regla para X

Scripts sin referencia en Makefile:
  - scripts/foo.py → revisar si es necesario

Tamaño: XX MB
Archivos más grandes:
  1. path/file (XX MB)
  ...

Acciones sugeridas:
  1. rm path/to/temp
  2. make clean
  3. git add path/to/new_work
```
