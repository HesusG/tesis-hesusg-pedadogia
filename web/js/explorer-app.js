/**
 * explorer-app.js — Explorer page controller
 * State management, filters, sidebar, viz tabs,
 * network, heatmap, parallel coords, detail radar
 */

// ── Shared Maps ──
const EX_ABBR = {
    eu_ai_act_2024: 'UE',
    espana_enia_2020: 'ES',
    francia_villani_report_2018: 'FR',
    canada_pan_canadian_ai_strategy_2017: 'CA',
    brasil_ebia_2021: 'BR',
    colombia_conpes_3975_2019: 'CO',
    japon_ai_strategy_2019: 'JP',
    corea_ai_strategy_2019: 'KR',
    singapur_nais_2019: 'SG',
    india_aiforall_2018: 'IN\u2081',
    india_nep_2020: 'IN\u2082',
    australia_ai_action_plan_2021: 'AU',
    unesco_genai_guidance_2023: 'UN',
    wef_future_of_jobs_2020: 'WEF',
};

const EX_CLUSTER_COLORS = { '1': '#d32f2f', '2': '#388e3c', '3': '#1976d2' };
const EX_CLUSTER_NAMES = { '1': 'Tecnológico', '2': 'Integral', '3': 'Regulación' };

const DIM_COLORS = {
    gobernanza: '#1976d2',
    curriculo: '#388e3c',
    formacion_docente: '#f57c00',
    infraestructura: '#7b1fa2',
    etica: '#d32f2f',
    investigacion: '#00838f',
    equidad: '#c2185b',
};

// ── State ──
let EX_DATA = null;
let EX_CHUNKS = null;
let EX_SELECTED = []; // up to 2 policy ids
let EX_THRESHOLD = 0.70;
let EX_REGION = 'all';
let EX_DIMENSION = 'all';
let detailRadarChart = null;

// ── Data Loading ──
async function loadExplorerData() {
    const [resultsRes, chunksRes] = await Promise.allSettled([
        fetch('data/results.json'),
        fetch('data/chunk_pairs.json'),
    ]);

    if (resultsRes.status === 'fulfilled' && resultsRes.value.ok) {
        EX_DATA = await resultsRes.value.json();
    } else {
        console.error('Failed to load results.json');
        return;
    }

    if (chunksRes.status === 'fulfilled' && chunksRes.value.ok) {
        EX_CHUNKS = await chunksRes.value.json();
    } else {
        console.warn('chunk_pairs.json not found — text comparison will use fallback mode');
    }
}

// ── Sidebar ──
function renderSidebar() {
    const list = document.getElementById('sidebar-list');
    if (!EX_DATA || !list) return;

    list.innerHTML = '';
    EX_DATA.policies.forEach(p => {
        const card = document.createElement('div');
        card.className = 'sb-card';
        card.dataset.id = p.id;
        card.dataset.region = p.region;
        card.style.borderLeftColor = p.region_color;

        card.innerHTML = `
            <span class="sb-card-abbr" style="color:${p.region_color}">${EX_ABBR[p.id] || ''}</span>
            <div class="sb-card-country">${p.country}</div>
            <div class="sb-card-meta">${p.year}</div>
        `;

        card.addEventListener('click', () => toggleSelection(p.id));
        list.appendChild(card);
    });

    updateSidebarCount();
}

function toggleSelection(policyId) {
    const idx = EX_SELECTED.indexOf(policyId);
    if (idx >= 0) {
        EX_SELECTED.splice(idx, 1);
    } else {
        if (EX_SELECTED.length >= 2) {
            EX_SELECTED.shift(); // remove oldest
        }
        EX_SELECTED.push(policyId);
    }
    onSelectionChanged();
}

function clearSelection() {
    EX_SELECTED = [];
    onSelectionChanged();
}

function selectPair(idA, idB) {
    EX_SELECTED = [idA, idB];
    onSelectionChanged();
}

