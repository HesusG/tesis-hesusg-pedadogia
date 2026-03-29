# Reflexión Crítica: De la Versión 1 al Rediseño

**Fecha**: 2026-03-28
**Autor**: Hesus García Cobos
**Programa**: Maestría en Pedagogía, UPAEP

---

## 1. Contexto

Entre enero y marzo de 2026 se desarrolló la primera versión (v1) de esta tesis: un análisis comparativo de políticas públicas sobre educación en inteligencia artificial. La v1 construyó un pipeline completo de análisis semántico (Python, ChromaDB, sentence-transformers), procesó 14 documentos de política de 12 países y 2 organismos internacionales, escribió 5 capítulos (~25,500 palabras), desarrolló una visualización web interactiva y produjo resultados que incluyen una matriz de similitud, puntuaciones por dimensión y clustering jerárquico.

La v1 fue un prototipo funcional. Demostró que el pipeline técnico funciona, que los documentos pueden compararse computacionalmente y que la combinación de métodos cualitativos y computacionales produce resultados interpretables. Sin embargo, una evaluación crítica revela problemas de fondo que comprometen la validez del trabajo como investigación académica rigurosa.

Este documento examina esos problemas con honestidad, extrae lecciones y establece los principios de diseño para la v2.

---

## 2. Diagnóstico de Problemas

### 2.1 El problema del martillo (*method-first thinking*)

El error más fundamental de la v1 fue comenzar por la herramienta y buscar después un problema que resolver con ella. La secuencia real fue:

1. "Sé programar y conozco los embeddings" → 2. "Puedo aplicarlos a documentos de política" → 3. "Las políticas de IA en educación son un tema interesante" → 4. "La pregunta de investigación es: ¿qué patrones existen?"

La secuencia correcta habría sido:

1. "Hay una brecha en la investigación comparativa de políticas educativas de IA" → 2. "¿Qué preguntas específicas necesitan respuesta?" → 3. "¿Qué métodos pueden responderlas mejor?" → 4. "Los embeddings ¿agregan valor sobre la lectura cuidadosa? ¿En qué específicamente?"

Grimmer y Stewart (2013) advierten explícitamente sobre este riesgo: "Automated text analysis methods are not a substitute for careful reading. Rather, they amplify and augment the careful reading of texts." El problema no es usar herramientas computacionales, sino no preguntarse *antes* qué tarea concreta deben realizar que la lectura humana no pueda.

En la v1, la respuesta honesta a "¿qué agregaron los embeddings que la lectura no pudo encontrar?" es: casi nada. Los clusters confirmaron lo que la lectura cualitativa ya mostraba. La similitud España-Brasil (0.965) era predecible por proximidad lingüística y marcos compartidos. El aislamiento del EU AI Act era trivial (es legislación, no estrategia). El hallazgo más útil — que la formación docente está suboperacionalizada en todos los países — no requirió embeddings.

**Lección**: Las preguntas de investigación deben formularse antes de elegir el método. El método debe justificarse por lo que puede hacer que otros métodos no pueden, no por su novedad.

### 2.2 Validación circular (*post-hoc queries*)

La metodología de la v1 describe un proceso aparentemente riguroso de triangulación en tres fases:

1. Fase cualitativa: lectura y codificación del corpus según 7 dimensiones
2. Fase computacional: análisis semántico con queries por dimensión
3. Triangulación: comparar hallazgos cualitativos y computacionales

El problema es que las queries computacionales de la Fase 2 se escribieron *después* de la Fase 1. La Tabla 4.1 del Cap 4 lo admite explícitamente: "Estas consultas se formularon a partir de las definiciones operativas de cada dimensión y se refinaron iterativamente comparando los fragmentos recuperados con los codificados cualitativamente."

Esto es validación circular. Si construyo las queries para que capturen lo que ya encontré leyendo, por supuesto que los resultados van a "converger." La Fase 3 (triangulación) no es entonces una validación independiente, sino una tautología disfrazada de método. La convergencia entre fases es un artefacto del diseño, no un hallazgo.

