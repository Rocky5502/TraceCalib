#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f pyproject.toml ]]; then
  echo "Run this script from the TraceCalib repository root." >&2
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[dev,ml,local]'

mkdir -p artifacts reports data/raw data/manifests/downloaded results

python scripts/validate_config.py
python scripts/preflight.py --write artifacts/machine_manifest.json
python scripts/check_local_models.py | tee artifacts/local_models.json

echo
printf '%s\n' "Bootstrap complete." "Next:" "  1. inspect artifacts/machine_manifest.json" "  2. inspect artifacts/local_models.json" "  3. configure .env without committing it" "  4. run python scripts/download_datasets.py --all" "  5. give Codex CODEX_PROMPT.md"