function onSelectionChanged() {
    // Update sidebar card styles
    document.querySelectorAll('.sb-card').forEach(card => {
        card.classList.toggle('selected', EX_SELECTED.includes(card.dataset.id));
    });

    // Update selection bar
    const bar = document.getElementById('sidebar-selection');
    const tags = document.getElementById('selection-tags');
    if (EX_SELECTED.length > 0) {
        bar.style.display = '';
        tags.innerHTML = EX_SELECTED.map(id => {
            const p = EX_DATA.policies.find(pol => pol.id === id);
            return `<span class="selection-tag" style="background:${p?.region_color || '#333'}">${EX_ABBR[id] || id}</span>`;
        }).join('');
    } else {
        bar.style.display = 'none';
    }

    // Update detail panel
    updateDetailPanel();

    // Update text panel
    if (EX_SELECTED.length === 2) {
        if (typeof loadTextComparison === 'function') {
            loadTextComparison(EX_SELECTED[0], EX_SELECTED[1]);
        }
        // Update text panel pair label
        const pairLabel = document.getElementById('text-panel-pair');
        if (pairLabel) {
            pairLabel.textContent = `${EX_ABBR[EX_SELECTED[0]]} vs ${EX_ABBR[EX_SELECTED[1]]}`;
        }
    }

    // Update chord highlights
    if (typeof updateChordHighlight === 'function') {
        updateChordHighlight(EX_SELECTED);
    }
}

function updateSidebarCount() {
    const count = document.getElementById('sidebar-count');
    const visible = document.querySelectorAll('.sb-card:not(.filtered-out)').length;
    if (count) count.textContent = `(${visible})`;
}

// ── Filters ──
function applyFilters() {
    EX_REGION = document.getElementById('filter-region').value;
    EX_DIMENSION = document.getElementById('filter-dimension').value;
    EX_THRESHOLD = parseFloat(document.getElementById('threshold-slider').value);

    document.getElementById('threshold-value').textContent = EX_THRESHOLD.toFixed(2);

    // Filter sidebar cards
    document.querySelectorAll('.sb-card').forEach(card => {
        const matchRegion = EX_REGION === 'all' || card.dataset.region === EX_REGION;
        card.classList.toggle('filtered-out', !matchRegion);
    });

    updateSidebarCount();

    // Update chord diagram with new threshold
    if (typeof renderChord === 'function') {
        renderChord(EX_DATA, EX_THRESHOLD);
    }

    // Update network with threshold
    renderExplorerNetwork();
}

function initFilters() {
    document.getElementById('filter-region').addEventListener('change', applyFilters);
    document.getElementById('filter-dimension').addEventListener('change', applyFilters);

    const slider = document.getElementById('threshold-slider');
    slider.addEventListener('input', () => {
        document.getElementById('threshold-value').textContent = parseFloat(slider.value).toFixed(2);
    });
    slider.addEventListener('change', applyFilters);
}

// ── Viz Tabs ──
function initVizTabs() {
    const tabs = document.querySelectorAll('#viz-tabs button');
    const panels = document.querySelectorAll('.viz-panel');
    const rendered = {};

    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            const viz = btn.dataset.viz;
            tabs.forEach(b => b.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`viz-${viz}`).classList.add('active');

            // Lazy render
            if (!rendered[viz]) {
                rendered[viz] = true;
                switch (viz) {
                    case 'chord':
                        if (typeof renderChord === 'function') renderChord(EX_DATA, EX_THRESHOLD);
                        break;
                    case 'network':
                        renderExplorerNetwork();
                        break;
                    case 'heatmap':
                        renderExplorerHeatmap();
                        break;
                    case 'parallel':
                        renderExplorerParallel();
                        break;
                }
            }
        });
    });
}

