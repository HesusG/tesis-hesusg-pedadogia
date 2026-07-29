<script setup>
// Perfil confuciano en 6 ejes (Vía A, medianas z contra el corpus de fondo).
// Fuente: web/data/confucian_radar_v3.json
const props = defineProps({
  paises: { type: Array, default: () => ['china', 'canada'] },
})

const ejes = [
  { k: 'ren',      zh: '仁',   pin: 'rén',     es: 'Benevolencia' },
  { k: 'li',       zh: '礼',   pin: 'lǐ',      es: 'Ritual' },
  { k: 'yi',       zh: '义',   pin: 'yì',      es: 'Rectitud' },
  { k: 'xiushen',  zh: '修身', pin: 'xiūshēn', es: 'Cultivo de sí' },
  { k: 'dezhi_fa', zh: '德治', pin: 'dézhì',   es: 'Virtud vs. norma' },
  { k: 'he',       zh: '和',   pin: 'hé',      es: 'Armonía' },
]

const datos = {
  china:     { label: 'China',          color: '#023BF2', v: { ren: 0.99, li: 0.18, yi: 1.07, xiushen: 0.52, dezhi_fa: 0.90, he: 0.45 } },
  canada:    { label: 'Canadá',         color: '#0B1C45', v: { ren: 0.98, li: 0.27, yi: 0.72, xiushen: 0.49, dezhi_fa: 0.88, he: -0.31 } },
  eeuu:      { label: 'Estados Unidos', color: '#8A93A6', v: { ren: 0.12, li: -0.80, yi: 0.48, xiushen: -0.20, dezhi_fa: -0.02, he: -0.69 } },
  alemania:  { label: 'Alemania',       color: '#8A93A6', v: { ren: 0.09, li: -0.20, yi: 0.11, xiushen: -0.03, dezhi_fa: 0.13, he: -0.27 } },
  australia: { label: 'Australia',      color: '#8A93A6', v: { ren: 0.13, li: 0.07, yi: -0.13, xiushen: -0.09, dezhi_fa: 0.51, he: 0.03 } },
  sudafrica: { label: 'Sudáfrica',      color: '#8A93A6', v: { ren: -0.05, li: 0.33, yi: -0.13, xiushen: -0.14, dezhi_fa: 0.08, he: 0.45 } },
  colombia:  { label: 'Colombia',       color: '#8A93A6', v: { ren: -0.37, li: -0.41, yi: -0.18, xiushen: 0.39, dezhi_fa: -0.16, he: -0.41 } },
}

const S = 300, C = S / 2, RAD = 96
const lo = -1.0, hi = 1.2
const r = v => ((Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo)) * RAD
const ang = i => (Math.PI * 2 * i) / ejes.length - Math.PI / 2
const pt = (v, i) => [C + r(v) * Math.cos(ang(i)), C + r(v) * Math.sin(ang(i))]
const poly = pais => ejes.map((e, i) => pt(datos[pais].v[e.k], i).join(',')).join(' ')
const anillos = [-0.5, 0, 0.5, 1.0]
</script>

<template>
  <div class="flex items-center gap-6">
    <svg :viewBox="`0 0 ${S} ${S}`" style="width: 430px; flex: 0 0 auto; font-family: 'IBM Plex Mono', monospace">
      <!-- anillos -->
      <circle v-for="a in anillos" :key="'a'+a" :cx="C" :cy="C" :r="r(a)"
              fill="none" :stroke="a === 0 ? '#0F1624' : '#DADEE6'" :stroke-width="a === 0 ? 1.2 : 0.8"
              :stroke-dasharray="a === 0 ? 'none' : '2 3'" />
      <!-- radios y etiquetas -->
      <g v-for="(e, i) in ejes" :key="e.k">
        <line :x1="C" :y1="C" :x2="C + RAD * Math.cos(ang(i))" :y2="C + RAD * Math.sin(ang(i))"
              stroke="#DADEE6" stroke-width="0.8" />
        <text :x="C + (RAD + 22) * Math.cos(ang(i))" :y="C + (RAD + 22) * Math.sin(ang(i)) - 3"
              text-anchor="middle" style="font-size:13px" fill="#0F1624">{{ e.zh }}</text>
        <text :x="C + (RAD + 22) * Math.cos(ang(i))" :y="C + (RAD + 22) * Math.sin(ang(i)) + 9"
              text-anchor="middle" style="font-size:7.5px" fill="#4D5566" letter-spacing="0.5">{{ e.es.toUpperCase() }}</text>
      </g>
      <!-- Series. La segunda va punteada a propósito: los perfiles casi coinciden,
           y con dos líneas sólidas del mismo grosor una tapa a la otra. -->
      <g v-for="(p, k) in props.paises" :key="p">
        <polygon :points="poly(p)" :stroke="datos[p].color" :stroke-width="k === 0 ? 2 : 1.6"
                 :stroke-dasharray="k === 0 ? 'none' : '5 3'"
                 :fill="datos[p].color" :fill-opacity="k === 0 ? 0.08 : 0" />
        <circle v-for="(e, i) in ejes" :key="p + e.k" :cx="pt(datos[p].v[e.k], i)[0]"
                :cy="pt(datos[p].v[e.k], i)[1]" :r="k === 0 ? 3 : 2.2" :fill="datos[p].color" />
      </g>
    </svg>

    <div class="flex flex-col gap-2">
      <div v-for="p in props.paises" :key="'lg' + p" class="flex items-center gap-2 font-mono text-[0.85rem]">
        <span :style="{ background: datos[p].color, width: '11px', height: '11px', display: 'inline-block' }" />
        {{ datos[p].label }}
      </div>
      <div class="kicker mt-2" style="max-width: 15ch; line-height: 1.5">
        Medianas z contra el corpus de fondo
      </div>
    </div>
  </div>
</template>
