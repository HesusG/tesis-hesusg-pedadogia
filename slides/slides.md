---
theme: default
title: "¿Quién forma a las personas?"
info: |
  Defensa de tesis. Maestría en Pedagogía, UPAEP.
  Qué dicen siete países sobre el papel del Estado en la educación en IA,
  y qué pasa cuando intentas medirlo.
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

# ¿Quién forma<br />a las personas?

## Lo que dicen siete países sobre la inteligencia artificial en la escuela, y qué pasó cuando intenté medirlo.

<div class="mt-6 flex gap-3">
  <span class="ac-chip">Tesis de maestría</span>
  <span class="ac-chip">Educación comparada</span>
  <span class="ac-chip">30 min</span>
</div>

<!--
0:00-1:00 · Saludar y arrancar por la pregunta, no por el método.
NO adelantar el resultado. La historia funciona si el jurado llega al tropiezo
conmigo, no si se lo cuento de entrada.
-->

---
layout: statement
---

<div class="max-w-4xl">
  <div class="kicker mb-5">De dónde salió esto</div>
  <div class="text-[1.6rem] leading-snug text-ink">
    Mientras escribía esta tesis, la <strong>SEP</strong> publicó sus diez líneas de acción sobre
    inteligencia artificial generativa, y la <strong>ANUIES</strong> su documento de gobernanza
    de IA para la educación superior.
  </div>
  <div class="mt-8 text-[1.6rem] leading-snug text-ink">
    Las dos hacen lo mismo que haría cualquiera: <em>mirar qué hicieron otros países</em>
    y tomar lo que parece funcionar.
  </div>
  <div class="mt-9 keyidea text-[1.45rem]">
    <span class="lbl">Y ahí me quedé atorado</span>
    Si vas a copiar la política de otro país, ¿cómo sabes qué estás copiando?
  </div>
</div>

<!--
1:00-2:30 · Esta es la lámina de motivación. Decirlo en primera persona.
El préstamo de políticas es la práctica normal en educación comparada
(Steiner-Khamsi). No la critico: pregunto cómo se hace bien.
-->

---

## El problema práctico

<div class="slide-body">
<div class="text-[1.35rem] max-w-4xl">
Cuando uno se sienta a comparar, se topa con que <strong>todos los documentos se parecen</strong>.
Hablan de formar talento, de preparar al país, de ética, de capacitar maestros.
</div>
<div class="mt-7 grid grid-cols-3 gap-5">
  <div class="ac-card p-6 text-[1.15rem]">«Formar talento en inteligencia artificial»</div>
  <div class="ac-card p-6 text-[1.15rem]">«Preparar a la nación para el futuro»</div>
  <div class="ac-card p-6 text-[1.15rem]">«Capacitar a los docentes»</div>
</div>
<div class="mt-8 text-[1.35rem] max-w-4xl">
Ese parecido puede significar tres cosas muy distintas: que un país copió a otro, que los dos
copiaron de la UNESCO, o que llegaron por su cuenta a lo mismo porque enfrentan el mismo
problema. <strong>Leer los documentos uno junto a otro no lo resuelve.</strong>
</div>
</div>
<div class="src">Steiner-Khamsi, G. (2014). Cross-national policy borrowing. Comparative Education, 50(2).</div>

<!--
2:30-4:00 · Sembrar que el parecido superficial es engañoso. Todavía sin método.
-->

---
layout: section
---

<div class="kicker mb-3">Parte 1</div>

# La diferencia que sí importa

## No es de qué hablan. Es de quién hace qué.

---

## Dos frases del mismo tema

<div class="slide-body">
<div class="grid grid-cols-2 gap-6">
  <div class="ac-card p-7">
    <div class="kicker mb-3">Documento A</div>
    <div class="text-[1.3rem]">El Estado <strong>fija el plan</strong>, las escuelas lo aplican, los maestros se capacitan según él, y se mide que la población alcance el nivel esperado.</div>
  </div>
  <div class="ac-card p-7">
    <div class="kicker mb-3">Documento B</div>
    <div class="text-[1.3rem]">El gobierno <strong>financia centros de investigación</strong> y pone reglas de privacidad. Universidades y empresas deciden qué hacer dentro de ellas.</div>
  </div>
</div>
<div class="mt-8 keyidea text-[1.35rem]">
  <span class="lbl">Los dos hablan de formar gente para la IA</span>
  En el primero, el que forma es <em>el Estado</em>. En el segundo, el Estado
  <em>pone el marco</em> y otros forman. Esa diferencia no está en las palabras.
</div>
</div>