// ── Detail Panel ──
function updateDetailPanel() {
    const placeholder = document.getElementById('detail-placeholder');
    const content = document.getElementById('detail-content');

    if (EX_SELECTED.length < 2) {
        placeholder.style.display = '';
        content.style.display = 'none';
        return;
    }

    placeholder.style.display = 'none';
    content.style.display = '';

    const [idA, idB] = EX_SELECTED;
    const pA = EX_DATA.policies.find(p => p.id === idA);
    const pB = EX_DATA.policies.find(p => p.id === idB);
    const idxA = EX_DATA.policy_ids.indexOf(idA);
    const idxB = EX_DATA.policy_ids.indexOf(idB);
    const sim = EX_DATA.similarity_matrix[idxA][idxB];

    document.getElementById('detail-title').textContent = `${EX_ABBR[idA]} vs ${EX_ABBR[idB]}`;
    document.getElementById('detail-sim-badge').textContent = `Similitud: ${sim.toFixed(3)}`;

    // Render radar overlay
    renderDetailRadar(idA, idB);

    // Meta info
    const meta = document.getElementById('detail-meta');
    const dimKeys = Object.keys(EX_DATA.dimension_labels);

    const scoresA = EX_DATA.dimension_scores[idA] || {};
    const scoresB = EX_DATA.dimension_scores[idB] || {};

    let metaHtml = `
        <div class="detail-meta-item">
            <span class="detail-meta-label">Doc A</span>
            <span class="detail-meta-value" style="color:${pA?.region_color}">${pA?.country} (${pA?.year})</span>
        </div>
        <div class="detail-meta-item">
            <span class="detail-meta-label">Doc B</span>
            <span class="detail-meta-value" style="color:${pB?.region_color}">${pB?.country} (${pB?.year})</span>
        </div>
    `;

    // Dimension comparison
    dimKeys.forEach(k => {
        const vA = (scoresA[k] || 0).toFixed(3);
        const vB = (scoresB[k] || 0).toFixed(3);
        const label = EX_DATA.dimension_labels[k].split(' ')[0];
        metaHtml += `
            <div class="detail-meta-item">
                <span class="detail-meta-label" style="color:${DIM_COLORS[k]}">${label}</span>
                <span class="detail-meta-value">${vA} / ${vB}</span>
            </div>
        `;
    });

    meta.innerHTML = metaHtml;
}

function renderDetailRadar(idA, idB) {
    const ctx = document.getElementById('detail-radar');
    if (!ctx) return;

    const dimKeys = Object.keys(EX_DATA.dimension_labels);
    const dimLabels = Object.values(EX_DATA.dimension_labels).map(l => l.split(' ')[0]);

    const pA = EX_DATA.policies.find(p => p.id === idA);
    const pB = EX_DATA.policies.find(p => p.id === idB);
    const scoresA = dimKeys.map(k => EX_DATA.dimension_scores[idA]?.[k] || 0);
    const scoresB = dimKeys.map(k => EX_DATA.dimension_scores[idB]?.[k] || 0);

    // Global average
    const avgScores = dimKeys.map(k => {
        const vals = EX_DATA.policies.map(p => EX_DATA.dimension_scores[p.id]?.[k] || 0).filter(v => v > 0);
        return vals.length > 0 ? vals.reduce((s, v) => s + v, 0) / vals.length : 0;
    });

    if (detailRadarChart) detailRadarChart.destroy();

    detailRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: dimLabels,
            datasets: [
                {
                    label: pA?.country || idA,
                    data: scoresA,
                    borderColor: pA?.region_color || '#1976d2',
                    backgroundColor: (pA?.region_color || '#1976d2') + '22',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointBackgroundColor: pA?.region_color || '#1976d2',
                },
                {
                    label: pB?.country || idB,
                    data: scoresB,
                    borderColor: pB?.region_color || '#d32f2f',
                    backgroundColor: (pB?.region_color || '#d32f2f') + '22',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointBackgroundColor: pB?.region_color || '#d32f2f',
                },
                {
                    label: 'Promedio global',
                    data: avgScores,
                    borderColor: 'rgba(0,0,0,0.15)',
                    backgroundColor: 'transparent',
                    borderWidth: 1,
                    borderDash: [4, 4],
                    pointRadius: 0,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 0.8,
                    ticks: { display: false },
                    pointLabels: { font: { family: "'JetBrains Mono'", size: 8 } },
                },
            },
            plugins: {
                legend: { labels: { font: { family: "'DM Sans'", size: 9 }, boxWidth: 12 } },
            },
        },
    });
}

