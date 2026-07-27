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

---

## SPIKE Fase 3 — experimento de idioma (ZH vs EN × origen chino/occidental)

**Diseño:** 6 pasajes de gobernanza del corpus China v3, clasificados por los 7 jueces en **chino Y en inglés** (traducido con gpt-4o-mini). 2×2: idioma × origen. 79/84 clasificaciones válidas (qwen sigue con errores de ruteo).

**Resultado (score medio, +2 = Estado-dirige/dézhì):**
| | occidental | chino | fila |
|---|---|---|---|
| ZH | 1.33 | 1.14 | 1.23 |
| EN | 1.11 | 0.91 | 1.00 |

- **Efecto IDIOMA (ZH−EN): +0.23** · **Efecto ORIGEN (chino−occ): −0.20**

**Hallazgos:**
1. **China=dézhì ROBUSTO:** todas las celdas ~+1 (0.91–1.33). El resultado no depende del idioma ni del origen → validez convergente fuerte.
2. **Sesgo de origen real (−0.20):** los modelos **chinos puntúan MENOS dézhì que los occidentales** → los occidentales **sobre-atribuyen estatismo**, los chinos lo normalizan. Es el sidequest confirmado: pequeño pero direccional y medible.
3. **Idioma ≈ origen (~0.2 en escala de 5), direcciones opuestas** → ninguno domina. Traducir amortigua levemente el dézhì (no lo invierte) → **traducir es defendible**; el efecto origen se reporta como hallazgo.

**Decisión de idioma resuelta:** dado que el efecto es chico y la traducción defendible, se usa EN como primario (contraste de origen limpio, comparable entre países) y se reporta el par ZH/EN como chequeo de robustez. El efecto origen entra al capítulo de discusión.

**Caveats:** 6 pasajes / 79 clasificaciones = preliminar; qwen a arreglar (ruteo OpenRouter). Confirmar con corpus completo.

**Estado:** ✅ el edge case de idioma quedó convertido en hallazgo medible; la señal China es robusta; el sidequest chino-vs-occidental tiene sustancia.

---

## SPIKE Fase 2f — ingesta de los 6 países restantes a `politicas_v3`

**Qué se hizo:** `ingest_countries.py` — EUA, Canadá, Colombia, Alemania, Sudáfrica, Australia (texto procesado, idioma original; embed multilingüe) con metadata Tier A y `genre` asignado a mano (control).

**Resultado:** `politicas_v3` = **2420 chunks, 7 países**. Por país: china 90 · canada 15 · colombia 315 · eeuu 306 · alemania 230 · sudafrica 1303 · australia 161.

**Hallazgos:**
- **Corpus desbalanceado** (Sudáfrica 1303 vs Canadá 15) — real: los docs varían de largo (el PC4IR es un reporte extenso; Canadá una estrategia corta). La **agregación por-documento** (distribución de scores por chunk, no conteo) lo maneja; se reporta.
- **Genre-control poblado:** strategy 578 · report 1307 · law 319 · action_plan 208 · guidance 8. Permite el matching por género (control del confusor).
- China está en chino (8 docs edu 2025-2026); los demás en su idioma original → la traducción a EN para el panel (Vía B) se hace en la comparación.

**Estado:** ✅ corpus v3 completo (7 países). Listo para la comparación central China-vs-liberales en dézhì.

---

## SPIKE Fase 4 — comparación cross-country en dézhì (China vs liberales)

**Diseño:** top-3 pasajes de gobernanza por país (7 países) de `politicas_v3` → traducidos a EN → clasificados por el panel de 7 jueces. n=124 clasificaciones válidas.

**Resultado — la afirmación central CONFIRMADA:**
| país | mediana | media |
|---|---|---|
| **China** | **+1.00** | +1.06 |
| EUA / Canadá / Colombia / Sudáfrica / Australia | 0.00 | ~0.00 |
| Alemania | 0.00 | **−0.25** (único lean liberal) |

**Hallazgos:**
1. **China se separa sola** (+1.0 vs todos en 0). El eje aísla el encuadre "Estado cultiva/dirige" que es específico de China. Método validado.
2. **Los liberales quedan en 0 (no negativo):** no dicen "derechos limitan al Estado" explícitamente; simplemente no encuadran al Estado como cultivador → neutral. Alemania (−0.25) = el único lean liberal (tradición de derechos). Eje = presencia de estatismo (0..+2).
3. **El payoff del método de dos vías:** con embeddings China≈Canadá (0.83/0.83, empate); con el LLM China +1.0 vs Canadá 0. **El LLM logra lo que el coseno no pudo** — arco narrativo de la tesis demostrado.
4. **Sidequest replicado:** occidental media +0.17 vs chino +0.07 → los modelos occidentales atribuyen algo más de estatismo, consistente con la Fase 3.

**Caveats:** K=3/país, n=124, preliminar; medianas mayormente 0 (pasajes de gobernanza escasos); China = corpus edu 2025-2026. Salida: `web/data/dezhi_country_comparison.json`.

**Veredicto:** ✅ el instrumento separa a China de los liberales en dézhì donde los embeddings fallaban. La afirmación central de la tesis tiene evidencia reproducible.

---

## SPIKE Fase 5 — robustez y validación del instrumento

**Pregunta:** los números de la Fase 4 salieron con K=3, n=124, panel 6/7 y sin caché. ¿Sobreviven a un panel completo y a K mayor, y **cuánto concuerdan realmente los jueces**? El spec (§5 reproducibilidad, §6 evaluación) exige responder esto antes de que las cifras entren a la tesis.

### El bug que invalidaba parte de la Fase 4

