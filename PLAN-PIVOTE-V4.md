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
- [x] It. 1: infraestructura completa (lexicons.py, rubric.py, eval_merge.py,
      rubrica.json de 25 criterios con citas fuente, +14 entradas bib)
- [x] It. 2: evaluación ejecutada — matriz 9×25 (Malasia 43 > Indonesia 38 > Singapur 36
      > Filipinas 32 > Tailandia 31 > China=Vietnam 30 > ASEAN 25 > UNESCO 24);
      léxicos eco/voz (voz negativa en 8/9; "Confucio" 1 mención patrimonial en todo el
      corpus; Pancasila 19); fiabilidad kappa 0.80/0.90, ±1 100%
- [x] It. 3: cap01 + título ("¿Eco Global o Voz Propia?...")
- [x] It. 4: cap02 — sección de evaluación de políticas + tradiciones como repertorio
      interpretativo + subsección Pancasila
- [x] It. 5: cap04 — rúbrica, escala, NATO, fiabilidad real, método eco/voz
- [x] It. 6: cap05 — pirámide invertida (76% innovación vs 28% equidad), perfiles,
      cruce calidad⊥identidad, caso Vietnam (convergencia selectiva)
- [x] It. 7: cap03 retocado + conclusiones + resumen/abstract
- [x] It. 8: fact-check adversarial ejecutado — 14 categorías verificadas OK, 8
      discrepancias detectadas y corregidas (conteos de niveles de Indonesia/Tailandia,
      rango UNESCO 0.667-0.729, perfil asimétrico de Indonesia, alcance del claim de
      sesgos, media 46%, restos 22×22 en cap04, hedging del "primer instrumento") +
      coherencia de criterios de selección en cap04 + compilación final limpia (81 pp.)

## Estado

- **BUCLE COMPLETO** (2026-06-10): tesis v4 terminada y verificada; output/tesis.pdf
- **PENDIENTE DEL AUTOR (importante)**: las puntuaciones de la rúbrica en
  `policies/eval/scores.json` son un BORRADOR producido por codificadores automáticos
  con justificaciones auditables (hojas en `policies/eval/sheets/`). Antes de la
  defensa, el autor debe revisar y apropiarse de las puntuaciones — especialmente las
  llamadas de juicio documentadas en `scores_draft/*.json` — y decidir cómo describir
  el procedimiento de codificación en cap04 (asistencia de IA en la codificación).
- **Notas**: compilar con `make pdf`; pipeline `USE_LOCAL_EMBEDDINGS=1 python3 -m pipeline`;
  léxicos `python3 -m pipeline.lexicons`; hojas `python3 -m pipeline.rubric`;
  consolidación `python3 -m pipeline.eval_merge`
