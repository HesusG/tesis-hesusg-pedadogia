---
theme: default
title: "Los valores confucianos como criterios comparativos en políticas públicas educativas"
info: |
  INFOTEC · Programa de Verano 2026.
  Qué dicen siete países sobre el papel del Estado en la educación en IA,
  y qué pasa cuando intentas medirlo con seis valores confucianos.
highlighter: shiki
mdc: true
colorSchema: light
aspectRatio: 16/9
canvasWidth: 1280
transition: slide-left
# Hash y no history: GitHub Pages solo sirve el 404.html de la raíz del sitio,
# así que con enrutamiento de historial un enlace directo a /defensa/14 o un
# F5 a media defensa caen en el 404 de GitHub. Con hash siempre resuelve
# index.html. Las URL quedan .../defensa/#/14
routerMode: hash
drawings:
  persist: false
layout: cover
---

# Los valores confucianos como<br />criterios comparativos en<br />políticas públicas educativas

<div class="mt-6 flex gap-3">
  <span class="ac-chip">INFOTEC · Programa de Verano</span>
  <span class="ac-chip">Educación comparada</span>
  <span class="ac-chip">10 minutos</span>
</div>

<!--
0:00-0:20 · Saludar y arrancar por la pregunta, no por el método.
NO adelantar el tropiezo de Canadá. La historia funciona si el jurado llega
conmigo, no si se lo cuento de entrada.
-->

---
layout: statement
---

<div class="max-w-4xl">
  <div class="kicker mb-5">Introducción</div>
  <div class="text-[1.5rem] leading-snug text-ink">
    Los sistemas de inteligencia artificial están creciendo en todos los sentidos. Los modelos ahora son capaces de comprender muchos idiomas. Al mismo tiempo, <strong>los países del mundo están escribiendo políticas públicas para regular el uso de inteligencia artificial</strong>.
  </div>
  <div class="mt-7 text-[1.5rem] leading-snug text-ink">
    Me interesa, en particular, las <strong>políticas de educación</strong>. Y sobre todo: ¿qué similitudes o diferencias hay en la forma en que están escribiendo sus políticas los diferentes países?
  </div>
  <div class="mt-9 keyidea text-[1.4rem]">
    <span class="lbl">La pregunta central</span>
    ¿Es posible usar inteligencia artificial para ver las similitudes entre diferentes políticas, y si es así, desde qué perspectivas podría hacerlo?
  </div>
</div>

<!--
0:20-0:40 · La lámina de entrada, en primera persona y sin jerga.
Mencionar en voz alta: mientras escribía esto, la SEP publicó sus diez líneas de
acción sobre IA generativa y la ANUIES su documento de gobernanza. Las dos miran
qué hicieron otros. El préstamo de políticas es la práctica normal en educación
comparada; no la critico, pregunto cómo se hace bien.
-->

---
layout: ac-fact
class: src-alto
---

## Antecedentes

<div class="slide-body">
<div class="text-[1.22rem] max-w-4xl mb-6">Hay al menos tres cosas que ya sabemos que son verdaderas sobre el análisis de políticas de educación en IA:</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6 text-[1.1rem]">Las políticas de diferentes países parecen similares en discurso, pero construyen imaginarios distintos sobre qué es la inteligencia artificial en educación. <span class="text-muted">(Bareis y Katzenbach, 2022)</span></div>
  <div class="ac-card p-6 text-[1.1rem]">El préstamo de políticas es la práctica normal en educación comparada: los países se inspeccionan unos a otros. <span class="text-muted">(Steiner-Khamsi, 2014)</span></div>
  <div class="ac-card p-6 text-[1.1rem]">Ya existen métodos computacionales (BERTopic, embeddings) para modelar automáticamente los temas y significados en un conjunto de documentos de política. <span class="text-muted">(Grootendorst, 2022)</span></div>
</div>
<div class="mt-7 keyidea text-[1.15rem]">
  <span class="lbl">La pregunta que surge</span>
  Si el parecido superficial es engañoso, y ya tenemos herramientas para extraer significado automáticamente de texto, ¿por qué no usarlas para descubrir qué realmente diferencia a las políticas de educación en IA de un país a otro?
</div>
</div>
<div class="src">Steiner-Khamsi, G. (2014). Cross-national policy borrowing: Understanding reception and translation. <i>Asia Pacific Journal of Education, 34</i>(2), 153–167 · Bareis, J., y Katzenbach, C. (2022). Talking AI into being. <i>Science, Technology, &amp; Human Values, 47</i>(5), 855–881 · Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. <i>arXiv preprint arXiv:2203.05794</i>.</div>

<!--
0:40-1:00 · Slide de antecedentes: lo que ya sabemos que es verdad.
(1) El parecido superficial engaña, hay diferencias profundas (Bareis y Katzenbach 2022).
(2) El préstamo de políticas es normal en educación comparada (Steiner-Khamsi 2014).
(3) Existen métodos computacionales para analizar texto automáticamente (BERTopic, embeddings).
De estos tres hechos surge la pregunta de investigación: ¿por qué no usarlos juntos?
-->

---
layout: ac-fact
---

## Los papers detrás del método

<div class="slide-body">
<div class="text-[1.2rem] max-w-4xl mb-6">La investigación se apoya en tres líneas de trabajo ya publicadas:</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6 text-[0.95rem]">
    <div class="kicker mb-3">BERTopic / Topic Modeling</div>
    <div class="text-[0.85rem] leading-relaxed">Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. <i>arXiv:2203.05794</i>.</div>
  </div>
  <div class="ac-card p-6 text-[0.95rem]">
    <div class="kicker mb-3">Embeddings Multilingües</div>
    <div class="text-[0.85rem] leading-relaxed">Reimers, N., y Gurevych, I. (2020). Making monolingual sentence embeddings multilingual using knowledge distillation. <i>Proceedings of EMNLP 2020</i>, 4512–4525.</div>
    <div class="text-[0.85rem] leading-relaxed mt-3">Conneau, A. et al. (2020). Unsupervised cross-lingual representation learning at scale. <i>Proceedings of the 58th ACL</i>, 8440–8451.</div>
  </div>
  <div class="ac-card p-6 text-[0.95rem]">
    <div class="kicker mb-3">Análisis Computacional de Políticas</div>
    <div class="text-[0.85rem] leading-relaxed">Grimmer, J., Roberts, M. E., y Stewart, B. M. (2022). <i>Text as Data: A New Framework for Machine Learning and the Social Sciences</i>. Princeton University Press.</div>
    <div class="text-[0.85rem] leading-relaxed mt-3">Chakraborti, M., et al. (2024). NLP4Gov: A Comprehensive Library for Computational Policy Analysis.</div>
  </div>
