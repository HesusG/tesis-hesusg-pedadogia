/**
 * app.js — Main application logic
 * Data loading, navigation, scroll animations, counters,
 * policy grid, cluster details, profile selector, scrollytelling
 */

// ── State ──
let DATA = null;

// ── Abbreviated label map (shared with charts.js) ──
const APP_ABBR = {
    eu_ai_act_2024: 'UE',
    espana_enia_2020: 'ES',
    francia_villani_report_2018: 'FR',
    canada_pan_canadian_ai_strategy_2017: 'CA',
    brasil_ebia_2021: 'BR',
    colombia_conpes_3975_2019: 'CO',
    japon_ai_strategy_2019: 'JP',
    corea_ai_strategy_2019: 'KR',
    singapur_nais_2019: 'SG',
    india_aiforall_2018: 'IN₁',
    india_nep_2020: 'IN₂',
    australia_ai_action_plan_2021: 'AU',
    unesco_genai_guidance_2023: 'UN',
    wef_future_of_jobs_2020: 'WEF',
};

// ── Data Loading ──
async function loadData() {
    try {
        const response = await fetch('data/results.json');
        if (!response.ok) {
            console.warn('No results.json found. Using placeholder data.');
            return getPlaceholderData();
        }
        return await response.json();
    } catch (e) {
        console.warn('Error loading data:', e);
        return getPlaceholderData();
    }
}

function getPlaceholderData() {
    return {
        policies: [],
        similarity_matrix: [],
        policy_ids: [],
        dimension_scores: {},
        dimension_labels: {
            gobernanza: 'Gobernanza y regulación',
            curriculo: 'Currículo e integración educativa',
            formacion_docente: 'Formación docente',
            infraestructura: 'Infraestructura y acceso',
            etica: 'Ética y valores',
            investigacion: 'Investigación e innovación',
            equidad: 'Equidad e inclusión',
        },
        clusters: {},
        region_colors: {
            europa: '#1976d2',
            americas: '#388e3c',
            asia_pacifico: '#d32f2f',
            internacional: '#7b1fa2',
        },
        metadata: {
            generated_at: null,
            embedding_model: 'pending',
            num_policies: 0,
        },
        tsne: [],
    };
}

// ── Animated Counter ──
function animateCounter(el, target, duration, isDecimal) {
    const start = performance.now();
    const format = isDecimal
        ? (v) => v.toFixed(3)
        : (v) => Math.round(v).toLocaleString('es-MX');

    function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = format(target * eased);
        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

// ── Progress Bar ──
function initProgress() {
    const bar = document.getElementById('progress');
    window.addEventListener('scroll', () => {
        const scrollTop = document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
        bar.style.width = progress + '%';
    });
}

// ── Side Navigation ──
function initSideNav() {
    const nav = document.getElementById('sidenav');
    const sections = document.querySelectorAll('section[id], header[id]');

    sections.forEach((section, i) => {
        if (i > 0) {
            const line = document.createElement('div');
            line.className = 'nav-line';
            nav.appendChild(line);
        }
        const dot = document.createElement('div');
        dot.className = 'nav-dot';
        const heading = section.querySelector('h2,h1');
        dot.dataset.label = heading ? heading.textContent.substring(0, 25) : '';
        dot.addEventListener('click', () => {
            section.scrollIntoView({ behavior: 'smooth' });
        });
        nav.appendChild(dot);
    });

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const index = Array.from(sections).indexOf(entry.target);
                    const dots = nav.querySelectorAll('.nav-dot');
                    dots.forEach((d, i) => d.classList.toggle('active', i === index));
                }
            });
        },
        { threshold: 0.3 }
    );

    sections.forEach((s) => observer.observe(s));
}

// ── Scroll Reveal with Counters ──
function initReveal() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('vis');

                    // Animate counters within revealed element
                    entry.target.querySelectorAll('[data-counter]').forEach(c => {
                        if (c.dataset.counted) return;
                        c.dataset.counted = 'true';
                        const target = parseFloat(c.dataset.counter);
                        const isDecimal = c.dataset.decimal === 'true';
                        animateCounter(c, target, 1500, isDecimal);
                    });

                    // Stagger grid children
                    if (entry.target.classList.contains('stagger-grid')) {
                        staggeredReveal(entry.target);
                    }
                }
            });
        },
        { threshold: 0.1 }
    );

    document.querySelectorAll('.rv').forEach((el) => observer.observe(el));
}

