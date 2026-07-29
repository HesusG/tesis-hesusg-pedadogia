<script setup>
defineProps({ hero: { type: String, default: '' } })
const base = import.meta.env.BASE_URL
</script>
<template>
  <div class="slidev-layout section ac-dark h-full flex flex-col justify-center">
    <div v-if="hero" class="section-hero" :style="{ backgroundImage: `url(${base + hero})` }" />
    <slot />
  </div>
</template>
