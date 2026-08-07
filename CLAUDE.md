# Tesis de Maestría en Pedagogía — UPAEP (v2)

## Proyecto
Análisis comparativo de políticas públicas sobre educación en inteligencia artificial: un estudio de 7 países (1 por continente político) mediante análisis semántico no supervisado, control lingüístico y trazado de difusión.

**Autor**: Hesus García Cobos
**Programa**: Maestría en Pedagogía, UPAEP
**Director**: Por confirmar
**Versión**: v2 (branch `v2/restructure`). La v1 se preserva en `main`.

## Países (v2)
| Región | País | Docs | Idioma | Status |
|--------|------|------|--------|--------|
| Norteamérica | USA | EO 14110 | EN | Pendiente |
| Norteamérica | Canadá | Pan-Canadian AI Strategy | EN | Listo |
| Latinoamérica | Colombia | CONPES 3975 | ES | Listo |
| Europa | Alemania | KI-Strategie 2020 | DE | Pendiente |
| África | Sudáfrica | PC4IR Report 2020 | EN | Pendiente |
| Oceanía | Australia | AI Action Plan 2021 | EN | Listo |
| Asia | China | 7 docs (2017-2025) | ZH→EN | Listo |

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
| `pipeline/` | Ingesta, embeddings, BERTopic, similitud, language control, validación |
| `policies/` | Documentos fuente (raw/, processed/, v1_archive/, metadata.json) |
| `china_research/` | Investigación de China integrada (downloads, traducciones, análisis) |
| `web/` | Visualización neobrutalist (Vanilla JS + Chart.js) |
| `slides/` | Presentación reveal.js para defensa |
| `output/` | Productos finales (PDF, DOCX) |
| `reflexion.md` | Autoevaluación crítica de v1 y principios de v2 |

## Metodología v2 (unsupervised-first)
1. **Fase 1**: BERTopic no supervisado → documentar temas emergentes ANTES de imponer framework
2. **Fase 2**: Pre-registrar dimensiones en `config.py` (commit a git = pre-registro)
3. **Fase 3**: Scoring supervisado por dimensiones
4. **Fase 4**: Control lingüístico (baseline EN-only, intra- vs inter-familia)
5. **Fase 5**: Validación: comparar no supervisado vs supervisado
6. **Fase 6**: China deep-dive (evolución temporal 2017→2025)

## Pipeline
- Embedding primario: `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers, 384 dims)
- BERTopic para topic modeling no supervisado
- Chunking: 800 chars, 200 overlap
- ChromaDB para almacenamiento vectorial (colección: `politicas_ia_educacion_v2`)
- 7 dimensiones pre-registradas: gobernanza, currículo, formación docente, infraestructura, ética, investigación, equidad

## LaTeX
- Clase personalizada: `upaep-thesis.cls`
- Citas: `natbib` + `apalike` (estilo APA en español)
- Compilación: `pdflatex` → `bibtex` → `pdflatex` × 2
- Exportar Word: `pandoc` con filtro de citas

## Web
- Diseño neobrutalist: Syne/DM Sans/JetBrains Mono, `#F5F0E8` fondo, bordes 3px, sombras 6px offset, `#FFD54F` acento
- Chart.js 4.x para visualizaciones
- Colores por región: Norteamérica=#1565c0, Latinoamérica=#388e3c, Europa=#6a1b9a, África=#e65100, Oceanía=#00838f, Asia=#d32f2f

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
- `make topics` para BERTopic no supervisado (Fase 1)
- `make language-control` para control lingüístico (Fase 4)
- `make validate` para validar pre-registro vs no-supervisado (Fase 5)
- `make ingest-refs` para ingestar bibliografía (PDFs → ChromaDB)
- `make factcheck-cap01` para fact-check numérico de cap01
- `make compute-advanced` para enriquecer datos web (UMAP, dendrograma, Sankey)
- `make download-policies` para descargar PDFs de políticas
