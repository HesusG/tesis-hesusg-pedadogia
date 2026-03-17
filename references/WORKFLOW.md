# Flujo de trabajo para gestión de referencias

## Diagrama general

```
Zotero (GUI) ──[Better BibTeX auto-export]──> document/referencias.bib
     │                                              │
     │  Research Rabbit ──[BibTeX export]──> Zotero  │
     │                                              │
     ▼                                              ▼
make refs-download    ← descarga PDFs vía Unpaywall + URLs directas
make refs-audit       ← verifica que cada cita tenga PDF local
make refs-audit-cap01 ← auditoría por capítulo
```

## Setup inicial

### 1. Instalar Better BibTeX en Zotero

- Descargar desde https://retorque.re/zotero-better-bibtex/
- En Zotero: Tools → Add-ons → Install from file
- Reiniciar Zotero

### 2. Importar referencias existentes

- File → Import → seleccionar `document/referencias.bib`
- Better BibTeX asignará las claves automáticamente

### 3. Configurar auto-export

- Seleccionar la colección de la tesis
- File → Export Library → Better BibTeX
- Marcar "Keep updated"
- Destino: `document/referencias.bib`
- Cada vez que se agregue o modifique una referencia en Zotero, el .bib se actualizará automáticamente

### 4. Vincular con Research Rabbit (opcional)

- Crear cuenta en https://www.researchrabbit.ai/
- Importar colección de Zotero
- Research Rabbit sugiere papers relacionados
- Agregar los que sirvan → se sincronizan a Zotero → se exportan al .bib

## Uso diario

### Agregar una nueva referencia

1. Agregar en Zotero (vía browser connector, DOI, o manualmente)
2. Better BibTeX actualiza `referencias.bib` automáticamente
3. Ejecutar `make refs-download` para intentar descargar el PDF
4. Ejecutar `make refs-audit` para verificar cobertura

### Antes de compilar un capítulo

```bash
make refs-audit-cap01   # Verificar que todas las citas del cap01 tienen PDF
make pdf-cap01          # Compilar
```

### Auditoría completa

```bash
make refs-audit         # Estado de todas las referencias
make refs-check         # Exit 1 si hay artículos/reportes sin PDF
```

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `make refs-download` | Descargar PDFs vía Unpaywall + URLs directas |
| `make refs-audit` | Auditoría completa: .bib vs PDFs locales |
| `make refs-audit-cap01` | Auditoría solo para citas del capítulo 1 |
| `make refs-check` | Verificación estricta (exit 1 si hay gaps descargables) |

## Convención de nombres de PDFs

```
{bibkey}_{short-title}.pdf
```

Ejemplo: `unesco2023genai_guidance-generative-ai-education.pdf`

- `bibkey`: clave del .bib (autor+año+keyword)
- `short-title`: descripción breve en kebab-case

## Fuentes de descarga (en orden de prioridad)

1. **URLs directas**: gov sites, UNESCO, ArXiv, open-access journals
2. **Unpaywall API**: busca versiones OA de artículos con DOI
3. **CrossRef API**: fallback para metadatos y enlaces PDF
4. **Manual**: libros, capítulos de libro, journals paywalled

## Notas

- Los libros NO se descargan automáticamente (requieren compra o biblioteca)
- El modo `--check` solo reporta como faltantes los items descargables (artículos, reportes), no los libros
- Unpaywall respeta los límites de la API: 1 request/segundo con email de contacto
- Los PDFs descargados manualmente se detectan por el prefijo del bibkey en el nombre del archivo
