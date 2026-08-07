<script setup>
defineProps({ who: { default: '' }, role: { default: '' } })
</script>
<template>
  <div class="slidev-layout quote h-full flex flex-col justify-center">
    <div class="text-blue font-display text-[4rem] leading-none">“</div>
    <div class="max-w-4xl">
      <slot />
    </div>
    <div v-if="who" class="mt-6 ac-rule pt-3">
      <span class="font-mono text-ink font-600">{{ who }}</span>
      <span v-if="role" class="text-muted font-mono text-[0.8rem]"> · {{ role }}</span>
    </div>
  </div>
</template>
