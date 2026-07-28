# Los hallazgos frente a la literatura: qué los respalda y qué los amenaza

**Para qué sirve este documento.** Cada hallazgo del trabajo se confronta aquí con literatura publicada. Se listan primero los apoyos y después las objeciones, porque las objeciones son las que hay que responder en la defensa. Las entradas marcadas ✅ las verifiqué (existen, con revista o repositorio identificable); las 🔍 son pistas por confirmar.

---

## 1. El empate China-Canadá

**Nuestro hallazgo.** Medidos por embeddings, China (+0.903) y Canadá (+0.881) quedan estadísticamente empatados en el eje dézhì, con intervalos traslapados. De los seis ejes confucianos, cinco dan empate entre ambos países y solo uno separa.

### Lo que lo respalda

✅ **Bareis, J. y Katzenbach, C. (2022). "Talking AI into Being: The Narratives and Imaginaries of National AI Strategies and Their Performative Politics".** *Science, Technology & Human Values*. DOI: 10.1177/01622439211030007.

Este es **el respaldo más directo que existe**, y ya está en tu bibliografía (te falta el PDF). Analizaron las estrategias de IA de China, Estados Unidos, Francia y Alemania y concluyeron que **la construcción narrativa es sorprendentemente parecida entre países**: todas presentan la IA como inevitable y disruptiva, y todas recurren a un legado nacional y a la competencia internacional. Pero **los imaginarios de fondo son muy distintos** y reflejan diferencias culturales y políticas profundas.

Eso es exactamente tu resultado, dicho en términos cualitativos:
- superficie narrativa uniforme → **los embeddings no pueden separar**
- imaginarios de fondo distintos → **el panel con rúbrica sí**

Tu aporte frente a ellos es que **conviertes esa observación cualitativa en una medición con intervalos**. Ellos afirman que las narrativas convergen; tú demuestras cuánto y dónde exactamente el método superficial se rompe. Esa es la frase con la que conviene posicionar la tesis.

✅ **Sobre Canadá en particular.** La Estrategia Pan-Canadiense de 2017 fue la primera del mundo, la dirigió el CIFAR con 125 millones de dólares y se concentró en **investigación y atracción de talento**. Análisis posteriores señalan que la consulta canadiense tenía un encuadre predeterminado, con las preguntas centradas en competitividad económica y atracción de inversión, y las de seguridad y derechos humanos tratadas como secundarias.

Eso explica el empate. Canadá escribe como **documento de misión estatal e inversión nacional**, que es el mismo registro retórico de China. Ninguno de los dos habla de derechos que limiten al Estado. La diferencia entre ambos no está en el registro sino en para qué se moviliza al Estado, y esa distinción es justo la que el coseno no captura.

### Lo que lo complica

🔍 **Es un documento de 6,446 caracteres, 15 fragmentos.** Ninguna literatura hace falta para ver el problema: la estimación de Canadá descansa en muy poco texto, de ahí su intervalo de confianza ancho. Antes de sostener la comparación conviene conseguir la versión vigente de la estrategia canadiense.

---

## 2. Los embeddings fallan para medir encuadre

**Nuestro hallazgo.** El método de proyección sobre ejes bipolares no distingue países que un lector humano distingue sin esfuerzo.

### Lo que lo respalda

Aquí ocurre algo cómodo: **las críticas metodológicas al método que usamos respaldan nuestra conclusión**, porque nuestra conclusión es que ese método falla en este caso.

✅ **Spirling, A. — *Word Embeddings: What works, what doesn't, and how to tell the difference*.** Revisión de referencia sobre los límites del método en ciencia política.

✅ **Crítica de la "sopa de vectores".** Las operaciones vectoriales con que se construyen dimensiones culturales compuestas pueden propagar errores pequeños y difíciles de detectar a lo largo de todo el análisis, comprometiendo la validez. Tu eje dézhì se construye restando un polo de otro y promediando anclas, así que esta crítica aplica de lleno.

✅ **Estabilidad dimensional.** Distintas proyecciones semánticas definidas de maneras distintas arrojan valores distintos para los mismos términos. Tu propio A/B de tres estrategias de anclaje encontró esto de primera mano: anclar cien por ciento en las Analectas invertía el orden China-Canadá. **Ese resultado tuyo es una réplica independiente de una limitación documentada.** Vale la pena reportarlo así.

✅ **Límite translingüístico.** Los embeddings entrenados en un idioma cargan los estereotipos de ese idioma, y las asociaciones difieren entre lenguas y culturas. Tu corpus mezcla chino, alemán, español e inglés, así que esta es una amenaza directa que ya intentaste acotar con el experimento de idioma de la Fase 3.

✅ **Ideología frente a encuadre.** La literatura sobre escalamiento ideológico con embeddings advierte que el encuadre produce asociaciones lingüísticas que **se confunden con posiciones ideológicas reales**. Es tu problema exacto: "el Estado lidera el esfuerzo nacional" es encuadre compartido, no posición compartida.

### Lo que lo complica

🔍 **La cuestión de la coherencia cultural.** Críticos del enfoque señalan que los símbolos culturales se usan de formas notoriamente incoherentes, y que los embeddings modelan el significado como algo demasiado coherente. Si el dézhì no forma un sistema coherente en los textos, la premisa misma de un eje único es discutible. **Esta objeción también toca tu Vía B**, no solo la A, porque la rúbrica supone que el concepto tiene un contenido estable.

---

## 3. El sesgo por origen del modelo