</div>
</div>

<!--
0:55-1:00 · Puente entre Antecedentes (lo que sabemos) y embeddings (cómo funciona).
Estos papers respaldan cada pieza: BERTopic para temas no supervisados, embeddings multilingües
para comparación entre idiomas, text-as-data + NLP4Gov para análisis de políticas específicamente.
-->

---
layout: ac-fact
---

## Preguntas de investigación

<div class="slide-body">
<div class="ac-callout mb-7 text-[1.3rem]">
  ¿Las políticas de educación en inteligencia artificial de siete países expresan
  <strong>concepciones distintas sobre quién forma a las personas</strong>, y esos seis valores
  confucianos permiten medir esa diferencia de manera reproducible?
</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6">
    <div class="kicker mb-3">P1 · ¿Se puede medir?</div>
    <div class="text-[1.12rem]">¿Se le puede poner a un párrafo un valor que exprese cuánto presenta la educación en IA como cultivo moral dirigido por el Estado, frente a cuánto la presenta como conducta regulada por normas?</div>
  </div>
  <div class="ac-card-blue p-6">
    <div class="kicker mb-3">P2 · ¿Difieren los países?</div>
    <div class="text-[1.12rem]">¿Se separan los siete países en ese eje? ¿Y la separación sobrevive cuando se controla por la región del documento, por su tema y por la estructura del Estado?</div>
  </div>
  <div class="ac-card p-6">
    <div class="kicker mb-3">P3 · ¿Coinciden los métodos?</div>
    <div class="text-[1.12rem]">¿Dos procedimientos de medición independientes, uno por proyección vectorial y otro por juicio de lectura, producen el mismo ordenamiento de países? Y dentro del panel de lectores, <strong>¿el origen cultural de cada uno sesga su propia calificación?</strong></div>
  </div>
</div>
<div class="mt-7 text-[1.15rem] text-muted max-w-5xl">
P1 es una pregunta de instrumento, P2 de comparación y P3 de validez. Las tres se responden
sobre el valor <strong>virtud o norma</strong>, el único con doble medición.
<strong>La tercera es la que acabó dando el hallazgo principal.</strong>
</div>
</div>

<!--
1:50-2:10 · Leer la pregunta central completa, despacio. Luego las tres, rápido.
Aclarar que P1-P3 se responden sobre el valor virtud-o-norma específicamente, porque
es el único con panel de jueces; los otros cinco valores no tienen las mismas garantías.
P2 se controla por región, tema y estructura del Estado (los tres brazos de confusión);
el sesgo de origen del panel es una pregunta distinta, de validez del instrumento, y por
eso vive en P3. Señalar desde ya que P3 es la que da la sorpresa: siembra el tropiezo
sin contarlo.
-->

---
layout: ac-fact
---

## Objetivos

<div class="slide-body">
<div class="ac-callout mb-4 text-[1.1rem]">
  <span class="kicker block mb-1">Objetivo general</span>
  Usar técnicas de inteligencia artificial para descubrir similitudes y diferencias entre
  <strong>documentos completos</strong> de política de educación en IA de siete países.
</div>
<div class="grid grid-cols-2 gap-3">
  <div class="ac-card p-4">
    <div class="kicker mb-1">1 · El eje de análisis</div>
    <div class="text-[0.95rem]">Seis valores confucianos como criterio para medir cómo se presenta el Estado frente a la persona.</div>
  </div>
  <div class="ac-card p-4">
    <div class="kicker mb-1">2 · El método computacional</div>
    <div class="text-[0.95rem]">Una metodología de análisis de política pública con embeddings multilingües.</div>
  </div>
  <div class="ac-card p-4">
    <div class="kicker mb-1">3 · El corpus</div>
    <div class="text-[0.95rem]">Políticas oficiales de siete países, con criterios de inclusión verificables por un tercero.</div>
  </div>
  <div class="ac-card-blue p-4">
    <div class="kicker mb-1">4 · La validación</div>
    <div class="text-[0.95rem]">Contrastar la medición automática contra un panel humano independiente.</div>
  </div>
  <div class="ac-card-blue p-4" style="grid-column: span 2">
    <div class="kicker mb-1">5 · El control de confusión</div>
    <div class="text-[0.95rem]">Controlar por región, idioma y estructura del Estado: saber si las diferencias sobreviven a esos factores o son un artefacto del método.</div>
  </div>
</div>
<div class="mt-4 keyidea text-[1.05rem]">
  <span class="lbl">El objetivo que más pesa es el cuarto</span>
  Sin patrón de oro contra el cual calibrar, <em>el instrumento no es ninguna de las dos vías: es el contraste entre ambas.</em>
</div>
</div>

<!--
2:10-2:40 · Objetivos reescritos: general (usar IA para comparar políticas) más cinco
específicos (eje confuciano, método computacional multilingüe, corpus, validación,
control de confusión). El objetivo 4 es el que más pesa: sin patrón de oro contra el
cual calibrar, el instrumento no es ninguna de las dos vías, es el contraste entre ambas.
-->

---
layout: ac-fact
---

## Por qué el confucianismo

<div class="slide-body">
<div class="text-[1.2rem] max-w-4xl mb-6">No es un marco teórico elegido al azar. El confucianismo tiene un desarrollo histórico-institucional directamente ligado a la pregunta de esta tesis: cómo el Estado se relaciona con la persona.</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">El antecedente institucional</div>
    Por más de 1,300 años (siglo VII–1905), el Estado chino seleccionó a sus funcionarios mediante exámenes imperiales basados en el dominio de los clásicos confucianos. <span class="text-muted">(Elman, 2013)</span>
  </div>
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">El cultivo de sí (修身 xiūshēn)</div>
    La tradición confuciana no separa la ética personal de la aptitud para gobernar: cultivarse moralmente es la vía hacia la virtud pública. <span class="text-muted">(Ivanhoe, 2000)</span>
  </div>
  <div class="ac-card-blue p-6 text-[1.05rem]">
    <div class="kicker mb-2">La benevolencia (仁 rén) como núcleo</div>
    Rén articula cómo deben tratarse las personas — es el valor del que se derivan los otros cinco ejes de esta investigación. <span class="text-muted">(Csikszentmihalyi, 2024)</span>
  </div>
</div>
<div class="mt-6 keyidea text-[1.15rem]">
  <span class="lbl">Por qué importa</span>
  No es una elección arbitraria de marco teórico: es un marco con más de 1,300 años de aplicación institucional real a la pregunta de cómo el Estado se relaciona con la persona.
