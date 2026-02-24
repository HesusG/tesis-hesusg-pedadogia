# Tesis de Maestría en Pedagogía — UPAEP

## Proyecto
Análisis comparativo de políticas públicas sobre educación en inteligencia artificial: un estudio de 12 países y 4 organismos internacionales mediante análisis semántico y visualización interactiva.

**Autor**: Hesus García Cobos
**Programa**: Maestría en Pedagogía, UPAEP
**Director**: Por confirmar

## Idioma
- Todo el contenido de la tesis se escribe en **español**.
- Nombres de variables, funciones y comentarios de código en **inglés**.
- Los commits en **español** con formato: `tipo(ámbito): descripción`
  - Tipos: feat, fix, docs, style, refactor, test, chore, data
  - Ámbitos: tesis, pipeline, web, slides, config

## Estructura

| Directorio | Propósito |
|------------|-----------|
| `document/` | Tesis en LaTeX (cls UPAEP, Times New Roman 12pt, carta, 1.5 espaciado) |
| `pipeline/` | Ingesta, embeddings (ChromaDB), similitud, análisis, exportación |
| `policies/` | Documentos fuente (raw/, processed/, metadata.json) |
| `web/` | Visualización neobrutalist (Vanilla JS + Chart.js) |
| `slides/` | Presentación reveal.js para defensa |
| `output/` | Productos finales (PDF, DOCX) |

## LaTeX
- Clase personalizada: `upaep-thesis.cls`
- Citas: `natbib` + `apalike` (estilo APA en español)
- Compilación: `pdflatex` → `bibtex` → `pdflatex` × 2
- Exportar Word: `pandoc` con filtro de citas

## Pipeline
- Embedding primario: `text-embedding-3-small` (OpenAI)
- Fallback: `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers)
- Chunking: 800 chars, 200 overlap
- ChromaDB para almacenamiento vectorial
- 7 dimensiones de análisis: gobernanza, currículo, formación docente, infraestructura, ética, investigación, equidad

## Web
- Diseño neobrutalist: Syne/DM Sans/JetBrains Mono, `#F5F0E8` fondo, bordes 3px, sombras 6px offset, `#FFD54F` acento
- Chart.js 4.x para visualizaciones
- Colores por región: Europa=#1976d2, Américas=#388e3c, Asia-Pacífico=#d32f2f, Internacional=#7b1fa2

## Escritura
- Voz activa, forma positiva, lenguaje concreto
- Sin patrones de IA: sin reencuadres dramáticos, sin abuso de guiones largos, sin vocabulario promocional
- Citar siempre con `\citep{}` o `\citet{}`
- Cada afirmación sustantiva necesita respaldo bibliográfico

## Convenciones
- `make pdf` para compilar tesis
- `make docx` para exportar Word (para revisión del asesor)
- `make pipeline` para ejecutar análisis completo
- `make web` para regenerar visualización
- `make status` para ver progreso por capítulo