// ── Explorer Network (with threshold slider) ──
function renderExplorerNetwork() {
    const container = document.getElementById('explorer-network-chart');
    if (!container || !EX_DATA || typeof d3 === 'undefined') return;

    container.innerHTML = '';

    const width = container.clientWidth || 600;
    const height = 450;

    const clusterMap = {};
    for (const [cid, members] of Object.entries(EX_DATA.clusters || {})) {
        members.forEach(id => { clusterMap[id] = cid; });
    }

    const nodes = EX_DATA.policies.map(p => ({
        id: p.id,
        label: EX_ABBR[p.id] || p.country,
        fullName: p.country,
        color: p.region_color,
        cluster: clusterMap[p.id] || '0',
    }));

    // Filter edges by threshold
    const allEdges = EX_DATA.network_edges || [];
    const links = [];
    const n = EX_DATA.policies.length;
    // Also build from similarity matrix for edges not in network_edges
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            const sim = EX_DATA.similarity_matrix[i][j];
            if (sim >= EX_THRESHOLD) {
                links.push({
                    source: EX_DATA.policy_ids[i],
                    target: EX_DATA.policy_ids[j],
                    weight: sim,
                });
            }
        }
    }

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const tooltip = d3.select(container)
        .append('div')
        .attr('class', 'net-tooltip')
        .style('display', 'none');

    const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(d => (1 - d.weight) * 250))
        .force('charge', d3.forceManyBody().strength(-180))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide(25));

    const link = svg.append('g')
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('stroke', 'rgba(26,26,26,0.12)')
        .attr('stroke-width', d => 1 + (d.weight - 0.5) * 6);

    const node = svg.append('g')
        .selectAll('g')
        .data(nodes)
        .join('g')
        .call(d3.drag()
            .on('start', (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
            .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
            .on('end', (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; })
        );

    node.append('circle')
        .attr('r', 18)
        .attr('fill', d => EX_CLUSTER_COLORS[d.cluster] || d.color)
        .attr('stroke', '#1a1a1a')
        .attr('stroke-width', 2)
        .style('cursor', 'pointer');

    node.append('text')
        .text(d => d.label)
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('fill', '#fff')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '9px')
        .attr('font-weight', 'bold')
        .style('pointer-events', 'none');

    node.on('mouseover', (event, d) => {
        tooltip.style('display', 'block')
            .html(`<strong>${d.fullName}</strong><br>${EX_CLUSTER_NAMES[d.cluster] || ''}`)
            .style('left', (event.offsetX + 15) + 'px')
            .style('top', (event.offsetY - 10) + 'px');
    })
    .on('mouseout', () => tooltip.style('display', 'none'))
    .on('click', (event, d) => {
        if (EX_SELECTED.length < 2 || EX_SELECTED.includes(d.id)) {
            toggleSelection(d.id);
        } else {
            selectPair(EX_SELECTED[1], d.id);
        }
    });

    simulation.on('tick', () => {
        link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
        node.attr('transform', d => {
            d.x = Math.max(20, Math.min(width - 20, d.x));
            d.y = Math.max(20, Math.min(height - 20, d.y));
            return `translate(${d.x},${d.y})`;
        });
    });
}

