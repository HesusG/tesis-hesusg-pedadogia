# Pipeline v3 — Instrumento agéntico de medición de encuadre confuciano en políticas de IA

**Estado:** spec de diseño (pre-registro). Commit a git = pre-registro (metodología v2, Fase 2).
**Autor:** Hesus García Cobos · Supervisión: Dra. Beatriz Juárez Aguilar · Maestría en Pedagogía, UPAEP · INFOTEC Veraneo 2026.

---

## 0. Propósito

Medir, de forma **reproducible y defendible**, cuánto resuenan las políticas públicas de IA en educación (7 países) con los valores confucianos, y qué revela esa resonancia sobre el modelo de gobernanza de cada país. El aporte de la tesis **es el método** (un instrumento validado), no un veredicto sobre un país.

**Problema central (ya validado empíricamente):** los ejes de embedding miden *similitud de superficie*; fallan donde el lenguaje converge ("el Estado lidera el esfuerzo nacional" lo dice toda estrategia). Por eso el instrumento es de **dos vías**:

- **Vía A — embeddings** para los ejes donde el lenguaje difiere (hé, rén, lǐ, xiūshēn) y como **línea base** documentada.
- **Vía B — clasificación LLM contra códebook pre-registrado** para el eje difícil (dézhì / gobernanza) y como medida primaria de encuadre.

El embedding que falla en dézhì **no se descarta**: es la evidencia que justifica escalar al LLM (arco narrativo del capítulo de método).

---

## 1. Decisiones de diseño (grill completo — 8 nodos)

| # | Nodo | Decisión |
|---|------|----------|
| 1 | Rol del retrieval | **Uniforme y pre-registrado**: misma consulta/criterio para todos los países; selección idéntica → sin sesgo por país. |
| 2 | Método de retrieval | **Denso + filtro de metadata**, y **comparar vs híbrido (denso+BM25) + rerank**, evaluado con golden set. Objetivo citable: Contextual Retrieval de Anthropic (−35/49/67% de fallos). |
| 3 | Metadata | **Dos capas**: Tier A manual/determinista (incluye `genre` = control del confusor, JAMÁS por LLM); Tier B auto-cacheado (blurb de contexto), solo para recuperar. Nombres de campo estilo Dublin Core. |
| 4 | Chunking | **Recursive 500/50** + **blurb de contexto** (Anthropic) por chunk. |
| 5 | Embedding | **`paraphrase-multilingual-MiniLM-L12-v2`** (multilingüe ES/DE/ZH/EN, local, reproducible). Opcional comparar con `multilingual-e5`/`BGE-M3` en la eval. |
| 6 | Prompt del clasificador | **XML-tagged** (`<contexto><instrucciones><rúbrica><salida>`), códebook "a la altura correcta". |
| 7 | Validación | **Panel multi-familia** (sin codificación humana): acuerdo ENTRE familias = validez convergente. Reporte **descriptivo, no inferencial** (DSL requiere muestra humana → trabajo futuro). |
| 8 | Arquitectura | **Workflow determinista** (el código controla el camino) + tools (salida JSON estricta) + **hooks = columna de auditoría** + capa agéntica fina y en cuarentena solo para exploración. |

**Sidequest integrado (validación transcultural):** el panel incluye modelos de **origen chino** (Qwen, DeepSeek) **vs occidental** (GPT, Gemini, Claude, Llama). Si coinciden → validez convergente transcultural. Si difieren → hallazgo propio: sesgo de origen del modelo en la clasificación cultural.

---

## 2. Arquitectura: workflow determinista + tools + hooks + agente fino

Fuentes autoritativas convergen (Anthropic *Building Effective Agents* 2024; OpenAI *Practical Guide to Building Agents* 2025; LangGraph docs): para un **instrumento de medición reproducible**, el camino de medición es un **workflow determinista**, no un agente autónomo (un agente que planea sus pasos vuelve el camino una variable no reproducible → rompe el pre-registro).

### Grafo de estados (aristas fijas; LLM solo en nodos etiquetados)