<!--
4:00-6:00 · El corazón de la tesis. Que el jurado vea la diferencia ANTES de
que le ponga nombre técnico. Si entienden esta lámina, entienden todo.
Estas dos son descripciones mías, no citas: lo digo en voz alta.
-->

---
layout: ac-split
---

## Esa diferencia ya tiene nombre

::left::

<div class="text-[1.2rem]">
No la inventé. La discusión sobre si la autoridad <strong>forma el carácter</strong> de la gente
o solo <strong>pone reglas</strong> tiene más de dos mil años en la tradición china, y también
atraviesa la teoría política occidental entre el Estado educador y el Estado limitado.
</div>
<div class="mt-6 text-[1.2rem]">
Uso el vocabulario chino por una razón práctica: <em>es el más preciso que encontré</em>.
Distingue las dos cosas con dos palabras, sin rodeos.
</div>

::right::

<div class="ac-card-blue p-6 mb-4">
  <div style="font-family: var(--font-display); font-weight: 800; font-size: 1.9rem; color: var(--ac-blue)">德治 dézhì</div>
  <div class="kicker mt-1 mb-3">Gobernar por la virtud</div>
  <div class="text-[1.08rem]">La autoridad educa con el ejemplo y forma el carácter de los gobernados.</div>
</div>
<div class="ac-card p-6">
  <div style="font-family: var(--font-display); font-weight: 800; font-size: 1.9rem; color: var(--ac-ink)">法 fǎ</div>
  <div class="kicker mt-1 mb-3">Gobernar por la norma</div>
  <div class="text-[1.08rem]">La autoridad pone reglas iguales para todos, y esas reglas también la limitan a ella.</div>
</div>
<div class="src">Pines, Y. (2023). Legalism in Chinese Philosophy. Stanford Encyclopedia of Philosophy.</div>

<!--
6:00-8:00 · Justificar POR QUÉ un marco chino y no uno occidental: por precisión
del vocabulario, no por exotismo. Y aclarar que se aplica igual a los siete
países, no solo a China. Eso desarma la acusación de esencializar.
-->

---
layout: statement
dark: true
---

<div class="max-w-4xl">
  <div class="kicker mb-4">En pocas palabras, esto hice</div>
  <div class="text-[1.75rem] leading-snug" style="color: rgba(255,255,255,0.95)">
    Tomé <strong>siete políticas nacionales</strong> de inteligencia artificial en educación,
    una por región del mundo.
  </div>
  <div class="mt-6 text-[1.75rem] leading-snug" style="color: rgba(255,255,255,0.95)">
    Le puse a cada párrafo una <strong>calificación del −2 al +2</strong> según si presenta al
    Estado formando personas o poniendo límites.
  </div>
  <div class="mt-6 text-[1.75rem] leading-snug" style="color: rgba(255,255,255,0.95)">
    Y como no me fiaba de mi propia regla, <span class="text-yellow">la apliqué dos veces,
    con dos métodos que no se parecen en nada.</span>
  </div>
</div>

<!--
8:00-9:00 · La lámina que faltaba. Si el jurado se distrae y vuelve, con esta
se reengancha. Decirla despacio, es la tesis en tres frases.
-->

---
layout: ac-fact
---

## La regla de medir

<div class="slide-body">
<table class="actable">
  <thead><tr><th style="width:10%">Valor</th><th style="width:42%">Qué tiene que decir el párrafo</th><th>Ejemplo del tipo de frase</th></tr></thead>
  <tbody>
    <tr><th class="text-blue">+2</th><td>El Estado dirige la formación moral de la gente</td><td class="dim">«elevar la calidad moral y científica de la nación»</td></tr>
    <tr><th>+1</th><td>El Estado planea y exige alineamiento, sin hablar de valores</td><td class="dim">«todas las escuelas incorporarán el plan»</td></tr>
    <tr><th>0</th><td>El párrafo no habla de la relación entre el poder y la persona</td><td class="dim">«se destinarán 125 millones al programa»</td></tr>
    <tr><th>−1</th><td>Hay lógica de derechos, pero de lado</td><td class="dim">«los proveedores deben proteger datos»</td></tr>
    <tr><th>−2</th><td>Los derechos limitan al propio Estado, y se pueden exigir</td><td class="dim">«el gobierno no interferirá con la libertad de expresión»</td></tr>
  </tbody>
</table>
<div class="mt-6 keyidea text-[1.2rem]">
  <span class="lbl">El cero no es «neutro», es «no aplica»</span>
  La mayoría de los párrafos de una política pública hablan de presupuesto, plazos y
  organigramas. Esos van a cero, y está bien.
</div>
</div>