// ── Staggered Reveal for Grid Children ──
function staggeredReveal(container) {
    const children = container.children;
    Array.from(children).forEach((child, i) => {
        child.style.transitionDelay = `${i * 0.05}s`;
    });
}

// ── Collapsibles ──
function initCollapsibles() {
    document.querySelectorAll('.rb-header').forEach((header) => {
        header.addEventListener('click', () => {
            header.parentElement.classList.toggle('open');
        });
    });
}

// ── Scrollytelling: Lazy Chart Rendering ──
function initScrollytelling() {
    const findingCharts = {
        'finding-triangle': { rendered: false, fn: () => renderFindingTriangle(DATA) },
        'finding-cluster1': { rendered: false, fn: () => renderFindingCluster1(DATA) },
        'finding-geography': { rendered: false, fn: () => renderFindingGeography(DATA) },
        'finding-teacher': { rendered: false, fn: () => renderFindingTeacherGap(DATA) },
        'finding-outlier': { rendered: false, fn: () => renderFindingOutlier(DATA) },
    };

    // Lazy-rendered new visualizations
    const lazyViz = {
        'network': { rendered: false, fn: () => { if (typeof renderNetwork === 'function') renderNetwork(DATA); } },
        'dendrogram': { rendered: false, fn: () => { if (typeof renderDendrogram === 'function') renderDendrogram(DATA); } },
        'sankey': { rendered: false, fn: () => { if (typeof renderSankey === 'function') renderSankey(DATA); } },
        'parallel': { rendered: false, fn: () => { if (typeof renderParallelCoords === 'function') renderParallelCoords(DATA); } },
    };

    const pairSection = document.getElementById('pairs');
    let pairsAnimated = false;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;

                // Finding charts
                const canvas = entry.target.querySelector('canvas');
                if (canvas && findingCharts[canvas.id] && !findingCharts[canvas.id].rendered) {
                    findingCharts[canvas.id].rendered = true;
                    findingCharts[canvas.id].fn();
                }

                // Lazy new visualizations
                const sectionId = entry.target.id;
                if (lazyViz[sectionId] && !lazyViz[sectionId].rendered) {
                    lazyViz[sectionId].rendered = true;
                    lazyViz[sectionId].fn();
                }

                // Pair bar animations
                if (sectionId === 'pairs' && !pairsAnimated) {
                    pairsAnimated = true;
                    setTimeout(() => {
                        if (typeof animatePairBars === 'function') animatePairBars();
                    }, 300);
                }

                // Pipeline step animations
                if (sectionId === 'methodology') {
                    const steps = entry.target.querySelectorAll('.pipeline-step');
                    steps.forEach((step, i) => {
                        setTimeout(() => step.classList.add('vis'), i * 150);
                    });
                }
            });
        },
        { threshold: 0.15 }
    );

    // Observe finding sections
    document.querySelectorAll('.finding').forEach(f => observer.observe(f));

    // Observe dark sections for pair animations
    if (pairSection) observer.observe(pairSection);

    // Observe methodology
    const methSection = document.getElementById('methodology');
    if (methSection) observer.observe(methSection);

    // Observe new visualization sections
    ['network', 'dendrogram', 'sankey', 'parallel'].forEach(id => {
        const el = document.getElementById(id);
        if (el) observer.observe(el);
    });
}

// ── Policy type and language maps ──
const POLICY_TYPES = {
    eu_ai_act_2024: 'Ley',
    espana_enia_2020: 'Estrategia nacional',
    francia_villani_report_2018: 'Reporte',
    canada_pan_canadian_ai_strategy_2017: 'Estrategia nacional',
    brasil_ebia_2021: 'Estrategia nacional',
    colombia_conpes_3975_2019: 'Política pública (CONPES)',
    japon_ai_strategy_2019: 'Estrategia nacional',
    corea_ai_strategy_2019: 'Estrategia nacional',
    singapur_nais_2019: 'Estrategia nacional',
    india_aiforall_2018: 'Estrategia nacional',
    india_nep_2020: 'Política educativa',
    australia_ai_action_plan_2021: 'Plan de acción',
    unesco_genai_guidance_2023: 'Guía sectorial',
    wef_future_of_jobs_2020: 'Reporte',
};