Nelson (2020) propuso la Teoría Fundamentada Computacional con tres etapas: *detección no supervisada de patrones, refinamiento cualitativo y confirmación computacional*. La v1 citó este marco pero invirtió la secuencia: refinó cualitativamente primero y usó lo computacional para confirmar, eliminando la posibilidad de descubrimiento genuino.

**Lección**: La triangulación requiere caminos analíticos genuinamente independientes. Lo no supervisado debe preceder a lo supervisado.

### 2.3 Ausencia de análisis no supervisado

Toda la v1 fue análisis supervisado. Las 7 dimensiones se definieron antes del análisis computacional. Las queries se alinearon con esas dimensiones. El clustering se interpretó a través de esas mismas dimensiones. En ningún momento se dejó que los datos "hablaran primero."

¿Qué habría revelado un análisis no supervisado?

- **Topic modeling** (BERTopic o LDA) sobre los chunks del corpus habría identificado temas emergentes sin presuponerlos. ¿Aparecerían las mismas 7 dimensiones? ¿O emergería un tema no anticipado — por ejemplo, "soberanía tecnológica" o "competitividad económica" — que las 7 dimensiones no capturan?
- **Clustering sin etiquetas previas** habría agrupado los documentos por similitud bruta. ¿Los clusters geográficos serían los mismos? ¿O emergerían agrupaciones por tipo de documento (estrategia vs. legislación vs. lineamientos), por extensión, o por idioma?
- **UMAP sin colores** habría mostrado la geometría del espacio vectorial sin las expectativas del investigador. Los patrones visibles en esa representación son hallazgos; las etiquetas que les ponemos después son interpretación.

La ausencia de análisis no supervisado significa que la v1 nunca tuvo la oportunidad de descubrir algo genuinamente inesperado. Todo lo "encontrado" ya estaba implícito en el diseño.

**Lección**: El análisis no supervisado debe ejecutarse y documentarse *antes* de imponer cualquier framework analítico.

### 2.4 Confusión lingüística no controlada

La v1 reportó una "convergencia iberoamericana" (España-Brasil: 0.965, España-Colombia: 0.934, Brasil-Colombia: 0.925) y afirmó que "no se explica solo por la afinidad lingüística — el modelo multilingüe opera sobre representaciones semánticas, no léxicas."

Esta afirmación carece de respaldo empírico. El español y el portugués son las dos lenguas romances más cercanas entre sí. Los modelos multilingües, aunque capturan semántica, no eliminan completamente la señal de proximidad lingüística de sus representaciones. Un par de documentos en español-portugués sobre temas diferentes probablemente obtendría mayor similitud que un par en español-coreano sobre el mismo tema.

¿Qué se debió hacer?

1. **Línea base en inglés**: Traducir todos los documentos al inglés y recalcular la matriz de similitud. La diferencia entre la matriz multilingüe y la monolingüe cuantifica el componente lingüístico.
2. **Comparación intra- vs. inter-idioma**: ¿La similitud media entre documentos del mismo idioma es significativamente mayor que entre documentos de idiomas diferentes?
3. **Test con corpus paralelo**: Embeber el mismo documento (por ejemplo, la guía de UNESCO) en múltiples idiomas y medir si las similitudes varían.

Nada de esto se hizo. La v1 identificó el confound en las limitaciones pero no lo cuantificó. La diferencia entre "posible limitación" y "limitación cuantificada" es la diferencia entre un reconocimiento pro forma y un trabajo riguroso.

**Lección**: Los confounds conocidos deben cuantificarse, no solo mencionarse.

### 2.5 Corpus incompleto y sesgado geográficamente

La v1 prometió 22 unidades de análisis y entregó 14. Las 8 faltantes incluyen algunos de los actores más importantes: Estados Unidos (mayor productor de tecnología de IA), China (mayor ecosistema de IA en educación, con corrección automática en 60,000 escuelas), Alemania (mayor economía europea), y la OCDE (principal organismo que produce datos comparativos en educación).

