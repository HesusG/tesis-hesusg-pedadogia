<script setup>
// El retrato vive en public/ y se resuelve con BASE_URL, igual que section.vue:
// hotlinkear Wikimedia rompía la portada al exportar o al presentar sin red.
const base = import.meta.env.BASE_URL
</script>

<template>
  <div class="slidev-layout cover h-full flex flex-col justify-between">
    <div class="flex items-center justify-between">
      <div class="wordmark text-[1.3rem] text-inkblue">INFOTEC<span class="text-blue"> · </span>Programa de Verano</div>
    </div>

    <!-- El título es el ancla: ocupa el ancho sobrante y la imagen es un acento
         lateral de tamaño fijo, no un hermano flex-1 que le robe la mitad del alto. -->
    <div class="flex items-center gap-10">
      <div class="flex-1 min-w-0">
        <slot />
      </div>
      <div class="duo round shrink-0" style="width: 240px; height: 240px">
        <img :src="`${base}confucio-tang.jpg`" alt="Retrato de Confucio, dinastía Tang"
             style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 22%" />
      </div>
    </div>

    <div class="ac-rule pt-3 flex items-end justify-between">
      <div class="font-mono text-[0.78rem] leading-relaxed text-ink">
        Hesus García Cobos<br />
        <span class="text-muted">Supervisora: María Beatriz Juárez Aguilar</span>
      </div>
    </div>
  </div>
</template>
