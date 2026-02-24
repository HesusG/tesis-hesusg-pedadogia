# /add-policy — Agregar Política al Corpus

## Trigger
User invokes `/add-policy <country> <document_name> [url]`

## Behavior
1. If URL provided, help download/extract the document
2. Extract text content from PDF/DOCX/HTML
3. Create processed text file in `policies/processed/{country}/`
4. Update `policies/metadata.json` with entry:
   ```json
   {
     "policy_id": "country_short_name_year",
     "country": "...",
     "region": "europa|americas|asia_pacifico|internacional",
     "title": "...",
     "title_es": "...",
     "year": 2024,
     "language": "en|es|fr|de|...",
     "source_url": "...",
     "document_type": "strategy|framework|regulation|guidelines|curriculum",
     "pages": null,
     "status": "raw|processed|ingested"
   }
   ```
5. Run ingestion into ChromaDB: `python3 -m pipeline.ingest --policy {policy_id}`
6. Verify ingestion: report chunk count and sample

## Countries
Europa: EU, España, Francia, Alemania, Finlandia, Estonia
Américas: EEUU, Canadá, México, Brasil, Chile, Colombia
Asia-Pacífico: China, Japón, Corea del Sur, Singapur, India, Australia
Internacional: UNESCO, OCDE, WEF, Banco Mundial
