.PHONY: install validate test lint preflight data pilot

install:
	python -m pip install -e '.[dev,ml]'

validate:
	python scripts/validate_config.py

test:
	pytest

lint:
	ruff check src scripts tests

preflight:
	python scripts/preflight.py --write artifacts/machine_manifest.json

data:
	python scripts/download_datasets.py --all

pilot:
	python scripts/run_pilot.py --config configs/experiments/pilot.yaml
