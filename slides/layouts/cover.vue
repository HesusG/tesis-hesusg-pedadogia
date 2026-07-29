<template>
  <div class="slidev-layout cover h-full flex flex-col justify-between">
    <div class="flex items-center justify-between">
      <div class="wordmark text-[1.3rem] text-inkblue">UPAEP<span class="text-blue"> · </span>Maestría en Pedagogía</div>
      <div class="kicker">Defensa de tesis · 2026</div>
    </div>

    <div class="flex-1 flex flex-col justify-center">
      <slot />
    </div>

    <div class="ac-rule pt-3 flex items-end justify-between">
      <div class="font-mono text-[0.78rem] leading-relaxed text-ink">
        Hesus García Cobos<br />
        <span class="text-muted">Director: Dr. Herminio Sánchez de la Barquera y Arroyo</span>
      </div>
      <div class="kicker text-right">
        7 países · 15 documentos<br />1,120 clasificaciones
      </div>
    </div>
  </div>
</template>
