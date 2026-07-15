# Spike log — Pipeline v3 (build por fases con metodología SPIKE)

Cada fase se desarrolla como un SPIKE: pregunta acotada → prototipo mínimo → verificación → reflexión de *cómo se hizo*. Este log acumula las reflexiones.

---

## SPIKE Fase 1 — Config + esquema + códebook (pre-registrado)

**Pregunta:** ¿podemos materializar toda la config pre-registrada (metadata 2 capas, códebook, panel chino/occidental) en un artefacto limpio y verificable del que cuelgue el pipeline?

**Qué se hizo (cómo):**
- Se creó el paquete `pipeline_v3/`.
- Se **rescató el códebook real** que el panel fable generó (workflow `wf_0f696743-1f1`) → `pipeline_v3/codebook.json`. No se inventó: es el artefacto auténtico, con la regla clave *"invertir/coordinar NO es dézhì"*.
- `pipeline_v3/config.py`: esquema Tier A (manual, incluye `genre` como control) / Tier B (auto-cacheado), vocabulario controlado de `genre`, campos filtrables de baja cardinalidad, y el **panel de jueces con etiqueta de origen** (western/chinese).
- Verificación: `python -m pipeline_v3.config` imprime todo y detecta jueces disponibles.

**Qué se aprendió / hallazgos:**
- Los **5 jueces con key están todos disponibles** (GPT, Gemini, Llama = occidentales; Qwen, DeepSeek = chinos). El sidequest transcultural es factible sin bloqueos.
- **Claude** no tiene key cruda pero entra por el harness → decisión pendiente de *cómo* lo añade el runtime (nota para Fase 4).
- El códebook existente es **solo para dézhì** (Vía B). Los otros 5 ejes van por Vía A (embeddings). Extender Vía B a más ejes = generar más códebooks (decisión futura, no ahora).

**Riesgos / abiertos surgidos:**
- `metadata.json` **no tiene `genre`** ni `adopting_body` — hay que llenar Tier A a mano para los 13 docs (tarea de Fase 2). Es el control del confusor: no se automatiza.
- `CONTEXT_BLURB_MODEL=gpt-4o-mini` exige cachear para reproducibilidad (Fase 2).
- Los IDs de modelos de Together (Qwen2.5-72B, DeepSeek-V3) hay que **probar que respondan** (smoke test en Fase 4) — definidos ≠ funcionando.

**Qué necesita la Fase 2:** llenar Tier A (genre, adopting_body, doc_type) para los 13 docs; implementar chunk 500/50 → blurb cacheado → embed → colección `politicas_v3`.

**Veredicto del spike:** ✅ la forma del config es la correcta y todo cuelga de aquí. Listo para congelar (pre-registro) y pasar a Fase 2.

---

## SPIKE Fase 2 (pre) — 3 ajustes + smoke test del edge case fǎ/Legalismo

**Ajustes hechos:** (1) panel → **OpenRouter** (una API, 7 jueces: 3 occidentales + **4 chinos** — Qwen, DeepSeek, GLM, Kimi); (2) **Claude = meta-juez** (Sonnet 4.5, adjudica desacuerdos + sintetiza, NO puntúa → sin circularidad); (3) smoke test del edge case.

**Pregunta del spike:** ¿el panel confunde una LEY DE CONTROL china (GenAI Measures 2023, legalista 法家) con "liberal" (polo negativo), por ser texto de "ley"?

**Resultado — contra mi hipótesis, en buen sentido:**
- **El error temido NO ocurre.** Ningún juez puso la ley en negativo/liberal; la pusieron en **0 (neutral)**. El códebook (Regla 1, dirección de la autoridad) **resiste la trampa fǎ**: no confunde "ley" con "derechos que limitan al Estado".
- **Mi criterio de test estaba mal especificado:** predije que la ley debía ser POSITIVA, pero un articulado **procedimental** (registro, seguridad, obligaciones a proveedores) es legítimamente **neutral** en el eje dézhì-de-*cultivo* — es Legalista-procedimental, no confuciano-cultivacional. El dézhì vive en el lenguaje **movilizacional** (NGAIDP = **+1**, "movilizar a la nación / rejuvenecimiento"), no en el articulado técnico.
- **Discriminación correcta:** NGAIDP (plan movilizacional) +1 · ley procedimental 0 · Canadá 0.

