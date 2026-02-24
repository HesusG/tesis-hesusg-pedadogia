/**
 * charts.js — Chart.js visualizations
 * Heatmap, Radar, Histogram, t-SNE, Dimension Comparison,
 * Cluster Radars, Finding Charts, Profile Charts
 */

// ── Region color map ──
const REGION_COLORS = {
    europa: '#1976d2',
    americas: '#388e3c',
    asia_pacifico: '#d32f2f',
    internacional: '#7b1fa2',
};

// ── Abbreviated labels ──
const ABBR_MAP = {
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

// ── Chart instances ──
let radarChart = null;
let profileRadarChart = null;
let profileBarChart = null;

// ── Heatmap color interpolation (white → yellow → orange → deep red) ──
function heatmapColorRGB(v) {
    const t = Math.max(0, Math.min(1, (v - 0.4) / 0.6)); // normalize 0.4–1.0 → 0–1
    let r, g, b;
    if (t < 0.33) {
        const s = t / 0.33;
        r = 255; g = Math.round(255 - s * 42); b = Math.round(255 - s * 176);
    } else if (t < 0.66) {
        const s = (t - 0.33) / 0.33;
        r = 255; g = Math.round(213 - s * 100); b = Math.round(79 - s * 42);
    } else {
        const s = (t - 0.66) / 0.34;
        r = Math.round(255 - s * 72); g = Math.round(113 - s * 85); b = Math.round(37 - s * 9);
    }
    return { r, g, b };
}

function heatmapColor(v) {
    const { r, g, b } = heatmapColorRGB(v);
    return `rgb(${r},${g},${b})`;
}

// ── Compute all 91 upper-triangle pairs ──
function computeAllPairs(data) {
    const pairs = [];
    const n = data.policies.length;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            pairs.push({
                i, j,
                idA: data.policies[i].id,
                idB: data.policies[j].id,
                labelA: ABBR_MAP[data.policies[i].id] || data.policies[i].country,
                labelB: ABBR_MAP[data.policies[j].id] || data.policies[j].country,
                countryA: data.policies[i].country,
                countryB: data.policies[j].country,
                colorA: data.policies[i].region_color,
                colorB: data.policies[j].region_color,
                value: data.similarity_matrix[i][j],
            });
        }
    }
    pairs.sort((a, b) => b.value - a.value);
    return pairs;
}

// ── Initialize all charts ──
function initCharts(data) {
    const allPairs = computeAllPairs(data);

    if (data.similarity_matrix && data.similarity_matrix.length > 0) {
        renderHeatmap(data);
        renderHistogram(data, allPairs);
        renderPairExtremes(data, allPairs);
    }
    if (data.policies.length > 0) {
        renderRadarControls(data);
        initRadarPresets(data);
    }
    if (data.umap && data.umap.length > 0) {
        renderUMAP(data);
    } else if (data.tsne && data.tsne.length > 0) {
        renderUMAP(data); // falls back to tsne coords inside
    }

    // Finding charts (lazy — rendered when visible via scrollytelling)
    window._findingData = { data, allPairs };
}