const POLICY_LANGS = {
    eu_ai_act_2024: 'en',
    espana_enia_2020: 'es',
    francia_villani_report_2018: 'fr',
    canada_pan_canadian_ai_strategy_2017: 'en',
    brasil_ebia_2021: 'pt',
    colombia_conpes_3975_2019: 'es',
    japon_ai_strategy_2019: 'en',
    corea_ai_strategy_2019: 'en',
    singapur_nais_2019: 'en',
    india_aiforall_2018: 'en',
    india_nep_2020: 'en',
    australia_ai_action_plan_2021: 'en',
    unesco_genai_guidance_2023: 'en',
    wef_future_of_jobs_2020: 'en',
};

// ── Navigate to Profile (reused by cards, UMAP click, network click) ──
function navigateToProfile(policyId) {
    const section = document.getElementById('profiles');
    if (!section) return;
    section.scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => {
        const btns = document.querySelectorAll('#profile-buttons button');
        btns.forEach(btn => btn.classList.remove('active'));
        const idx = DATA.policy_ids.indexOf(policyId);
        if (idx >= 0 && btns[idx]) {
            btns[idx].classList.add('active');
            const p = DATA.policies[idx];
            if (p) {
                btns[idx].style.background = p.region_color;
                btns[idx].style.color = '#fff';
            }
        }
        showProfile(policyId);
    }, 600);
}

// ── Policy Grid (14 cards with type + language — clickable) ──
function renderPolicyGrid() {
    const grid = document.getElementById('policy-grid');
    if (!DATA || !DATA.policies.length || !grid) return;

    grid.innerHTML = '';

    DATA.policies.forEach((p) => {
        const card = document.createElement('div');
        card.className = 'policy-card clickable';
        card.style.borderLeftColor = p.region_color;

        const docType = POLICY_TYPES[p.id] || 'Documento';
        const lang = POLICY_LANGS[p.id] || 'en';

        card.innerHTML = `
            <div class="pc-country">${p.country}</div>
            <div class="pc-meta-row">
                <span class="pc-year">${p.year}</span>
                <span class="policy-lang">${lang}</span>
            </div>
            <div class="pc-title">${p.title}</div>
            <div class="policy-type" style="border-color:${p.region_color};color:${p.region_color}">${docType}</div>
        `;
        card.addEventListener('click', () => navigateToProfile(p.id));
        grid.appendChild(card);
    });
}


// ── Cluster Details (with mini radars) ──
function renderClusterDetails() {
    const container = document.getElementById('cluster-details');
    if (!DATA || !DATA.clusters || !container) return;

    const clusterInfo = {
        1: {
            name: 'Cluster 1: Estrategias Tecnológicas',
            desc: 'Políticas orientadas a investigación, innovación y desarrollo de talento en IA. Priorizan las dimensiones de currículo e investigación por encima de gobernanza y equidad. Incluye políticas de países con enfoques pragmáticos y orientados al mercado.',
            accent: '#d32f2f',
        },
        2: {
            name: 'Cluster 2: Estrategias Integrales',
            desc: 'Políticas con enfoque multidimensional: gobernanza, equidad, formación y tecnología. Representan una visión holística de la educación en IA. Incluye a los tres países iberoamericanos, que son los más similares entre sí en todo el corpus.',
            accent: '#388e3c',
        },
        3: {
            name: 'Cluster 3: Regulación (Outlier)',
            desc: 'El EU AI Act es un texto legislativo con vocabulario jurídico especializado que lo separa radicalmente del resto del corpus. Fuerte en gobernanza y ética, débil en currículo y formación docente.',
            accent: '#1976d2',
        },
    };

    container.innerHTML = '';

    for (const [cid, members] of Object.entries(DATA.clusters)) {
        const info = clusterInfo[cid] || { name: `Cluster ${cid}`, desc: '', accent: '#999' };

        const memberTags = members.map(pid => {
            const p = DATA.policies.find(pol => pol.id === pid);
            return p
                ? `<span class="region-tag" style="background:${p.region_color};font-size:0.75rem;margin:0.15rem">${p.country}</span>`
                : pid;
        }).join(' ');

        const canvasId = `cluster-radar-${cid}`;

        const panel = document.createElement('div');
        panel.className = 'cluster-detail';
        panel.innerHTML = `
            <h3>${info.name}</h3>
            <div class="cluster-desc">${info.desc}</div>
            <div class="cluster-members">${memberTags}</div>
            <div class="cluster-radar-wrap">
                <canvas id="${canvasId}" height="200"></canvas>
            </div>
        `;
        container.appendChild(panel);

        // Render mini radar after DOM insertion
        setTimeout(() => {
            if (typeof renderClusterRadar === 'function') {
                renderClusterRadar(canvasId, members, DATA);
            }
        }, 100);
    }
}

