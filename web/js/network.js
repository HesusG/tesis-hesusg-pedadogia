/**
 * network.js — D3.js force-directed network graph + dendrogram
 * Requires d3.v7 loaded globally
 */

// ── Shared abbreviation map ──
const NET_ABBR = {
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

const CLUSTER_COLORS = { '1': '#d32f2f', '2': '#388e3c', '3': '#1976d2' };
const CLUSTER_NAMES = {
    '1': 'Tecnológico',
    '2': 'Integral',
    '3': 'Regulación',
};

// ── Force-directed network graph ──
function renderNetwork(data) {
    const container = document.getElementById('network-chart');
    if (!container || !data.network_edges || !data.network_edges.length) return;
    if (typeof d3 === 'undefined') return;

    container.innerHTML = '';

    const width = container.clientWidth;
    const height = 550;

    // Build cluster map
    const clusterMap = {};
    for (const [cid, members] of Object.entries(data.clusters || {})) {
        members.forEach(id => { clusterMap[id] = cid; });
    }

    // Build nodes
    const nodes = data.policies.map(p => ({
        id: p.id,
        label: NET_ABBR[p.id] || p.country,
        fullName: p.country,
        color: p.region_color,
        cluster: clusterMap[p.id] || '0',
    }));

    // Build links (D3 needs source/target as ids or indices)
    const links = data.network_edges.map(e => ({
        source: e.source,
        target: e.target,
        weight: e.weight,
    }));

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height]);

    // Tooltip
    const tooltip = d3.select(container)
        .append('div')
        .attr('class', 'net-tooltip')
        .style('display', 'none');

    // Force simulation
    const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id)
            .distance(d => (1 - d.weight) * 300))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide(28));

    // Links
    const link = svg.append('g')
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('stroke', 'rgba(26,26,26,0.15)')
        .attr('stroke-width', d => 1 + (d.weight - 0.7) * 10);

    // Node groups
    const node = svg.append('g')
        .selectAll('g')
        .data(nodes)
        .join('g')
        .call(drag(simulation));

    // Circle
    node.append('circle')
        .attr('r', 20)
        .attr('fill', d => CLUSTER_COLORS[d.cluster] || d.color)
        .attr('stroke', '#1a1a1a')
        .attr('stroke-width', 2.5)
        .style('cursor', 'pointer');

    // Label
    node.append('text')
        .text(d => d.label)
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .attr('fill', '#fff')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '10px')
        .attr('font-weight', 'bold')
        .style('pointer-events', 'none');

    // Hover
    node.on('mouseover', (event, d) => {
        tooltip.style('display', 'block')
            .html(`<strong>${d.fullName}</strong><br>Cluster: ${CLUSTER_NAMES[d.cluster] || d.cluster}`)
            .style('left', (event.offsetX + 15) + 'px')
            .style('top', (event.offsetY - 10) + 'px');
    })
    .on('mouseout', () => tooltip.style('display', 'none'))
    .on('click', (event, d) => {
        if (typeof navigateToProfile === 'function') navigateToProfile(d.id);
    });

    // Tick
    simulation.on('tick', () => {
        link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
        node.attr('transform', d => {
            d.x = Math.max(22, Math.min(width - 22, d.x));
            d.y = Math.max(22, Math.min(height - 22, d.y));
            return `translate(${d.x},${d.y})`;
        });
    });

    // Drag behavior
    function drag(sim) {
        return d3.drag()
            .on('start', (event, d) => {
                if (!event.active) sim.alphaTarget(0.3).restart();
                d.fx = d.x; d.fy = d.y;
            })
            .on('drag', (event, d) => {
                d.fx = event.x; d.fy = event.y;
            })
            .on('end', (event, d) => {
                if (!event.active) sim.alphaTarget(0);
                d.fx = null; d.fy = null;
            });
    }

    // Legend
    const legend = svg.append('g').attr('transform', `translate(${width - 180}, 20)`);
    Object.entries(CLUSTER_NAMES).forEach(([cid, name], i) => {
        const g = legend.append('g').attr('transform', `translate(0, ${i * 24})`);
        g.append('circle').attr('r', 8).attr('fill', CLUSTER_COLORS[cid]);
        g.append('text').text(name).attr('x', 14).attr('dy', '0.35em')
            .attr('font-family', "'DM Sans', sans-serif").attr('font-size', '11px').attr('fill', '#555');
    });
}


