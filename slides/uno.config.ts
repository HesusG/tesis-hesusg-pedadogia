import { defineConfig } from 'unocss'

// AcademIAS brand — "PLATE / PROTOCOL": off-white paper, electric-blue frame,
// monospace body, Archivo display, engravings + blue duotone. Hard edges.
// (Icons are inline SVG via components/Ico.vue — no iconify dependency.)
export default defineConfig({
  shortcuts: {
    // Surfaces & chrome
    'ac-hair': 'border border-[#DADEE6]',
    'ac-rule': 'border-t border-[#DADEE6]',
    'ac-chip': 'inline-block border border-[#023BF2] px-2 py-1 text-[0.7rem] tracking-widest uppercase font-mono',
    'ac-idx': 'font-mono text-[#023BF2] font-600 tracking-widest',
    'ac-card': 'border border-[#DADEE6] bg-white p-5',
    'ac-card-blue': 'border-[1.5px] border-[#023BF2] bg-white p-5',
    'ac-btn': 'inline-block border-[1.5px] border-[#023BF2] px-4 py-2 uppercase tracking-wider font-mono text-[#023BF2]',
    // Labels & callouts — hairline + surface fill (brand: no thick side-tabs)
    'ac-label': 'font-mono uppercase tracking-[0.14em] text-[0.72rem] text-[#4D5566]',
    'ac-callout': 'border border-[#DADEE6] bg-[#F4F7FB] px-5 py-4',
    'ac-callout-yellow': 'border border-[#DADEE6] bg-[#FBFCE0] px-5 py-4',
    // Color helpers
    'bg-paper': 'bg-[#FAFCFE]',
    'bg-surface': 'bg-[#F4F7FB]',
    'bg-blue': 'bg-[#023BF2]',
    'bg-navy': 'bg-[#0B1C45]',
    'text-blue': 'text-[#023BF2]',
    'text-ink': 'text-[#0F1624]',
    'text-ink-blue': 'text-[#022187]',
    'text-muted': 'text-[#4D5566]',
    'text-yellow': 'text-[#EDF400]',
    'mark-yellow': 'bg-[#EDF400] text-[#022187] px-1',
  },
  theme: {
    fontFamily: {
      sans: 'Archivo, system-ui, sans-serif',
      display: 'Archivo, system-ui, sans-serif',
      wordmark: '"Bodoni Moda", Georgia, serif',
      mono: '"IBM Plex Mono", ui-monospace, monospace',
    },
    colors: {
      paper: '#FAFCFE',
      surface: '#F4F7FB',
      blue: '#023BF2',
      press: '#032EBB',
      inkblue: '#022187',
      navy: '#0B1C45',
      ink: '#0F1624',
      muted: '#4D5566',
      line: '#DADEE6',
      yellow: '#EDF400',
    },
  },
})