`glm` no fallaba "de forma intermitente" como asumió la Fase 2-pre: fallaba **determinísticamente**. GLM-4.6 es un modelo de razonamiento y el techo de 400 `max_tokens` se agotaba en la cadena de razonamiento antes de emitir el JSON → `finish_reason=length`, `content=None`. A temperatura 0 los 3 reintentos repetían el mismo fallo. Subiendo el techo a 4000 (sin suprimir el razonamiento: cada familia debe leer el códebook como lo haría naturalmente) el panel quedó en **490/490, 7/7 jueces, cero errores**.

Consecuencia honesta: el `n=124` de la Fase 4 tenía un **juez chino sistemáticamente ausente**, justo en el sidequest que mide sesgo occidental-vs-chino. Las cifras de esta fase reemplazan a las de aquella.

**Segundo plumbing:** `qwen/qwen-2.5-72b-instruct` estaba **retirado** de OpenRouter — el error de ruteo de la Fase 2-pre nunca fue del provider. Reemplazo fijado por fecha: `qwen/qwen3-235b-a22b-2507`. Re-versionado consciente del pre-registro, no un cambio silencioso.

### Resultados (K=10, 7 países, 490 clasificaciones, panel completo)

**1. La separación de China se sostiene y ahora tiene intervalo.** Bootstrap sobre *pasajes* (la unidad de muestreo — remuestrear clasificaciones sueltas fingiría independencia entre los 7 jueces que leen el mismo pasaje):

| país | media | IC95 |
|---|---|---|
| **China** | **+0.94** | **[+0.73, +1.17]** |
| Sudáfrica | +0.06 | [−0.04, +0.21] |
| Canadá | 0.00 | [0.00, 0.00] |
| Colombia / Australia | −0.03 | [−0.16, +0.10] |
| Alemania | −0.10 | [−0.24, 0.00] |
| EUA | −0.30 | [−0.73, 0.00] |

El IC de China **no se solapa con ninguno** → la separación no es un artefacto de K pequeño.

**2. Acuerdo inter-juez — el hallazgo incómodo que hay que reportar.** α ordinal de Krippendorff = **0.600**, κ de Fleiss = 0.455. Eso queda **por debajo del umbral 0.667** que el propio Krippendorff fija como mínimo para conclusiones tentativas. Pero el acuerdo *observado* es alto: **79.9% exacto, 98.8% dentro de ±1 punto** (1470 pares). La brecha es la **paradoja de kappa** (Feinstein & Cicchetti 1990): con la distribución concentrada en 0, la corrección por azar deprime α. Se reportan **ambos**, no uno u otro. Lectura defendible: el instrumento es **fiable a nivel de agregado por país** (ver punto 1), **no** para afirmar nada sobre un pasaje individual.

**3. El sesgo de origen ahora es una medición, no una impresión.** Brecha pareada por pasaje occidental − chino = **+0.098, IC95 [+0.037, +0.162] → excluye el 0**. Los modelos occidentales atribuyen sistemáticamente más estatismo. Y a la vez la correlación pasaje a pasaje es **r = +0.870**: concuerdan mucho, con un desplazamiento sistemático pequeño. Las dos cosas son ciertas y ambas van al capítulo de discusión.

**4. Vía A vs Vía B, ahora sobre los 7 países.** El MVP de embeddings solo cubría 3 documentos; `via_a.py` proyecta el eje ganador (híbrido/tuned6) sobre `politicas_v3` completo:

| país | Vía A (z) | Vía B (LLM) |
|---|---|---|
| China | +0.916 | +0.943 |
| **Canadá** | **+0.895** | **0.000** |
| Australia | +0.538 | −0.029 |
| Alemania | +0.176 | −0.100 |
| Sudáfrica | +0.136 | +0.057 |
| Colombia | −0.094 | −0.029 |
| EUA | −0.654 | −0.300 |

Spearman ρ = +0.667 (coinciden en la tendencia general) **pero China − Canadá: Vía A +0.020 vs Vía B +0.943**. Y con IC bootstrap sobre la mediana Vía A, los intervalos de China [+0.64, +1.07] y Canadá [+0.75, +1.44] **se solapan ampliamente**: el empate no es coincidencia de dos puntos, es incapacidad del método. **El arco narrativo de la tesis queda demostrado sobre el corpus completo, no sobre 3 documentos.**

### Reproducibilidad (spec §5, ahora sí)

- Cada salida cruda **cacheada en disco** con hash del códebook → re-correr es *replay*, no re-llamar; si la rúbrica cambia, la caché se invalida sola.
- **Log de auditoría** JSONL con modelo, timestamp, intento y hash por clasificación.
- Traducciones ZH/ES/DE→EN cacheadas.
- `dezhi_records.jsonl`: las 490 clasificaciones crudas, provenance completa para la tesis.
- κ y α implementados **sin dependencias externas** y **verificados contra `krippendorff` y `statsmodels`** con coincidencia exacta en los 3 niveles (`make dezhi-test`) — la métrica que sostiene el capítulo de validación no depende de mi aritmética.

**Caveats vivos:** K=10 sigue siendo poco (10 pasajes/país); Canadá tiene solo 15 chunks en el corpus, así que su Vía A es ruidosa (de ahí el IC ancho); sin codificación humana no hay ancla externa (trabajo futuro / supervisora); el eje sigue funcionando como **presencia de estatismo (0..+2)**, no como continuo estatista↔liberal.

**Veredicto:** ✅ el instrumento pasa de "resultado preliminar" a "medición con intervalos, acuerdo cuantificado y sesgo acotado". El límite honesto — α por debajo del umbral a nivel pasaje — queda documentado como límite, no escondido.