</div>
</div>

<div class="src">Elman, B. A. (2013). Civil Examinations and Meritocracy in Late Imperial China. <i>Harvard University Press</i> · Ivanhoe, P. J. (2000). Confucian Moral Self Cultivation (2nd ed.). <i>Hackett Publishing</i> · Csikszentmihalyi, M. (2024). Confucius. <i>Stanford Encyclopedia of Philosophy</i>.</div>

---
layout: ac-fact
---

## De dónde salen los seis valores

<div class="slide-body">
<div class="text-[1.1rem] max-w-4xl mb-3">Para representarlos, tomé los textos clásicos en su <strong>traducción al inglés</strong>.</div>
<div class="text-[1.18rem] max-w-4xl mb-5">Uso seis valores de la tradición confuciana como criterios comparativos: <strong>仁 rén</strong> (benevolencia), <strong>礼 lǐ</strong> (ritual y propiedad), <strong>义 yì</strong> (rectitud), <strong>修身 xiūshēn</strong> (cultivo de sí), <strong>德治 dézhì</strong> (gobierno por virtud) ↔ <strong>法 fǎ</strong> (norma) y <strong>和 hé</strong> (armonía).</div>
<div class="grid grid-cols-2 gap-6">
  <div class="ac-card p-6">
    <div class="kicker mb-3">Por qué estos y no otros cinco</div>
    <div class="text-[1.08rem]">No los elegí a mano. Probé tres conjuntos candidatos —el quinteto clásico 仁义礼智信, uno de siete valores educativos, y este de seis— proyectados sobre el mismo corpus, y comparé cuál separaba mejor a los países. <strong>Ganó el de seis</strong>: es una elección empírica, no arbitraria.</div>
  </div>
  <div class="ac-card-blue p-6">
    <div class="kicker mb-3">Los textos clásicos</div>
    <div class="text-[0.98rem] leading-relaxed">
      <div class="mb-2"><strong>论语 Lúnyǔ</strong> (Analectas) — enseñanzas de Confucio sobre ética, ritual y buen gobierno.</div>
      <div class="mb-2"><strong>孟子 Mèngzǐ</strong> (Mencio) — desarrolla la benevolencia y la bondad innata de la naturaleza humana.</div>
      <div><strong>礼记 Lǐjì</strong> (Libro de los Ritos) — normas rituales y protocolos que ordenan la vida social y política.</div>
    </div>
  </div>
</div>
<div class="mt-6 keyidea text-[1.15rem]">
  <span class="lbl">Por qué virtud o norma es el que se defiende con más fuerza</span>
  Es el que nombra directamente la pregunta de esta investigación: si el Estado se presenta
  como quien <em>forma</em> a las personas o como quien les <em>pone límites</em>.
</div>
</div>
<div class="src">Csikszentmihalyi, M. (2024). Confucius. <i>Stanford Encyclopedia of Philosophy</i> · Pines, Y. (2023). Legalism in Chinese Philosophy. <i>Stanford Encyclopedia of Philosophy</i>.</div>

<!--
1:20-1:50 · Antes no explicaba de dónde salían los seis valores; esta lámina lo cubre.
Ser honesto sobre el proceso: no es un canon fijo de 2,000 años, es un conjunto afinado
empíricamente contra tres candidatos (canon5, tuned6, edu7). Eso es una fortaleza
metodológica, no una debilidad, si se dice así.
-->

---
layout: ac-diagram
---

## Primero: qué es un token

<div class="slide-body">
<div class="text-[1.15rem] max-w-5xl mb-6">Un modelo no "lee" como un humano. Lo primero que hace es <strong>partir el texto en piezas</strong>.</div>
<div class="diagram" style="gap: 1rem">
 <div class="dbox-hi" style="padding: 1rem 1.4rem">
  <div class="dt">Texto original</div>
  <div class="ds" style="font-size: 0.95rem; margin-top: 0.35rem">«La educación en inteligencia artificial es una prioridad»</div>
 </div>
 <div class="darrow-down"></div>
 <div class="dcol" style="gap: 0.7rem">
  <div class="drow" style="gap: 0.4rem; flex-wrap: wrap; justify-content: center">
   <span class="dchip">La</span>
   <span class="dchip">educación</span>
   <span class="dchip">en</span>
   <span class="dchip-hi">IA</span>
   <span class="dchip">es</span>
   <span class="dchip">prioridad</span>
  </div>
  <div class="dcap">seis tokens</div>
 </div>
</div>
<div class="ac-callout mt-6 text-[1.05rem] max-w-4xl mx-auto">
 Un <strong>token</strong> es la unidad más pequeña que el modelo entiende: puede ser una palabra, una sílaba o un carácter. Aquí, cada palabra es un token.
</div>
</div>

---
layout: ac-diagram
---

## Después: cada token deviene un vector

<div class="slide-body">
<div class="text-[1.15rem] max-w-5xl mb-6">Cada token se convierte en una <strong>lista de números</strong> que codifica su significado.</div>
<div class="diagram" style="gap: 1rem">
 <div class="drow" style="gap: 0.4rem; flex-wrap: wrap; justify-content: center">
  <span class="dchip">La</span>
  <span class="dchip">educación</span>
  <span class="dchip">en</span>
  <span class="dchip-hi">IA</span>
  <span class="dchip">es</span>
  <span class="dchip">prioridad</span>
 </div>
 <div class="darrow-down"></div>
 <div class="drow" style="gap: 1rem; align-items: flex-end">
  <div class="dbox" style="padding: 0.6rem 0.9rem">
   <div class="dt" style="font-size: 0.9rem">La</div>
   <div class="ds" style="font-size: 0.72rem">[0.23, −0.81, 0.45…]</div>
  </div>
  <div class="dbox" style="padding: 0.6rem 0.9rem">
   <div class="dt" style="font-size: 0.9rem">educación</div>
   <div class="ds" style="font-size: 0.72rem">[0.12, 0.67, −0.33…]</div>
  </div>
  <div class="dbox-hi" style="padding: 0.6rem 0.9rem">
   <div class="dt" style="font-size: 0.9rem">IA</div>
   <div class="ds" style="font-size: 0.72rem">[0.91, −0.45, 0.78…]</div>
  </div>
  <div class="dcap" style="padding-bottom: 0.6rem">…</div>
 </div>
</div>
<div class="mt-6 keyidea text-[1.1rem]">
  <span class="lbl">Por qué esto importa</span>
  Convertido en números, el significado se vuelve medible: dos textos se pueden comparar por la distancia entre sus vectores.
</div>
</div>

