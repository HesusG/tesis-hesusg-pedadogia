# Descargas pendientes: lista única

Consolida lo que estaba disperso en `bibliografia-pendiente.md` y `lista-busqueda-jstor.md` más lo que salió de la segunda investigación. **Ordenada por prioridad, no por tema.**

**Cobertura del `.bib`: 68 de 93 (73%).** Verificar con `make refs-audit`.

> **Nota sobre el audit.** Los diez PDF del bloque 0 están en `references/` pero **no** en `document/referencias.bib`, por decisión: el `.bib` debe reflejar lo que la tesis realmente cita. Por eso `make refs-audit` los reportará como archivos huérfanos. Es el comportamiento esperado, no un error. Cuando cites uno, le creas su entrada.

---

## Bloque 0 · Ya descargados y verificados

No tienes que hacer nada con estos. Están en `references/`, se comprobó que son PDF reales, con más de una página y con el título del texto extraído coincidiendo con la referencia.

| Archivo | Qué es | Para qué te sirve |
|---|---|---|
| `lmpanel2026rater_…` | Gara (2026), panel de modelos como evaluadores | **El precedente de tu diseño.** α=0.86 y la advertencia de que acuerdo no es validez |
| `halterman2025codebook_…` | Halterman y Keith, *Political Analysis* | **La objeción más fuerte contra tu Vía B** |
| `gilardi2023chatgpt_…` | Gilardi et al., *PNAS* | El apoyo canónico para anotar con modelos |
| `tornberg2024best_…` | Törnberg, buenas prácticas | Justifica tu nivel de documentación |
| `egami2023dsl_…` | Egami et al., NeurIPS | **El método para pasar de descriptivo a inferencia válida** |
| `llmhacking2025_…` | Riesgos ocultos de anotar con LLM | Por qué tu caché y tu log importan |
| `silicon2024_…` | Reproducibilidad en anotación | Mismo uso |
| `validating2026_…` | Amenazas epistémicas y normas emergentes | Capítulo de límites |
| `proxy2026presumption_…` | De embeddings a medidas sociales válidas | Marco teórico de tu Vía A |
| `ziems2023can_…` | Ziems et al., LLM y ciencia social computacional | Panorama general |

---

## Bloque 1 · Prioridad alta: lo que sostiene argumentos que ya escribiste

Estos cinco cambian lo que puedes afirmar. Bájalos primero.