```
START
 → ingest_pdf          [CODE]  PDF → texto limpio + provenance (source, page)
 → chunk               [CODE]  recursive 500/50, fronteras deterministas
 → contextualize       [LLM]   blurb de contexto por chunk (Anthropic); cacheado → reproducible
 → embed               [CODE]  multilingual-MiniLM (modelo+revisión fijados)
 → store               [CODE]  ChromaDB (snapshot de colección, IDs estables)
 → [GATE] review_index [HITL]  interrupt opcional: confirmar corpus/índice antes de gastar cómputo
 → retrieve            [CODE]  top-k UNIFORME, métrica fija, filtro de metadata exacto — sin LLM
 → [GUARD] check_ctx   [CODE]  cobertura del set recuperado; si es pobre → marca para revisión
 → classify_panel      [LLM]   panel multi-familia (chino+occidental), temp 0, esquema estricto,
                               prompt fijo = códebook pre-registrado; paralelo por modelo
 → aggregate           [CODE]  reconciliación determinista (mayoría/ponderada); registra desacuerdo
 → [GATE] adjudicate   [HITL]  interrupt SOLO si desacuerdo del panel > umbral
 → validate            [CODE]  chequeos de esquema/rango; acuerdo entre familias; Vía A vs Vía B
 → report              [CODE]  scores + provenance completa (contexto recuperado, salidas crudas
                               por modelo, manifiesto de modelos/versiones)
 → END
```

- **Determinista (código):** ingest, chunk, embed, store, retrieve, aggregate, validate, report. Cargan la garantía de reproducibilidad.
- **Nodos LLM:** `contextualize`, `classify_panel` (y opcional grader). Todos a temp 0, modelos fijados, prompts fijos, salidas cacheadas.
- **Guardrails (hooks):** salida estructurada forzada en `classify_panel`; chequeos de rango/consistencia en `validate`.
- **Human-in-the-loop (`interrupt`):** solo `review_index` y `adjudicate` (compuertas de aprobación, no ruteo autónomo).
- **Autonomía real del agente:** en ninguna parte del camino de medición. Único lugar defendible: un sub-loop CRAG de reformulación de query **offline, durante desarrollo**, para afinar retrieval — nunca en la corrida pre-registrada.

### Mapeo de lo que el usuario pidió (agent loop, tools, hooks, system prompt)
| Pedido | Dónde vive |
|---|---|
| System prompt | El códebook en XML, "a la altura correcta" (Anthropic *context engineering*). |
| Tools | `retrieve_passages`, `classify_passage`, `record_score` — pocas, bien descritas, **salida JSON `strict:true`** (OpenAI structured outputs). |
| Hooks | **Columna de auditoría/reproducibilidad**: `PostToolUse` → log inmutable (modelo+versión+timestamp) por clasificación; `PreToolUse` → guardrail que rechaza salida fuera del códebook. |
| Agent loop | Capa fina y en cuarentena sobre las mismas tools, **solo exploración interactiva** ("reclasifica y explica", "compara X vs Y"). Nunca produce los números de la tesis. |

**LangGraph es opcional**: regala checkpoints/persistencia/HITL/tracing, pero su valor aquí es la auditoría, no la autonomía. La misma arquitectura corre como pipeline tipado simple (menor riesgo de dependencia). *La arquitectura es el entregable; LangGraph, una conveniencia.*

---

## 3. Esquema de metadata (dos capas)

Principio: **manual para lo que MEDIMOS, LLM congelado para lo que RECUPERAMOS.** Filtrable/indexado = pequeño y de baja cardinalidad (Pinecone). Nombres estilo Dublin Core (ISO 15836).

**Tier A — nivel documento, manual/verificado (denormalizado a cada chunk):**
`doc_id` (str), `country` (str), `region` (str), `genre` (enum: strategy|law|action_plan|report — **control del confusor, nunca LLM**), `language` (enum ISO), `year` (int), `adopting_body` (str), `doc_type_official` (str), `source_uri` (str), `n_pages` (int), `ingest_version` (str).

**Tier B — nivel chunk, auto-congelado-cacheado (solo retrieval):**
`chunk_id`, `parent_doc_id`, `chunk_index`, `page`, `char_start/end` (derivados); `context` (blurb Anthropic, prepend al texto antes de embeber); `summary`/`keywords`/`questions_answered` (opcionales, LlamaIndex); `emb_model`, `ctx_model` (fijados para reproducibilidad).

Agregar política futura = 1 ficha JSON Tier A + 1 pasada de extracción cacheada.

---

## 4. Clasificador y panel

- **Códebook pre-registrado** (ya redactado por panel fable; incluye la regla clave *"invertir/coordinar NO es dézhì"*). Vive en el system prompt XML; se commitea = pre-registro.
- **Salida estricta** por pasaje: `{eje, score ∈ [-2,2], rationale, confidence}` con JSON Schema `strict`.
- **Panel multi-familia (disponible con las claves actuales):**
  - Occidental: **GPT** (OpenAI), **Gemini** (Google), **Claude** (harness), **Llama** (Together).
  - Chino: **Qwen** (Together), **DeepSeek** (Together).
