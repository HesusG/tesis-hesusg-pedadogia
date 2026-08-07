<script setup>
// Eje dézhì↔fǎ por país (Vía B, panel de 7 jueces).
// Fuente: web/data/dezhi_country_comparison.json + dezhi_validation.json
// Valores fijos aquí a propósito: la diapositiva no debe depender de un fetch.
const filas = [
  { pais: 'China',          m:  0.943, lo:  0.729, hi:  1.171, hi_lite: true },
  { pais: 'Sudáfrica',      m:  0.057, lo: -0.043, hi:  0.214 },
  { pais: 'Colombia',       m:  0.014, lo:  0.000, hi:  0.043 },
  { pais: 'Australia',      m: -0.029, lo: -0.171, hi:  0.086 },
  { pais: 'Canadá',         m: -0.057, lo: -0.143, hi:  0.000 },
  { pais: 'Alemania',       m: -0.100, lo: -0.243, hi:  0.000 },
  { pais: 'Estados Unidos', m: -0.486, lo: -0.871, hi: -0.143 },
]

const W = 560, H = 250, L = 118, R = 18, T = 14
const min = -1.0, max = 1.3
const plotW = W - L - R
const x = v => L + ((v - min) / (max - min)) * plotW
const paso = (H - T - 22) / filas.length
const y = i => T + i * paso + paso / 2
const ticks = [-1, -0.5, 0, 0.5, 1]
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" class="w-full" style="font-family: 'IBM Plex Mono', monospace">
    <!-- rejilla -->
    <g>
      <line v-for="t in ticks" :key="'g'+t" :x1="x(t)" :x2="x(t)" :y1="T - 4" :y2="H - 22"
            :stroke="t === 0 ? '#0F1624' : '#DADEE6'" :stroke-width="t === 0 ? 1.4 : 1" />
      <text v-for="t in ticks" :key="'l'+t" :x="x(t)" :y="H - 8" text-anchor="middle"
            style="font-size:9.5px" fill="#4D5566">{{ t > 0 ? '+' + t : t }}</text>
    </g>

    <!-- barras + intervalo -->
    <g v-for="(f, i) in filas" :key="f.pais">
      <text :x="L - 8" :y="y(i) + 3.5" text-anchor="end" style="font-size:10.5px"
            :fill="f.hi_lite ? '#022187' : '#0F1624'" :font-weight="f.hi_lite ? 600 : 400">{{ f.pais }}</text>

      <rect :x="Math.min(x(0), x(f.m))" :y="y(i) - 7" :width="Math.max(Math.abs(x(f.m) - x(0)), 1.2)"
            height="14" :fill="f.hi_lite ? '#023BF2' : '#B9C6E8'" />

      <line :x1="x(f.lo)" :x2="x(f.hi)" :y1="y(i)" :y2="y(i)" stroke="#0F1624" stroke-width="1.2" />
      <line :x1="x(f.lo)" :x2="x(f.lo)" :y1="y(i) - 4.5" :y2="y(i) + 4.5" stroke="#0F1624" stroke-width="1.2" />
      <line :x1="x(f.hi)" :x2="x(f.hi)" :y1="y(i) - 4.5" :y2="y(i) + 4.5" stroke="#0F1624" stroke-width="1.2" />

      <text :x="x(f.hi) + 6" :y="y(i) + 3.5" style="font-size:9.5px"
            :fill="f.hi_lite ? '#022187' : '#4D5566'" :font-weight="f.hi_lite ? 600 : 400">
        {{ f.m > 0 ? '+' : '' }}{{ f.m.toFixed(3) }}
      </text>
    </g>

    <!-- polos -->
    <text :x="L" :y="T - 2" style="font-size:8.5px" fill="#4D5566" letter-spacing="1.2">DERECHOS COMO LÍMITE</text>
    <text :x="W - R" :y="T - 2" style="font-size:8.5px" fill="#4D5566" text-anchor="end" letter-spacing="1.2">ESTADO QUE CULTIVA</text>
  </svg>
</template>