| # | Referencia | Dónde | Guardar como |
|---|---|---|---|
| 1 | **Bareis y Katzenbach (2022)**, *Talking AI into Being*, ST&HV | [doi.org/10.1177/01622439211030007](https://doi.org/10.1177/01622439211030007) · SAGE | `bareis2022talking_talking-ai-into-being.pdf` |
| 2 | **Angle, S. (2010)**, *Debating the Rule of Law and Virtue Politics* | SSRN, id 1644571. La descarga directa devuelve HTML; entra a la página y usa el botón | `angle2010debating_rule-of-law-virtue-politics.pdf` |
| 3 | **Törnberg (2025)**, *LLMs Outperform Expert Coders*, SSCR | [doi.org/10.1177/08944393241286471](https://doi.org/10.1177/08944393241286471) · SAGE | `tornberg2025llms_outperform-expert-coders.pdf` |
| 4 | **Ball (1998)**, *Big Policies/Small World*, Comparative Education | [doi.org/10.1080/03050069828225](https://doi.org/10.1080/03050069828225) · T&F o JSTOR | `ball1998big_big-policies-small-world.pdf` |
| 5 | **Holmes et al. (2022)**, *State of the art in AI and education* | [doi.org/10.1111/ejed.12533](https://doi.org/10.1111/ejed.12533) · Wiley | `holmes2022state_state-of-the-art-ai-education.pdf` |

**Por qué el 1 es el primero de todos.** Es el trabajo que más te respalda, ya está en tu `.bib` sin PDF, y te da la frase de posicionamiento de la tesis: ellos observaron cualitativamente que las narrativas de las estrategias de IA convergen, tú lo mides y muestras dónde exactamente se rompe el método superficial.

---

## Bloque 2 · Artículos con DOI que siguen faltando

| Referencia | DOI | Guardar como |
|---|---|---|
| Gulson y Webb (2019), *Digitizing education policy* | 10.1177/0263775818813144 | `gulson2019digitizing_digitizing-education-policy.pdf` |
| Mishra y Koehler (2006), TPACK | 10.1111/j.1467-9620.2006.00684.x | `mishra2006technological_tpack.pdf` |

Mishra **no tiene versión abierta** según Unpaywall. Es un clásico muy citado que circula en repositorios de autor: búscalo por título en Google Scholar y usa el enlace de la derecha.

---

## Bloque 3 · Sinología: la brecha de la premisa

En 93 entradas del `.bib` no hay **ninguna** fuente de filosofía china, y el códebook de dézhì se apoya hoy en un panel de modelos. Esta es la brecha más seria que queda.

| Referencia | Tipo | Nota |
|---|---|---|
| **Stanford Encyclopedia of Philosophy**, entrada "Confucius" | Acceso abierto | [plato.stanford.edu/entries/confucius/](https://plato.stanford.edu/entries/confucius/). Gratis, revisada por pares. **Empieza por aquí.** |
| **El Amine, L.**, *Classical Confucian Political Thought* | Libro, Princeton UP | Reconstrucción del pensamiento político clásico |
| **Kim, S.**, *Theorizing Confucian Virtue Politics* | Libro, Cambridge UP | Mencio y Xunzi |
| **Elman, B. (2000)**, *A Cultural History of Civil Examinations in Late Imperial China* | Libro, UC Press | El antecedente histórico de tu interacción país por tema |
| **Elman y Woodside (eds.)**, *Education and Society in Late Imperial China, 1600-1900* | Libro | Complemento |
| *Philosophy East and West* | Revista en JSTOR | Buscar: `rule by virtue`, `dezhi`, `moral cultivation state` |
| *Dao: A Journal of Comparative Philosophy* | Revista | Buscar: `Confucian education`, `self-cultivation` |
| **Tu Weiming**; **Daniel A. Bell** | Por autor | Humanismo confuciano moderno y meritocracia política |

---

## Bloque 4 · Documentos de política que faltan como PDF

No son artículos y no necesitan JSTOR. De varios ya tienes el texto plano en el repositorio; falta el PDF para el archivo bibliográfico.

| Clave | Qué es | Dónde |
|---|---|---|
| `china2017ai` | Plan de IA de Nueva Generación 2017 | Texto en `policies/raw/china/3_new_gen_ai_development_plan_2017_en.txt` |
| `southafrica2020pc4ir` | Reporte PC4IR de Sudáfrica | Texto en `policies/processed/sudafrica_4ir_2020.txt` |
| `germany2018aistrategy` | KI-Strategie 2018 | bundesregierung.de |
| `estonia2019krattai` | Estrategia Kratt de Estonia | kratid.ee |
| `anuies2024gobernanza`, `mexia2025centro`, `sep2026ia` | Documentos mexicanos | ANUIES, IA-MX, SEP |

**Además, del corpus (ver `docs/corpus-objetivo.md`):** Australia (National AI Plan, dic 2025) y Sudáfrica (National AI Policy Framework, oct 2024) tienen reemplazos vigentes localizados, pero **sus portales bloquean la descarga automatizada**. El de Australia cuelga en HTTP/2; el sudafricano sirve un envoltorio Joomla en vez del archivo. Desde un navegador normal deberían bajar sin problema.

---

## Bloque 5 · Libros

Requieren compra o biblioteca. Sin atajo.

**Si solo puedes conseguir dos:** Krippendorff (2018), *Content Analysis*, y Grimmer, Roberts y Stewart (2022), *Text as Data*. Son los que sostienen tu capítulo de método: el primero es la fuente del α que reportas, el segundo el marco de "texto como dato". Los estás citando para justificar decisiones concretas, así que conviene tenerlos y no citarlos de oídas.

Los otros once: Bereday (1964), Bray y Manzon (2014), Noah y Eckstein (1969), Steiner-Khamsi (2004), Howlett y Ramesh (2003), Lasswell (1951), Moretti (2013), Creswell (2018), Hernández Sampieri (2014), Williamson (2017), Collingridge (1980).

---

## Regla que no conviene romper

Ninguna referencia entra a `document/referencias.bib` sin haber visto el texto completo. El precedente está en `docs/corpus-objetivo.md`: en abril de 2026 se retiró un borrador de política nacional de inteligencia artificial de Sudáfrica porque su bibliografía contenía citas inventadas por una IA.
