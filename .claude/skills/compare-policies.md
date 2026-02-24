# /compare-policies — Comparar Políticas

## Trigger
User invokes `/compare-policies <policy1> <policy2> [--dimension <dim>]`
Or: `/compare-policies --all [--dimension <dim>]`

## Behavior
1. **Pairwise comparison**:
   - Retrieve embeddings for both policies from ChromaDB
   - Calculate cosine similarity (overall and per-dimension)
   - Identify most similar and most different sections
   - Generate qualitative comparison summary

2. **Full comparison** (`--all`):
   - Generate 16x16 similarity matrix
   - Identify natural clusters (hierarchical clustering)
   - Score each policy on 7 dimensions
   - Export results to `web/data/results.json`

3. **Dimension filter** (`--dimension`):
   - Focus analysis on one of the 7 dimensions:
     1. Gobernanza y regulación
     2. Currículo e integración educativa
     3. Formación docente
     4. Infraestructura y acceso
     5. Ética y valores
     6. Investigación e innovación
     7. Equidad e inclusión

## Output
- Similarity scores (0-1 scale)
- Key differences and similarities in natural language
- Cluster membership
- Suggested narrative for thesis Chapter 5
