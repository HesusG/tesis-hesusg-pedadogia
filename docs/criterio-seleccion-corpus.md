# Criterio de selección del corpus documental

**Estado:** pre-registro. Commitear este archivo fija la regla; cambiarla después exige re-versionar y dejar constancia del motivo.
**Autor:** Hesus García Cobos · Maestría en Pedagogía, UPAEP.

---

## 0. Por qué existe este documento

Hasta ahora el corpus era una **lista de archivos**, no el resultado de una regla. Eso deja la tesis expuesta a una objeción de un minuto en la defensa: *"¿por qué el CONPES 3975 de Colombia y no su política de 2023?"*. Sin criterio escrito, cualquier respuesta suena post-hoc.

Este documento fija la regla, la aplica **hacia atrás** a lo que ya está en el corpus, y **declara las fallas que la propia regla revela**. Documentar una asimetría no la arregla, pero convierte un hueco oculto en una limitación declarada, que es lo que un lector puede evaluar.

---

## 1. Unidad de análisis

La unidad es el **documento de política pública**: un texto adoptado formalmente por un órgano de gobierno, que fija una posición o un curso de acción del Estado.

No son unidad de análisis: artículos académicos, reportes de consultoras u organismos privados, notas de prensa, discursos, borradores no adoptados, ni sitios web institucionales.

---

## 2. Criterios de inclusión

Un documento entra al corpus si cumple **todos**:

**C1 — Adopción oficial.** Emitido por un órgano de gobierno con competencia para hacerlo (ejecutivo, ministerio, comisión estatal, cuerpo legislativo). Se registra el órgano en `adopting_body`.

**C2 — Alcance nacional.** El documento aplica al conjunto del país. Los documentos subnacionales (provinciales, estatales, municipales) **no entran en la comparación principal**; solo pueden usarse en un brazo declarado por separado, y nunca mezclados con documentos nacionales de otros países.

**C3 — Contenido sustantivo de IA.** La inteligencia artificial debe ser objeto del documento, no una mención incidental. Se satisface con **cualquiera** de estas tres condiciones, en este orden de preferencia:
  1. la IA aparece en el título del documento;
  2. el documento dedica una sección propia a la IA;
  3. el documento registra ≥50 menciones de IA en el texto completo.

> *Nota de medición:* la **densidad** de menciones (por cada mil caracteres) **no es comparable entre idiomas**. `人工智能` ocupa 4 caracteres y "artificial intelligence" ocupa 23, lo que infla la densidad del chino unas cinco veces. Por eso C3 usa conteo absoluto y presencia estructural, nunca densidad.

**C4 — Vigencia y corte temporal.** Se toma el documento vigente más reciente de su tipo a la **fecha de corte: 30 de junio de 2026**. Si un documento fue reemplazado por una versión posterior, entra la posterior.

**C5 — Texto verbatim y verificable.** Se requiere el texto completo tal como fue publicado, obtenido de fuente oficial con URL registrada en `source_uri`. **No se admiten resúmenes ni paráfrasis**, incluidas las producidas por herramientas automáticas. (Esta regla nace de un hallazgo propio: en la Fase 2b, `WebFetch` devolvió el Plan Quinquenal **parafraseado** por un modelo pequeño; solo `curl` + extracción de HTML recuperó el texto real.)

**C6 — Par documental por país.** Para que la comparación sea simétrica, cada país aporta **dos** documentos:
  - **(a) Estrategia general de IA**: la política nacional de IA vigente.
  - **(b) IA en educación**: el documento nacional que aplica la IA al sistema educativo.

C6 es una consecuencia directa del SPIKE Fase 6, que mostró una **interacción país × tema**: el encuadre dézhì no se explica ni por el país solo ni por el tema solo. Sin el par, la comparación entre países confunde ambos factores.

---

## 3. Criterios de exclusión

Se excluye explícitamente:

- **Organismos supranacionales e internacionales** (UE, UNESCO, OCDE, WEF) de la comparación entre países. Pueden usarse como **controles declarados**, nunca como si fueran un país.
- **Documentos sectoriales estrechos** que no fijan posición general del Estado.
- Documentos que cumplen C1 pero no C3 (mencionan IA de paso).

---

## 4. Aplicación retroactiva al corpus actual

Aplicando la regla a `politicas_v3` tal como está hoy:

