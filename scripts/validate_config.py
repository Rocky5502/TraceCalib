from __future__ import annotations

from pathlib import Path

from tracecalib.config import load_yaml


REQUIRED = [
    Path("configs/datasets.yaml"),
    Path("configs/models.yaml"),
    Path("configs/agents.yaml"),
    Path("configs/hardware.yaml"),
    Path("configs/results.yaml"),
    Path("configs/experiments/pilot.yaml"),
    Path("configs/experiments/study.yaml"),
    Path("configs/experiments/rq5.yaml"),
]


def main() -> None:
    for path in REQUIRED:
        data = load_yaml(path)
        if not data:
            raise RuntimeError(f"Empty configuration: {path}")
        print(f"OK {path}")

    study = load_yaml("configs/experiments/study.yaml")
    if study.get("status") != "PRE_FREEZE":
        print(
            f"WARNING: study status is {study.get('status')}; "
            "verify protocol freeze intentionally changed"
        )

    endpoints = study.get("primary_endpoints", {})
    expected_rqs = {"rq1", "rq2", "rq3", "rq4", "rq5"}
    missing = expected_rqs.difference(endpoints)
    if missing:
        raise RuntimeError(f"Missing primary endpoints for: {sorted(missing)}")

    rq5 = load_yaml("configs/experiments/rq5.yaml")
    targets = rq5.get("local_leave_one_family_out", {}).get("targets", [])
    if len(targets) < 3:
        raise RuntimeError("RQ5 requires at least three frozen local target families")
    if rq5.get("api_portability", {}).get("provider_ranking_is_objective"):
        raise RuntimeError("RQ5 API tier must remain a portability study, not a provider leaderboard")

    print("Configuration validation complete: RQ1-RQ5 present and PRE_FREEZE guards intact.")


if __name__ == "__main__":
    main()