// ── Profile Selector ──
function renderProfileSelector() {
    const container = document.getElementById('profile-buttons');
    if (!DATA || !DATA.policies.length || !container) return;

    container.innerHTML = '';
    DATA.policies.forEach(p => {
        const btn = document.createElement('button');
        btn.textContent = APP_ABBR[p.id] || p.country;
        btn.style.borderColor = p.region_color;
        btn.addEventListener('click', () => {
            container.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            btn.style.background = p.region_color;
            btn.style.color = '#fff';
            showProfile(p.id);
        });
        container.appendChild(btn);
    });
}

function showProfile(policyId) {
    const info = document.getElementById('profile-info');
    if (!DATA || !info) return;

    const policy = DATA.policies.find(p => p.id === policyId);
    if (!policy) return;

    const idx = DATA.policy_ids.indexOf(policyId);
    const sims = DATA.similarity_matrix[idx]
        .map((v, i) => ({ id: DATA.policy_ids[i], value: v }))
        .filter(s => s.id !== policyId);

    const avgSim = sims.reduce((s, v) => s + v.value, 0) / sims.length;
    const mostSimilar = sims.reduce((a, b) => a.value > b.value ? a : b);
    const leastSimilar = sims.reduce((a, b) => a.value < b.value ? a : b);

    // Find cluster
    let clusterName = '—';
    for (const [cid, members] of Object.entries(DATA.clusters)) {
        if (members.includes(policyId)) {
            clusterName = `Cluster ${cid}`;
            break;
        }
    }

    const mostP = DATA.policies.find(p => p.id === mostSimilar.id);
    const leastP = DATA.policies.find(p => p.id === leastSimilar.id);

    info.innerHTML = `
        <h3 style="color:${policy.region_color}">${policy.country}</h3>
        <div class="profile-meta">${policy.title} (${policy.year})</div>
        <div class="profile-stats">
            <div class="ps-item">
                <div class="ps-value">${avgSim.toFixed(3)}</div>
                <div class="ps-label">Sim. promedio</div>
            </div>
            <div class="ps-item">
                <div class="ps-value">${clusterName}</div>
                <div class="ps-label">Agrupación</div>
            </div>
            <div class="ps-item">
                <div class="ps-value" style="font-size:0.9rem">${mostP?.country || mostSimilar.id}</div>
                <div class="ps-label">Más similar (${mostSimilar.value.toFixed(3)})</div>
            </div>
            <div class="ps-item">
                <div class="ps-value" style="font-size:0.9rem">${leastP?.country || leastSimilar.id}</div>
                <div class="ps-label">Menos similar (${leastSimilar.value.toFixed(3)})</div>
            </div>
        </div>
    `;

    // Render profile charts
    if (typeof renderProfileRadar === 'function') renderProfileRadar(policyId, DATA);
    if (typeof renderProfileBar === 'function') renderProfileBar(policyId, DATA);
}

// ── Explainer Tabs ──
function initExplainerTabs() {
    const tabs = document.querySelectorAll('#explainer-tabs button');
    const panels = document.querySelectorAll('.explainer-panel');
    if (!tabs.length) return;

    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            tabs.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            const panel = document.querySelector(`.explainer-panel[data-panel="${btn.dataset.tab}"]`);
            if (panel) panel.classList.add('active');
            // Render viz for the active panel
            renderExplainerViz(btn.dataset.tab);
        });
    });
}