**Hallazgo metodológico nuevo (importante):** el **polo negativo (liberal) casi no se activa** — casi todo lo no-estatista cae en 0, no en negativo (igual que el hallazgo previo con embeddings: Canadá no salió claramente liberal). El eje mide *presencia de estatismo* (0..+2 en la práctica), no un continuo limpio estatista↔liberal, porque los documentos rara vez articulan "los derechos limitan al Estado". **Se debe reportar así.**

**Plumbing cazado (para eso era el smoke test):**
- `qwen`: error de ruteo de proveedor en OpenRouter (`does not support endpoint: completions`) → fix: fijar provider / otra variante.
- `glm`, `kimi`: errores intermitentes (1-2 de 5) → falta reintento.
- `gpt`, `gemini`, `llama`, `deepseek`: 100% OK. Panel efectivo: **6/7** (qwen a arreglar).

**Sidequest preliminar:** media occidental **+0.27** vs china **+0.18** — muy cerca (buena señal de convergencia), muestra minúscula, sin significado aún.

**Antes de la Fase 2 completa:** (a) fijar qwen (provider), (b) reintento en glm/kimi, (c) decidir tratar el eje como **0..+2** (presencia de estatismo) en el reporte, (d) opcional: ejemplos al códebook para separar neutral-0 de liberal-negativo.

**Veredicto:** ✅ el edge case que temía no ocurre (códebook robusto a la trampa fǎ); el spike re-especificó el eje, destapó el polo-liberal-poco-activado, y cazó bugs de plumbing — todo antes de gastar en la ingesta completa.

---

## SPIKE Fase 2b — corpus China 2025-2026 de IA-educación (feasibility)

**Pregunta:** ¿podemos recuperar ~10 políticas chinas de IA-educación (2025-2026) con **texto completo verbatim**?

**Hallazgo honesto sobre "10 de 2026":** NO existe. Solo **~5 docs genuinamente 2026** con texto (flagship "IA+Educación" MoE abr-2026, su Q&A, Plan Quinquenal educación jun-2026, guía Guangdong may-2026, reporte docentes). Casi todos los "planes provinciales 2026" citados **son 2025**. Para ~10 se enmarca como **"2025-2026"** (+ capa provincial 2025: Beijing, Shanghai, Zhejiang, Henan, Jiangsu). Decidido con el usuario.

**Feasibility de recuperación (lo que el spike probó):**
- **curl funciona**: los 2 nacionales 2026 → HTTP 200, texto verbatim UTF-8, `人工智能` presente (flagship 100 menciones = todo IA-educación; Plan Quinquenal 7 = IA es una sección).
- **WebFetch NO sirve para verbatim**: resume con un modelo chico (el Plan Quinquenal salió *parafraseado*, "简体转述"). El flagship sí salió completo por suerte (doc corto). → **usar curl + extracción de HTML**, no WebFetch.

**Riesgos / abiertos:**
- URLs exactas de los **provinciales 2025 faltan** (la research dio dominios) → hay que pinearlas una por una.
- Todo en **chino** → traducir ZH→EN (decisión previa: todos los jueces leen el mismo inglés → contraste de origen limpio). Reusar Qwen/OpenRouter o `china_research/translate.py`.
- Encoding: eol.cn sin `charset` declarado (asumir UTF-8, verificar); moe.gov.cn utf-8.

**Pipeline confirmado:** `curl → strip HTML → clean → translate ZH→EN → chunk 500/50 → blurb → embed → politicas_v3`.

**Veredicto:** ✅ feasible vía curl. Próximo: `fetch_china.py` (curl+extract) para las URLs confirmadas + pinear provinciales + traducir + ingerir.

---

## SPIKE Fase 2c — fetch_china.py (construir + jalar)

**Qué se hizo:** `pipeline_v3/fetch_china.py` (curl + extracción HTML→texto, solo stdlib) con el **registro pre-registrado de 10 docs** (metadata Tier A: doc_id, genre, scope, adopting_body, year, título) → `china_2026_registry.json`.

**Resultado del run:**
- ✅ **4/5 con-URL jalados con texto verbatim:** flagship (6.3k chars, 人工智能×96) · Q&A (3.2k, ×59) · **15º Plan Quinquenal (7.9k, ×7) — COMPLETO por curl** (WebFetch lo había parafraseado → vindica "curl, no WebFetch") · reporte docentes (1.4k, ×6).
- ⚠️ **Guangdong: 0 chars** — el portal `szns.gov.cn` tiene el contenido en un **PDF adjunto**; necesita vía PDF (pypdf, ya en el repo) o la URL del PDF (`jyj.gz.gov.cn/.../10608660.pdf`).
- ⏳ **5 provinciales 2025: URL exacta pendiente** (Beijing, Zhejiang, Henan, Jiangsu + Consejo de Estado "IA+").

