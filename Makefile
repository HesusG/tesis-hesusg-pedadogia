# Tesis de Maestría en Pedagogía — UPAEP
# Hesus García Cobos

SHELL := /bin/bash
TEX_DIR := document
TEX_MAIN := main
OUTPUT_DIR := output
PIPELINE_DIR := pipeline
WEB_DIR := web

.PHONY: all pdf pdf-cap01 docx pipeline web figures setup clean status chunks help refs-audit refs-audit-cap01 refs-download refs-check verify-cap01 ingest-refs factcheck-cap01 compute-advanced download-policies topics language-control validate ingest-analects confucian-mvp

all: pdf web

# ── LaTeX ──────────────────────────────────────────────
pdf:
	cd $(TEX_DIR) && pdflatex $(TEX_MAIN).tex
	cd $(TEX_DIR) && bibtex $(TEX_MAIN) || true
	cd $(TEX_DIR) && pdflatex $(TEX_MAIN).tex
	cd $(TEX_DIR) && pdflatex $(TEX_MAIN).tex
	cp $(TEX_DIR)/$(TEX_MAIN).pdf $(OUTPUT_DIR)/tesis.pdf
	@echo "✓ PDF generado: $(OUTPUT_DIR)/tesis.pdf"

pdf-cap01:
	cd $(TEX_DIR) && pdflatex main_cap01.tex
	cd $(TEX_DIR) && bibtex main_cap01 || true
	cd $(TEX_DIR) && pdflatex main_cap01.tex
	cd $(TEX_DIR) && pdflatex main_cap01.tex
	cp $(TEX_DIR)/main_cap01.pdf $(OUTPUT_DIR)/tesis_cap01.pdf
	@echo "✓ PDF Cap01: $(OUTPUT_DIR)/tesis_cap01.pdf"

pdf-shorter:
	cd $(TEX_DIR) && pdflatex main_shorter.tex
	cd $(TEX_DIR) && bibtex main_shorter || true
	cd $(TEX_DIR) && pdflatex main_shorter.tex
	cd $(TEX_DIR) && pdflatex main_shorter.tex
	cp $(TEX_DIR)/main_shorter.pdf $(OUTPUT_DIR)/tesis_shorter.pdf
	@echo "✓ PDF Shorter: $(OUTPUT_DIR)/tesis_shorter.pdf"

docx-shorter:
	cd $(TEX_DIR) && pandoc main_shorter.tex \
		--from=latex \
		--to=docx \
		--bibliography=referencias.bib \
		--citeproc \
		-o ../$(OUTPUT_DIR)/tesis_shorter.docx
	@echo "✓ DOCX Shorter: $(OUTPUT_DIR)/tesis_shorter.docx"

docx: pdf
	cd $(TEX_DIR) && pandoc $(TEX_MAIN).tex \
		--from=latex \
		--to=docx \
		--bibliography=referencias.bib \
		--citeproc \
		--reference-doc=../scripts/upaep-reference.docx \
		-o ../$(OUTPUT_DIR)/tesis.docx 2>/dev/null || \
	cd $(TEX_DIR) && pandoc $(TEX_MAIN).tex \
		--from=latex \
		--to=docx \
		--bibliography=referencias.bib \
		--citeproc \
		-o ../$(OUTPUT_DIR)/tesis.docx
	@echo "✓ DOCX generado: $(OUTPUT_DIR)/tesis.docx"

# ── Pipeline ───────────────────────────────────────────
pipeline:
	python3 -m pipeline.ingest --all
	python3 -m pipeline.similarity
	python3 -m pipeline.analysis
	python3 -m pipeline.export
	@echo "✓ Pipeline completo"

ingest:
	python3 -m pipeline.ingest --all

similarity:
	python3 -m pipeline.similarity

export:
	python3 -m pipeline.export
	@echo "✓ Datos exportados a $(WEB_DIR)/data/results.json"

chunks:
	python3 -m pipeline.export_chunks
	@echo "✓ chunk_pairs.json exportado a $(WEB_DIR)/data/"

# ── Web ────────────────────────────────────────────────
web: export
	@echo "✓ Visualización actualizada en $(WEB_DIR)/index.html"

# ── Figures ────────────────────────────────────────────
figures:
	python3 -m pipeline.visualize
	@echo "✓ Figuras generadas en $(TEX_DIR)/figures/generated/"

# ── Setup ──────────────────────────────────────────────
setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	@echo "✓ Entorno configurado. Activar con: source .venv/bin/activate"

