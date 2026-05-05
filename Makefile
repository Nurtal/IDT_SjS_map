# SjD-BoolAttractors — convenience shortcuts
# Usage: make <target>

.PHONY: help env all figures clean test lint phase1 phase2 phase3 phase4 phase5

PYTHON  := .venv/bin/python3
CORES   := 4

help:
	@echo "SjD-BoolAttractors targets:"
	@echo "  make env        Create/update .venv from pyproject.toml"
	@echo "  make all        Run full pipeline (phases 1-5) via Snakemake"
	@echo "  make figures    Generate all manuscript figures"
	@echo "  make phase1     Sanitize BNET only"
	@echo "  make phase2     Compute attractors only"
	@echo "  make phase3     Annotate attractors only"
	@echo "  make phase4     Run control analysis only"
	@echo "  make phase5     Run therapeutic validation only"
	@echo "  make test       Run pytest suite"
	@echo "  make lint       Run ruff + mypy"
	@echo "  make clean      Remove generated results (keeps raw data)"

env:
	python3 -m venv .venv
	.venv/bin/pip install -q --upgrade pip
	.venv/bin/pip install -q -e ".[dev]"

all:
	$(PYTHON) -m snakemake --snakefile workflow/Snakefile --cores $(CORES)

figures:
	$(PYTHON) -m snakemake --snakefile workflow/Snakefile --cores $(CORES) all_figures

phase1:
	$(PYTHON) src/conversion/sanitize_bnet.py \
	    models/sbmlqual/v1/sjd_map_reduced.bnet \
	    models/sbmlqual/v1/sjd_map_reduced_clean.bnet \
	    data/processed/bnet_name_map.csv

phase2:
	$(PYTHON) src/analysis/compute_attractors.py

phase3:
	$(PYTHON) src/validation/annotate_attractors.py

phase4:
	$(PYTHON) src/validation/control_analysis.py

phase5:
	$(PYTHON) src/validation/therapeutic_validation.py

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check src/ workflow/
	$(PYTHON) -m mypy src/ --ignore-missing-imports

clean:
	rm -rf results/phase2/*.csv results/phase3/*.csv results/phase4/*.csv \
	       results/phase5/*.csv results/phase5/*.md results/phase4/*.md \
	       figures/phase2/*.png figures/phase3/*.png figures/phase4/*.png \
	       figures/phase5/*.png logs/
	@echo "Cleaned regenerable outputs. Raw data and models preserved."
