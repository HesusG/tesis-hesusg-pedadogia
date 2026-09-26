# Decisiones del proyecto

Este archivo existe para no volver a explicar lo mismo. Recoge qué quiero, qué no
quiero, qué ya está cerrado y qué sigue pendiente. Si trabajas en este repositorio
—persona o agente— léelo antes de proponer nada.

Última actualización: 26 de septiembre de 2026.

---

## Lo que NO quiero

Estas cuatro son reglas duras. No son preferencias de estilo.

**1. Nunca commitear ni pushear sin que yo lo pida.**
Prepara los cambios, déjalos listos, y espera instrucción explícita. Publicar en
GitHub Pages cuenta como push.

**2. Ningún número inventado, ni como ilustración.**
Toda cifra que aparezca en la presentación o en la tesis debe poder rastrearse a
`web/data/*.json`, a los caches de `pipeline_v3/cache/`, o al código. Si no existe el
dato real, no se pone un número aproximado ni un ejemplo "representativo": se cambia el
enfoque de la lámina. Un ejemplo inventado que parece real es peor que no tener ejemplo.

**3. No tocar las notas de speaker.**
Los bloques `<!-- -->` de `slides/slides.md` quedan congelados hasta que yo abra ese
frente, aunque veas que los tiempos están descolocados. Ya sé que lo están.

**4. Nunca versionar archivos personales.**
Jamás entran a un commit, aunque aparezcan en `git status`: las cartas INFOTEC
(`document/carta_*`), `document/firma.png`, `.chroma_db/`, `pipeline/chroma_db/`,
y los PDF de `output/`.

---

## Lo que sí quiero

**El mensaje de la presentación es uno solo:** un método por sí solo miente; hacen falta
dos. Con una sola vía habría publicado que China y Canadá se parecen, y la segunda vía lo
desmiente. Todo lo que no sirva a esa idea sobra en el cuerpo del deck.

**Menos texto, más diagramas.** Las láminas de tarjetas de texto promedian ~950
caracteres; las que tienen diagrama, ~400. El objetivo son ≤500 caracteres por lámina de
cuerpo. Varios diagramas distintos, no uno solo repetido.

**Imágenes que argumentan, no que decoran.** Dominio público, descargadas al repositorio
(nunca hotlink), en duotono azul con las clases `.duo` y `.engrave` que ya existen en
`styles/index.css`. Una imagen entra si sostiene un argumento; si solo rellena, no entra.

**Honestidad metodológica como fortaleza.** Los límites reales se declaran: n=7 países,
cinco de los seis ejes son exploratorios, el acuerdo entre jueces es moderado. Pero no
falsa modestia: sí hay validación —test de confusión con 630 clasificaciones y
experimento de idioma— y hay que mostrarla.

---

## Cambio de marco (26 de septiembre de 2026)

Esto reemplaza al diseño confuciano en la tesis. Los resultados de la Vía A y la Vía B,
el deck de INFOTEC y el paper siguen siendo válidos como trabajo previo, pero el marco de
la tesis ya no es el de los seis ejes.

| Tema | Decisión |
|---|---|
| Criterio de comparación | Los 7 apartados de la sección 6 de Miao et al. (2021), más la distinción de Schiff (2022) entre educación para la IA e IA para la educación. UNESCO no los llama "siete áreas": tratarlos como categorías es decisión propia y se declara. |
| Razón del cambio | Los seis ejes se eligieron por poder de separación, no por pertinencia pedagógica. |
| Método | 100 % automático y exploratorio, en una sola cadena: fragmentos → recuperación por país → panel de 7 modelos con contexto de los fragmentos vecinos → bases vectoriales por categoría → distancias entre países por categoría → control de idioma y medida de acuerdo. Sin codificación manual. |
| Preguntas | Central: distancia entre países dentro de cada categoría UNESCO. P1 cobertura, P2 distancia, P3 robustez. Sin hipótesis; tres supuestos declarados. |
| Intervención | No hay. Se sigue el precedente de Arturo Ayala (misma asesora): la tesis se inspira en la investigación-acción y la intervención ocurre después del estudio. |
| Producto | Un Space en Hugging Face con criterios fijos donde otros suben políticas y ven los resultados. Se describe en la tesis y no se evalúa. |
| Estructura del capítulo 2 | Estado del arte en pasado y marco teórico en presente, según la presentación de Continuidad. |
| Portada | Formato de Arturo, con la Dra. Andrea Saldivar Reyes como asesora. |
| Archivos vigentes | `cap01-planteamiento-unesco.tex`, `cap02-marco-conceptual.tex`, `cap03-acercamiento.tex`, compilados en `avance-2026-09.tex`. `main.tex` todavía no los integra. |

---

## Cerrado

| Tema | Decisión |
|---|---|
| Prioridad | Deck INFOTEC ahora. Tesis, diciembre. |
| Estructura del deck | Se conserva. El problema era densidad, no narrativa. |
| Presupuesto | Hasta 13 minutos, una lámina más. |
| Lámina nueva | El test de confusión. |
| Vía A / Vía B | Vía B al frente como principal. Vía A queda exploratoria. |
| Panel de jueces | Son siete modelos, no lectores humanos. Nunca llamarlos humanos. |
| Enfoque del paper | Metodológico: el panel multi-LLM por origen. |
| Venues | Primero sin costo de publicación; de pago como plan B. Fecha antes de diciembre. Incluir español. |
| Versiones cortas de la tesis | `main_short` y `main_shorter` se congelan como obsoletas. Solo `main.tex` es válida. |
| Corpus chino | El 15º Plan Quinquenal se excluye de la Vía A (`DEEP_DIVE_DOCS`). China entra con 90 fragmentos, no 271. Debe declararse siempre. |

---

## Pendiente

- **Notas de speaker.** Solo 10 de 24 láminas tienen. Los tiempos quedaron descolocados
  por el reordenamiento y dos conservan marcas de la versión de 30 minutos. Una nota
  apunta a la lámina de México que se borró. Congelado por decisión propia.
- **Publicar en GitHub Pages.** El sitio en línea está desactualizado. Se reconstruye
  `web/defensa` y se sube cuando yo lo pida.
- **Capítulos `-short` y `-shorter`.** Siguen en el diseño v2. No se mantienen.
- **`cap03-marco-contextual`.** Habla de 22 unidades de análisis. No es un error: es el
  panorama revisado, distinto de los 7 países medidos. Se deja como está.

---

## Contexto que cuesta caro olvidar

**Hay dos pipelines.** `pipeline_v3/` es el vigente y el que produjo todos los resultados
publicados. `pipeline/` es la fase v2 exploratoria. Confundirlos ya causó que se
documentara la configuración equivocada en la tesis: chunking 800/200 en vez de 500/50,
colección `politicas_ia_educacion_v2` en vez de `politicas_v3`, un solo clasificador en
vez del panel de siete.

**Los documentos de tesis suelen estar mejor que la presentación.** Cuando haya
discrepancia entre `slides/slides.md` y `document/chapters/cap05-resultados.tex`, revisa
primero el capítulo: en la auditoría de agosto de 2026, los `.tex` tenían los números
correctos y era el deck el que se había desviado.