<!--
9:00-11:00 · Explicar la escala con ejemplos, no con la definición formal.
Insistir en el cero: el jurado va a preguntar por qué Canadá dio cero, y esta
lámina ya deja puesta la respuesta.
-->

---
layout: ac-diagram
---

## Las dos formas de medir

<div class="slide-body">
<div class="diagram">
  <div class="drow" style="gap: 3rem">
    <div class="dcol">
      <span class="dchip">MÉTODO 1</span>
      <div class="dbox"><div class="dt">La computadora compara</div><div class="ds">convierte el texto en números<br />y mide qué tan parecido es<br /><span class="dneg">no lee: calcula distancias</span></div></div>
    </div>
    <div class="dcol">
      <span class="dchip dchip-hi">MÉTODO 2</span>
      <div class="dbox dbox-hi"><div class="dt">Siete lectores automáticos</div><div class="ds">cada uno lee el párrafo con la regla<br />en la mano y pone su calificación<br /><span style="color:var(--ac-inkblue)">4 hechos en China, 3 en Occidente</span></div></div>
    </div>
  </div>
  <div class="darrow-down-dot"></div>
  <div class="dsum" style="max-width: 62ch">
    Si los dos dan lo mismo, la medición es creíble.<br />
    Si dan cosas distintas, algo falla, y el desacuerdo dice dónde.
  </div>
</div>
</div>

<!--
11:00-13:00 · Traducir sin jerga: "embeddings" = la computadora convierte texto
en números; "panel de jueces" = siete lectores automáticos.
Explicar por qué 4 chinos y 3 occidentales: para poder revisar si el origen del
lector cambia la calificación. Es un control, no adorno.
-->

---

## Por qué siete lectores y no uno

<div class="slide-body">
<div class="grid grid-cols-[1.15fr_1fr] gap-8 items-start">
  <div>
    <div class="text-[1.2rem]">Igual que en una encuesta a expertos: <strong>ninguno es infalible</strong>, y por eso se
    pregunta a varios. Lo que vale no es el juicio de uno, sino que coincidan.</div>
    <div class="mt-6 text-[1.2rem]">Los puse a leer <strong>diez párrafos por país</strong>, siempre sobre el mismo tema, para que
    la comparación fuera justa entre un documento largo y uno corto.</div>
    <div class="mt-6 ac-callout text-[1.1rem]">
      Cada lector deja escrito <strong>por qué</strong> puso esa calificación. Las 1,120 lecturas,
      con su justificación, están guardadas y cualquiera puede revisarlas.
    </div>
  </div>
  <div>
    <div class="kicker mb-3">Y sí coincidieron</div>
    <table class="actable">
      <tbody>
        <tr><th>Dieron exactamente lo mismo</th><td class="yes">83%</td></tr>
        <tr><th>Se separaron como mucho un punto</th><td class="yes">99%</td></tr>
        <tr><th>Se contradijeron de fondo</th><td class="dim">casi nunca</td></tr>
      </tbody>
    </table>
    <div class="mt-4 text-[1.05rem] text-muted">Ese 99% es el dato importante: nunca pasó que uno leyera «el Estado forma» y otro «el Estado se limita» en el mismo párrafo.</div>
  </div>
</div>
</div>

<!--
13:00-15:00 · Aquí va el acuerdo entre jueces, pero en castellano.
Si preguntan por los índices formales (Fleiss, Krippendorff) están en el anexo:
alfa ordinal 0.697, arriba del umbral de 0.667. No los pongo en la línea
principal porque el público es de pedagogía.
-->

---
layout: section
---

<div class="kicker mb-3">Parte 2</div>

# Qué salió

---

## China se separa. Los demás no.

<div class="slide-body">
<BarrasPais />
<div class="mt-2 text-[1.05rem] text-muted">Cada línea negra es el margen de error. Cuando dos líneas no se tocan, la diferencia es real y no del azar. Los seis de abajo son indistinguibles entre sí.</div>
</div>
<div class="src">Siete lectores × diez párrafos × siete países = 490 lecturas.</div>

<!--
15:00-17:00 · Leer la gráfica en voz alta, no darla por obvia.
China arriba y su margen no toca a nadie. Estados Unidos abajo: su plan de 2025
saca al Estado de la conducción a propósito.
Canadá en cero exacto: NO decir todavía por qué. Se explica en la parte 3.
-->

---
layout: ac-fact
---

## Antes de celebrar, tres explicaciones aburridas