// ── Custom Canvas Heatmap ──
function renderHeatmap(data) {
    const canvas = document.getElementById('heatmap-chart');
    if (!canvas) return;

    const labels = data.policies.map(p => ABBR_MAP[p.id] || p.country);
    const fullNames = data.policies.map(p => p.country);
    const regionColors = data.policies.map(p => p.region_color);
    const matrix = data.similarity_matrix;
    const n = labels.length;

    // Cluster membership for border overlays
    const clusterMembers = data.clusters || {};
    const clusterBorders = Object.entries(clusterMembers).map(([cid, members]) => {
        const indices = members.map(id => data.policy_ids.indexOf(id)).filter(i => i >= 0).sort((a, b) => a - b);
        return { id: cid, indices };
    });

    const dpr = window.devicePixelRatio || 1;
    const labelMargin = 60;
    const legendHeight = 40;
    const topMargin = 60;

    function draw() {
        const containerWidth = canvas.parentElement.clientWidth - 32;
        const totalSize = Math.min(containerWidth, 700);
        const gridSize = totalSize - labelMargin;
        const cellSize = gridSize / n;
        const canvasW = totalSize;
        const canvasH = totalSize + legendHeight + 10;

        canvas.width = canvasW * dpr;
        canvas.height = canvasH * dpr;
        canvas.style.width = canvasW + 'px';
        canvas.style.height = canvasH + 'px';

        const ctx = canvas.getContext('2d');
        ctx.scale(dpr, dpr);
        ctx.clearRect(0, 0, canvasW, canvasH);

        const ox = labelMargin;
        const oy = topMargin;

        // Draw cells
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                const v = matrix[i][j];
                const x = ox + j * cellSize;
                const y = oy + i * cellSize;

                // Cell fill
                ctx.fillStyle = heatmapColor(v);
                ctx.fillRect(x, y, cellSize, cellSize);

                // Diagonal hatching
                if (i === j) {
                    ctx.fillStyle = 'rgba(0,0,0,0.06)';
                    ctx.fillRect(x, y, cellSize, cellSize);
                }

                // Cell border
                ctx.strokeStyle = 'rgba(0,0,0,0.08)';
                ctx.lineWidth = 0.5;
                ctx.strokeRect(x, y, cellSize, cellSize);

                // Value text
                const { r, g, b } = heatmapColorRGB(v);
                const lum = 0.299 * r + 0.587 * g + 0.114 * b;
                ctx.fillStyle = lum < 160 ? '#fff' : '#1a1a1a';
                ctx.font = `${Math.max(8, cellSize * 0.28)}px 'JetBrains Mono', monospace`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(v.toFixed(2), x + cellSize / 2, y + cellSize / 2);
            }
        }

        // Y-axis labels (left)
        ctx.textAlign = 'right';
        ctx.textBaseline = 'middle';
        for (let i = 0; i < n; i++) {
            ctx.fillStyle = regionColors[i];
            ctx.font = `bold ${Math.max(9, cellSize * 0.32)}px 'JetBrains Mono', monospace`;
            ctx.fillText(labels[i], ox - 6, oy + i * cellSize + cellSize / 2);
        }

        // X-axis labels (top)
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        for (let j = 0; j < n; j++) {
            ctx.save();
            ctx.translate(ox + j * cellSize + cellSize / 2, oy - 6);
            ctx.rotate(-Math.PI / 4);
            ctx.fillStyle = regionColors[j];
            ctx.font = `bold ${Math.max(9, cellSize * 0.32)}px 'JetBrains Mono', monospace`;
            ctx.textAlign = 'right';
            ctx.fillText(labels[j], 0, 0);
            ctx.restore();
        }

        // Cluster border overlays
        const clusterColors = { '1': '#d32f2f', '2': '#388e3c', '3': '#1976d2' };
        clusterBorders.forEach(({ id, indices }) => {
            if (indices.length < 2) return;
            const min = indices[0];
            const max = indices[indices.length - 1];
            const cx = ox + min * cellSize - 2;
            const cy = oy + min * cellSize - 2;
            const cw = (max - min + 1) * cellSize + 4;
            ctx.strokeStyle = clusterColors[id] || '#999';
            ctx.lineWidth = 2.5;
            ctx.setLineDash([6, 4]);
            ctx.strokeRect(cx, cy, cw, cw);
            ctx.setLineDash([]);
        });

        // Color legend bar
        const legendY = oy + n * cellSize + 20;
        const legendW = gridSize * 0.7;
        const legendX = ox + (gridSize - legendW) / 2;
        const legendH = 14;
        const steps = 60;
        for (let s = 0; s < steps; s++) {
            const t = s / (steps - 1);
            const v = 0.4 + t * 0.6;
            ctx.fillStyle = heatmapColor(v);
            ctx.fillRect(legendX + (legendW / steps) * s, legendY, legendW / steps + 1, legendH);
        }
        ctx.strokeStyle = '#1a1a1a';
        ctx.lineWidth = 1.5;
        ctx.strokeRect(legendX, legendY, legendW, legendH);

        // Legend labels
        ctx.fillStyle = '#1a1a1a';
        ctx.font = "11px 'JetBrains Mono', monospace";
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText('0.40', legendX, legendY + legendH + 4);
        ctx.fillText('0.70', legendX + legendW / 2, legendY + legendH + 4);
        ctx.fillText('1.00', legendX + legendW, legendY + legendH + 4);
    }

    draw();

    // Tooltip on hover
    const tooltip = document.createElement('div');
    tooltip.style.cssText = 'position:fixed;background:#1a1a1a;color:#F5F0E8;padding:6px 10px;font:12px "JetBrains Mono",monospace;pointer-events:none;z-index:9999;display:none;border:2px solid #FFD54F;box-shadow:3px 3px 0 rgba(0,0,0,0.3)';
    document.body.appendChild(tooltip);

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const gridSize = (Math.min(canvas.parentElement.clientWidth - 32, 700)) - labelMargin;
        const cellSize = gridSize / n;
        const col = Math.floor((mx - labelMargin) / cellSize);
        const row = Math.floor((my - topMargin) / cellSize);

        if (col >= 0 && col < n && row >= 0 && row < n) {
            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 12) + 'px';
            tooltip.style.top = (e.clientY - 30) + 'px';
            tooltip.textContent = `${fullNames[row]} ↔ ${fullNames[col]}: ${matrix[row][col].toFixed(3)}`;
        } else {
            tooltip.style.display = 'none';
        }
    });

    canvas.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
    });

    // Redraw on resize
    window.addEventListener('resize', draw);
}

