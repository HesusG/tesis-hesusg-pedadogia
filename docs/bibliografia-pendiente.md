# Bibliografía: qué falta y dónde conseguirlo

**Cobertura actual: 68 de 93 referencias con PDF local (73%).** Verificar con `make refs-audit`.

---

## 0. Dos arreglos ya hechos

**Siete PDFs estaban en la raíz del repositorio**, no en `references/`. Seguían la convención de nombres correcta pero nunca se movieron, así que la auditoría los reportaba como faltantes: Conneau (XLM-R), Finlandia 2017, Alemania 2020, Grootendorst (BERTopic), Kozlowski (Geometry of Culture), NLP4Gov y Reimers (Sentence-BERT). Ya están en su lugar.

**Un bug en `references/ref_audit.py`**: la expresión regular que extrae la clave del nombre de archivo era `[a-z]+\d{4}`, que no puede parsear claves con dígitos antes del año. `nlp4gov2024` no coincidía con nada, así que un PDF que **sí estaba en disco** se reportaba como faltante. Corregido: ahora corta en el primer guion bajo, que es la convención declarada.

---

## 1. Lo que necesita tu acceso institucional (4 artículos)

Estos aparecen en Unpaywall como de acceso abierto, pero las editoriales bloquean la descarga automática. **Con tu sesión de UPAEP o INFOTEC abierta, estos enlaces deberían darte el PDF directo.** Guárdalos en `references/` con el nombre indicado.

| Clave | Referencia | Enlace directo | Guardar como |
|---|---|---|---|
| `ball1998big` | Ball, *Big Policies/Small World*, Comparative Education (1998) | [doi.org/10.1080/03050069828225](https://doi.org/10.1080/03050069828225) | `ball1998big_big-policies-small-world.pdf` |
| `bareis2022talking` | Bareis & Katzenbach, *Talking AI into Being*, ST&HV (2022) | [doi.org/10.1177/01622439211030007](https://doi.org/10.1177/01622439211030007) | `bareis2022talking_talking-ai-into-being.pdf` |
| `gulson2019digitizing` | Gulson & Webb, *Digitizing education policy*, EPD Society & Space (2019) | [doi.org/10.1177/0263775818813144](https://doi.org/10.1177/0263775818813144) | `gulson2019digitizing_digitizing-education-policy.pdf` |
| `holmes2022state` | Holmes et al., *State of the art in AI and education*, Eur. J. of Education (2022) | [doi.org/10.1111/ejed.12533](https://doi.org/10.1111/ejed.12533) | `holmes2022state_state-of-the-art-ai-education.pdf` |

`mishra2006technological` (TPACK, Teachers College Record) **no tiene versión abierta** según Unpaywall. Es un clásico muy citado y circula en repositorios de autor; búscalo por título en Google Scholar y usa el enlace "[PDF]" de la derecha.

> **Nota sobre JSTOR:** no puedo descargar de JSTOR. Requiere autenticación institucional y la descarga automatizada viola sus términos de uso. Ball (1998) es el candidato más probable de estar ahí; los otros tres son de Taylor & Francis, SAGE y Wiley, y con tu acceso los bajas directo del DOI.

---

## 2. Documentos de política que faltan (5)

No son artículos académicos, son documentos oficiales. No necesitan JSTOR y varios ya los tienes en texto plano dentro del repositorio; solo falta el PDF para el archivo bibliográfico.

| Clave | Qué es | Dónde está |
|---|---|---|
| `china2017ai` | Plan de Desarrollo de IA de Nueva Generación (2017) | Texto ya en `policies/raw/china/3_new_gen_ai_development_plan_2017_en.txt` |
| `southafrica2020pc4ir` | Reporte PC4IR de Sudáfrica | Texto ya en `policies/processed/sudafrica_4ir_2020.txt` |
| `germany2018aistrategy` | KI-Strategie alemana 2018 | bundesregierung.de |
| `estonia2019krattai` | Estrategia Kratt de Estonia | kratid.ee / kaust.ee |
| `anuies2024gobernanza`, `mexia2025centro`, `sep2026ia` | Documentos mexicanos | ANUIES, IA-MX, SEP |

---

## 3. Libros (13)

Requieren compra o biblioteca; no hay atajo. Estos son los que sostienen tu marco metodológico:

**Educación comparada:** Bereday (1964), Bray & Manzon (2014), Noah & Eckstein (1969), Steiner-Khamsi (2004)
**Política pública:** Howlett & Ramesh (2003), Lasswell (1951)
**Método y texto como dato:** Grimmer, Roberts & Stewart (2022), Krippendorff (2018), Moretti (2013), Creswell (2018), Hernández Sampieri (2014)
**Tecnología y educación:** Williamson (2017), Collingridge (1980)

**Prioridad si hay que elegir:** Krippendorff (2018) y Grimmer et al. (2022). Son los que sostienen directamente tu capítulo de método: el primero es la fuente del α que reportas, el segundo el marco de "texto como dato". Los citas para justificar decisiones concretas, así que conviene tenerlos a mano y no citarlos de oídas.

---

## 4. Qué me falta saber de ti

No sé **qué temas específicos** te pidió tu asesor buscar en JSTOR. Si me los dices, te armo los términos de búsqueda y las entradas `.bib` listas para que solo pegues el PDF.

Dado el tema de tu tesis, lo que probablemente falte y JSTOR cubre bien:

- **Filosofía política confuciana** y el concepto de 德治 (dézhì): fuentes primarias y comentario académico. Ahora mismo tu códebook se apoya en un panel de modelos, no en literatura sinológica. **Ese es el hueco bibliográfico más serio que tienes**: mides un concepto confuciano sin citar a los especialistas en confucianismo.
- **Política educativa china** contemporánea y su relación con el Estado.
- **Educación comparada**, tradición metodológica (JSTOR tiene *Comparative Education Review* completa).