<div class="slide-body">
<div class="text-[1.2rem] mb-5 max-w-5xl">China puede salir alto por razones que no tienen nada que ver con lo que quiero medir. Probé las tres que se me ocurrieron, con documentos de otros países.</div>
<table class="actable">
  <thead>
    <tr><th style="width:26%">¿Y si es...?</th><th style="width:36%">Entonces debería pasar</th><th>Qué pasó</th></tr>
  </thead>
  <tbody>
    <tr><th>...cosa de Asia</th><td class="dim">Corea, Japón y Singapur también suben</td><td><span class="no">No subieron.</span> Japón dio cero exacto</td></tr>
    <tr><th>...cosa del tema</th><td class="dim">Los documentos educativos de otros países suben</td><td><span class="no">No subieron.</span> El de la UNESCO se fue al otro lado</td></tr>
    <tr><th>...cosa de China</th><td class="dim">Todo lo chino sube por igual</td><td class="dim">Tampoco. Su plan de IA <em>general</em> da mucho menos</td></tr>
  </tbody>
</table>
<div class="mt-6 keyidea text-[1.2rem]">
  <span class="lbl">Lo que queda</span>
  No es la región, ni el tema, ni China en bloque. Es <strong>China cuando habla de educación</strong>.
  Su plan general da +0.26; su plan educativo, +0.94.
</div>
</div>

<!--
17:00-19:00 · Este es el argumento fuerte y hay que darle tiempo.
La conclusión NO es "China es autoritaria". Es que el lenguaje de formar
personas aparece justo donde la teoría confuciana dice que debe aparecer:
en la educación. Es una prueba de que el instrumento mide lo que dice medir.
-->

---

## El cabo suelto que dejo declarado

<div class="slide-body">
<div class="grid grid-cols-[1.1fr_1fr] gap-8 items-center">
  <div>
    <div class="text-[1.2rem]">Faltaba una cuarta explicación: <strong>¿y si es la forma de gobierno?</strong> China es un
    Estado de partido único. Vietnam también, y además comparte la herencia cultural.
    Era el caso que decidía.</div>
    <div class="mt-6 text-[1.2rem]">Vietnam salió en <strong>+0.20</strong>. Más alto que los países liberales, sí.
    Pero <em>igual que Corea del Sur</em>, que no es Estado de partido único.</div>
    <div class="mt-6 ac-callout text-[1.1rem]">
      La prueba necesitaba dos condiciones y solo se cumplió una.
      <strong>No puedo concluir nada sobre la forma de gobierno.</strong> Queda abierto.
    </div>
  </div>
  <div>
    <table class="actable">
      <tbody>
        <tr><th>China, educación</th><td class="yes">+0.94</td></tr>
        <tr><th>China, plan general</th><td>+0.26</td></tr>
        <tr><th>Corea del Sur</th><td>+0.20</td></tr>
        <tr><th>Vietnam</th><td>+0.20</td></tr>
        <tr><th>Malasia</th><td class="dim">+0.13</td></tr>
        <tr><th>Japón</th><td class="dim">0.00</td></tr>
        <tr><th>UNESCO</th><td class="dim">−0.16</td></tr>
      </tbody>
    </table>
  </div>
</div>
</div>

<!--
19:00-20:30 · Contar un resultado que NO salió es lo que hace creíble a los que
sí salieron. Si un sinodal iba a preguntar por Vietnam, ya está contestado.
-->

---
layout: section
---

<div class="kicker mb-3">Parte 3</div>

# El tropiezo

## Aquí es donde la tesis dejó de ser sobre China.

---

## Los dos métodos no dijeron lo mismo

<div class="slide-body">
<div class="grid grid-cols-[1fr_1.05fr] gap-8 items-center">
  <div>
    <table class="actable">
      <thead><tr><th></th><th class="text-right">Computadora</th><th class="text-right">Lectores</th></tr></thead>
      <tbody>
        <tr><th>China</th><td style="text-align:right">+0.90</td><td style="text-align:right" class="yes">+0.94</td></tr>
        <tr><th>Canadá</th><td style="text-align:right">+0.88</td><td style="text-align:right">0.00</td></tr>
        <tr><th>Diferencia</th><td style="text-align:right" class="dim">0.02</td><td style="text-align:right" class="dim">0.94</td></tr>
      </tbody>
    </table>
    <div class="mt-6 text-[1.2rem]">Para la computadora, los documentos de China y Canadá son
    <em>prácticamente el mismo texto</em>. Para los lectores, están en extremos opuestos.</div>
  </div>
  <div class="keyidea text-[1.3rem]">
    <span class="lbl">Mi primera reacción</span>
    Pensé que el error estaba en los lectores. Así que fui a leer el documento
    canadiense yo mismo, párrafo por párrafo.
  </div>
</div>
</div>

<!--
20:30-22:00 · Contarlo como me pasó: creí que había un bug. La siguiente lámina
es el giro. No adelantarlo.
-->

