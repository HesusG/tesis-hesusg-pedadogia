/**
 * explorer-chord.js — D3 Chord Diagram
 * Shows similarity relationships between 14 policies.
 * Arcs = documents (colored by region), ribbons = similarity pairs.
 */

let chordTooltip = null;

function renderChord(data, threshold) {
    const container = document.getElementById('chord-chart');
    if (!container || typeof d3 === 'undefined') return;

    container.innerHTML = '';

    const width = Math.min(container.clientWidth || 600, 600);
    const height = Math.min(width, 550);
    const outerRadius = Math.min(width, height) / 2 - 40;
    const innerRadius = outerRadius - 22;

    const n = data.policies.length;
    const policyIds = data.policy_ids;

    // Build adjacency matrix for chord layout
    // Values: similarity above threshold, 0 otherwise
    const matrix = [];
    for (let i = 0; i < n; i++) {
        const row = [];
        for (let j = 0; j < n; j++) {
            if (i === j) {
                row.push(0);
            } else {
                const sim = data.similarity_matrix[i][j];
                row.push(sim >= threshold ? sim : 0);
            }
        }
        matrix.push(row);
    }

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2},${height / 2})`);

    const chord = d3.chord()
        .padAngle(0.04)
        .sortSubgroups(d3.descending);

    const chords = chord(matrix);

    const arc = d3.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);

    const ribbon = d3.ribbon()
        .radius(innerRadius);

    // Tooltip
    if (!chordTooltip) {
        chordTooltip = document.createElement('div');
        chordTooltip.className = 'chord-tooltip';
        document.body.appendChild(chordTooltip);
    }

    // Draw arcs (groups)
    const group = svg.append('g')
        .selectAll('g')
        .data(chords.groups)
        .join('g');

    group.append('path')
        .attr('d', arc)
        .attr('fill', d => data.policies[d.index].region_color)
        .attr('stroke', '#1a1a1a')
        .attr('stroke-width', 1.5)
        .style('cursor', 'pointer')
        .on('mouseover', function(event, d) {
            // Fade non-connected ribbons
            svg.selectAll('.chord-ribbon')
                .style('opacity', r =>
                    r.source.index === d.index || r.target.index === d.index ? 0.85 : 0.05
                );

            const p = data.policies[d.index];
            chordTooltip.style.display = 'block';
            chordTooltip.style.left = (event.clientX + 12) + 'px';
            chordTooltip.style.top = (event.clientY - 30) + 'px';
            chordTooltip.innerHTML = `<strong>${p.country}</strong><br>${EX_ABBR[p.id]} · ${p.year}`;
        })
        .on('mouseout', function() {
            svg.selectAll('.chord-ribbon').style('opacity', 0.65);
            chordTooltip.style.display = 'none';
        })
        .on('click', function(event, d) {
            toggleSelection(data.policies[d.index].id);
        });

    // Arc labels
    group.append('text')
        .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
        .attr('dy', '0.35em')
        .attr('transform', d =>
            `rotate(${(d.angle * 180 / Math.PI - 90)})` +
            `translate(${outerRadius + 8})` +
            (d.angle > Math.PI ? 'rotate(180)' : '')
        )
        .attr('text-anchor', d => d.angle > Math.PI ? 'end' : 'start')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '9px')
        .attr('font-weight', 'bold')
        .attr('fill', d => data.policies[d.index].region_color)
        .text(d => EX_ABBR[data.policies[d.index].id] || '');

    // Draw ribbons
    svg.append('g')
        .selectAll('path')
        .data(chords)
        .join('path')
        .attr('class', 'chord-ribbon')
        .attr('d', ribbon)
        .attr('fill', d => {
            // Blend colors of the two endpoints
            const cA = data.policies[d.source.index].region_color;
            return cA;
        })
        .attr('stroke', 'rgba(26,26,26,0.08)')
        .attr('stroke-width', 0.5)
        .style('opacity', 0.65)
        .style('cursor', 'pointer')
        .on('mouseover', function(event, d) {
            d3.select(this).style('opacity', 0.95);

            const pA = data.policies[d.source.index];
            const pB = data.policies[d.target.index];
            const sim = data.similarity_matrix[d.source.index][d.target.index];

            chordTooltip.style.display = 'block';
            chordTooltip.style.left = (event.clientX + 12) + 'px';
            chordTooltip.style.top = (event.clientY - 30) + 'px';
            chordTooltip.innerHTML = `<strong>${pA.country} \u2194 ${pB.country}</strong><br>Similitud: ${sim.toFixed(3)}`;
        })
        .on('mouseout', function() {
            d3.select(this).style('opacity', 0.65);
            chordTooltip.style.display = 'none';
        })
        .on('click', function(event, d) {
            const idA = data.policies[d.source.index].id;
            const idB = data.policies[d.target.index].id;
            selectPair(idA, idB);
        });

    // Legend
    const legendData = [
        { label: 'Europa', color: '#1976d2' },
        { label: 'Américas', color: '#388e3c' },
        { label: 'Asia-Pac', color: '#d32f2f' },
        { label: 'Intl', color: '#7b1fa2' },
    ];

    const legend = svg.append('g')
        .attr('transform', `translate(${-width/2 + 10}, ${-height/2 + 10})`);

    legendData.forEach((item, i) => {
        const g = legend.append('g').attr('transform', `translate(0, ${i * 18})`);
        g.append('rect').attr('width', 10).attr('height', 10).attr('fill', item.color);
        g.append('text')
            .text(item.label)
            .attr('x', 14).attr('dy', '0.8em')
            .attr('font-family', "'DM Sans', sans-serif")
            .attr('font-size', '9px')
            .attr('fill', '#555');
    });

    // Threshold indicator
    svg.append('text')
        .attr('x', width/2 - 10)
        .attr('y', -height/2 + 12)
        .attr('text-anchor', 'end')
        .attr('font-family', "'JetBrains Mono', monospace")
        .attr('font-size', '9px')
        .attr('fill', '#999')
        .text(`umbral \u2265 ${threshold.toFixed(2)}`);
}

function updateChordHighlight(selectedIds) {
    if (!selectedIds || selectedIds.length < 2) return;

    const svg = d3.select('#chord-chart svg');
    if (svg.empty()) return;

    svg.selectAll('.chord-ribbon')
        .style('opacity', d => {
            if (!EX_DATA) return 0.65;
            const idA = EX_DATA.policies[d.source.index]?.id;
            const idB = EX_DATA.policies[d.target.index]?.id;
            if (selectedIds.includes(idA) && selectedIds.includes(idB)) return 0.95;
            return 0.3;
        });
}