Analizar "políticas globales de IA en educación" sin Estados Unidos, China ni la OCDE es como analizar política económica global sin Estados Unidos, China ni el FMI. No invalida todo el trabajo, pero las conclusiones no pueden pretender generalidad.

Además, la muestra estaba sesgada hacia países hispano- y lusohablantes (España, Colombia, Brasil, México, Chile) y anglófonos (Canadá, Australia, Singapur), con representación limitada de Asia (Japón, Corea, India) y ninguna de África ni del Medio Oriente.

**Lección**: Es mejor analizar 7-8 países con profundidad y cobertura completa que prometer 22 y entregar 14 con huecos en los casos más importantes.

### 2.6 Contribución limitada al conocimiento

Los hallazgos principales de la v1 fueron:

1. España, Brasil y Colombia son similares → predecible por idioma y marcos compartidos
2. Japón, Corea, Singapur y Canadá forman un cluster tecnológico → confirma la literatura existente
3. EU AI Act es un outlier → trivial (diferente género discursivo)
4. Francia se alinea con Latinoamérica → moderadamente interesante, pero no explicado
5. Formación docente está suboperacionalizada → hallazgo sólido, pero no requirió embeddings

¿Qué habría sido una contribución genuina? Ejemplos:
- Descubrir un tema latente en las políticas que ningún marco existente captura
- Cuantificar la proporción de similitud atribuible a idioma vs. contenido
- Rastrear la difusión de ideas específicas (por ejemplo, mostrar que la frase "IA ética" se origina en documentos de la OCDE y se replica verbatim en políticas nacionales)
- Demostrar que el análisis computacional puede escalar a corpus mucho más grandes donde la lectura humana sería impráctica

La v1 no hizo ninguna de estas cosas. Su contribución fue metodológica ("los embeddings se pueden usar en educación comparada") más que sustantiva ("estos son los patrones reales de convergencia global").

**Lección**: La contribución debe definirse antes de comenzar. "Aplicar herramienta X al campo Y" no es una contribución; "responder pregunta Z que no podía responderse sin herramienta X" sí lo es.

---

## 3. Lecciones Aprendidas

1. **Las preguntas preceden al método.** Formular la pregunta de investigación primero, luego evaluar qué métodos pueden responderla. Si la lectura cuidadosa puede responderla igual de bien, los embeddings son decorativos.

2. **Lo no supervisado precede a lo supervisado.** Dejar que los datos revelen estructura antes de imponerla. Documentar los hallazgos no supervisados antes de aplicar cualquier framework. Las divergencias entre lo emergente y lo esperado son los hallazgos más interesantes.

3. **Controlar los confounds conocidos.** Si sabes que el idioma puede inflar la similitud, cuantifícalo. Si sabes que la extensión del documento afecta los embeddings, normalízalo. "Posible limitación" no es suficiente; se necesitan números.

4. **Profundidad sobre amplitud.** 7 países analizados completamente > 22 países con 36% faltante. Cada caso incluido debe tener documento procesado, análisis cualitativo completo y cobertura en todas las dimensiones.

5. **La honestidad metodológica es una fortaleza.** Reconocer lo que los embeddings no pueden hacer (distinguir retórica de compromiso, separar señal lingüística de señal temática) no debilita el trabajo; lo hace más creíble.

6. **El prototipo tiene valor.** La v1 no fue un fracaso. Demostró que el pipeline funciona, identificó los problemas metodológicos antes de la defensa, y generó infraestructura técnica reutilizable. Es un prototipo, no un producto terminado.

---

## 4. Principios de Diseño para v2

### 4.1 Question-first

La v2 comenzará con una pregunta que *requiere* análisis computacional para ser respondida:

> ¿En qué medida las políticas nacionales de educación en IA exhiben evidencia de difusión transfronteriza, y puede el análisis semántico distinguir convergencia temática genuina de similitud lingüística o estructural?