// ── Explainer Visualizations ──
const explainerRendered = {};
function renderExplainerViz(tab) {
    if (explainerRendered[tab]) return;
    explainerRendered[tab] = true;

    if (tab === 'embeddings') renderExplainerEmbeddings();
    if (tab === 'similarity') renderExplainerSimilarity();
    if (tab === 'dimensions') renderExplainerDimensions();
}

function renderExplainerEmbeddings() {
    const canvas = document.getElementById('explainer-embed-viz');
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    const w = 320, h = 220;
    canvas.width = w * dpr; canvas.height = h * dpr;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    // Show 3 "documents" as colored dots in a 2D space
    const docs = [
        { x: 80, y: 70, label: 'España', color: '#388e3c' },
        { x: 110, y: 90, label: 'Brasil', color: '#388e3c' },
        { x: 95, y: 55, label: 'Colombia', color: '#388e3c' },
        { x: 250, y: 160, label: 'EU AI Act', color: '#1976d2' },
    ];

    // Grid
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    for (let i = 0; i < 8; i++) {
        ctx.beginPath(); ctx.moveTo(i * 40, 0); ctx.lineTo(i * 40, h); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, i * 30); ctx.lineTo(w, i * 30); ctx.stroke();
    }

    // Draw connecting line between close docs
    ctx.strokeStyle = 'rgba(255,213,79,0.3)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(80, 70); ctx.lineTo(110, 90); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(110, 90); ctx.lineTo(95, 55); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(80, 70); ctx.lineTo(95, 55); ctx.stroke();
    ctx.setLineDash([]);

    // Annotation
    ctx.font = "italic 10px 'DM Sans', sans-serif";
    ctx.fillStyle = 'rgba(255,255,255,0.4)';
    ctx.textAlign = 'center';
    ctx.fillText('cerca = temas parecidos', 95, 120);
    ctx.fillText('lejos = temas distintos', 200, 130);

    // Dots
    docs.forEach(d => {
        ctx.beginPath();
        ctx.arc(d.x, d.y, 10, 0, Math.PI * 2);
        ctx.fillStyle = d.color;
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.fillStyle = '#fff';
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(d.label, d.x, d.y + 15);
    });

    // Arrow between groups
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 5]);
    ctx.beginPath(); ctx.moveTo(130, 90); ctx.lineTo(230, 155); ctx.stroke();
    ctx.setLineDash([]);

    // Title
    ctx.font = "bold 11px 'Syne', sans-serif";
    ctx.fillStyle = '#FFD54F';
    ctx.textAlign = 'left';
    ctx.fillText('Espacio vectorial (simplificado)', 10, 200);
}

function renderExplainerSimilarity() {
    const canvas = document.getElementById('explainer-sim-viz');
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    const w = 320, h = 220;
    canvas.width = w * dpr; canvas.height = h * dpr;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    // Draw a simple scale bar from 0 to 1
    const barY = 60, barH = 30, barX = 30, barW = 260;
    const steps = 50;
    for (let s = 0; s < steps; s++) {
        const t = s / (steps - 1);
        const v = 0.4 + t * 0.6;
        ctx.fillStyle = heatmapColor(v);
        ctx.fillRect(barX + (barW / steps) * s, barY, barW / steps + 1, barH);
    }
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.strokeRect(barX, barY, barW, barH);

    // Labels
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.fillText('0.40', barX, barY + barH + 16);
    ctx.fillText('0.70', barX + barW / 2, barY + barH + 16);
    ctx.fillText('1.00', barX + barW, barY + barH + 16);

    // Markers for key pairs
    const markers = [
        { v: 0.416, label: 'UE↔WEF', y: barY - 8 },
        { v: 0.965, label: 'ES↔BR', y: barY - 8 },
        { v: 0.750, label: 'Mayoría', y: barY - 8 },
    ];
    markers.forEach(m => {
        const mx = barX + ((m.v - 0.4) / 0.6) * barW;
        ctx.strokeStyle = '#FFD54F';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(mx, barY); ctx.lineTo(mx, barY - 14); ctx.stroke();
        ctx.fillStyle = '#FFD54F';
        ctx.font = "bold 9px 'JetBrains Mono', monospace";
        ctx.textAlign = 'center';
        ctx.fillText(m.label, mx, barY - 18);
    });

    // Bottom explanation
    ctx.font = "10px 'DM Sans', sans-serif";
    ctx.fillStyle = 'rgba(255,255,255,0.5)';
    ctx.textAlign = 'left';
    ctx.fillText('← Muy distintos', barX, barY + barH + 40);
    ctx.textAlign = 'right';
    ctx.fillText('Casi idénticos →', barX + barW, barY + barH + 40);

    ctx.font = "bold 11px 'Syne', sans-serif";
    ctx.fillStyle = '#FFD54F';
    ctx.textAlign = 'left';
    ctx.fillText('Escala de similitud coseno', 10, 200);
}

