# /neobrutalist — Generar Páginas Neobrutalist

## Trigger
User invokes `/neobrutalist <description of page or section>`

## Design System
Follow the established design system from `sample_tesis/sample_neo_brutalist.html`:

### CSS Variables
```css
:root {
  --bg: #F5F0E8;
  --fg: #1a1a1a;
  --bg-alt: #E8E2D2;
  --border: 3px solid #1a1a1a;
  --shadow: 6px 6px 0 #1a1a1a;
  --yellow: #FFD54F;
  --ease: cubic-bezier(0.22, 1, 0.36, 1);
}
```

### Region Colors (for thesis viz)
- Europa: `#1976d2`
- Américas: `#388e3c`
- Asia-Pacífico: `#d32f2f`
- Internacional: `#7b1fa2`

### Fonts
- **Display** (h1-h3): `'Syne', sans-serif` (weights: 400, 600, 700, 800)
- **Body**: `'DM Sans', sans-serif` (weights: 300, 400, 500, 700)
- **Code/Labels**: `'JetBrains Mono', monospace` (weights: 400, 500, 700)

### Components
- **Hero**: Full-width, large Syne heading, JetBrains Mono subtitle tag
- **Section grid** (`.sec-grid`): Alternating image+text layout
- **Collapsible cards** (`.rb`): Click to expand, border + shadow, smooth transition
- **Takeaway boxes** (`.tk`): Yellow left border, highlighted insight
- **Progress bar**: Fixed top, 6px height, tracks scroll
- **Side nav dots**: Fixed left, IntersectionObserver-activated
- **Synthesis cards** (`.pc`): Grid of comparison cards
- **Dark sections**: `background: var(--fg); color: var(--bg);`

### Animations
- **fadeUp**: `translateY(30px) → translateY(0)`, `opacity: 0 → 1`
- **Reveal**: `.rv` class → `.vis` class via IntersectionObserver (threshold: 0.15)
- **Scroll progress**: Fixed top bar tracking page scroll
- **Hover**: `transform: translate(-3px, -3px)` + enhanced shadow

### Responsive Breakpoints
- Desktop: default
- Tablet: `@media (max-width: 900px)` — single column, smaller fonts
- Mobile: `@media (max-width: 600px)` — stacked layout, adjusted padding

### Rules
1. Always use the CSS variables, never hardcode colors
2. All interactive elements get border + shadow treatment
3. Use `.rv` class on elements that should animate on scroll
4. JetBrains Mono for all labels, tags, and metadata text
5. Minimum touch target: 44px on mobile
6. Every section should work without JavaScript (progressive enhancement)
