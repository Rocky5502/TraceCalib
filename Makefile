.PHONY: install validate test lint preflight data pilot smoke-rq5 rq5

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

smoke-rq5:
	python scripts/smoke_rq5.py

rq5:
	python scripts/evaluate_rq5.py --predictions artifacts/frozen/rq5_predictions.parquet --output-dir results/rq5
