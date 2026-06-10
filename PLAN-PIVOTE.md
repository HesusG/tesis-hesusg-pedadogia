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

## Nuevo corpus (por verificar disponibilidad)

| País | Documento candidato | Año | CHC |
|------|--------------------|-----|-----|
| Vietnam | Decisión 127/QD-TTg — Estrategia Nacional de IA | 2021 | Sí |
| Singapur | NAIS 2019 / NAIS 2.0 | 2019/2023 | Sí |
| Malasia | AI Roadmap 2021–2025 (AI-RMAP) | 2021 | Parcial |
| Indonesia | Stranas KA | 2020 | No |
| Tailandia | National AI Strategy and Action Plan 2022–2027 | 2022 | No |
| Filipinas | National AI Strategy Roadmap (NAISR / 2.0) | 2021/2024 | No |
| ASEAN | Guide on AI Governance and Ethics | 2024 | Regional |
| UNESCO | Guidance for Generative AI in Education (se conserva) | 2023 | Referencia |

Se conservan del corpus anterior: `singapur` (NAIS 2019), `unesco`. El resto de países
(Europa, Américas, Japón, Corea, India, Australia, WEF) salen del corpus pero pueden citarse
como contexto global en cap. 1.

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
- [ ] It. 1: verificar disponibilidad de documentos (agentes web en curso) y literatura CHC;
      decidir corpus definitivo; descargar PDFs a `policies/raw/`
- [ ] It. 2: actualizar `metadata.json` + `referencias.bib` (políticas SEA + CHC)
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

- **Última iteración**: 0 (2026-06-09)
- **En curso**: agentes de investigación web (documentos SEA + bibliografía CHC)
- **Bloqueos**: disponibilidad de documentos oficiales en inglés para Vietnam/Indonesia/
  Tailandia (los resultados del cap. 5 dependen de re-ejecutar el pipeline con PDFs reales)