---
layout: statement
dark: true
---

<div class="max-w-4xl">
  <div class="kicker mb-4">Lo que encontré al abrirlo</div>
  <div class="font-display font-800 leading-none" style="font-size: 2.7rem">
    No era una política.<br />
    <span class="text-yellow">Era una página web guardada en PDF.</span>
  </div>
  <div class="mt-8 text-[1.3rem]" style="color: rgba(255,255,255,0.9)">
    Con la fecha de captura arriba, el menú de navegación, la lista del consejo asesor
    con los cargos de cada miembro, un botón de <strong>«Donate Now»</strong> y el pie para
    suscribirse al boletín.
  </div>
  <div class="mt-7 text-[1.3rem]" style="color: rgba(255,255,255,0.9)">
    De los diez párrafos que se midieron, <strong>cinco eran eso</strong>.
  </div>
</div>

<!--
22:00-23:30 · El giro de la historia. Pausa después de decirlo.
Ser explícito en que es un error MÍO de armado del corpus, no de nadie más.
Reconocerlo antes de que lo encuentren vale más que esconderlo.
-->

---
layout: ac-fact
---

## Primera reacción: ¿y si el error es mío?

<div class="slide-body">
<div class="grid grid-cols-2 gap-6">
  <div class="ac-card p-7">
    <div class="kicker mb-3">Los siete lectores</div>
    <div class="text-[1.2rem]">Leyeron una lista de miembros del consejo asesor y pusieron <strong>cero</strong>.</div>
    <div class="mt-3 text-[1.1rem] text-muted">Que es exactamente lo correcto: ese párrafo no habla del poder ni de las personas.</div>
  </div>
  <div class="ac-card-blue p-7">
    <div class="kicker mb-3">La computadora</div>
    <div class="text-[1.2rem]">Leyó lo mismo y le puso <strong>+0.88</strong>, casi idéntico al plan educativo chino.</div>
    <div class="mt-3 text-[1.1rem] text-muted">Vio las palabras «inteligencia artificial», «talento», «nacional», «liderazgo» y concluyó parecido.</div>
  </div>
</div>
<div class="mt-8 keyidea text-[1.3rem]">
  <span class="lbl">Pero esto no prueba nada todavía</span>
  Con un documento malo, cualquiera puede fallar. La pregunta de verdad era otra:
  <em>¿el empate desaparece si comparo dos políticas reales?</em>
</div>
</div>

<!--
23:30-25:00 · Resistir la tentación de cantar victoria aquí. Un critico diria,
con razon, que el metodo fallo porque el dato era basura. Hay que ir a ver.
-->

---
layout: statement
---

<div class="max-w-4xl">
  <div class="kicker mb-5">Lo que hice entonces</div>
  <div class="text-[1.55rem] leading-snug text-ink">
    Busqué la estrategia oficial de Canadá. Existe, y es reciente:
    <strong>«AI for All»</strong>, firmada por el Ministro de Innovación, Ciencia e Industria
    el <strong>4 de junio de 2026</strong>. Cincuenta páginas, con ISBN.
  </div>
  <div class="mt-7 text-[1.55rem] leading-snug text-ink">
    Cambié el documento y <em>volví a correr todo</em>. Canadá pasó de 15 a 210 párrafos.
  </div>
  <div class="mt-8 keyidea text-[1.4rem]">
    <span class="lbl">La pregunta</span>
    ¿Sigue la computadora sin poder distinguir a Canadá de China?
  </div>
</div>

<!--
25:00-26:00 · Momento de suspenso corto. No adelantar.
-->

---
layout: ac-fact
---

## Sí. El empate aguanta.

<div class="slide-body">
<table class="actable">
  <thead><tr><th style="width:34%"></th><th class="text-right" style="width:22%">Antes<br /><span class="dim">página web</span></th><th class="text-right" style="width:22%">Ahora<br /><span class="dim">estrategia real</span></th><th>Qué pasó</th></tr></thead>
  <tbody>
    <tr><th>Canadá, computadora</th><td style="text-align:right">+0.88</td><td style="text-align:right">+0.78</td><td class="dim">Bajó poco</td></tr>
    <tr><th>Canadá, lectores</th><td style="text-align:right">0.00</td><td style="text-align:right">−0.06</td><td class="dim">Sigue en el grupo del cero</td></tr>
    <tr><th>Distancia con China, computadora</th><td style="text-align:right">0.02</td><td style="text-align:right">0.07</td><td><span class="no">Empate, igual que antes</span></td></tr>
    <tr><th>Distancia con China, lectores</th><td style="text-align:right">0.94</td><td style="text-align:right" class="yes">1.00</td><td><span class="yes">Un punto entero</span></td></tr>
  </tbody>