Esta pregunta hace de los embeddings el *objeto* de estudio, no solo una herramienta. Preguntar "¿la similitud es temática o lingüística?" requiere análisis computacional porque el lector humano no puede cuantificar el componente lingüístico.

### 4.2 Unsupervised-first

La secuencia analítica será:
1. Análisis no supervisado (BERTopic, clustering múltiple, UMAP) → documentar hallazgos
2. Pre-registro de dimensiones analíticas (commit a git antes de correr scoring)
3. Análisis supervisado por dimensiones
4. Comparación formal entre hallazgos supervisados y no supervisados

### 4.3 Language controls

El componente lingüístico se cuantificará mediante:
- Línea base monolingüe (todo traducido al inglés)
- Comparación intra- vs. inter-idioma
- Test con corpus paralelo (mismo documento en múltiples idiomas)

### 4.4 Fewer cases, deeper analysis

7 países, un representante por continente político:
- **Norteamérica**: Estados Unidos, Canadá
- **Latinoamérica**: Colombia
- **Europa**: Alemania
- **África**: Sudáfrica
- **Oceanía**: Australia
- **Asia**: China (7 documentos longitudinales, 2017-2025)

### 4.5 Pre-registro

Las dimensiones analíticas y las queries se definirán basándose exclusivamente en la literatura y se commitearán a git *antes* de ingestar los documentos de la v2. El historial de git funciona como registro de pre-especificación. Cualquier cambio posterior se documenta y justifica explícitamente.

### 4.6 China como caso longitudinal

La asimetría de China (7 documentos vs. 1-2 de otros países) no es un problema sino una oportunidad. Permite:
- Análisis temporal (evolución 2017→2025)
- Sensitivity analysis (¿cambian los resultados si se usa solo el doc de 2017?)
- Una contribución metodológica sobre la comparabilidad de corpus asimétricos

---

## 5. Lo que se Conserva de v1

### Infraestructura técnica
- **Pipeline completo**: ingest → embedding → similarity → analysis → export (modular, bien probado)
- **ChromaDB**: modelo de almacenamiento vectorial funcional
- **Modelo de embeddings**: `paraphrase-multilingual-MiniLM-L12-v2` (384 dims, local, reproducible)
- **Web visualization**: framework neobrutalist con Chart.js, D3, Plotly
- **LaTeX class**: `upaep-thesis.cls` (UPAEP, Times New Roman 12pt, carta, 1.5 esp.)
- **Makefile**: sistema de build con targets para cada fase

### Conocimiento acumulado
- Comprensión profunda de 14 políticas de IA en educación
- Bibliografía consolidada (~50 entradas verificadas)
- Análisis de debilidades documentado (este documento + weakpoints_analysis)
- Experiencia con los problemas prácticos: encoding, extracción de PDFs, chunking, manejo de idiomas

### Documentos reutilizables
- 3 de los 14 documentos procesados corresponden a países de la v2 (Canadá, Colombia, Australia)
- 7 documentos de China ya descargados y traducidos al inglés
- Bibliografía y PDFs de referencia

### Lo que NO se conserva
- Los capítulos de la tesis (se reescriben completamente)
- La configuración de países en `config.py` (se reemplaza)
- Los resultados (results.json, matrices, clusters)
- Las queries de dimensiones (se pre-registran desde cero)
- La narrativa de "22 unidades de análisis" (ahora son 7 países)

---

## Nota Final

Este documento no es un ejercicio de autoflagelación. La v1 fue un trabajo ambicioso que produjo infraestructura valiosa y conocimiento útil. Pero la honestidad intelectual exige reconocer que el enfoque tenía fallas de diseño que, si no se corrigen, un comité de tesis identificaría. Corregirlas ahora, antes de la defensa, es preferible a descubrirlas durante ella.

La v2 no parte de cero. Parte de un prototipo que demostró qué funciona y qué no. Eso es más valioso que empezar sin experiencia.