**Hallazgos:**
- El extractor stdlib (curl + regex, filtra líneas con contenido chino) **funciona para páginas gov/edu HTML estándar**; falla en portales cuyo contenido real es un PDF/iframe → se necesita un segundo camino (PDF).
- Se amplió `GENRE_VOCAB` con **"guidance"** (Q&A, guía Guangdong).

**Estado corpus China v3: 4 sólidos** (todos 2026 nacionales). Para ~10 faltan: Guangdong (PDF) + 5 provinciales (URLs).

**Next:** (a) pinear URLs provinciales 2025, (b) extraer Guangdong vía PDF, (c) traducir ZH→EN los ~10, (d) chunk+blurb+embed → `politicas_v3`.

---

## SPIKE Fase 2d — cierre del corpus China 2025-2026

**Qué se hizo:** research pineó las 5 URLs provinciales/nacionales 2025 (con línea de apertura confirmada); se cablearon en `fetch_china.py` y se re-corrió.

**Corpus cerrado: 8 documentos sólidos** con texto verbatim (ZH):
| doc | chars | 人工智能 | año |
|---|---|---|---|
| flagship "IA+Educación" | 6.3k | 96 | 2026 |
| Q&A del MoE | 3.2k | 59 | 2026 |
| 15º Plan Quinquenal educación | 7.9k | 7 | 2026 |
| reporte docentes IA-gen | 1.4k | 6 | 2026 |
| Consejo de Estado "IA+" | 5.6k | 92 | 2025 |
| Beijing K-12 IA | 4.9k | 96 | 2025 |
| Zhejiang IA+Educación (mirror) | 4.5k | 86 | 2025 |
| Henan IA+Educación (mirror) | 4.1k | 77 | 2025 |

**2 pendientes (marcados `needs_review`/`url_pendiente`):**
- `jiangsu`: página oficial y mirror Nanjing son **JS-dinámicos** (46 chars) → sin mirror estático.
- `guangdong`: portal 0-chars + PDF **504** (servidor bloquea).

**Hallazgos:**
- Los sitios gov **provinciales** chinos **geo-bloquean o renderizan por JS** → los **mirrors académicos .edu.cn** (zjnu, zztrc) son la vía confiable para el texto verbatim.
- El extractor stdlib funciona en HTML servido; falla en JS/PDF (esperado). Umbral <800 chars → `needs_review` (registro honesto, no comitea casi-vacíos).

**Estado:** ✅ corpus China v3 con **8 docs sólidos** (el "gran universo" 2025-2026, mucho más rico que los 7 longitudinales previos). Jiangsu/Guangdong = alternativa futura.

**Next real:** traducir ZH→EN los 8 → chunk 500/50 + blurb → embed → `politicas_v3`.

---

## SPIKE Fase 2e — ingesta del corpus China a `politicas_v3`

**Qué se hizo:** `pipeline_v3/ingest.py` — chunk 500/50 → embed multilingüe (texto chino ORIGINAL) → ChromaDB `politicas_v3` con metadata Tier A. Los 8 docs sólidos → **90 chunks**.

**Hallazgo clave (valida una decisión):** una query en **español** recuperó chunks **chinos** a dist 0.25 → el embedding `multilingual-MiniLM` **puentea idiomas por sí solo**. Por eso **NO se traduce para el store/retrieval** (Vía A); se guarda el original, consistente con los demás países en su idioma. La traducción ZH→EN queda solo para el clasificador (Vía B), como paso posterior cacheado.

**Flagged (mejoras posteriores, no bloquean el corpus):** (a) blurb de contexto Anthropic por chunk; (b) traducción ZH→EN para que los jueces occidentales lean inglés (Vía B).

**Nota:** chunks de 500 chars en chino son densos (~1 char ≈ 1 palabra) → flagship 6.3k = 15 chunks. Aceptable; documentado.

**Estado:** ✅ corpus China 2025-2026 (8 docs / 90 chunks) EN el store, consultable cross-lingual.

**Next:** (a) ingerir los otros 6 países a `politicas_v3`; (b) blurb + traducción; (c) correr el clasificador panel (7 jueces chino/occidental) sobre `politicas_v3`.