# ── Status ─────────────────────────────────────────────
status:
	@echo "═══ Estado de la Tesis ═══"
	@echo ""
	@for f in $(TEX_DIR)/chapters/cap*.tex; do \
		name=$$(basename $$f .tex); \
		words=$$(detex $$f 2>/dev/null | wc -w || echo 0); \
		todos=$$(grep -c 'TODO\|FIXME\|XXX' $$f 2>/dev/null || echo 0); \
		cites=$$(grep -co '\\citep\|\\citet' $$f 2>/dev/null || echo 0); \
		printf "  %-30s  %5s palabras  %2s citas  %2s TODOs\n" "$$name" "$$words" "$$cites" "$$todos"; \
	done
	@echo ""
	@total=$$(cat $(TEX_DIR)/chapters/cap*.tex | detex 2>/dev/null | wc -w || echo 0); \
	echo "  Total: $$total palabras (~$$(( $$total / 250 )) páginas)"

# ── References ────────────────────────────────────────
refs-audit:
	python3 references/ref_audit.py

refs-audit-cap01:
	python3 references/ref_audit.py --chapter cap01

refs-download:
	python3 references/download_references.py

refs-check:
	python3 references/ref_audit.py --check

# ── Verify ────────────────────────────────────────────
verify-cap01:
	python3 -m pipeline.verify_chapter --chapter cap01

# ── v2 Analysis (unsupervised-first) ─────────────────
topics:
	python3 -m pipeline.topic_model
	@echo "✓ BERTopic: temas no supervisados generados"

language-control:
	python3 -m pipeline.language_control
	@echo "✓ Análisis de control lingüístico completado"

validate:
	python3 -m pipeline.validation
	@echo "✓ Validación pre-registro vs no-supervisado completada"

# ── Fact-check ────────────────────────────────────────
ingest-refs:
	python3 -m pipeline.ingest_bibliography

factcheck-cap01:
	python3 -m pipeline.verify_facts --chapter cap01

# ── Confucian axes MVP (usa .venv por sentence-transformers) ──
ingest-analects:
	.venv/bin/python -m pipeline.ingest_analects

confucian-mvp:
	.venv/bin/python -m pipeline.confucian_axes
	@echo "✓ Ejes confucianos MVP → web/data/confucian_mvp.json"

# ── Advanced compute ─────────────────────────────────
compute-advanced:
	python3 scripts/compute_advanced.py
	@echo "✓ Datos avanzados (UMAP, dendrograma, Sankey) generados"

# ── Download policies ────────────────────────────────
download-policies:
	python3 scripts/download_policies.py
	@echo "✓ Políticas descargadas"

# ── Clean ──────────────────────────────────────────────
clean:
	cd $(TEX_DIR) && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
	@echo "✓ Archivos auxiliares eliminados"

# ── Help ───────────────────────────────────────────────
help:
	@echo "Comandos disponibles:"
	@echo "  make pdf       — Compilar tesis a PDF"
	@echo "  make docx      — Exportar tesis a Word"
	@echo "  make pipeline  — Ejecutar pipeline completo"
	@echo "  make ingest    — Solo ingesta de políticas"
	@echo "  make export    — Solo exportar datos para web"
	@echo "  make web       — Actualizar visualización web"
	@echo "  make figures   — Generar figuras para tesis"
	@echo "  make setup     — Configurar entorno Python"
	@echo "  make status    — Ver progreso por capítulo"
	@echo "  make chunks    — Exportar chunk_pairs.json para explorador"
	@echo "  make pdf-cap01 — Compilar PDF solo hasta capítulo 1"
	@echo "  make refs-audit     — Auditar referencias .bib vs PDFs locales"
	@echo "  make refs-audit-cap01 — Auditar solo cap01"
	@echo "  make refs-download  — Descargar PDFs via Unpaywall/URLs"
	@echo "  make refs-check     — Verificar cobertura (exit 1 si hay gaps)"
	@echo "  make verify-cap01   — Verificar cap01 semánticamente contra ChromaDB"
	@echo "  make ingest-refs    — Ingestar PDFs de bibliografía para fact-check"
	@echo "  make factcheck-cap01 — Fact-check numérico de cap01 (híbrido)"
	@echo "  make topics     — BERTopic: análisis no supervisado (Fase 1)"
	@echo "  make language-control — Control lingüístico (Fase 3)"
	@echo "  make validate   — Validar pre-registro vs no-supervisado"
	@echo "  make ingest-analects  — Indexar Analectas en ChromaDB (MVP)"
	@echo "  make confucian-mvp    — Ejes confucianos sobre 3 políticas (MVP)"
	@echo "  make compute-advanced — Generar datos avanzados (UMAP, Sankey)"
	@echo "  make download-policies — Descargar PDFs de políticas"
	@echo "  make clean     — Limpiar archivos auxiliares"
