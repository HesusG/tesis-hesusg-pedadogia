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
