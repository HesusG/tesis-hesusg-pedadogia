/**
 * explorer-text.js — Text Comparison Panel
 * Loads policy text, chunks it client-side, colors by dimension.
 * If chunk_pairs.json exists, shows matched chunks with scores.
 */

const TEXT_CACHE = {};
const CHUNK_SIZE = 800;
const CHUNK_OVERLAP = 200;

const DIM_LABELS = {
    gobernanza: 'Gobernanza',
    curriculo: 'Currículo',
    formacion_docente: 'Form. docente',
    infraestructura: 'Infraestructura',
    etica: 'Ética',
    investigacion: 'Investigación',
    equidad: 'Equidad',
};

// Keywords per dimension for fallback coloring
const DIM_KEYWORDS = {
    gobernanza: ['regulación', 'regulation', 'ley', 'law', 'gobierno', 'government', 'governance', 'gobernanza', 'legislat', 'normat', 'supervisión', 'marco legal', 'compliance'],
    curriculo: ['currículo', 'curriculum', 'educación', 'education', 'plan de estudi', 'course', 'school', 'escuela', 'learning', 'aprendizaje', 'teaching', 'enseñanza', 'literacy', 'alfabetización'],
    formacion_docente: ['docente', 'teacher', 'profesorado', 'capacitación', 'training', 'profesional', 'formación', 'educator', 'pedagog', 'instructor'],
    infraestructura: ['infraestructura', 'infrastructure', 'connectivity', 'conectividad', 'internet', 'hardware', 'digital', 'cloud', 'computing', 'plataform', 'platform', 'data center'],
    etica: ['ética', 'ethic', 'privacidad', 'privacy', 'sesgo', 'bias', 'transparencia', 'transparency', 'rights', 'derechos', 'responsible', 'responsable', 'fairness'],
    investigacion: ['investigación', 'research', 'innovación', 'innovation', 'I+D', 'R&D', 'development', 'desarrollo', 'scientific', 'científic', 'laborator', 'patent'],
    equidad: ['equidad', 'equity', 'inclusión', 'inclusion', 'brecha', 'gap', 'diversidad', 'diversity', 'género', 'gender', 'vulnerable', 'acceso', 'access', 'igualdad', 'equality'],
};

function chunkText(text) {
    const chunks = [];
    let start = 0;
    while (start < text.length) {
        const end = start + CHUNK_SIZE;
        const chunk = text.substring(start, end).trim();
        if (chunk) chunks.push(chunk);
        start += CHUNK_SIZE - CHUNK_OVERLAP;
    }
    return chunks;
}

function guessDimension(text) {
    const lower = text.toLowerCase();
    let bestDim = 'gobernanza';
    let bestCount = 0;

    for (const [dim, keywords] of Object.entries(DIM_KEYWORDS)) {
        let count = 0;
        for (const kw of keywords) {
            const regex = new RegExp(kw, 'gi');
            const matches = lower.match(regex);
            if (matches) count += matches.length;
        }
        if (count > bestCount) {
            bestCount = count;
            bestDim = dim;
        }
    }
    return bestDim;
}

