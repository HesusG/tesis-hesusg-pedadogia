# Defensa de tesis — deck Slidev

Formato academias.dev («PLATE / PROTOCOL»): papel hueso, marco ultramar, IBM Plex Mono
de cuerpo, Archivo de títulos, sin sombras.

## Correr

```bash
cd slides
npm install
npm run dev        # http://localhost:3030
```

## Exportar

```bash
npm run build      # sitio estático a ../web/defensa/
npm run export     # PDF a ../output/defensa-tesis.pdf
```

## Estructura

| Archivo | Qué es |
|---|---|
| `slides.md` | Contenido. Las notas del orador llevan minutaje |
| `layouts/` | `cover`, `section`, `statement`, `ac-fact`, `ac-split`, `ac-agenda`, `ac-diagram`, `quote` |
| `components/BarrasPais.vue` | Barras con intervalo de confianza, SVG puro |
| `components/RadarConfucio.vue` | Radar de los seis ejes, SVG puro |
| `styles/index.css` | Sistema de diseño |
| `uno.config.ts` | Tokens y atajos |

Los dos componentes de gráfica llevan las cifras dentro del archivo, no las leen de
`web/data/`. Es a propósito: una diapositiva no debe depender de un fetch en vivo.
Al cambiar los datos hay que tocar el `.vue` y anotarlo en el encabezado.

## Reglas de estilo (no romper)

- Azul `#023BF2` sobre papel `#FAFCFE`; navy `#0B1C45` en las divisorias; amarillo
  `#EDF400` solo como acento puntual.
- Bordes de pelo (1–1.5px), esquinas duras. Nada de sombras suaves ni pestañas de color.
- Énfasis con `<em>` amarillo, no con `border-l-4`.
- Sin rayas largas ni flechas `->` en el texto.