</table>
<div class="mt-7 keyidea text-[1.3rem]">
  <span class="lbl">Este es el resultado, ya sin excusas</span>
  Una estrategia nacional de cincuenta páginas frente al plan educativo chino.
  La computadora <em>sigue sin poder separarlos</em>. Los lectores los separan por un punto completo.
</div>
</div>

<!--
26:00-28:00 · La lamina mas importante de la defensa. El hallazgo ya no depende
de un documento defectuoso: aguanta con dos politicas de verdad.
Decir tambien lo que SI cambio: de los seis valores, tres dejaron de empatar.
El que sigue empatado es justo el que mide gobernar por la virtud.
-->

---

## Por qué pasa, en una frase

<div class="slide-body">
<div class="text-[1.5rem] max-w-5xl leading-snug">
El método automático mide <strong>de qué habla</strong> un texto.
</div>
<div class="mt-5 text-[1.5rem] max-w-5xl leading-snug">
Lo que yo quería medir es <em>quién hace qué a quién</em>.
</div>
<div class="mt-9 text-[1.25rem] max-w-4xl text-muted">
Las dos cosas se parecen lo suficiente como para confundirse, y son distintas.
«El Estado formará a los estudiantes» y «se formará a especialistas del Estado»
tienen casi las mismas palabras y dicen cosas opuestas. Un lector lo nota
en la primera lectura. Un método que promedia palabras, no.
</div>
</div>

<!--
25:00-26:00 · La explicación mecánica. Corta y en voz alta.
-->

---
layout: section
---

<div class="kicker mb-3">Parte 4</div>

# Qué significa esto

---
layout: ac-fact
---

## Para tres públicos distintos

<div class="slide-body">
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-6">
    <div class="kicker mb-3">Para quien hace política</div>
    <div class="text-[1.12rem]">Copiar una política porque «dice lo mismo que la nuestra» es copiar a ciegas.
    La pregunta previa es <strong>quién forma a quién</strong>, y no está en el vocabulario.</div>
  </div>
  <div class="ac-card-blue p-6">
    <div class="kicker mb-3">Para quien investiga</div>
    <div class="text-[1.12rem]">La herramienta de moda para comparar documentos en varios idiomas
    <strong>no mide lo que uno cree</strong> cuando lo que importa es el papel de cada actor.</div>
  </div>
  <div class="ac-card p-6">
    <div class="kicker mb-3">Para México</div>
    <div class="text-[1.12rem]">SEP y ANUIES están escribiendo ahora. Vale la pena preguntarse
    qué papel le estamos dando al Estado, <strong>antes</strong> de tomar prestado de nadie.</div>
  </div>
</div>
<div class="mt-8 keyidea text-[1.25rem]">
  <span class="lbl">Y una advertencia para mí mismo</span>
  Si el método automático hubiera sido el único, habría publicado que
  <em>Canadá y China piensan casi igual</em> sobre el papel del Estado en la educación.
  Con un número, un intervalo y una gráfica bonita.
</div>
</div>

<!--
26:00-27:30 · El "y qué". Tres públicos, uno por columna.
La advertencia final es la que da la lección metodológica sin sermonear.
-->

---
layout: ac-fact
---

## Lo que no puedo afirmar

<div class="slide-body">
<table class="actable">
  <thead><tr><th style="width:26%">Límite</th><th>Qué significa</th></tr></thead>
  <tbody>
    <tr><th>El corpus se me coló</th><td>Un documento defectuoso llegó hasta el análisis final. Ya está sustituido y la medición repetida, pero lo detectó el desacuerdo entre métodos, no mi revisión del corpus. Hace falta un chequeo automático de ruido de página web antes de cada corrida</td></tr>
    <tr><th>Nadie humano revisó</th><td>Los siete lectores son automáticos. Que coincidan entre sí dice que son <strong>consistentes</strong>, no que tengan razón</td></tr>
    <tr><th>Documentos, no aulas</th><td>Mido lo que un Estado <strong>escribe</strong>. No lo que hace, ni lo que pasa con los estudiantes</td></tr>
    <tr><th>Siete casos</th><td>Elegidos uno por región. No permiten generalizar a todos los países del mundo</td></tr>
  </tbody>
</table>
</div>

<!--
27:30-29:00 · Decir los límites yo, antes que ellos. Empezar por Canadá,
que es el más incómodo, es lo que da credibilidad al resto.
-->

---

## Lo que sigue, con nombre y costo