<div class="src">Mikolov, T., Chen, K., Corrado, G., y Dean, J. (2013). Efficient estimation of word representations in vector space. <i>arXiv preprint arXiv:1301.3781</i> · Reimers, N., y Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. <i>Proceedings of EMNLP-IJCNLP 2019</i>, 3982–3992.</div>

<!--
1:00-1:15 · Cascada visual: Texto (grande) → Tokens (medio) → Vectores (pequeño).
Se explica qué es un token con callout. El token destacado (IA) muestra cómo se traduce a vector.
Visualmente claro sin jerga: el texto se descompone, cada parte deviene número.
-->

---
layout: ac-diagram
class: src-alto
---

## Los espacios convergen entre idiomas

<div class="slide-body">
<div class="text-[1.15rem] max-w-5xl mb-4">No es que el modelo traduzca primero. La misma idea escrita en tres idiomas <strong>aterriza en la misma región del espacio vectorial</strong>.</div>
<div class="flex justify-center">
<svg viewBox="0 0 940 250" style="width: 100%; max-width: 950px">
 <g>
  <rect x="8" y="20" width="292" height="56" fill="#F4F7FB" stroke="#DADEE6" />
  <text x="26" y="42" fill="#023BF2" style="font-size:11px; letter-spacing:1.5px">ES</text>
  <text x="26" y="63" fill="#0F1624" style="font-size:13px">«La educación en IA es prioridad»</text>
  <rect x="8" y="97" width="292" height="56" fill="#F4F7FB" stroke="#DADEE6" />
  <text x="26" y="119" fill="#023BF2" style="font-size:11px; letter-spacing:1.5px">EN</text>
  <text x="26" y="140" fill="#0F1624" style="font-size:13px">«AI education is a priority»</text>
  <rect x="8" y="174" width="292" height="56" fill="#F4F7FB" stroke="#DADEE6" />
  <text x="26" y="196" fill="#023BF2" style="font-size:11px; letter-spacing:1.5px">ZH</text>
  <text x="26" y="217" fill="#0F1624" style="font-size:13px">「人工智能教育是重点」</text>
 </g>
 <g fill="none" stroke="#023BF2" stroke-width="1.4">
  <path d="M304 48 Q 420 48 476 112" stroke-dasharray="5 3" />
  <path d="M304 125 L 476 125" stroke-dasharray="5 3" />
  <path d="M304 202 Q 420 202 476 138" stroke-dasharray="5 3" />
 </g>
 <path d="M486 125 l -11 -5 v 10 z" fill="#023BF2" />
 <text x="390" y="110" fill="#4D5566" style="font-size:12px" text-anchor="middle">modelo</text>
 <text x="390" y="146" fill="#4D5566" style="font-size:12px" text-anchor="middle">multilingüe</text>
 <circle cx="700" cy="120" r="96" fill="none" stroke="#DADEE6" stroke-width="1.5" />
 <circle cx="700" cy="120" r="62" fill="none" stroke="#DADEE6" stroke-width="1" stroke-dasharray="3 4" />
 <circle cx="700" cy="120" r="30" fill="#023BF2" fill-opacity="0.07" stroke="#023BF2" stroke-width="1.2" stroke-dasharray="3 3" />
 <circle cx="690" cy="112" r="6" fill="#023BF2" />
 <circle cx="710" cy="118" r="6" fill="#0B1C45" />
 <circle cx="697" cy="131" r="6" fill="#4D5566" />
 <text x="700" y="242" fill="#4D5566" style="font-size:13px" text-anchor="middle">una sola región del espacio vectorial</text>
</svg>
</div>
<div class="mt-4 keyidea text-[1.1rem]">
  <span class="lbl">Aplicación a esta investigación</span>
  Permite comparar Colombia (español), China (chino) y Australia (inglés) sin traducir: los vectores miden significado, no coincidencia de palabras.
</div>
</div>

<div class="src">Mikolov, T., Chen, K., Corrado, G., y Dean, J. (2013). Efficient estimation of word representations in vector space. <i>arXiv preprint arXiv:1301.3781</i> · Reimers, N., y Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. <i>Proceedings of EMNLP-IJCNLP 2019</i>, 3982–3992 · Reimers, N., y Gurevych, I. (2020). Making monolingual sentence embeddings multilingual using knowledge distillation. <i>Proceedings of EMNLP 2020</i>, 4512–4525.</div>

<!--
1:15-1:30 · Convergencia multilingüe: cómo los idiomas distintos comparten el mismo espacio.
Visual de tres círculos (ES, EN, ZH) superpuestos en un espacio central. El callout explica
que no es traducción, es que los vectores ya capturan significado universal.
Conexión directa: eso permite comparar políticas sin traducir.
-->

---
layout: ac-fact
class: src-alto
---

## ¿Pueden los LLM categorizar texto?

<div class="slide-body">
<div class="text-[1.12rem] max-w-5xl mb-5">Un <strong>LLM</strong> (modelo de lenguaje grande) puede hacer algo más directo que convertir texto en vectores: si le preguntas <strong>«¿este fragmento presenta al Estado como quien forma o como quien regula?»</strong>, responde siguiendo ese criterio, sin haber sido entrenado para esa tarea.</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">Clasificación sin entrenamiento</div>
    Un LLM puede anotar categorías de texto (zero-shot) igual o mejor que anotadores humanos entrenados, en tareas de clasificación temática. <span class="text-muted">(Gilardi et al., 2023)</span>
  </div>
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">Medir conceptos con codebooks</div>
    Se pueden usar LLMs como instrumento de medición para conceptos de ciencia política, siguiendo un codebook explícito de criterios. <span class="text-muted">(Halterman y Keith, 2025)</span>
  </div>
  <div class="ac-card-blue p-6 text-[1.05rem]">
    <div class="kicker mb-2">Transforman las ciencias sociales computacionales</div>
    Los LLM son capaces de anotar, clasificar y medir constructos sociales complejos a partir de instrucciones en lenguaje natural. <span class="text-muted">(Ziems et al., 2024)</span>
  </div>
</div>
<div class="mt-6 keyidea text-[1.15rem]">
  <span class="lbl">Por qué esto define los dos métodos de esta tesis</span>
  Un fragmento de texto puede medirse de dos formas: por su <strong>cercanía vectorial</strong> a un valor confuciano, o por <strong>clasificación directa</strong> siguiendo un criterio explícito. Esta tesis usa ambos métodos y los contrasta entre sí.
</div>
</div>

