.DEFAULT_GOAL := help
PIXI ?= pixi
RUN = $(PIXI) run --locked
MODE ?= replay
export OFFLINE = 1
export MPLCONFIGDIR = $(CURDIR)/build/matplotlib

.PHONY: help test lint check-data check-contracts verify-data all acquire storage-report manifests clean-env
help:
	@echo 'Targets: test lint check-data check-contracts verify-data all acquire storage-report manifests clean-env'
test:
	$(RUN) python -m pytest -q
lint:
	$(RUN) ruff check code tests
	$(RUN) ruff format --check code tests
check-data:
	$(RUN) python -m pytest -q tests/integrity tests/readers
check-contracts:
	$(RUN) python code/check_contracts.py --mode $${CHECK_MODE:-full}
verify-data:
	$(RUN) python code/verify_data.py
all: verify-data
	$(RUN) python code/01a_sample_coverage.py
	$(RUN) python code/02f_build_outcome_coverage.py
	$(RUN) python code/04_reproduce.py --spec config/specs/historical_international.yaml
	$(RUN) python code/04_reproduce.py --spec config/specs/historical_us_states.yaml
	$(RUN) python code/historical_summary.py
	$(RUN) python code/assess_index_coverage.py
acquire:
	OFFLINE=0 $(RUN) python code/acquire_sources.py
storage-report:
	$(RUN) python code/storage_report.py
manifests:
	$(RUN) python code/build_manifests.py
clean-env:
	$(RUN) python code/clean_env.py

include $(wildcard make/*.mk)