- **Agregación determinista** por pasaje (mediana/mayoría) + registro de desacuerdo.
- **Métrica de validación:** acuerdo inter-familia (κ de Fleiss / correlación) — y explícitamente **origen-chino vs origen-occidental**.

---

## 5. Reproducibilidad y pre-registro

- Fijar: modelo de embedding + revisión (fuente dominante de varianza — Wang, Zhao, Tallent & Guo 2025, arXiv 2509.18869), IDs/versiones de cada LLM, versiones de librerías, snapshot de colección Chroma.
- `temperature=0` y decoding fijo en cada clasificación; registrar `seed` donde exista.
- **Cachear artefactos**: chunks, embeddings, sets recuperados, salidas crudas por modelo → re-correr = replay, no re-llamar.
- **Commit** de códebook + prompts + config = pre-registro (git).
- **Hooks** escriben el log de auditoría inmutable con el manifiesto completo por corrida.

---

## 6. Evaluación

- **Retrieval:** golden set de pasajes de gobernanza → recall@k; **comparar denso vs híbrido+rerank** (target Anthropic Contextual Retrieval). Opcional: IoU de chunks (estilo `lab_4` dlai-ce) para comparar chunkers.
- **Clasificador:** acuerdo inter-familia + inter-origen (chino vs occidental). Reporte **descriptivo** (N=7 no admite inferencia fuerte; DSL con muestra humana = trabajo futuro).
- **Observabilidad:** tracing (Phoenix o LangSmith) por corrida.
- **Vía A vs Vía B:** dónde coinciden embeddings y LLM (validez convergente) y dónde solo el LLM separa (justifica la Vía B).

---

## 7. Fases de implementación (build completo — 7 países)

1. **Config + esquema** (`config.py`): metadata schema (Tier A/B), códebook, AXIS set, panel de modelos, todo pre-registrado.
2. **Ingesta v3**: los 7 países → recursive 500/50 → blurb de contexto (cacheado) → embed → Chroma (colección `politicas_v3`, metadata Tier A completa). Incluye USA, Alemania, Sudáfrica (pendientes) + los 7 docs China.
3. **Retrieval + eval**: denso+metadata y híbrido+rerank; golden set; recall@k; elegir ganador (verificado, no supuesto).
4. **Clasificador panel**: tools con salida estricta; panel chino+occidental; agregación; hooks de auditoría.
5. **Validación**: acuerdo inter-familia e inter-origen; Vía A (embeddings) vs Vía B (LLM); tablas.
6. **Report + sitio**: resultados reales de los 7 países en el sitio INFOTEC; manifiesto de reproducibilidad.
7. **Empaque reutilizable**: CLI (`ingest`, `retrieve-eval`, `classify`, `report`) + docs de "cómo agregar una política".

---

## 8. Límites honestos (para el capítulo de discusión)

- **Sesgo compartido de LLM:** varias familias lo reducen, no lo borran; el ancla verdadera sería un experto humano (trabajo futuro / supervisora). El contraste chino-vs-occidental es la mejor mitigación disponible sin humano.
- **Sin inferencia formal:** sin muestra humana + DSL, es medición descriptiva validada, no prueba estadística.
- **dézhì:** el encuadre de gobernanza vía texto es difícil incluso para el LLM; se reporta el poder y el límite.
- **Confusor de traducción** ZH→EN: aplicar el control lingüístico (Fase 4) también a la medición LLM.
- **Dependencia de proveedores** (Ollion et al. 2024): fijar versiones, archivar prompts y salidas crudas, replicar con un modelo de pesos abiertos (Qwen/Llama vía Together) como ancla reproducible.

---

## 9. Fuentes clave

Anthropic *Building Effective Agents* (2024); Anthropic *Building agents with the Claude Agent SDK* / *Writing effective tools* / *Effective context engineering* (2025); Anthropic *Contextual Retrieval* (2024); OpenAI *A Practical Guide to Building Agents* (2025); OpenAI Agents SDK / structured outputs (2025); LangGraph docs (workflows-and-agents, persistence, interrupts, durable-execution); Kozlowski et al. *Geometry of Culture* (ASR 2019); Grand et al. *Semantic projection* (Nat Hum Behav 2022); Taylor & Stoltz *semantic-direction CMD* (JCSS 2021); Belrose et al. *LEACE* (NeurIPS 2023); Gilardi et al. (PNAS 2023); Törnberg (2023/2025); Egami et al. *DSL* (NeurIPS 2023); Roberts, Stewart & Nielsen *Text Matching* (AJPS 2020); Card et al. *Media Frames Corpus* (ACL 2015); Wang, Zhao, Tallent & Guo *ReproRAG* (arXiv 2509.18869, 2025); Dublin Core (ISO 15836).