<div class="slide-body">
<div class="grid grid-cols-[1.1fr_1fr] gap-8 items-center">
  <div>
    <div class="text-[1.25rem]">La falta más seria es que <strong>ningún humano calificó nada</strong>.
    Eso tiene solución conocida y barata.</div>
    <div class="mt-6 keyidea">
      <span class="lbl">Concretamente</span>
      Que <em>dos personas</em> califiquen a mano unos <em>50 párrafos</em> al azar,
      con la misma regla, y usar eso para corregir a los lectores automáticos.
    </div>
    <div class="mt-6 text-[1.15rem] text-muted">Es la diferencia entre decir «esto es lo que observé»
    y poder decir «esto es lo que pasa». Semanas de trabajo, no meses.</div>
  </div>
  <div>
    <div class="kicker mb-3">Pendientes, en orden</div>
    <ul class="text-[1.1rem]">
      <li>Calificación humana de 50 párrafos</li>
      <li>Actualizar Australia y Sudáfrica, que ya tienen versión nueva</li>
      <li>Medir los otros cinco valores con los dos métodos</li>
    </ul>
  </div>
</div>
</div>
<div class="src">Egami, Hinck, Stewart y Wei (2023). Design-based supervised learning. NeurIPS.</div>

---
layout: statement
dark: true
---

<div class="max-w-4xl">
  <div class="kicker mb-4">Para cerrar</div>
  <div class="font-display font-800 leading-none" style="font-size: 2.9rem">
    Empecé preguntando qué dicen siete países<br />
    sobre quién forma a las personas.
  </div>
  <div class="mt-8 text-[1.4rem]" style="color: rgba(255,255,255,0.9)">
    Encontré que <strong>sí se puede medir</strong>, que China se separa de forma clara,
    y que el lugar donde se separa es justo donde la teoría decía.
  </div>
  <div class="mt-6 text-[1.4rem]" style="color: rgba(255,255,255,0.9)">
    Y encontré algo que no buscaba: <span class="text-yellow">que la herramienta con la que hoy
    se comparan políticas no distingue quién forma a quién.</span> Lo descubrí por un documento
    defectuoso, lo comprobé con dos políticas de verdad.
  </div>
  <div class="mt-10 kicker">Hesus García Cobos · Maestría en Pedagogía · UPAEP 2026</div>
</div>

<!--
29:00-30:00 · Cerrar volviendo a la pregunta del principio. Agradecimientos
en voz alta, no en lámina.
-->

---
layout: section
---

<div class="kicker mb-3">Anexos</div>

# Material de respaldo

## Para preguntas del jurado.

---
layout: ac-fact
---

## Anexo · Los números formales del acuerdo

<div class="slide-body">
<div class="grid grid-cols-2 gap-6">
  <table class="actable">
    <thead><tr><th colspan="2">Acuerdo entre los siete lectores</th></tr></thead>
    <tbody>
      <tr><th>Coincidencia exacta</th><td>0.817</td></tr>
      <tr><th>Dentro de ±1 punto</th><td>0.991</td></tr>
      <tr><th>Kappa de Fleiss</th><td>0.522</td></tr>
      <tr><th>Alfa de Krippendorff, ordinal</th><td class="yes">0.681</td></tr>
      <tr><th>Umbral convencional</th><td class="dim">0.667</td></tr>
    </tbody>
  </table>
  <table class="actable">
    <thead><tr><th colspan="2">¿Sesga el origen del lector?</th></tr></thead>
    <tbody>
      <tr><th>Lectores occidentales</th><td>+0.076</td></tr>
      <tr><th>Lectores chinos</th><td>+0.029</td></tr>
      <tr><th>Diferencia</th><td>+0.048</td></tr>
      <tr><th>Margen de error</th><td class="dim">[−0.012, +0.111] · <strong>incluye el cero</strong></td></tr>
      <tr><th>Correlación entre ambos grupos</th><td>0.898</td></tr>
    </tbody>
  </table>
</div>
<div class="mt-5 text-[1.05rem] text-muted">
El margen de error incluye el cero, así que <strong>no se puede afirmar que haya sesgo</strong>. Y si lo hay,
va al revés de lo esperado: son los lectores occidentales, no los chinos, quienes califican más alto
en el polo confuciano. Los dos grupos ordenan los párrafos casi igual.
</div>
<div class="mt-3 text-[1.05rem] text-muted">
El kappa (0.522) sale bajo comparado con el 82% de coincidencia porque castiga que casi todos
los párrafos caigan en cero. Es un artefacto conocido, no una falla de la medición.
</div>
</div>

---
layout: ac-fact
---

## Anexo · Los seis valores, no solo uno

