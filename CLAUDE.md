# Tesis de Maestría en Pedagogía — UPAEP

## Proyecto
Raíces confucianas en las políticas de inteligencia artificial y educación del Sudeste Asiático: análisis semántico comparativo de 9 unidades (Vietnam, Singapur, Malasia, Indonesia, Tailandia, Filipinas, China como caso ancla confuciano, ASEAN y UNESCO) mediante la lente de Culturas de Herencia Confuciana (CHC). Ver `PLAN-PIVOTE.md` para el estado del pivote (rama `v3/sudeste-asiatico-confuciano`).

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
- Compilación: `make pdf` (usa `pdflatex`×3+`bibtex` si existe; si no, `tectonic`)
- Exportar Word: `pandoc` con filtro de citas

## Pipeline
- Embedding primario: `paraphrase-multilingual-MiniLM-L12-v2` (local; el corpus incluye indonesio)
- Alternativa configurable: `text-embedding-3-small` (OpenAI; requiere OPENAI_API_KEY)
- Ejecutar con: `make pipeline` (equivale a `USE_LOCAL_EMBEDDINGS=1 python3 -m pipeline`)
- Chunking: 800 chars, 200 overlap
- ChromaDB para almacenamiento vectorial
- 7 dimensiones de análisis: gobernanza, currículo, formación docente, infraestructura, ética, investigación, equidad
- Variable de diseño CHC por país: fuerte (China, Vietnam, Singapur), parcial (Malasia), ausente (Indonesia, Tailandia, Filipinas)

## Web
- Diseño neobrutalist: Syne/DM Sans/JetBrains Mono, `#F5F0E8` fondo, bordes 3px, sombras 6px offset, `#FFD54F` acento
- Chart.js 4.x para visualizaciones
- Colores por región: Asia Oriental=#880e4f, Sudeste Asiático=#d32f2f, Regional (ASEAN)=#f57c00, Internacional=#7b1fa2
- Colores CHC: fuerte=#b71c1c, parcial=#f57c00, ausente=#1976d2

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
