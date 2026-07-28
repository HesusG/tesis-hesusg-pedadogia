# Corpus objetivo: qué documentos faltan y cuáles están vencidos

**Estado:** resultado de aplicar `docs/criterio-seleccion-corpus.md` (criterios C4 vigencia y C6 par documental) buscando los documentos vigentes al corte del 30 de junio de 2026.

---

## 0. Hallazgo previo: el corpus actual tiene documentos derogados

Buscar los documentos vigentes destapó que **dos de los siete países están representados por textos que ya no rigen**:

| País | Documento en el corpus | Problema |
|---|---|---|
| **EUA** | Executive Order 14110 (2023) | **REVOCADA** en enero de 2025 |
| **Colombia** | CONPES 3975 (2019) | **Vigencia terminada en 2022** |

No es un detalle. Significa que la medición de EUA y Colombia describe una postura estatal que fue explícitamente abandonada. Ambos deben reemplazarse antes de la corrida definitiva.

---

## 1. Hallazgo estructural: la asimetría no es solo del corpus, es de los Estados

Al buscar el documento de **IA en educación** de cada país apareció algo que no es un obstáculo logístico sino un dato sustantivo para la tesis:

> **En los países federales, la educación no es competencia del gobierno nacional.**

- **Canadá** no tiene ministerio federal de educación. La educación es competencia exclusiva de las provincias. **No existe** una política nacional canadiense de IA en educación, y no puede existir sin reforma constitucional.
- **Alemania**: la educación es competencia de los *Länder*. Lo más cercano a un documento nacional es la recomendación de la **KMK** (Kultusministerkonferenz, octubre de 2024), que es un órgano de coordinación entre estados, no un ministerio federal.
- **EUA**: la política educativa es estatal. El gobierno federal actúa por órdenes ejecutivas y por condicionamiento de fondos, no por currículo. Más de la mitad de los departamentos estatales de educación emitieron guías propias.
- **China** emite un plan nacional de IA en educación, firmado por el Ministerio de Educación junto con otros cuatro ministerios, que aplica a todo el sistema.

**Por qué esto importa para la tesis:** la existencia misma de un documento nacional de IA en educación **es un indicador del grado de centralización del Estado en la formación de personas**. Que China tenga uno y Canadá estructuralmente no pueda tenerlo no es ruido que haya que corregir: es evidencia del mismo fenómeno que el eje dézhì intenta medir.

Esto obliga a una decisión metodológica explícita, y **cualquiera de las tres opciones es defendible mientras se declare**:

1. **Emparejar por equivalente funcional**: tomar el documento de mayor alcance que exista (KMK en Alemania, orden ejecutiva federal en EUA, marco provincial de referencia en Canadá) y declarar la diferencia de rango.
2. **Emparejar por nivel de gobierno**: comparar solo documentos nacionales, aceptando que algunos países tendrán casilla vacía, y **reportar la ausencia como dato**.
3. **Medir la centralización aparte**: convertir el nivel de adopción en una variable propia del análisis en vez de un confusor a controlar.

**Recomendación:** la opción 3, complementada con la 1. Convierte el problema en hallazgo. La opción 2 desperdicia información.

---

## 2. Candidatos localizados

### (a) Estrategia nacional de IA vigente

| País | Documento vigente | Fecha | Estado |
|---|---|---|---|
| China | State Council «IA+» | 2025 | ✅ ya en corpus |
| **EUA** | **America's AI Action Plan** (+ EO 14179) | jul 2025 | ⬜ reemplaza EO 14110 |
| **Colombia** | **CONPES 4144**, Política Nacional de IA | feb 2025 | ⬜ reemplaza CONPES 3975 |
| **Sudáfrica** | **National AI Policy Framework** (DCDT) | oct 2024 | ⬜ reemplaza reporte 4IR |
| **Australia** | **National AI Plan** | dic 2025 | ⬜ actualiza plan 2021 |
| Canadá | Pan-Canadian AI Strategy / AI for All (ISED) | ⚠️ verificar | ⬜ el de 2017 es muy corto (15 frag.) |
| Alemania | KI-Strategie | ⚠️ verificar si hay posterior a 2020 | ⬜ |

> **Nota sobre Sudáfrica:** existe un borrador de Política Nacional de IA de 2026, pero **fue retirado en abril de 2026 porque su bibliografía contenía citas falsas alucinadas por una IA**. No es elegible (no fue adoptado) y además conviene citarlo en el capítulo de discusión: es un caso real de fallo de IA dentro del propio proceso de política pública que la tesis estudia.

### (b) IA en educación

