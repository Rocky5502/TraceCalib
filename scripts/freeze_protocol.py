from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


FILES = [
    "configs/datasets.yaml",
    "configs/models.yaml",
    "configs/agents.yaml",
    "configs/hardware.yaml",
    "configs/experiments/study.yaml",
    "configs/results.yaml",
    "docs/RESEARCH_QUESTIONS.md",
    "docs/EXPERIMENT_PROTOCOL.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="e.g. protocol-v1")
    parser.add_argument("--out", default="artifacts/protocol_freeze.json")
    args = parser.parse_args()
    manifest = {
        "freeze_id": args.id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_sha(),
        "files": {name: digest(Path(name)) for name in FILES},
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
