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