function renderExplainerDimensions() {
    const canvas = document.getElementById('explainer-dim-viz');
    if (!canvas) return;
    if (!DATA || !DATA.dimension_labels) return;
    const dpr = window.devicePixelRatio || 1;
    const w = 320, h = 220;
    canvas.width = w * dpr; canvas.height = h * dpr;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    // Show avg score per dimension as horizontal bars
    const dimKeys = Object.keys(DATA.dimension_labels);
    const dimLabels = Object.values(DATA.dimension_labels);
    const avgs = dimKeys.map(k => {
        const scores = DATA.policies.map(p => DATA.dimension_scores[p.id]?.[k] || 0).filter(v => v > 0);
        return scores.length > 0 ? scores.reduce((s, v) => s + v, 0) / scores.length : 0;
    });

    const barH = 18;
    const gap = 6;
    const labelW = 100;
    const maxBarW = 180;
    const startY = 15;

    dimLabels.forEach((label, i) => {
        const y = startY + i * (barH + gap);
        const shortLabel = label.split(' ')[0];
        const bw = (avgs[i] / 0.8) * maxBarW;

        // Bar
        ctx.fillStyle = '#FFD54F';
        ctx.globalAlpha = 0.15 + (avgs[i] / 0.8) * 0.7;
        ctx.fillRect(labelW, y, bw, barH);
        ctx.globalAlpha = 1;
        ctx.strokeStyle = 'rgba(255,255,255,0.2)';
        ctx.lineWidth = 1;
        ctx.strokeRect(labelW, y, maxBarW, barH);

        // Label
        ctx.font = "10px 'JetBrains Mono', monospace";
        ctx.fillStyle = '#ccc';
        ctx.textAlign = 'right';
        ctx.textBaseline = 'middle';
        ctx.fillText(shortLabel, labelW - 8, y + barH / 2);

        // Score
        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.fillStyle = '#FFD54F';
        ctx.textAlign = 'left';
        ctx.fillText(avgs[i].toFixed(3), labelW + bw + 6, y + barH / 2);
    });

    ctx.font = "bold 11px 'Syne', sans-serif";
    ctx.fillStyle = '#FFD54F';
    ctx.textAlign = 'left';
    ctx.fillText('Promedio por dimensión (14 políticas)', 10, 200);
}

// ── Initialize ──
async function init() {
    DATA = await loadData();

    initProgress();
    initSideNav();

    // Render data-driven components
    renderPolicyGrid();
    renderClusterDetails();
    renderProfileSelector();

    // Initialize scroll animations
    initReveal();
    initCollapsibles();

    // Initialize charts if data is available
    if (DATA.policies.length > 0 && typeof initCharts === 'function') {
        initCharts(DATA);
    }

    // Explainer tabs + initial viz
    initExplainerTabs();
    renderExplainerViz('embeddings');

    // Scrollytelling for lazy chart rendering
    initScrollytelling();

    // Hero counters fire after initial load
    setTimeout(() => {
        document.querySelectorAll('#hero [data-counter]').forEach(c => {
            if (c.dataset.counted) return;
            c.dataset.counted = 'true';
            const target = parseFloat(c.dataset.counter);
            animateCounter(c, target, 1500, false);
        });
    }, 500);
}

document.addEventListener('DOMContentLoaded', init);