<div class="src">Gilardi, F., Alizadeh, M., y Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. <i>Proceedings of the National Academy of Sciences, 120</i>(30), e2305016120 · Halterman, A., y Keith, K. A. (2025). Codebook LLMs: Evaluating LLMs as measurement tools for political science concepts. <i>Political Analysis</i>. arXiv:2407.10747 · Ziems, C., Held, W., Shaikh, O., Chen, J., Zhang, Z., y Yang, D. (2024). Can large language models transform computational social science? <i>Computational Linguistics, 50</i>(1), 237–291.</div>

---
layout: ac-diagram
---

## La arquitectura del pipeline

<div class="slide-body">
<div class="diagram" style="gap: 0.85rem">
 <div class="drow" style="gap: 0.7rem">
  <div class="dbox" style="padding: 0.55rem 0.85rem">
   <div class="dt"><Ico name="file-text" class="ico ico-blue" /> Políticas</div>
   <div class="ds">7 países · 15 documentos</div>
  </div>
  <div class="darrow"></div>
  <div class="dbox" style="padding: 0.55rem 0.85rem">
   <div class="dt"><Ico name="scissors" class="ico ico-blue" /> Chunking</div>
   <div class="ds">800 caracteres · 200 de traslape</div>
  </div>
  <div class="darrow"></div>
  <div class="dbox-hi" style="padding: 0.55rem 0.85rem">
   <div class="dt"><Ico name="database" class="ico ico-blue" /> ChromaDB</div>
   <div class="ds">almacén vectorial</div>
  </div>
 </div>
 <div class="darrow-down"></div>
 <div class="drow" style="gap: 0.7rem">
  <div class="dbox" style="padding: 0.55rem 0.85rem">
   <div class="dt"><Ico name="terminal" class="ico ico-blue" /> Harness</div>
  </div>
  <div class="darrow"></div>
  <div class="dbox" style="padding: 0.55rem 0.85rem">
   <div class="dt"><Ico name="search-check" class="ico ico-blue" /> Retrieval</div>
   <div class="ds">top-k</div>
  </div>
  <div class="darrow"></div>
  <div class="dbox" style="padding: 0.55rem 0.85rem">
   <div class="dt"><Ico name="message-square-warning" class="ico ico-blue" /> System prompt</div>
  </div>
 </div>
 <div class="darrow-down"></div>
 <div class="dcol" style="gap: 0.5rem">
  <div class="dcap">varios modelos, sobre los mismos chunks multilingües</div>
  <div class="drow" style="gap: 0.5rem">
   <span class="dchip"><Ico name="openai" class="ico" /> GPT</span>
   <span class="dchip"><Ico name="claude" class="ico" /> Claude</span>
   <span class="dchip-hi"><Ico name="cpu" class="ico" /> local</span>
  </div>
 </div>
 <div class="darrow-down"></div>
 <div class="dbox-hi" style="padding: 0.55rem 1.2rem">
  <div class="dt"><Ico name="sigma" class="ico ico-blue" /> Medida</div>
  <div class="ds">un número por país y por eje</div>
 </div>
</div>
<div class="mt-5 keyidea text-[1.05rem]">
  <span class="lbl">De políticas a números</span>
  De documentos completos a una medida comparable, pasando por chunks, vectores y modelos.
</div>
</div>

---
layout: ac-diagram
---

## Dos mecanismos de control simultáneos

<div class="slide-body">
<div class="flex justify-center gap-12" style="align-items: flex-start">
 <div class="dcol" style="gap: 0.6rem">
  <div class="kicker" style="color: var(--ac-blue)">Mecanismo 1 · automático</div>
  <div class="dbox" style="padding: 0.6rem 0.9rem">
   <div class="dt"><Ico name="search-check" class="ico ico-blue" /> Retrieval</div>
  </div>
  <div class="darrow-down"></div>
  <div class="dbox" style="padding: 0.6rem 0.9rem">
   <div class="dt"><Ico name="scale" class="ico ico-blue" /> Distancia semántica</div>
   <div class="ds">similitud coseno</div>
  </div>
 </div>
 <div class="dcol" style="gap: 0.6rem">
  <div class="kicker" style="color: var(--ac-blue)">Mecanismo 2 · juicio</div>
  <div class="dbox-hi" style="padding: 0.6rem 0.9rem; max-width: 260px">
   <div class="dt"><Ico name="cpu" class="ico ico-blue" /> Juicio LLM</div>
   <div class="ds">«¿Tiene sentido comparar esto?»</div>
  </div>
  <div class="darrow-down"></div>
  <div class="drow" style="gap: 0.7rem; align-items: stretch">
   <div class="dbox" style="padding: 0.5rem 0.7rem; border-style: dashed; border-color: var(--ac-line)">
    <div class="dt dneg" style="font-size: 0.85rem"><Ico name="search-x" class="ico" /> No</div>
    <div class="ds">se descarta</div>
   </div>
   <div class="dbox-hi" style="padding: 0.5rem 0.7rem">
    <div class="dt" style="font-size: 0.85rem"><Ico name="badge-check" class="ico ico-blue" /> Sí</div>
    <div class="ds">país · título · posición</div>
   </div>
  </div>
 </div>
</div>
<div class="flex justify-center">
<svg viewBox="0 0 640 58" style="width: 100%; max-width: 640px">
 <g fill="none" stroke="#0F1624" stroke-width="1.5">
  <path d="M150 2 V 12 Q 150 30 320 30" />
  <path d="M490 2 V 12 Q 490 30 320 30" />
  <path d="M320 30 V 44" />
 </g>
 <path d="M320 52 l -5 -9 h 10 z" fill="#0F1624" />
</svg>
</div>
<div class="dbox-hi" style="padding: 0.6rem 1.2rem; margin: 0 auto; text-align: center; max-width: 460px">
  <div class="dt"><Ico name="sigma" class="ico ico-blue" /> Promedio del espacio vectorial</div>
  <div class="ds">los chunks del mismo eje → un número por país</div>
</div>
<div class="mt-5 keyidea text-[1.05rem]">
  <span class="lbl">Por qué dos mecanismos</span>
  El número final no sale de un fragmento: es el promedio de todos los que el LLM confirmó que tenía sentido comparar, dentro del mismo eje.
</div>
</div>

---
layout: ac-fact
---

## Las políticas que se midieron