// ── Histogram of all similarity pairs ──
function renderHistogram(data, allPairs) {
    const ctx = document.getElementById('histogram-chart');
    if (!ctx) return;

    const values = allPairs.map(p => p.value);
    const binCount = 10;
    const min = 0.40;
    const max = 1.00;
    const binWidth = (max - min) / binCount;
    const bins = new Array(binCount).fill(0);
    const binLabels = [];

    for (let i = 0; i < binCount; i++) {
        const lo = min + i * binWidth;
        binLabels.push(`${lo.toFixed(2)}–${(lo + binWidth).toFixed(2)}`);
    }

    values.forEach(v => {
        const idx = Math.min(Math.floor((v - min) / binWidth), binCount - 1);
        if (idx >= 0) bins[idx]++;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: binLabels,
            datasets: [{
                label: 'Pares',
                data: bins,
                backgroundColor: bins.map((_, i) => {
                    const t = i / (binCount - 1);
                    return `rgba(${Math.round(255 * (1 - t * 0.3))}, ${Math.round(213 - t * 160)}, ${Math.round(79 - t * 30)}, 0.8)`;
                }),
                borderColor: '#1a1a1a',
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.raw} pares`,
                    },
                },
            },
            scales: {
                x: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 9 }, maxRotation: 45 },
                    grid: { display: false },
                },
                y: {
                    beginAtZero: true,
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 }, stepSize: 5 },
                    title: { display: true, text: 'Cantidad de pares', font: { family: "'DM Sans'" } },
                },
            },
        },
    });

    // Stats panel
    renderSimilarityStats(values);
}

// ── Similarity Stats ──
function renderSimilarityStats(values) {
    const panel = document.getElementById('similarity-stats');
    if (!panel) return;

    const sorted = [...values].sort((a, b) => a - b);
    const mean = values.reduce((s, v) => s + v, 0) / values.length;
    const median = sorted.length % 2 === 0
        ? (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2
        : sorted[Math.floor(sorted.length / 2)];
    const stdDev = Math.sqrt(values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length);

    const stats = [
        { label: 'Media', value: mean.toFixed(3) },
        { label: 'Mediana', value: median.toFixed(3) },
        { label: 'Mínimo', value: sorted[0].toFixed(3) },
        { label: 'Máximo', value: sorted[sorted.length - 1].toFixed(3) },
        { label: 'Desv. Est.', value: stdDev.toFixed(3) },
    ];

    panel.innerHTML = stats.map(s =>
        `<div class="stat-box">
            <div class="stat-value" data-counter="${s.value}" data-decimal="true">${s.value}</div>
            <div class="stat-label">${s.label}</div>
        </div>`
    ).join('');
}

// ── Pair Extremes (top/bottom 10) with glows ──
function renderPairExtremes(data, allPairs) {
    const topContainer = document.getElementById('top-pairs');
    const bottomContainer = document.getElementById('bottom-pairs');
    if (!topContainer || !bottomContainer) return;

    const top10 = allPairs.slice(0, 10);
    const bottom10 = [...allPairs].reverse().slice(0, 10);

    function renderPairs(container, pairs, colorFn, glowClass, isTop) {
        container.innerHTML = pairs.map((p, i) => {
            const pct = ((p.value - 0.4) / 0.6) * 100;
            const glow = i < 3 ? glowClass : '';
            const marker = i === 0 ? '<span style="margin-right:2px">★</span>' : '';
            return `<div class="pair-row">
                <span class="pair-left" style="color:${p.colorA}">${p.labelA}</span>
                <div class="pair-bar-wrap">
                    <div class="pair-bar" style="--bar-width:${pct}%;background:${colorFn(p)}" data-fill></div>
                </div>
                <span class="pair-right" style="color:${p.colorB}">${p.labelB}</span>
                <span class="pair-score ${glow}">${marker}${p.value.toFixed(3)}</span>
            </div>`;
        }).join('');
    }

    renderPairs(topContainer, top10, () => 'var(--yellow)', 'glow-yellow', true);
    renderPairs(bottomContainer, bottom10, () => 'rgba(255,255,255,0.3)', 'glow-red', false);
}

// ── Trigger pair bar animations ──
function animatePairBars() {
    document.querySelectorAll('.pair-bar[data-fill]').forEach(bar => {
        bar.classList.add('fill');
    });
}

// ── Plotly UMAP Scatter with Cluster Hulls ──
function renderUMAP(data) {
    const container = document.getElementById('umap-chart');
    if (!container) return;
    if (typeof Plotly === 'undefined') return;

    // Use UMAP coords if available, fall back to t-SNE
    const coords = data.umap || data.tsne;
    if (!coords || coords.length === 0) return;

    // Build cluster map
    const clusterMap = {};
    for (const [cid, members] of Object.entries(data.clusters || {})) {
        members.forEach(id => { clusterMap[id] = cid; });
    }

    const clusterNames = { '1': 'Tecnológico', '2': 'Integral', '3': 'Regulación' };
    const clusterColors = { '1': '#d32f2f', '2': '#388e3c', '3': '#1976d2' };

    // Group points by cluster
    const clusterGroups = {};
    data.policies.forEach((p, i) => {
        const cid = clusterMap[p.id] || '0';
        if (!clusterGroups[cid]) clusterGroups[cid] = { x: [], y: [], text: [], ids: [], labels: [] };
        clusterGroups[cid].x.push(coords[i][0]);
        clusterGroups[cid].y.push(coords[i][1]);
        clusterGroups[cid].text.push(`${p.country}<br>${p.title} (${p.year})`);
        clusterGroups[cid].ids.push(p.id);
        clusterGroups[cid].labels.push(ABBR_MAP[p.id] || p.country);
    });

    // Build traces
    const traces = [];
    const shapes = [];

    for (const [cid, group] of Object.entries(clusterGroups)) {
        const color = clusterColors[cid] || '#999';
        traces.push({
            x: group.x,
            y: group.y,
            text: group.text,
            customdata: group.ids,
            mode: 'markers+text',
            type: 'scatter',
            name: `Cluster ${cid}: ${clusterNames[cid] || cid}`,
            textposition: 'top center',
            textfont: { family: 'JetBrains Mono, monospace', size: 10, color: '#1a1a1a' },
            marker: {
                size: 18,
                color: color,
                line: { width: 2.5, color: '#1a1a1a' },
            },
            hovertemplate: '%{text}<extra></extra>',
            // Show abbreviated labels on each point
            text: group.labels,
        });

        // Convex hull shape for clusters with 3+ members
        if (group.x.length >= 3) {
            const hullPoints = computeConvexHull2D(group.x, group.y);
            if (hullPoints.length >= 3) {
                const path = 'M' + hullPoints.map(p => `${p[0]},${p[1]}`).join('L') + 'Z';
                shapes.push({
                    type: 'path',
                    path: path,
                    fillcolor: color + '15',
                    line: { color: color + '60', width: 2, dash: 'dash' },
                });
            }
        }
    }

    const layout = {
        showlegend: true,
        legend: { font: { family: 'DM Sans, sans-serif', size: 11 }, x: 0, y: 1 },
        xaxis: { showgrid: true, gridcolor: 'rgba(0,0,0,0.05)', zeroline: false, showticklabels: false, title: '' },
        yaxis: { showgrid: true, gridcolor: 'rgba(0,0,0,0.05)', zeroline: false, showticklabels: false, title: '' },
        shapes: shapes,
        margin: { l: 30, r: 30, t: 20, b: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        hovermode: 'closest',
        dragmode: 'pan',
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['lasso2d', 'select2d', 'autoScale2d'],
        displaylogo: false,
    };

    Plotly.newPlot(container, traces, layout, config);

    // Click to navigate to profile
    container.on('plotly_click', (eventData) => {
        const pt = eventData.points[0];
        if (pt && pt.customdata && typeof navigateToProfile === 'function') {
            navigateToProfile(pt.customdata);
        }
    });
}

// ── Convex hull helper for 2D points ──
function computeConvexHull2D(xs, ys) {
    const pts = xs.map((x, i) => [x, ys[i]]);
    if (pts.length < 3) return pts;

    pts.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);

    const lower = [];
    for (const p of pts) {
        while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], p) <= 0) lower.pop();
        lower.push(p);
    }
    const upper = [];
    for (const p of [...pts].reverse()) {
        while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], p) <= 0) upper.pop();
        upper.push(p);
    }
    upper.pop(); lower.pop();
    return lower.concat(upper);
}

// ── Plotly Sankey: Region → Cluster ──
function renderSankey(data) {
    const container = document.getElementById('sankey-chart');
    if (!container || !data.sankey) return;
    if (typeof Plotly === 'undefined') return;

    const sankey = data.sankey;
    const nodeIds = sankey.nodes.map(n => n.id);

    const regionColors = {
        europa: '#1976d2',
        americas: '#388e3c',
        asia_pacifico: '#d32f2f',
        internacional: '#7b1fa2',
    };

    const clusterColors = {
        cluster_1: '#d32f2f',
        cluster_2: '#388e3c',
        cluster_3: '#1976d2',
    };

    const nodeColors = sankey.nodes.map(n => {
        return regionColors[n.id] || clusterColors[n.id] || '#999';
    });

    const links = sankey.links.map(l => ({
        source: nodeIds.indexOf(l.source),
        target: nodeIds.indexOf(l.target),
        value: l.value,
        label: l.policies.join(', '),
        color: (regionColors[l.source] || '#999') + '55',
    }));

    const trace = {
        type: 'sankey',
        orientation: 'h',
        node: {
            pad: 20,
            thickness: 25,
            line: { color: '#1a1a1a', width: 2 },
            label: sankey.nodes.map(n => n.label),
            color: nodeColors,
            hovertemplate: '%{label}<extra></extra>',
        },
        link: {
            source: links.map(l => l.source),
            target: links.map(l => l.target),
            value: links.map(l => l.value),
            color: links.map(l => l.color),
            customdata: links.map(l => l.label),
            hovertemplate: '%{customdata}<extra></extra>',
        },
    };

    const layout = {
        font: { family: 'DM Sans, sans-serif', size: 13, color: '#F5F0E8' },
        margin: { l: 20, r: 20, t: 20, b: 20 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
    };

    Plotly.newPlot(container, [trace], layout, {
        responsive: true,
        displayModeBar: false,
    });
}

// ── Plotly Parallel Coordinates ──
function renderParallelCoords(data) {
    const container = document.getElementById('parallel-chart');
    if (!container) return;
    if (typeof Plotly === 'undefined') return;

    const dimKeys = Object.keys(data.dimension_labels);
    const dimLabels = Object.values(data.dimension_labels);

    const clusterMap = {};
    for (const [cid, members] of Object.entries(data.clusters || {})) {
        members.forEach(id => { clusterMap[id] = parseInt(cid); });
    }

    const clusterValues = data.policies.map(p => clusterMap[p.id] || 0);

    // Build dimension arrays
    const dimensions = dimKeys.map((k, i) => ({
        label: dimLabels[i].split(' ')[0],
        values: data.policies.map(p => data.dimension_scores[p.id]?.[k] || 0),
        range: [0, 0.8],
    }));

    const trace = {
        type: 'parcoords',
        line: {
            color: clusterValues,
            colorscale: [
                [0, '#999'],
                [0.33, '#d32f2f'],
                [0.66, '#388e3c'],
                [1, '#1976d2'],
            ],
            showscale: false,
        },
        dimensions: dimensions,
    };

    const layout = {
        font: { family: 'DM Sans, sans-serif', size: 12 },
        margin: { l: 80, r: 40, t: 30, b: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
    };

    Plotly.newPlot(container, [trace], layout, {
        responsive: true,
        displayModeBar: false,
    });
}

// ── Radar Controls ──
function renderRadarControls(data) {
    const controls = document.getElementById('radar-controls');
    if (!controls) return;

    controls.innerHTML = '';
    for (let i = 0; i < 3; i++) {
        const select = document.createElement('select');
        select.id = `radar-select-${i}`;
        select.style.cssText = "font-family:var(--font-mono);border:var(--border);padding:0.3rem 0.5rem;background:#fff;margin-right:0.5rem";

        const defaultOpt = document.createElement('option');
        defaultOpt.value = '';
        defaultOpt.textContent = i === 2 ? '(opcional)' : `Política ${i + 1}`;
        select.appendChild(defaultOpt);

        data.policies.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.id;
            opt.textContent = p.country;
            select.appendChild(opt);
        });

        select.addEventListener('change', () => updateRadar(data));
        controls.appendChild(select);
    }
}

// ── Radar Presets ──
function initRadarPresets(data) {
    const presets = {
        'iberoamerica': ['espana_enia_2020', 'brasil_ebia_2021', 'colombia_conpes_3975_2019'],
        'asia-tech': ['japon_ai_strategy_2019', 'corea_ai_strategy_2019', 'singapur_nais_2019'],
        'edu-vs-reg': ['unesco_genai_guidance_2023', 'eu_ai_act_2024', 'india_nep_2020'],
    };

    const buttons = document.querySelectorAll('#radar-presets button');
    const controls = document.getElementById('radar-controls');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const preset = btn.dataset.preset;
            if (preset === 'custom') {
                if (controls) controls.style.display = '';
                return;
            }

            if (controls) controls.style.display = 'none';
            const ids = presets[preset];
            if (ids) updateRadarWithIds(data, ids);
        });
    });

    // Start with Iberoamerica
    updateRadarWithIds(data, presets['iberoamerica']);
}

function updateRadarWithIds(data, policyIds) {
    const ctx = document.getElementById('radar-chart');
    if (!ctx) return;

    const dimKeys = Object.keys(data.dimension_labels);
    const dimLabels = Object.values(data.dimension_labels);
    // Fixed visually distinct palette (blue, red, gold)
    const fixedColors = ['#1976d2', '#d32f2f', '#FFD54F'];
    const fixedBorders = ['#1976d2', '#d32f2f', '#b8960a'];

    const datasets = policyIds.map((pid, i) => {
        const policy = data.policies.find(p => p.id === pid);
        const scores = data.dimension_scores[pid] || {};
        const values = dimKeys.map(k => scores[k] || 0);
        const color = fixedColors[i] || '#7b1fa2';
        const border = fixedBorders[i] || '#7b1fa2';

        return {
            label: policy?.country || pid,
            data: values,
            borderColor: border,
            backgroundColor: color + '22',
            borderWidth: 3,
            pointRadius: 5,
            pointBackgroundColor: color,
        };
    });

    if (radarChart) radarChart.destroy();

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: { labels: dimLabels, datasets },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 0.8,
                    ticks: { stepSize: 0.2, font: { family: "'JetBrains Mono'", size: 10 } },
                    pointLabels: { font: { family: "'DM Sans'", size: 11 } },
                },
            },
            plugins: {
                legend: { labels: { font: { family: "'DM Sans'" } } },
            },
        },
    });
}

function updateRadar(data) {
    const selected = [];
    for (let i = 0; i < 3; i++) {
        const sel = document.getElementById(`radar-select-${i}`);
        if (sel && sel.value) selected.push(sel.value);
    }
    if (selected.length < 2) return;
    updateRadarWithIds(data, selected);
}

// ── Cluster Radars ──
function renderClusterRadar(canvasId, memberIds, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const dimKeys = Object.keys(data.dimension_labels);
    const dimLabels = Object.values(data.dimension_labels);

    // Average scores across cluster members
    const avgScores = dimKeys.map(k => {
        const vals = memberIds
            .map(id => data.dimension_scores[id]?.[k] || 0)
            .filter(v => v > 0);
        return vals.length > 0 ? vals.reduce((s, v) => s + v, 0) / vals.length : 0;
    });

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: dimLabels.map(l => l.split(' ')[0]),
            datasets: [{
                label: 'Promedio',
                data: avgScores,
                borderColor: '#FFD54F',
                backgroundColor: 'rgba(255, 213, 79, 0.15)',
                borderWidth: 2,
                pointRadius: 3,
                pointBackgroundColor: '#FFD54F',
            }],
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 0.8,
                    ticks: { display: false },
                    pointLabels: { font: { family: "'JetBrains Mono'", size: 8 }, color: '#ccc' },
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    angleLines: { color: 'rgba(255,255,255,0.1)' },
                },
            },
            plugins: { legend: { display: false } },
        },
    });
}

// ── Finding: Iberoamerican Triangle ──
function renderFindingTriangle(data) {
    const ctx = document.getElementById('finding-triangle');
    if (!ctx) return;

    const ids = ['espana_enia_2020', 'brasil_ebia_2021', 'colombia_conpes_3975_2019'];
    const labels = ids.map(id => ABBR_MAP[id]);
    const pairs = [];
    for (let i = 0; i < ids.length; i++) {
        for (let j = i + 1; j < ids.length; j++) {
            const idxI = data.policy_ids.indexOf(ids[i]);
            const idxJ = data.policy_ids.indexOf(ids[j]);
            pairs.push({
                label: `${labels[i]}↔${labels[j]}`,
                value: data.similarity_matrix[idxI][idxJ],
            });
        }
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: pairs.map(p => p.label),
            datasets: [{
                data: pairs.map(p => p.value),
                backgroundColor: ['#388e3c99', '#388e3cBB', '#388e3cDD'],
                borderColor: '#388e3c',
                borderWidth: 2,
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    min: 0.85, max: 1.0,
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                },
                y: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 11 } },
                    grid: { display: false },
                },
            },
        },
    });
}

// ── Finding: Cluster 1 member similarities ──
function renderFindingCluster1(data) {
    const ctx = document.getElementById('finding-cluster1');
    if (!ctx) return;

    const members = data.clusters['1'] || [];
    const labels = members.map(id => ABBR_MAP[id] || id);

    // Average similarity of each member with other members
    const avgSims = members.map(id => {
        const idx = data.policy_ids.indexOf(id);
        const sims = members
            .filter(m => m !== id)
            .map(m => data.similarity_matrix[idx][data.policy_ids.indexOf(m)]);
        return sims.reduce((s, v) => s + v, 0) / sims.length;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                data: avgSims,
                backgroundColor: members.map(id => {
                    const p = data.policies.find(pol => pol.id === id);
                    return (p?.region_color || '#999') + '99';
                }),
                borderColor: members.map(id => {
                    const p = data.policies.find(pol => pol.id === id);
                    return p?.region_color || '#999';
                }),
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: false, min: 0.6,
                    title: { display: true, text: 'Similitud promedio intra-cluster', font: { family: "'DM Sans'", size: 11 } },
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                },
                x: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 11 } },
                    grid: { display: false },
                },
            },
        },
    });
}

// ── Finding: Teacher Training Gap ──
function renderFindingTeacherGap(data) {
    const ctx = document.getElementById('finding-teacher');
    if (!ctx) return;

    const entries = data.policies.map(p => ({
        label: ABBR_MAP[p.id] || p.country,
        score: data.dimension_scores[p.id]?.formacion_docente || 0,
        color: p.region_color,
    }));
    entries.sort((a, b) => b.score - a.score);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: entries.map(e => e.label),
            datasets: [{
                data: entries.map(e => e.score),
                backgroundColor: entries.map(e => e.color + '99'),
                borderColor: entries.map(e => e.color),
                borderWidth: 2,
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    beginAtZero: true, max: 0.7,
                    title: { display: true, text: 'Puntaje — Formación Docente', font: { family: "'DM Sans'", size: 11 } },
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                },
                y: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                    grid: { display: false },
                },
            },
        },
    });
}

// ── Finding: EU Outlier ──
function renderFindingOutlier(data) {
    const ctx = document.getElementById('finding-outlier');
    if (!ctx) return;

    const euIdx = data.policy_ids.indexOf('eu_ai_act_2024');
    if (euIdx === -1) return;

    const entries = data.policies
        .filter(p => p.id !== 'eu_ai_act_2024')
        .map(p => {
            const idx = data.policy_ids.indexOf(p.id);
            return {
                label: ABBR_MAP[p.id] || p.country,
                value: data.similarity_matrix[euIdx][idx],
                color: p.region_color,
            };
        });
    entries.sort((a, b) => a.value - b.value);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: entries.map(e => e.label),
            datasets: [{
                data: entries.map(e => e.value),
                backgroundColor: entries.map(e => e.color + '99'),
                borderColor: entries.map(e => e.color),
                borderWidth: 2,
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    min: 0.3, max: 0.7,
                    title: { display: true, text: 'Similitud con EU AI Act', font: { family: "'DM Sans'", size: 11 } },
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                },
                y: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                    grid: { display: false },
                },
            },
        },
    });
}

// ── Finding: Geography vs Orientation ──
function renderFindingGeography(data) {
    const ctx = document.getElementById('finding-geography');
    if (!ctx) return;

    // Show surprising cross-regional pairs
    const surprises = [
        { a: 'francia_villani_report_2018', b: 'brasil_ebia_2021', expected: 'Mismo cluster' },
        { a: 'canada_pan_canadian_ai_strategy_2017', b: 'japon_ai_strategy_2019', expected: 'Mismo cluster' },
        { a: 'francia_villani_report_2018', b: 'eu_ai_act_2024', expected: 'Distinto cluster' },
        { a: 'canada_pan_canadian_ai_strategy_2017', b: 'brasil_ebia_2021', expected: 'Distinto cluster' },
    ];

    const labels = surprises.map(s =>
        `${ABBR_MAP[s.a]}↔${ABBR_MAP[s.b]}`
    );
    const values = surprises.map(s => {
        const i = data.policy_ids.indexOf(s.a);
        const j = data.policy_ids.indexOf(s.b);
        return data.similarity_matrix[i][j];
    });
    const colors = surprises.map(s =>
        s.expected === 'Mismo cluster' ? '#388e3c' : '#d32f2f'
    );

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: colors.map(c => c + '99'),
                borderColor: colors,
                borderWidth: 2,
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        afterLabel: (ctx) => surprises[ctx.dataIndex].expected,
                    },
                },
            },
            scales: {
                x: {
                    min: 0.4, max: 1.0,
                    ticks: { font: { family: "'JetBrains Mono'", size: 10 } },
                },
                y: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 11 } },
                    grid: { display: false },
                },
            },
        },
    });
}

// ── Profile: Radar ──
function renderProfileRadar(policyId, data) {
    const ctx = document.getElementById('profile-radar');
    if (!ctx) return;

    const dimKeys = Object.keys(data.dimension_labels);
    const dimLabels = Object.values(data.dimension_labels);
    const policy = data.policies.find(p => p.id === policyId);
    const scores = data.dimension_scores[policyId] || {};
    const values = dimKeys.map(k => scores[k] || 0);
    const color = policy?.region_color || '#1976d2';

    if (profileRadarChart) profileRadarChart.destroy();

    profileRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: dimLabels.map(l => l.split(' ')[0]),
            datasets: [{
                label: policy?.country || policyId,
                data: values,
                borderColor: color,
                backgroundColor: color + '22',
                borderWidth: 2,
                pointRadius: 4,
                pointBackgroundColor: color,
            }],
        },
        options: {
            responsive: true,
            scales: {
                r: {
                    beginAtZero: true, max: 0.8,
                    ticks: { stepSize: 0.2, font: { family: "'JetBrains Mono'", size: 9 } },
                    pointLabels: { font: { family: "'DM Sans'", size: 10 } },
                },
            },
            plugins: { legend: { display: false } },
        },
    });
}

// ── Profile: Similarity Bar ──
function renderProfileBar(policyId, data) {
    const ctx = document.getElementById('profile-bar');
    if (!ctx) return;

    const idx = data.policy_ids.indexOf(policyId);
    if (idx === -1) return;

    const entries = data.policies
        .filter(p => p.id !== policyId)
        .map(p => {
            const pIdx = data.policy_ids.indexOf(p.id);
            return {
                label: ABBR_MAP[p.id] || p.country,
                value: data.similarity_matrix[idx][pIdx],
                color: p.region_color,
            };
        });
    entries.sort((a, b) => b.value - a.value);

    if (profileBarChart) profileBarChart.destroy();

    profileBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: entries.map(e => e.label),
            datasets: [{
                data: entries.map(e => e.value),
                backgroundColor: entries.map(e => e.color + '99'),
                borderColor: entries.map(e => e.color),
                borderWidth: 1,
            }],
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    min: 0.3, max: 1.0,
                    ticks: { font: { family: "'JetBrains Mono'", size: 9 } },
                },
                y: {
                    ticks: { font: { family: "'JetBrains Mono'", size: 9 } },
                    grid: { display: false },
                },
            },
        },
    });
}