| Documento | País | Año | Menciones IA | C2 nacional | C3 sustantivo | Veredicto |
|---|---|---|---|---|---|---|
| `alemania_ki_strategie_2020` | Alemania | 2020 | 557 | ✅ | ✅ título | **entra** (a) |
| `australia_ai_action_plan_2021` | Australia | 2021 | 353 | ✅ | ✅ título | **entra** (a) |
| `canada_pan_canadian_ai_strategy_2017` | Canadá | 2017 | 38 | ✅ | ✅ título | **entra** (a), ver §5.3 |
| `eeuu_eo14110_2023` | EUA | 2023 | 457 | ✅ | ✅ título | **entra** (a) |
| `colombia_conpes_3975_2019` | Colombia | 2019 | **29** | ✅ | ⚠️ título parcial | **marginal**, ver §5.1 |
| `sudafrica_4ir_2020` | Sudáfrica | 2020 | **222** en 586k | ✅ | ⚠️ tema es 4IR | **marginal**, ver §5.1 |
| `cn_ai_edu_action_2026` | China | 2026 | 96 | ✅ | ✅ título | **entra** (b) |
| `cn_statecouncil_aiplus_2025` | China | 2025 | 92 | ✅ | ✅ título | **entra** (a) |
| `cn_ai_edu_qa_2026` | China | 2026 | 59 | ✅ | ✅ | **entra** (b) |
| `cn_edu_15fyp_2026` | China | 2026 | **7** | ✅ | ⚠️ sección | **marginal** |
| `cn_teachers_genai_report_2026` | China | 2026 | **6** | ✅ | ❌ | **sale** por C3 |
| `cn_beijing_k12_ai_2025` | China | 2025 | 98 | ❌ municipal | ✅ | **sale** por C2 |
| `cn_zhejiang_ai_edu_2025` | China | 2025 | 87 | ❌ provincial | ✅ | **sale** por C2 |
| `cn_henan_ai_edu_2025` | China | 2025 | 77 | ❌ provincial | ✅ | **sale** por C2 |

**La regla expulsa 4 de los 14 documentos**, tres de ellos chinos por ser subnacionales. Esto es incómodo pero correcto: comparar el plan de la Comisión de Educación de Beijing contra la estrategia nacional de Canadá no es una comparación entre países.

---

## 5. Asimetrías que la regla deja al descubierto

### 5.1 Dos documentos "de IA" que apenas hablan de IA

Colombia (**29** menciones en 141k caracteres) y Sudáfrica (**222** en 586k, sobre la Cuarta Revolución Industrial en general) fueron seleccionados como "la política de IA del país", pero ninguno tiene la IA como objeto central. Ambos pasan C1 y C2, y solo marginalmente C3.

Consecuencia: cuando estos países puntúan cerca de cero en los ejes, **no se puede distinguir** entre "el país no encuadra así" y "el documento no habla del tema". Hay que buscar reemplazos vigentes o declarar la limitación.

### 5.2 El volumen de texto está desbalanceado, y no en la dirección que parecía

| País | Fragmentos |
|---|---|
| Sudáfrica | 1303 |
| Colombia | 315 |
| EUA | 306 |
| Alemania | 230 |
| Australia | 161 |
| **China** | **90** |
| Canadá | 15 |

China tiene **muchos documentos cortos**; los demás, **uno largo**. Contra la intuición inicial, China es el segundo corpus más pequeño: Sudáfrica sola aporta catorce veces más texto. El conteo de documentos engaña; el de fragmentos es el que importa.

La agregación por país usa la **distribución de puntajes por fragmento**, no la suma, lo que hace la comparación menos sensible al volumen. Aun así hay que reportarlo.

### 5.3 Canadá tiene 15 fragmentos

La Pan-Canadian AI Strategy son 6,446 caracteres. Con esa base, cualquier estimador para Canadá es ruidoso, y de ahí sale el intervalo de confianza ancho que aparece en la Vía A. Canadá necesita su documento vigente (la estrategia fue renovada después de 2017) o hay que declarar el límite.

### 5.4 Desfase temporal

El corpus mezcla 2017 con 2026. Nueve años en política de IA son una era entera. C4 lo corrige hacia adelante, pero exige **volver a buscar** el documento vigente de cada país.

---

## 6. Corpus objetivo

Aplicando C6, el corpus completo son **14 documentos**: 7 países × 2 tipos, todos nacionales, todos vigentes al corte.

| País | (a) Estrategia de IA | (b) IA en educación |
|---|---|---|
| China | State Council "IA+" 2025 ✅ | Plan de acción IA-educación 2026 ✅ |
| EUA | EO 14110 (2023) ⚠️ revisar vigencia | ❌ falta |
| Canadá | ⚠️ buscar versión vigente | ❌ falta |
| Colombia | ⚠️ reemplazar (C3 marginal) | ❌ falta |
| Alemania | KI-Strategie 2020 ⚠️ revisar vigencia | ❌ falta |
| Sudáfrica | ⚠️ reemplazar (C3 marginal) | ❌ falta |
| Australia | AI Action Plan 2021 ⚠️ revisar vigencia | ❌ falta |

**Faltan 6 documentos de IA en educación y hay que revisar 6 estrategias.** Ese es el trabajo pendiente, y ahora está cuantificado en vez de intuido.

---

## 7. Qué cambia y qué no en los resultados ya obtenidos

Los resultados de las fases 5 y 6 se obtuvieron con el corpus **previo** a esta regla. No se reescriben retroactivamente; se reportan como lo que son, y esta regla define el corpus de la medición definitiva.

Lo que **no** cambia: el hallazgo metodológico central. Que los embeddings no separen a China de Canadá en cinco de seis ejes es una propiedad del método, no del corpus.

Lo que **sí** puede cambiar: los valores por país, en particular Colombia y Sudáfrica (documentos marginales en C3) y Canadá (base mínima). La dirección del efecto de China está sostenida por la Fase 6, que ya controló el tema con documentos que sí cumplen C3.