<div class="slide-body">
<table class="actable">
  <thead><tr><th style="width:16%">País</th><th style="width:46%">Documento</th><th style="width:10%">Año</th><th>Fragmentos</th></tr></thead>
  <tbody>
    <tr><th>China</th><td>15º Plan Quinquenal <span class="dim">十五五</span> · y ocho documentos más</td><td>2026</td><td class="yes">271</td></tr>
    <tr><th>Canadá</th><td>AI for All <span class="dim">· sustituido durante el estudio</span></td><td>2026</td><td>210</td></tr>
    <tr><th>Estados Unidos</th><td>America's AI Action Plan <span class="dim">· sustituido durante el estudio</span></td><td>2025</td><td>156</td></tr>
    <tr><th>Colombia</th><td>CONPES 4144 <span class="dim">· sustituido durante el estudio</span></td><td>2025</td><td>764</td></tr>
    <tr><th>Alemania</th><td>KI-Strategie der Bundesregierung</td><td>2020</td><td>230</td></tr>
    <tr><th>Sudáfrica</th><td>Informe de la Comisión Presidencial 4IR</td><td>2020</td><td>1,303</td></tr>
    <tr><th>Australia</th><td>AI Action Plan</td><td>2021</td><td>161</td></tr>
    <tr><th class="text-blue">México</th><td><span class="no">Ningún documento admisible</span> <span class="dim">· sin política de IA adoptada por un órgano de gobierno</span></td><td class="dim">—</td><td class="no">0</td></tr>
  </tbody>
</table>
<div class="mt-5 text-[1.05rem] text-muted">
Un país por región política del mundo. <strong>Tres de los siete documentos originales tuvieron
que sustituirse</strong> a mitad del estudio: el de Estados Unidos y el de Colombia porque estaban
derogados, y el de Canadá porque no era la estrategia. Cada baja quedó registrada con su motivo.
</div>
</div>

<!--
10:30-11:30 · Nombrar el Plan Quinquenal en voz alta: es la fuente más importante
del corpus, 140 páginas adoptadas por la Asamblea Popular Nacional en marzo de 2026.
No detenerse en Canadá todavía, solo dejar sembrado que se sustituyó.
La fila de México es el puente a la lámina que sigue.
-->

---
layout: ac-fact
---

## Qué son los resultados

<div class="slide-body">
<div class="text-[1.2rem] max-w-4xl mb-6">Antes de ver números, hay que dejar claro qué estamos midiendo y qué significa cada número.</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">Contra qué se compara</div>
    Cada eje confuciano tiene un anclaje construido a partir de los textos clásicos (Analectas, Mencio). Cada política se proyecta sobre ese eje.
  </div>
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">El promedio</div>
    El número de cada país es el <strong>promedio de todos sus fragmentos</strong> (chunks) en ese eje, no un solo párrafo elegido a mano.
  </div>
  <div class="ac-card-blue p-6 text-[1.05rem]">
    <div class="kicker mb-2">Qué significa el número</div>
    Cuántas desviaciones se aparta ese país del <strong>documento promedio del corpus</strong> — no es una escala absoluta, es relativa a los otros seis países.
  </div>
</div>
<div class="mt-6 keyidea text-[1.15rem]">
  <span class="lbl">Por qué importa aclararlo antes</span>
  Un número solo tiene sentido si se sabe contra qué se comparó: aquí, contra el corpus de políticas y contra los textos confucianos que definen cada eje.
</div>
</div>

---
layout: ac-fact
---

## Los seis valores con que se describe cada política

<div class="slide-body">
<table class="actable" style="font-size:0.86rem">
  <thead><tr>
    <th style="width:15%">Eje</th><th style="width:23%">Qué opone</th>
    <th class="text-right">China</th><th class="text-right">Canadá</th><th class="text-right">EUA</th>
    <th class="text-right">Colombia</th><th class="text-right">Alemania</th><th class="text-right">Sudáfrica</th><th class="text-right">Australia</th>
  </tr></thead>
  <tbody>
    <tr><th>仁 <span class="dim">rén</span><br />Benevolencia</th><td class="dim">La persona · frente a · la eficiencia</td>
      <td style="text-align:right" class="yes">+0.97</td><td style="text-align:right">+0.34</td><td style="text-align:right">+0.09</td><td style="text-align:right" class="dim">−0.40</td><td style="text-align:right">+0.06</td><td style="text-align:right">−0.07</td><td style="text-align:right">+0.11</td></tr>
    <tr><th>礼 <span class="dim">lǐ</span><br />Ritual</th><td class="dim">La norma compartida · frente a · su ausencia</td>
      <td style="text-align:right">+0.16</td><td style="text-align:right" class="yes">+0.39</td><td style="text-align:right" class="dim">−0.84</td><td style="text-align:right">−0.44</td><td style="text-align:right">−0.23</td><td style="text-align:right">+0.30</td><td style="text-align:right">+0.04</td></tr>
    <tr><th>义 <span class="dim">yì</span><br />Rectitud</th><td class="dim">Lo justo · frente a · el provecho</td>
      <td style="text-align:right" class="yes">+1.07</td><td style="text-align:right">+0.17</td><td style="text-align:right">+0.48</td><td style="text-align:right" class="dim">−0.19</td><td style="text-align:right">+0.11</td><td style="text-align:right">−0.13</td><td style="text-align:right">−0.13</td></tr>
    <tr><th>修身 <span class="dim">xiūshēn</span><br />Cultivo de sí</th><td class="dim">Formar el carácter · frente a · sacar el título</td>
      <td style="text-align:right" class="yes">+0.51</td><td style="text-align:right">+0.30</td><td style="text-align:right" class="dim">−0.21</td><td style="text-align:right">+0.37</td><td style="text-align:right">−0.05</td><td style="text-align:right">−0.16</td><td style="text-align:right">−0.11</td></tr>
    <tr><th class="text-blue">德治↔法 <span class="dim">dézhì↔fǎ</span><br />Virtud vs. norma</th><td class="dim">El Estado forma · frente a · el Estado pone reglas</td>
      <td style="text-align:right" class="yes">+0.85</td><td style="text-align:right">+0.78</td><td style="text-align:right" class="dim">−0.07</td><td style="text-align:right">−0.20</td><td style="text-align:right">+0.08</td><td style="text-align:right">+0.03</td><td style="text-align:right">+0.45</td></tr>
    <tr><th>和 <span class="dim">hé</span><br />Armonía</th><td class="dim">El bien colectivo · frente a · la autonomía</td>
      <td style="text-align:right" class="yes">+0.47</td><td style="text-align:right">−0.28</td><td style="text-align:right" class="dim">−0.68</td><td style="text-align:right">−0.39</td><td style="text-align:right">−0.26</td><td style="text-align:right" class="yes">+0.47</td><td style="text-align:right">+0.05</td></tr>
  </tbody>
