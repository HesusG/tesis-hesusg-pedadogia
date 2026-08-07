<script setup>
defineProps({ dark: { type: Boolean, default: false } })
</script>
<template>
  <div :class="['slidev-layout statement h-full flex flex-col justify-center items-start', dark ? 'ac-dark' : '']">
    <slot />
  </div>
</template>