// ── Explorer Heatmap (canvas, clickable) ──
function renderExplorerHeatmap() {
    const canvas = document.getElementById('explorer-heatmap');
    if (!canvas || !EX_DATA) return;

    const labels = EX_DATA.policies.map(p => EX_ABBR[p.id] || p.country);
    const colors = EX_DATA.policies.map(p => p.region_color);
    const matrix = EX_DATA.similarity_matrix;
    const n = labels.length;

    const dpr = window.devicePixelRatio || 1;
    const labelMargin = 50;
    const topMargin = 50;
    const parentWidth = canvas.parentElement.clientWidth - 20;
    const totalSize = Math.min(parentWidth, 550);
    const gridSize = totalSize - labelMargin;
    const cellSize = gridSize / n;

    canvas.width = totalSize * dpr;
    canvas.height = (totalSize + 10) * dpr;
    canvas.style.width = totalSize + 'px';
    canvas.style.height = (totalSize + 10) + 'px';

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    function heatColor(v) {
        const t = Math.max(0, Math.min(1, (v - 0.4) / 0.6));
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
        return { r, g, b, css: `rgb(${r},${g},${b})` };
    }

    // Draw cells
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            const v = matrix[i][j];
            const x = labelMargin + j * cellSize;
            const y = topMargin + i * cellSize;
            const c = heatColor(v);
            ctx.fillStyle = c.css;
            ctx.fillRect(x, y, cellSize, cellSize);

            ctx.strokeStyle = 'rgba(0,0,0,0.06)';
            ctx.lineWidth = 0.5;
            ctx.strokeRect(x, y, cellSize, cellSize);

            if (cellSize > 24) {
                const lum = 0.299 * c.r + 0.587 * c.g + 0.114 * c.b;
                ctx.fillStyle = lum < 160 ? '#fff' : '#1a1a1a';
                ctx.font = `${Math.max(7, cellSize * 0.26)}px 'JetBrains Mono', monospace`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(v.toFixed(2), x + cellSize / 2, y + cellSize / 2);
            }
        }
    }

    // Labels
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    for (let i = 0; i < n; i++) {
        ctx.fillStyle = colors[i];
        ctx.font = `bold ${Math.max(8, cellSize * 0.3)}px 'JetBrains Mono', monospace`;
        ctx.fillText(labels[i], labelMargin - 4, topMargin + i * cellSize + cellSize / 2);
    }
    ctx.textAlign = 'center';
    for (let j = 0; j < n; j++) {
        ctx.save();
        ctx.translate(labelMargin + j * cellSize + cellSize / 2, topMargin - 4);
        ctx.rotate(-Math.PI / 4);
        ctx.fillStyle = colors[j];
        ctx.font = `bold ${Math.max(8, cellSize * 0.3)}px 'JetBrains Mono', monospace`;
        ctx.textAlign = 'right';
        ctx.fillText(labels[j], 0, 0);
        ctx.restore();
    }

    // Click handler
    canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const col = Math.floor((mx - labelMargin) / cellSize);
        const row = Math.floor((my - topMargin) / cellSize);
        if (col >= 0 && col < n && row >= 0 && row < n && row !== col) {
            selectPair(EX_DATA.policy_ids[row], EX_DATA.policy_ids[col]);
        }
    });

    // Tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'chord-tooltip';
    document.body.appendChild(tooltip);

    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const col = Math.floor((mx - labelMargin) / cellSize);
        const row = Math.floor((my - topMargin) / cellSize);
        if (col >= 0 && col < n && row >= 0 && row < n) {
            tooltip.style.display = 'block';
            tooltip.style.left = (e.clientX + 12) + 'px';
            tooltip.style.top = (e.clientY - 30) + 'px';
            const pA = EX_DATA.policies[row];
            const pB = EX_DATA.policies[col];
            tooltip.textContent = `${pA.country} \u2194 ${pB.country}: ${matrix[row][col].toFixed(3)}`;
        } else {
            tooltip.style.display = 'none';
        }
    });

    canvas.addEventListener('mouseleave', () => tooltip.style.display = 'none');
    canvas.style.cursor = 'pointer';
}

// ── Explorer Parallel Coordinates ──
function renderExplorerParallel() {
    const container = document.getElementById('explorer-parallel-chart');
    if (!container || !EX_DATA || typeof Plotly === 'undefined') return;

    const dimKeys = Object.keys(EX_DATA.dimension_labels);
    const dimLabels = Object.values(EX_DATA.dimension_labels);

    const clusterMap = {};
    for (const [cid, members] of Object.entries(EX_DATA.clusters || {})) {
        members.forEach(id => { clusterMap[id] = parseInt(cid); });
    }

    const clusterValues = EX_DATA.policies.map(p => clusterMap[p.id] || 0);

    const dimensions = dimKeys.map((k, i) => ({
        label: dimLabels[i].split(' ')[0],
        values: EX_DATA.policies.map(p => EX_DATA.dimension_scores[p.id]?.[k] || 0),
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
        customdata: EX_DATA.policies.map(p => p.country),
    };

    const layout = {
        font: { family: 'DM Sans, sans-serif', size: 12 },
        margin: { l: 60, r: 30, t: 30, b: 30 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
    };

    Plotly.newPlot(container, [trace], layout, {
        responsive: true,
        displayModeBar: false,
    });
}

// ── Text Panel Toggle ──
function initTextPanel() {
    const panel = document.getElementById('text-panel');
    const toggle = document.getElementById('text-panel-toggle');
    if (!toggle) return;

    // Start collapsed
    panel.classList.add('collapsed');

    toggle.addEventListener('click', () => {
        panel.classList.toggle('collapsed');
    });
}

// ── Initialize ──
async function initExplorer() {
    await loadExplorerData();
    if (!EX_DATA) return;

    renderSidebar();
    initFilters();
    initVizTabs();
    initTextPanel();

    // Clear selection button
    document.getElementById('btn-clear-selection')?.addEventListener('click', clearSelection);

    // Render initial chord diagram
    if (typeof renderChord === 'function') {
        renderChord(EX_DATA, EX_THRESHOLD);
    }
}

document.addEventListener('DOMContentLoaded', initExplorer);