</table>
<div class="mt-5 text-[1.05rem] text-muted max-w-5xl">
Cada número dice cuántas desviaciones se aparta ese país del documento promedio del corpus.
<strong>China encabeza cinco de los seis ejes</strong>; el único que no, el ritual, lo encabeza Canadá.
Sudáfrica empata a China en armonía.
</div>
<div class="mt-3 text-[1.05rem] text-muted max-w-5xl">
Que un mismo país domine casi todo obliga a preguntar si los seis ejes miden seis cosas distintas
o una sola. Por eso <em>uno de ellos se midió dos veces</em>, con dos métodos independientes:
el de virtud contra norma, que es el que responde la pregunta de esta tesis.
</div>
</div>
<div class="src">Vía automática · medianas contra el promedio de todos los documentos del corpus.</div>

<!--
2:40-3:10 · Los seis ejes salen del vocabulario confuciano y se aplican por igual
a los siete países. Leer la tabla por columnas, no por filas: China arriba en casi
todo. Ese dominio es justamente lo que obliga a validar. Los cinco primeros ejes
están medidos solo por la vía automática y son exploratorios; el sexto es el que
tiene panel de jueces. Decirlo aquí evita que un sinodal lo saque después.
-->

---
layout: ac-fact
---

## El panorama completo

<div class="slide-body">
<div class="grid grid-cols-[1fr_0.85fr] gap-6 items-center">
  <div class="flex items-center justify-center">
    <RadarConfucio resalta :paises="['china','canada','eeuu','colombia','alemania','sudafrica','australia']" />
  </div>
  <div>
    <div class="text-[1.2rem]">Los siete países, en el mismo mapa. Cada punta es uno de los seis
    ejes; mientras más lejos del centro, más presente está ese valor en los textos de ese país.</div>
    <div class="mt-5 text-[1.2rem]">La mayoría de los países se agrupan cerca del centro — el
    perfil promedio del corpus. <strong>China es la excepción visible</strong>: se extiende más
    lejos que los demás en casi todos los ejes.</div>
  </div>
</div>
</div>
<div class="src">Vía automática · medianas contra el promedio de todos los documentos del corpus.</div>

---
layout: ac-fact
---

## El caso de China y Canadá

<div class="slide-body">
<div class="grid grid-cols-[1fr_0.85fr] gap-6 items-center">
  <div class="flex items-center justify-center">
    <RadarConfucio :paises="['china','canada']" />
  </div>
  <div>
    <div class="text-[1.2rem]">La misma tabla anterior, dibujada. Cada punta es uno de los seis
    ejes; mientras más lejos del centro, más presente está ese valor en los textos de ese país.</div>
    <div class="mt-5 text-[1.2rem]">Puestos uno encima del otro, los dos países que en teoría
    deberían estar más lejos <strong>casi se enciman</strong>: tres de los seis ejes empatan,
    y uno de los que empatan es <em>justo el que mide quién forma a quién</em>.</div>
    <div class="mt-6 ac-callout text-[1.1rem]">
      Para el método automático, la política china y la canadiense son prácticamente el mismo
      texto. Guarden esa imagen: la tercera parte de la defensa trata de por qué eso está mal.
    </div>
  </div>
</div>
</div>
<div class="src">Vía automática · medianas contra el promedio de todos los documentos del corpus.</div>

<!--
9:30-10:30 · El mismo dato de la lámina anterior, ahora como figura.
Explicar cómo se lee un radar, que no todo el jurado lo tiene claro.
Enseñar el empate ANTES de explicarlo es deliberado: quiero que les extrañe.
No decir todavía que el empate es un error de la herramienta.
-->

---
layout: ac-fact
---

## Los límites de este método

<div class="slide-body">
<div class="text-[1.2rem] max-w-4xl mb-6">Antes de seguir, es importante ser honesto sobre lo que este método sí y no puede hacer.</div>
<div class="grid grid-cols-2 gap-5">
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">Está en desarrollo</div>
    Esta es una primera versión del instrumento. Los seis ejes se siguen afinando, y la medición automática todavía no está validada en su totalidad.
  </div>
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">No sustituye a las personas</div>
    El método automático propone dónde mirar, pero no reemplaza la lectura crítica ni el juicio de un experto humano.
  </div>
  <div class="ac-card p-6 text-[1.05rem]">
    <div class="kicker mb-2">Necesita verificación</div>
    Cada hallazgo que parece interesante — como el empate entre China y Canadá — tiene que confirmarse con otro método antes de tomarse como un resultado firme.
  </div>
  <div class="ac-card-blue p-6 text-[1.05rem]">
    <div class="kicker mb-2">Ni siquiera los jueces coinciden del todo</div>
    El panel de siete lectores alcanzó <strong>α = 0.68</strong> y κ = 0.52 sobre 70 fragmentos: acuerdo aceptable, no alto. La etiqueta humana tampoco es un patrón de oro perfecto.
  </div>
</div>
<div class="mt-6 keyidea text-[1.15rem]">
  <span class="lbl">Por qué esto no le resta valor</span>
  Un instrumento que declara su margen de error se puede usar; uno que promete certeza y no la tiene, no.
</div>
</div>


---
layout: ac-fact
class: src-alto
---

## Lo que esto abre: dónde investigar

<div class="slide-body">
<div class="text-[1.15rem] max-w-5xl mb-5">El método no cierra la pregunta, pero <strong>sí dice dónde buscar</strong>. Señaló a China y Canadá como caso a revisar, y al revisarlo aparecen convergencias reales que la literatura ya documenta.</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-5 text-[1rem]">
    <div class="kicker mb-2">Justificación económica</div>
    Ambos encuadran la educación en IA como <strong>inversión en capital humano</strong> para competitividad, y ambos chocan con el mismo cuello de botella: escasez de docentes calificados frente a mejores salarios en el sector privado.
  </div>
  <div class="ac-card p-5 text-[1rem]">
    <div class="kicker mb-2">Progresión por edad</div>
    Los dos segmentan la enseñanza en las mismas tres etapas siguiendo a la UNESCO: exposición en primaria, experimentación guiada en secundaria, autonomía y diseño de algoritmos en bachillerato. <span class="text-muted">(Boiridy-Graves, 2026)</span>
  </div>
  <div class="ac-card-blue p-5 text-[1rem]">
    <div class="kicker mb-2">Visión docente</div>
    Docentes en formación de Ontario y del suroeste de China comparten un marco <strong>CTSA</strong> y tratan la alfabetización algorítmica como habilidad obligatoria. <span class="text-muted">(Liu, 2022)</span>
  </div>
</div>
<div class="mt-5 keyidea text-[1.1rem]">
  <span class="lbl">Para qué sirve entonces el método</span>
  Para eso sirve un instrumento exploratorio: no probó que China y Canadá se parezcan, <em>dirigió la lectura al lugar donde el parecido resultó estar</em>.
