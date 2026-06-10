# Plan de pivote: Sudeste Asiático + herencia confuciana

> Documento de trabajo del bucle iterativo. Cada iteración actualiza la sección **Estado**.

## Nueva dirección (decisión del autor, 2026-06-09)

La tesis pasa de un estudio global (12 países + 4 organismos) a un estudio enfocado en el
**Sudeste Asiático**, con atención específica a las **raíces confucianas** de los sistemas
educativos de la región.

## Encuadre académico

La herencia confuciana NO es uniforme en el Sudeste Asiático:

- **Fuerte**: Vietnam (milenio de influencia china, sistema de exámenes mandarinales),
  Singapur (mayoría étnica china, campaña de ética confuciana años 80, Shared Values 1991).
- **Parcial**: Malasia (minoría china significativa).
- **Débil/ausente**: Indonesia (islámica, herencia hindú-budista), Tailandia (budista),
  Filipinas (herencia católica colonial).

Por tanto, el marco se formula como **lente de Culturas de Herencia Confuciana (CHC)**:
comparar cómo los países CHC (Vietnam, Singapur) y no-CHC (Indonesia, Tailandia, Malasia,
Filipinas) del Sudeste Asiático formulan sus políticas de IA en educación, y si la herencia
confuciana (autoridad docente, cultura de examen, meritocracia, esfuerzo, centralización)
predice diferencias en las 7 dimensiones de análisis. Esto evita el error esencialista de
tratar a toda la región como confuciana y convierte la variación interna en la pregunta de
investigación.

## Nuevo corpus (VERIFICADO Y DESCARGADO, 2026-06-09)

| País | Documento | Año | CHC | Estado |
|------|-----------|-----|-----|--------|
| **China** | Outline 15th Five-Year Plan 2026–2030 (trad. EUCLERA, 181 pp.) | 2026 | Fuerte (ancla) | ✓ 391k chars |
| Vietnam | Decisión 127/QD-TTg (trad. inglesa LuatVietnam) | 2021 | Fuerte | ✓ 28k chars |
| Singapur | NAIS 2.0 (oficial) | 2023 | Fuerte | ✓ 67k chars |
| Malasia | AI-RMAP 2021–2025 | 2021 | Parcial | ✓ 119k chars |
| Indonesia | Stranas KA (en indonesio, sin versión EN) | 2020 | Ausente | ✓ 350k chars |
| Tailandia | National AI Strategy 2022–2027 (versión EN, 28 pp.) | 2022 | Ausente | ✓ 13k chars (corto) |
| Filipinas | NAISR 2.0 | 2024 | Ausente | ✓ 74k chars |
| ASEAN | Guide on AI Governance and Ethics | 2024 | Regional | ✓ 191k chars |
| UNESCO | Guidance for Generative AI in Education (conservado) | 2023 | Internacional | ✓ |

**Decisión del autor (2026-06-09)**: China DEBE incluirse, en particular el último plan
quinquenal (15º, 2026–2030) con su iniciativa AI+. Se incorpora como **caso ancla de la
civilización confuciana** (región `asia_oriental`): el diseño compara los países del Sudeste
Asiático contra el sistema de origen confuciano, lo que refuerza la lente CHC.

Salen del corpus: Europa, Américas, Japón, Corea, India, Australia, WEF (citables como
contexto global en cap. 1). Notas metodológicas pendientes: Tailandia corto (versión EN
abreviada), Indonesia en idioma original, Vietnam vía traducción de tercero (LuatVietnam).

## Acciones por capítulo (del relevamiento)

1. **cap01-planteamiento** (ALTO): reemplazar alcance de 22 unidades por 6 países SEA + lente
   CHC; nuevas preguntas de investigación; justificación regional.
2. **cap02-marco-teorico** (MEDIO): AÑADIR sección "Herencia educativa confuciana" (~1.200
   palabras): CHC (Biggs & Watkins), modelo confuciano (Marginson), crítica al constructo;
   conexión con adopción tecnológica y estilo de política educativa.
3. **cap03-marco-contextual** (CRÍTICO): eliminar Europa/Américas/Asia no-SEA (~2.500
   palabras); añadir secciones de Vietnam, Indonesia, Tailandia, Malasia, Filipinas;
   ampliar Singapur; añadir contexto ASEAN y mapa de herencia confuciana regional;
   reconstruir síntesis preliminar.
4. **cap04-metodologia** (BAJO): nueva Tabla 1 del corpus (6-8 unidades); ajustar conteos de
   fragmentos; nota metodológica sobre idiomas/traducción; añadir variable CHC al marco.
5. **cap05-resultados** (CRÍTICO): re-ejecutar pipeline con nuevo corpus; reconstruir las 7
   dimensiones; matriz de similitud 6×6/8×8; NUEVA sección CHC vs no-CHC.
6. **conclusiones** (MEDIO): reescribir respuestas a objetivos y hallazgos.
7. **frontmatter/preámbulo** (ALTO): nuevo título, resumen, palabras clave.
8. **referencias.bib**: +20-30 entradas (políticas SEA + literatura CHC).
9. **pipeline/policies**: actualizar `metadata.json`, descargar PDFs nuevos, re-ejecutar
   `make pipeline`; actualizar `web/` (colores por subgrupo CHC).

## Hoja de ruta del bucle

- [x] It. 0: rama `v3/sudeste-asiatico-confuciano`, relevamiento, este plan
- [x] It. 1: verificación de documentos + literatura CHC (24 refs verificadas); corpus
      definitivo descargado a `policies/raw/` (9 unidades, China incluida por decisión
      del autor); textos extraídos a `policies/processed/`
- [x] It. 2: `metadata.json` v2.0 + `referencias.bib` (24 CHC + 9 políticas); `config.py`
      con regiones nuevas y clasificación CHC
- [ ] It. 3: reescribir cap01 + frontmatter/título
- [ ] It. 4: cap02 — sección de herencia confuciana
- [ ] It. 5: cap03 — reescritura mayor (países SEA)
- [ ] It. 6: re-ejecutar pipeline con nuevo corpus
- [ ] It. 7: cap05 — resultados con datos reales del pipeline + análisis CHC vs no-CHC
- [ ] It. 8: cap04 ajustes + conclusiones + resumen
- [ ] It. 9: compilar PDF, revisar consistencia (sin restos de "22 unidades"/"17 países"),
      fact-check de citas
- [ ] It. 10: autorreflexión final, `make pdf` limpio, actualizar web/slides si hay tiempo

## Estado

- **Última iteración**: 2 (2026-06-09)
- **Siguiente**: It. 3 — reescribir cap01 + frontmatter/título con el nuevo encuadre
  (9 unidades: China ancla + 6 SEA + ASEAN + UNESCO)
- **Bloqueos**: ninguno para la escritura; `make pipeline` (It. 6) requiere OPENAI_API_KEY
  o USE_LOCAL_EMBEDDINGS=1 — verificar al llegar
- **Notas**: PDFs crudos no se versionan (gitignore); processed/ sí. Bib keys del corpus:
  china2026fyp, vietnam2021ai, singapore2023nais2, malaysia2021airmap, indonesia2020stranas,
  thailand2022ai, philippines2024naisr, asean2024guide, unesco2023genai, deped2026ai (extra)