| País | Candidato | Nivel | Nota |
|---|---|---|---|
| China | Plan de acción «IA+Educación» | nacional | ✅ ya en corpus |
| **EUA** | EO *Advancing AI Education for American Youth* (abr 2025) + *Dear Colleague Letter* del Dept. de Educación (jul 2025) | federal | ⬜ |
| **Alemania** | KMK, *Handlungsempfehlung KI in schulischen Bildungsprozessen* (oct 2024) | interestatal | ⬜ no es federal |
| **Australia** | *Australian Framework for Generative AI in Schools* | nacional | ⬜ |
| Canadá | — | — | ❌ **no existe a nivel nacional** (competencia provincial) |
| Colombia | ⚠️ por buscar (MinEducación / MinTIC) | — | ⬜ |
| Sudáfrica | ⚠️ por buscar (Dept. of Basic Education) | — | ⬜ |

---

## 2-bis. Ampliar el brazo asiático: por qué Vietnam vale más que el resto

El SPIKE Fase 6 añadió Corea, Japón y Singapur como brazo de "vecindario confuciano" y ninguno se despegó de cero. Eso descartó que el efecto fuera regional. Pero **quedó una explicación alternativa sin probar**: los tres son democracias o híbridos de mercado. Ninguno comparte con China la estructura de **Estado-partido**.

O sea, hoy no puedes distinguir entre estas tres hipótesis:

| Hipótesis | Qué predice |
|---|---|
| Es China específicamente | Solo China puntúa alto |
| Es la herencia confuciana | Corea, Japón, Singapur también deberían subir. **Ya refutada** |
| Es la estructura de Estado-partido | Un Estado-partido confuciano no chino también sube |

**Vietnam resuelve el empate.** Es el único país que comparte con China las dos condiciones: pertenece a la esfera cultural confuciana, junto con Corea y Japón, **y** es un Estado-partido de partido único. Si Vietnam puntúa alto, el efecto es de la estructura política. Si puntúa cero, es de China.

Un solo documento decide una pregunta que hoy queda abierta. Ningún otro país del sudeste asiático rinde tanto.

**Los demás ASEAN sirven como control no confuciano.** Indonesia, Malasia, Tailandia y Filipinas son de mayoría musulmana, budista o católica. Si alguno subiera, el eje estaría capturando algo distinto de lo confuciano. Seis de los diez miembros de ASEAN ya tienen estrategia nacional de IA.

### Estado de disponibilidad

| País | Documento | Estado |
|---|---|---|
| **Vietnam** | Decisión 127/QĐ-TTg (ene 2021), *Estrategia Nacional de I+D y Aplicación de IA hasta 2030* | ⚠️ **Existe y hay versión en inglés, pero no la pude bajar en texto verbatim.** El portal `en.baochinhphu.vn` sirve una nota de prensa con menú de navegación: 27 mil caracteres de los cuales solo 10 son menciones de IA. **No cumple C5.** Hace falta el texto de la decisión, no la nota |
| Vietnam (actualización) | Estrategia actualizada y primera Ley de IA, anunciadas para fines de 2025 | 🔍 verificar si ya se publicaron |
| Filipinas | National AI Strategy Roadmap 2.0 (2024-2025) | 🔍 por localizar |
| Malasia | National AI Roadmap 2021-2025 y directrices AIGE | 🔍 por localizar |
| Indonesia | Stranas KA | 🔍 por localizar |
| Tailandia | Estrategia nacional de IA | 🔍 por localizar |

### Advertencia metodológica

Estos países **no entran en la comparación principal de siete**. Entran en el **brazo de control declarado**, igual que Corea, Japón y Singapur en la Fase 6. Esa distinción importa: agregar países al conjunto principal cambiaría el diseño pre-registrado; agregarlos al brazo de control no. Los resultados publicados no se mueven.

---

## 3. Trabajo pendiente, cuantificado

1. **Reemplazar 4 documentos vencidos o marginales**: EUA, Colombia, Sudáfrica, Australia.
2. **Verificar vigencia** de Canadá y Alemania.
3. **Conseguir 4 documentos educativos** localizables: EUA, Alemania, Australia, y buscar Colombia y Sudáfrica.
4. **Declarar la casilla vacía de Canadá** como dato, no como falla.
5. **Re-correr la medición completa** con el corpus nuevo y comparar contra los resultados actuales.

El punto 5 importa: los resultados de las fases 5 y 6 se obtuvieron con el corpus viejo. Cambiar el corpus **puede mover los valores por país**. Lo que no debería moverse es el hallazgo metodológico (que los embeddings no separan a China de Canadá en cinco de seis ejes), porque es una propiedad del método.
