<script setup>
// Inline SVG icons (no iconify dependency, guaranteed to render in CI).
// Keys match the lucide/simple-icons names used in slides.md so markup stays stable.
defineProps({ name: { type: String, required: true } })

// stroke icons (currentColor); rendered inside a 24x24 viewBox
const stroke = {
  'cpu': '<rect x="6" y="6" width="12" height="12" rx="1.5"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 2v2.5M15 2v2.5M9 19.5V22M15 19.5V22M2 9h2.5M2 15h2.5M19.5 9H22M19.5 15H22"/>',
  'message-square-warning': '<path d="M4 4h16v12H8l-4 4z"/><path d="M12 7.5v3.5M12 13.5h.01"/>',
  'search-check': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/><path d="M8 11l2 2 4-4"/>',
  'search-x': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/><path d="M9 9l4 4M13 9l-4 4"/>',
  'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
  'gavel': '<path d="M13 3l5 5-3 3-5-5z"/><path d="M8.5 8.5l-5 5 3 3 5-5"/><path d="M14 15l5 5M4 21h9"/>',
  'scale': '<path d="M12 3v18M6 21h12M5 7h14"/><path d="M5 7l-2.5 6a3 3 0 0 0 6 0z"/><path d="M19 7l2.5 6a3 3 0 0 1-6 0z"/>',
  'badge-check': '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-5"/>',
  'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><path d="M12 18v3M9 21h6"/>',
  'notebook-pen': '<path d="M5 4h9v16H5z"/><path d="M5 9h9M5 13h5"/><path d="M18 5l2.5 2.5L15 13h-2.5v-2.5z"/>',
  'network': '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7.2v3.3M11 11l-5 6M13 11l5 6"/>',
  'video': '<rect x="3" y="6" width="12" height="12" rx="2"/><path d="M15 10l6-3v10l-6-3z"/>',
  'users': '<circle cx="9" cy="8" r="3"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16 5.5a3 3 0 0 1 0 6M17.5 20a6 6 0 0 0-2-4.2"/>',
  'wrench': '<path d="M15 3a5 5 0 0 0-4 8L4 18l2 2 7-7a5 5 0 0 0 8-4l-3.2 3.2-2.8-.4-.4-2.8z"/>',
  'pen-tool': '<path d="M12 2l2.5 6.5L21 11l-6.5 2.5L12 20l-2.5-6.5L3 11l6.5-2.5z"/>',
}
// brand marks (filled/stroke approximations, monochrome/neutral)
const brand = {
  'claude': '<path d="M12 2v20M2 12h20M4.9 4.9l14.2 14.2M19.1 4.9L4.9 19.1"/>',
  'googlegemini': '<path d="M12 2.5c.6 4.8 4.2 8.4 9 9-4.8.6-8.4 4.2-9 9-.6-4.8-4.2-8.4-9-9 4.8-.6 8.4-4.2 9-9z"/>',
  'openai': '<path d="M12 3a4.2 4.2 0 0 1 3.6 6.3A4.2 4.2 0 0 1 12 21a4.2 4.2 0 0 1-3.6-11.7A4.2 4.2 0 0 1 12 3z"/><circle cx="12" cy="12" r="2"/>',
}
</script>
<template>
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"
       stroke-linecap="round" stroke-linejoin="round"
       v-html="stroke[name] || brand[name] || ''" />
</template>