<div class="slide-body">
<div class="flex items-center justify-center">
  <RadarConfucio :paises="['china','canada']" />
</div>
<div class="mt-3 text-center text-[1.05rem] text-muted">
China frente a Canadá con el método automático, ya con la estrategia canadiense real. Tres de los seis empatan: ritual, cultivo de sí y virtud/norma.
</div>
</div>
<div class="src">Método 1 · medianas contra el promedio de todos los documentos del corpus.</div>

---
layout: ac-fact
---

## Anexo · El corpus

<div class="slide-body">
<table class="actable">
  <thead><tr><th>País</th><th>Documentos</th><th>Fragmentos</th><th>Estado</th></tr></thead>
  <tbody>
    <tr><th>China</th><td>9</td><td>271</td><td class="yes">Válido</td></tr>
    <tr><th>Sudáfrica</th><td>1</td><td>1,303</td><td class="dim">Válido; hay versión más nueva</td></tr>
    <tr><th>Colombia</th><td>1</td><td>764</td><td class="yes">Válido, reemplazado durante el estudio</td></tr>
    <tr><th>Alemania</th><td>1</td><td>230</td><td class="yes">Válido</td></tr>
    <tr><th>Australia</th><td>1</td><td>161</td><td class="dim">Válido; hay versión más nueva</td></tr>
    <tr><th>Estados Unidos</th><td>1</td><td>156</td><td class="yes">Válido, reemplazado durante el estudio</td></tr>
    <tr><th>Canadá</th><td>1</td><td>210</td><td class="yes">Sustituido durante el estudio</td></tr>
  </tbody>
</table>
<div class="mt-5 text-[1.05rem] text-muted">
Tres de los siete documentos originales tuvieron que sustituirse. Estados Unidos y Colombia
porque estaban derogados; Canadá porque no era la estrategia sino una página web, y eso se
detectó al final, al investigar por qué los dos métodos no coincidían.
</div>
</div>

---
layout: ac-fact
---

## Anexo · La objeción de fondo al eje

<div class="slide-body">
<div class="ac-callout mb-6 text-[1.15rem]">
  <strong>La objeción.</strong> La doctrina oficial china sostiene que gobernar por la ley y
  gobernar por la virtud son <em>complementarios</em>, no opuestos. Xi Jinping lo dijo así
  en 2018. Mi escala los pone en extremos contrarios.
</div>
<div class="grid grid-cols-3 gap-5">
  <div class="ac-card p-5">
    <div class="kicker mb-2">Respuesta 1</div>
    <div class="text-[1.08rem]">La escala no mide qué cree un Estado. Mide cómo aparece el ciudadano en el párrafo: como alguien a quien se forma, o como alguien con límites que puede exigir.</div>
  </div>
  <div class="ac-card-blue p-5">
    <div class="kicker mb-2">Respuesta 2</div>
    <div class="text-[1.08rem]">Si fueran complementarios, los textos jurídicos chinos deberían dar cerca de cero y los educativos alto. <strong>Es justo lo que pasó.</strong> La objeción predice mi resultado.</div>
  </div>
  <div class="ac-card p-5">
    <div class="kicker mb-2">Respuesta 3</div>
    <div class="text-[1.08rem]">La escala necesita dos extremos para funcionar. Que el instrumento los oponga no significa que China los oponga.</div>
  </div>
</div>
</div>

<!--
Si un sinodal con formación en derecho chino levanta la mano, esta es la lámina.
La respuesta 2 es la fuerte: la objeción, si es cierta, predice el patrón observado.
-->

---
layout: ac-fact
---

## Anexo · Las cuatro predicciones, escritas antes de medir

<div class="slide-body">
<table class="actable">
  <thead><tr><th style="width:8%"></th><th style="width:50%">Lo que predije</th><th>Qué pasó</th></tr></thead>
  <tbody>
    <tr><th>1</th><td class="dim">China sale más alto que los países liberales</td><td class="yes">Se cumplió</td></tr>
    <tr><th>2</th><td class="dim">No es cosa de la región</td><td class="yes">Se cumplió</td></tr>
    <tr><th>3</th><td class="dim">El origen del lector no cambia la calificación</td><td class="yes">Se sostiene</td></tr>
    <tr><th>4</th><td class="dim">Los dos métodos coinciden</td><td class="no">Falló</td></tr>
  </tbody>
</table>
<div class="mt-6 keyidea text-[1.2rem]">
  <span class="lbl">Por qué importa que estuvieran escritas antes</span>
  Quedaron con fecha en el repositorio, junto con la regla de medir, <em>antes</em> de correr nada.
  Cualquiera puede comprobar que no ajusté el método al resultado que quería.
</div>
</div>