// ── Dendrogram ──
function renderDendrogram(data) {
    const container = document.getElementById('dendrogram-chart');
    if (!container || !data.dendrogram) return;
    if (typeof d3 === 'undefined') return;

    container.innerHTML = '';

    const Z = data.dendrogram.linkage_matrix;
    const labels = data.dendrogram.labels;
    const n = labels.length;

    // Build cluster map for leaf coloring
    const clusterMap = {};
    for (const [cid, members] of Object.entries(data.clusters || {})) {
        members.forEach(id => { clusterMap[id] = cid; });
    }

    // Convert scipy linkage to D3 hierarchy
    // Z[i] = [cluster_a, cluster_b, distance, count]
    // Nodes 0..n-1 are original leaves, n..2n-2 are internal
    const nodeMap = {};
    for (let i = 0; i < n; i++) {
        nodeMap[i] = { name: labels[i], label: NET_ABBR[labels[i]] || labels[i], leaf: true };
    }
    for (let i = 0; i < Z.length; i++) {
        const [a, b, dist] = Z[i];
        nodeMap[n + i] = {
            name: `merge_${i}`,
            distance: dist,
            children: [nodeMap[a], nodeMap[b]],
        };
    }
    const root = d3.hierarchy(nodeMap[n + Z.length - 1]);

    const margin = { top: 30, right: 30, bottom: 90, left: 30 };
    const width = Math.max(container.clientWidth, 600);
    const height = 500;
    const innerW = width - margin.left - margin.right;
    const innerH = height - margin.top - margin.bottom;

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Cluster layout (dendrogram)
    const cluster = d3.cluster().size([innerW, innerH]);
    cluster(root);

    // Y scale based on distance (height in dendrogram)
    const maxDist = d3.max(Z, d => d[2]);
    const yScale = d3.scaleLinear()
        .domain([0, maxDist * 1.05])
        .range([innerH, 0]);

    // Assign y positions based on merge distance
    function assignY(node) {
        if (node.data.leaf) {
            node.y = innerH; // leaves at bottom
        } else {
            node.y = yScale(node.data.distance || 0);
        }
        if (node.children) node.children.forEach(assignY);
    }
    assignY(root);

    // Elbow links
    g.selectAll('.dendro-link')
        .data(root.links())
        .join('path')
        .attr('class', 'dendro-link')
        .attr('d', d => {
            return `M${d.source.x},${d.source.y}` +
                   `V${d.target.y}` +
                   `H${d.target.x}`;
        })
        .attr('fill', 'none')
        .attr('stroke', '#666')
        .attr('stroke-width', 2);

    // Leaf labels
    const leaves = root.leaves();
    leaves.forEach(leaf => {
        const cid = clusterMap[leaf.data.name] || '0';
        const color = CLUSTER_COLORS[cid] || '#555';

        g.append('circle')
            .attr('cx', leaf.x)
            .attr('cy', leaf.y)
            .attr('r', 5)
            .attr('fill', color);

        g.append('text')
            .attr('x', leaf.x)
            .attr('y', leaf.y + 16)
            .attr('text-anchor', 'middle')
            .attr('font-family', "'JetBrains Mono', monospace")
            .attr('font-size', '10px')
            .attr('font-weight', 'bold')
            .attr('fill', color)
            .text(leaf.data.label);

        // Full name below abbreviation
        const policy = data.policies.find(p => p.id === leaf.data.name);
        if (policy) {
            g.append('text')
                .attr('x', leaf.x)
                .attr('y', leaf.y + 28)
                .attr('text-anchor', 'middle')
                .attr('font-family', "'DM Sans', sans-serif")
                .attr('font-size', '8px')
                .attr('fill', '#888')
                .text(policy.country.length > 12 ? policy.country.substring(0, 12) + '…' : policy.country);
        }
    });

    // Cluster threshold line (find the cut that gives 3 clusters)
    // With ward linkage, the 3-cluster cut is between the 2nd and 3rd highest merges
    if (Z.length >= 2) {
        const sortedDists = Z.map(z => z[2]).sort((a, b) => b - a);
        const cutDist = (sortedDists[1] + sortedDists[2]) / 2;
        const cutY = yScale(cutDist);

        g.append('line')
            .attr('x1', 0).attr('x2', innerW)
            .attr('y1', cutY).attr('y2', cutY)
            .attr('stroke', '#FFD54F')
            .attr('stroke-width', 2)
            .attr('stroke-dasharray', '8,4');

        g.append('text')
            .attr('x', innerW - 5)
            .attr('y', cutY - 8)
            .attr('text-anchor', 'end')
            .attr('font-family', "'JetBrains Mono', monospace")
            .attr('font-size', '10px')
            .attr('fill', '#FFD54F')
            .text('Umbral 3 clusters');
    }

    // Y axis with distance labels
    const yAxis = d3.axisLeft(yScale).ticks(5).tickFormat(d3.format('.2f'));
    g.append('g')
        .call(yAxis)
        .selectAll('text')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '9px');

    g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -innerH / 2)
        .attr('y', -margin.left + 12)
        .attr('text-anchor', 'middle')
        .attr('font-family', "'DM Sans', sans-serif")
        .attr('font-size', '11px')
        .attr('fill', '#888')
        .text('Distancia (Ward)');
}
