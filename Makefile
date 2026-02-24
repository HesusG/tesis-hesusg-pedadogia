# Tesis de Maestría en Pedagogía — UPAEP
# Hesus García Cobos

SHELL := /bin/bash
TEX_DIR := document
TEX_MAIN := main
OUTPUT_DIR := output
PIPELINE_DIR := pipeline
WEB_DIR := web

.PHONY: all pdf docx pipeline web figures setup clean status help

all: pdf web

# ── LaTeX ──────────────────────────────────────────────
pdf:
	cd $(TEX_DIR) && pdflatex $(TEX_MAIN).tex
	cd $(TEX_DIR) && bibtex $(TEX_MAIN) || true
	cd $(TEX_DIR) && pdflatex $(TEX_MAIN).tex
	cd $(TEX_DIR) && pdflatex $(TEX_MAIN).tex
	cp $(TEX_DIR)/$(TEX_MAIN).pdf $(OUTPUT_DIR)/tesis.pdf
	@echo "✓ PDF generado: $(OUTPUT_DIR)/tesis.pdf"

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
	@echo "  make clean     — Limpiar archivos auxiliares"
