# /build-web — Actualizar Visualización Web

## Trigger
User invokes `/build-web`

## Behavior
1. Run `python3 -m pipeline.export` to regenerate `web/data/results.json`
2. Verify JSON structure contains:
   - `policies`: array of policy metadata
   - `similarity_matrix`: 16x16 cosine similarities
   - `dimension_scores`: 16x7 scores
   - `clusters`: hierarchical grouping results
   - `dimension_labels`: the 7 dimension names
3. Verify `web/index.html` references are correct
4. Open browser or suggest: `python3 -m http.server 8000 --directory web/`

## Data Format
```json
{
  "policies": [...],
  "similarity_matrix": [[...]],
  "dimension_scores": [[...]],
  "clusters": [...],
  "dimension_labels": [...],
  "metadata": {
    "generated_at": "ISO date",
    "embedding_model": "text-embedding-3-small",
    "num_policies": 16
  }
}
```
