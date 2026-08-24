from __future__ import annotations

from pathlib import Path

from tracecalib.config import load_yaml


REQUIRED = [
    Path("configs/datasets.yaml"),
    Path("configs/models.yaml"),
    Path("configs/agents.yaml"),
    Path("configs/hardware.yaml"),
    Path("configs/experiments/pilot.yaml"),
    Path("configs/experiments/study.yaml"),
]


def main() -> None:
    for path in REQUIRED:
        data = load_yaml(path)
        if not data:
            raise RuntimeError(f"Empty configuration: {path}")
        print(f"OK {path}")

    study = load_yaml("configs/experiments/study.yaml")
    if study.get("status") != "PRE_FREEZE":
        print(f"WARNING: study status is {study.get('status')}; verify protocol freeze intentionally changed")
    print("Configuration validation complete.")


if __name__ == "__main__":
    main()