**Nuestro hallazgo.** Los jueces occidentales califican los textos como más estatistas que los chinos, con una diferencia de +0.058 cuyo intervalo no toca el cero, y una correlación de 0.91 entre ambos grupos.

### Lo que lo respalda

✅ **"Echoes of power: investigating geopolitical bias in US and China large language models".** *Humanities and Social Sciences Communications* (Nature). Documenta divergencias sistemáticas de evaluación alineadas con el origen geopolítico y cultural del modelo.

✅ **Shan, X., Teng, Y., Wang, Y., Zhao, H. y Wang, Y. (2025). "Collectivism and individualism political bias in large language models".** *Big Data & Society*. DOI: 10.1177/20539517251343861. Encuentra que los modelos chinos (ChatGLM, InternLM, Baichuan, Qwen) muestran sesgo colectivista en el campo social.

✅ **Comparaciones GPT-4o frente a DeepSeek-R1** reportan que el primero exhibe sesgos occidentales suaves en encuadre y énfasis, y el segundo sesgos más explícitos alineados con perspectivas estatales chinas.

🔍 **"It's the humans, not the data: Geopolitical bias in LLMs originates in post-training, amplified by the language of the prompt"** (arXiv 2605.23825). Relevante para ti porque sugiere que **el sesgo se origina en el post-entrenamiento y lo amplifica el idioma del prompt**. Tu diseño usa inglés para todos los jueces, lo cual, según esta línea, sería una decisión acertada para acotarlo.

### Lo que hay que explicar bien

Existe una **aparente contradicción** que conviene anticipar. La literatura dice que los modelos chinos son *más colectivistas*. Tu hallazgo dice que califican los textos como *menos estatistas*. Suena opuesto, pero no lo es, y la explicación es el mecanismo:

> Un modelo que **normaliza** el encuadre estatista lo registra como menos digno de mención. Lo que mides no es cuán colectivista es el modelo, sino **cuánto estatismo le atribuye a un texto ajeno**. Un juez para quien la dirección estatal es el fondo normal marca menos desviación que uno para quien es anómala.

Escribe esa distinción explícitamente en el capítulo de discusión. Si no la haces tú, alguien te va a presentar la literatura como si te contradijera.

---

## 4. La interacción país por tema

**Nuestro hallazgo.** El encuadre dézhì se concentra en la política china de IA en educación, no en cualquier documento chino ni en cualquier documento educativo.

### Lo que lo respalda

✅ **La literatura sobre 立德树人 (lìdé shùrén, "cultivar personas de carácter moral").** Xi Jinping lo estableció como **la tarea fundamental de la educación**, y la política oficial ordena tomarlo como eje central del trabajo ideológico y político a lo largo de todo el proceso educativo. Está documentado en el sistema de política de educación moral china y vinculado a los doce valores socialistas fundamentales.

Eso significa que tu hallazgo **no es un artefacto de medición: es una política declarada**. El Estado chino afirma abiertamente que la función de la educación es formar moralmente. Tu instrumento detectó algo que existe y está escrito.

✅ **CSET (Georgetown) publicó una traducción al inglés del Plan de Acción "IA + Educación"**, el mismo documento de tu corpus. Sirve para citar el documento en inglés y para contrastar tu lectura con la de un centro especializado.

✅ **Elman, B. (2000), *A Cultural History of Civil Examinations in Late Imperial China***. El antecedente histórico: el Estado chino lleva siglos usando la educación como instrumento de cultivo moral y selección. Tu interacción tiene profundidad histórica, no es un rasgo de la era Xi.

### Lo que lo complica

✅ **"Negotiating AI(s) futures: competing imaginaries of AI by stakeholders in the US, China and Germany".** *Journal of Science Communication*. **Esta es la objeción más seria del documento.** Muestra que industria, gobierno, academia, medios y sociedad civil **co-construyen y disputan** las visiones de futuro de la IA, y desafía explícitamente la idea de que las percepciones nacionales sean monolíticas.

Tu diseño asigna **un valor por país**. Esa literatura dice que un país no tiene una sola voz. Tu defensa razonable: no mides la opinión de un país, mides **el encuadre de sus documentos oficiales adoptados**, que es un objeto distinto y más acotado. Pero tienes que decirlo, porque es exactamente por donde te van a entrar.

🔍 **"Betting on (un)certain futures: sociotechnical imaginaries of AI and varieties of techno-developmentalism in Asia".** *Information, Communication & Society*. Identifica un imaginario tecno-desarrollista **compartido** en Singapur, Taiwán y Hong Kong. Si existe un imaginario asiático común, tu hallazgo de que Corea, Japón y Singapur puntúan cerca de cero merece contraste con esta línea: quizá comparten algo que tu eje no captura.

---

## 5. Cómo usar esto

**Lo primero que conviene conseguir:** el PDF de Bareis y Katzenbach. Es el trabajo que más te respalda, ya está en tu `.bib` y te da la frase de posicionamiento: ellos observaron cualitativamente la convergencia narrativa, tú la mides y muestras dónde se rompe el método superficial.

**Lo segundo:** el artículo del *Journal of Science Communication* sobre imaginarios en disputa, porque es la objeción que hay que responder de frente en la sección de límites.

**Un movimiento retórico que te conviene:** las críticas al método de Kozlowski no debilitan tu tesis, la sostienen. Tu resultado es que ese método falla en este caso, y la literatura ya documentó por qué podía fallar. Cítalas como marco de tu hallazgo, no como amenaza.

**Advertencia.** Ninguna referencia de este documento debe entrar al `.bib` sin haber visto el texto completo.
