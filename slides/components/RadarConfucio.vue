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
  // Único eje bipolar de los seis: se etiqueta con sus dos polos. Escribir solo
  // 德治 lo presentaba como un valor más, igual que 仁 o 礼, y eso es falso.
  { k: 'dezhi_fa', zh: '德治↔法', pin: 'dézhì↔fǎ', es: 'Virtud vs. norma' },
  { k: 'he',       zh: '和',   pin: 'hé',      es: 'Armonía' },
]

const datos = {
  china:     { label: 'China',          color: '#023BF2', v: { ren: 0.97, li: 0.16, yi: 1.07, xiushen: 0.51, dezhi_fa: 0.85, he: 0.47 } },
  canada:    { label: 'Canadá',         color: '#0B1C45', v: { ren: 0.34, li: 0.39, yi: 0.17, xiushen: 0.30, dezhi_fa: 0.78, he: -0.28 } },
  eeuu:      { label: 'Estados Unidos', color: '#8A93A6', v: { ren: 0.09, li: -0.84, yi: 0.48, xiushen: -0.21, dezhi_fa: -0.07, he: -0.68 } },
  alemania:  { label: 'Alemania',       color: '#8A93A6', v: { ren: 0.06, li: -0.23, yi: 0.11, xiushen: -0.05, dezhi_fa: 0.08, he: -0.26 } },
  australia: { label: 'Australia',      color: '#8A93A6', v: { ren: 0.11, li: 0.04, yi: -0.13, xiushen: -0.11, dezhi_fa: 0.45, he: 0.05 } },
  sudafrica: { label: 'Sudáfrica',      color: '#8A93A6', v: { ren: -0.07, li: 0.30, yi: -0.13, xiushen: -0.16, dezhi_fa: 0.03, he: 0.47 } },
  colombia:  { label: 'Colombia',       color: '#8A93A6', v: { ren: -0.40, li: -0.44, yi: -0.19, xiushen: 0.37, dezhi_fa: -0.20, he: -0.39 } },
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