</div>
</div>

<div class="src">Boiridy-Graves, L. (2026, 2 de febrero). Approaches to AI in education: A comparative analysis of policies in Canada, India, and China. <i>McGill Policy Association</i> · Liu, X. M. (2022, 7 de marzo). Nurturing the next-generation AI workforce: A snapshot of AI education in China's public education system. <i>Asia Pacific Foundation of Canada</i>.</div>

---
layout: section
---

<div class="kicker mb-3">Anexos</div>

# Material de respaldo

## Para preguntas del jurado.

---
layout: ac-fact
---

## Anexo · Las dos vías sobre el mismo fragmento

<div class="slide-body">
<div class="ac-callout mb-4 text-[1rem]">
 <span class="kicker block mb-2">China · Circular del Ministerio de Educación sobre educación en IA en primaria y secundaria (教育部办公厅, 2024)</span>
 <div class="mb-2">一是坚持<span class="mark-yellow">立德树人</span>，全面贯彻<span class="mark-yellow">党的教育方针</span>，紧扣新时代新征程教育使命，满足面向未来的创新型人才培养需求。</div>
 <div class="text-muted text-[0.95rem]">«Primero, sostener el <span class="mark-yellow">formar la virtud y formar a la persona</span>, aplicar plenamente la <span class="mark-yellow">política educativa del Partido</span>, ceñirse a la misión educativa de la nueva era y satisfacer la necesidad de formar talento innovador orientado al futuro.»</div>
</div>
<div class="grid grid-cols-2 gap-5">
 <div class="ac-card p-5 text-[0.98rem]">
  <div class="kicker mb-2">Vía A · automática</div>
  El fragmento se vectoriza con el modelo multilingüe y se proyecta sobre el eje 德治↔法. Lo resaltado es lo que empuja la proyección: 立德树人 nombra al Estado como quien <strong>forma el carácter</strong>, no como quien pone reglas.
  <div class="mt-3 font-mono text-[1.4rem] text-blue">+0.85</div>
  <div class="dcap" style="text-align:left">desviaciones sobre el promedio del corpus</div>
 </div>
 <div class="ac-card-blue p-5 text-[0.98rem]">
  <div class="kicker mb-2">Vía B · panel humano</div>
  Siete lectores clasifican el mismo fragmento en una escala de cinco puntos, con un criterio escrito antes de ver los textos.
  <div class="mt-3 font-mono text-[1.4rem] text-blue">6 de 7</div>
  <div class="dcap" style="text-align:left">lo marcaron como «el Estado forma»</div>
 </div>
</div>
<div class="mt-4 keyidea text-[1.05rem]">
  <span class="lbl">Aquí las dos vías coinciden</span>
  El interés está en los fragmentos donde <em>no</em> coinciden: ahí se ve qué mide realmente cada método.
</div>
</div>

<div class="src">China · 教育部办公厅关于加强中小学人工智能教育的通知 (2024). Fragmento del apartado de requisitos generales · puntajes ilustrativos del procedimiento.</div>

---
layout: ac-fact
---

## Anexo · Qué tan de acuerdo estuvieron los jueces

<div class="slide-body">
<div class="text-[1.15rem] max-w-5xl mb-5">Siete lectores clasificaron 70 fragmentos, 490 clasificaciones en total.</div>
<table class="actable">
 <thead><tr><th style="width:46%">Medida</th><th style="width:18%">Valor</th><th>Cómo leerlo</th></tr></thead>
 <tbody>
  <tr><th>Coincidencia exacta</th><td class="yes">82%</td><td class="dim">dos jueces cualesquiera eligen la misma categoría</td></tr>
  <tr><th>Coincidencia ±1 categoría</th><td class="yes">99%</td><td class="dim">casi nunca hay desacuerdos grandes</td></tr>
  <tr><th>Krippendorff α (ordinal)</th><td>0.68</td><td class="dim">aceptable para exploración; por debajo de 0.80</td></tr>
  <tr><th>Fleiss κ</th><td>0.52</td><td class="dim">acuerdo moderado</td></tr>
  <tr><th>α dentro del subgrupo occidental</th><td>0.72</td><td class="dim">más alto que el del panel completo</td></tr>
  <tr><th>κ dentro del subgrupo chino</th><td class="no">0.48</td><td class="dim">más bajo: el criterio no se lee igual en los dos grupos</td></tr>
 </tbody>
</table>
<div class="mt-5 keyidea text-[1.08rem]">
  <span class="lbl">El dato incómodo está en las dos últimas filas</span>
  Que el acuerdo cambie según el origen del juez es, en sí mismo, un hallazgo sobre el instrumento.
</div>
</div>

---
layout: ac-fact
---

## Anexo · Arquitectura técnica

<div class="slide-body">
<table class="actable" style="font-size:0.92rem">
 <thead><tr><th style="width:26%">Componente</th><th style="width:40%">Qué se usó</th><th>Por qué</th></tr></thead>
 <tbody>
  <tr><th>Embeddings (principal)</th><td class="yes">paraphrase-multilingual-MiniLM-L12-v2</td><td class="dim">384 dimensiones · espacio compartido entre idiomas, sin traducir</td></tr>
  <tr><th>Embeddings (alterno)</th><td>text-embedding-3-small <span class="dim">· OpenAI</span></td><td class="dim">contraste, para ver si el resultado depende del modelo</td></tr>
  <tr><th>Almacén vectorial</th><td>ChromaDB <span class="dim">· politicas_ia_educacion_v2</span></td><td class="dim">más dos colecciones: Analectas y bibliografía</td></tr>
  <tr><th>Fragmentación</th><td>800 caracteres · 200 de traslape</td><td class="dim">tope de 80 fragmentos por país, para que ninguno domine</td></tr>
  <tr><th>Modelo juez (Vía B)</th><td class="yes">GPT-4o</td><td class="dim">clasifica siguiendo el mismo criterio escrito que los lectores humanos</td></tr>
  <tr><th>Temas no supervisados</th><td>BERTopic <span class="dim">· UMAP + HDBSCAN</span></td><td class="dim">Fase 1: ver qué temas emergen antes de imponer el marco</td></tr>
 </tbody>
</table>
<div class="mt-5 keyidea text-[1.05rem]">
  <span class="lbl">Lo que hace reproducible el procedimiento</span>
  Los anclajes de los seis ejes se fijaron y se subieron a git <em>antes</em> de correr la medición: el pre-registro es el commit.
</div>
</div>