async function fetchPolicyText(policyId) {
    if (TEXT_CACHE[policyId]) return TEXT_CACHE[policyId];

    try {
        const res = await fetch(`../policies/processed/${policyId}.txt`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const text = await res.text();
        TEXT_CACHE[policyId] = text;
        return text;
    } catch (e) {
        console.warn(`Could not load text for ${policyId}:`, e);
        return null;
    }
}

function findChunkPairs(idA, idB) {
    if (!EX_CHUNKS || !EX_CHUNKS.pairs) return null;

    // Search both orderings
    return EX_CHUNKS.pairs.find(p =>
        (p.doc_a === idA && p.doc_b === idB) ||
        (p.doc_a === idB && p.doc_b === idA)
    );
}

async function loadTextComparison(idA, idB) {
    const headerA = document.getElementById('text-header-a');
    const headerB = document.getElementById('text-header-b');
    const chunksContainerA = document.getElementById('text-chunks-a');
    const chunksContainerB = document.getElementById('text-chunks-b');

    if (!chunksContainerA || !chunksContainerB) return;

    const pA = EX_DATA.policies.find(p => p.id === idA);
    const pB = EX_DATA.policies.find(p => p.id === idB);

    headerA.innerHTML = `<span style="color:${pA?.region_color}">${pA?.country || idA}</span>`;
    headerB.innerHTML = `<span style="color:${pB?.region_color}">${pB?.country || idB}</span>`;

    chunksContainerA.innerHTML = '<div style="opacity:0.4;padding:1rem;font-size:0.8rem">Cargando...</div>';
    chunksContainerB.innerHTML = '<div style="opacity:0.4;padding:1rem;font-size:0.8rem">Cargando...</div>';

    // Expand the text panel
    const panel = document.getElementById('text-panel');
    if (panel.classList.contains('collapsed')) {
        panel.classList.remove('collapsed');
    }

    // Load texts in parallel
    const [textA, textB] = await Promise.all([
        fetchPolicyText(idA),
        fetchPolicyText(idB),
    ]);

    if (!textA || !textB) {
        chunksContainerA.innerHTML = '<div style="opacity:0.4;padding:1rem;font-size:0.8rem">Texto no disponible</div>';
        chunksContainerB.innerHTML = '<div style="opacity:0.4;padding:1rem;font-size:0.8rem">Texto no disponible</div>';
        return;
    }

    const chunksA = chunkText(textA);
    const chunksB = chunkText(textB);

    // Check if we have pre-computed chunk pairs
    const pairData = findChunkPairs(idA, idB);
    const isReversed = pairData && pairData.doc_a !== idA;

    // Build match maps (chunk index -> match info)
    const matchMapA = {};
    const matchMapB = {};

    if (pairData && pairData.top_chunks) {
        pairData.top_chunks.forEach(tc => {
            const chunkAData = isReversed ? tc.chunk_b : tc.chunk_a;
            const chunkBData = isReversed ? tc.chunk_a : tc.chunk_b;

            if (!matchMapA[chunkAData.index]) {
                matchMapA[chunkAData.index] = {
                    targetIndex: chunkBData.index,
                    similarity: tc.similarity,
                    dimension: chunkAData.dimension,
                };
            }
            if (!matchMapB[chunkBData.index]) {
                matchMapB[chunkBData.index] = {
                    targetIndex: chunkAData.index,
                    similarity: tc.similarity,
                    dimension: chunkBData.dimension,
                };
            }
        });
    }

    // Render chunks
    renderChunks(chunksContainerA, chunksA, matchMapA, 'a', chunksContainerB);
    renderChunks(chunksContainerB, chunksB, matchMapB, 'b', chunksContainerA);
}

function renderChunks(container, chunks, matchMap, side, otherContainer) {
    // Limit display for performance
    const maxDisplay = 150;
    const displayChunks = chunks.slice(0, maxDisplay);

    container.innerHTML = '';

    displayChunks.forEach((text, i) => {
        const el = document.createElement('div');
        el.className = 'chunk';
        el.dataset.index = i;

        const match = matchMap[i];
        const dim = match ? match.dimension : guessDimension(text);
        el.dataset.dim = dim;

        if (match) {
            el.classList.add('matched');
            el.innerHTML = `
                <span class="chunk-badge">${match.similarity.toFixed(2)}</span>
                <span class="chunk-index">#${i}</span>
                ${escapeHtml(text.substring(0, 300))}${text.length > 300 ? '...' : ''}
            `;
        } else {
            el.innerHTML = `
                <span class="chunk-index">#${i}</span>
                ${escapeHtml(text.substring(0, 300))}${text.length > 300 ? '...' : ''}
            `;
        }

        // Click to highlight matching chunk
        el.addEventListener('click', () => {
            // Clear all highlights
            container.querySelectorAll('.chunk').forEach(c => c.classList.remove('highlighted'));
            otherContainer.querySelectorAll('.chunk').forEach(c => c.classList.remove('highlighted'));

            el.classList.add('highlighted');

            if (match) {
                const targetEl = otherContainer.querySelector(`.chunk[data-index="${match.targetIndex}"]`);
                if (targetEl) {
                    targetEl.classList.add('highlighted');
                    targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });

        container.appendChild(el);
    });

    if (chunks.length > maxDisplay) {
        const more = document.createElement('div');
        more.style.cssText = 'opacity:0.4;padding:0.5rem;font-size:0.7rem;text-align:center';
        more.textContent = `+ ${chunks.length - maxDisplay} fragmentos más`;
        container.appendChild(more);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
