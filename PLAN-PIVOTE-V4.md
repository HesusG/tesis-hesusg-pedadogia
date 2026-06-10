# Plan v4: "¿Eco global o voz propia?"

> Estado del bucle de la rama `v4/eco-global-voz-propia` (creada desde v3).
> Plan aprobado: ~/.claude/plans/mighty-purring-widget.md

## Título y pregunta

**¿Eco global o voz propia? La educación en las estrategias de inteligencia artificial
del Sudeste Asiático frente al marco de la UNESCO**

PR central: ¿Qué calidad de diseño tienen los componentes educativos de las políticas de
IA del Sudeste Asiático y China, evaluados con el marco de la UNESCO (Miao et al. 2021),
y se aproximan esas políticas al repertorio global (UNESCO/ASEAN) o a los vocabularios de
sus propias tradiciones (confuciana, Pancasila)?

Decisiones del autor: tesis completa candidata (compite con v3); mitad evaluación / mitad
semántica; confucianismo como recurso interpretativo + contexto de gobernanza (no causal,
no rúbrica normativa); título legible elegido por el autor.

## Diseño

- **Evaluación ex-ante**: rúbrica deductiva de los 7 bloques + 14 recomendaciones de
  Miao et al. 2021 (escala 0-3: ausente/mencionado/con instrumentos/metas SMART);
  codificación de instrumentos NATO (Hood); filtro aspiración-vs-realidad (Fatima 2022).
  Puntuación humana sobre pasajes recuperados (hojas auditables en `policies/eval/sheets/`).
- **Semántica**: proximidad de cada política a plantillas globales vs. léxicos de
  tradiciones locales (`pipeline/lexicons.py`, índice de voz); reutiliza matriz v3 como
  evidencia de isomorfismo.
- **Vacíos verificados**: no hay rúbrica publicada del marco UNESCO; no hay verificación
  empírica del vocabulario filosófico regional en políticas; sin tesis duplicada.

## Hoja de ruta

- [x] It. 0: rama v4, plan aprobado
- [ ] It. 1: infraestructura — `pipeline/lexicons.py` ✓, `pipeline/rubric.py` ✓,
      `policies/eval/rubrica.json` (agente redactando), `references/rubrica-unesco.md`,
      +12-15 entradas bib (Hood, Howlett, Fatima×2, Schiff, Bareis&Katzenbach, Nilsson,
      OCDE 2021, UNESCO RAM, AI CFT 2024, Chilisa&Mertens, van Noordt)
- [ ] It. 2: ejecutar — hojas de puntuación top-k, puntuar rúbrica 9 documentos,
      computar léxicos; verificar fiabilidad (re-codificar ≥2 docs)
- [ ] It. 3: cap01 + título + resumen (nueva PR; OE2=rúbrica como contribución; OE4=eco/voz)
- [ ] It. 4: cap02 — sección "Evaluación de políticas públicas"; reposicionar sección
      confuciana a repertorio interpretativo (+Pancasila); conservar críticas CHC
- [ ] It. 5: cap04 — protocolo de rúbrica, instrumentos, fiabilidad, léxicos
- [ ] It. 6: cap05 — matriz de evaluación + instrumentos + eco/voz + triangulación
- [ ] It. 7: cap03 retoque (intro/transiciones) + conclusiones + resumen
- [ ] It. 8: fact-check adversarial + compilación final + web

## Estado

- **Última iteración**: 0→1 en curso (2026-06-09)
- **En curso**: agente redactando rúbrica desde el texto real de la sección 6 de
  Miao et al. 2021 (verificado: el PDF no contiene rúbrica propia)
- **Notas**: compilar con `make pdf`; pipeline `USE_LOCAL_EMBEDDINGS=1 python3 -m pipeline`;
  léxicos `python3 -m pipeline.lexicons`; hojas `python3 -m pipeline.rubric`
