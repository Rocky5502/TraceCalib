from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from tracecalib.config import load_yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the frozen pilot run plan. Agent execution adapters are added in the next implementation phase.")
    parser.add_argument("--config", default="configs/experiments/pilot.yaml")
    parser.add_argument("--out", default="artifacts/pilot_plan.json")
    args = parser.parse_args()

    config = load_yaml(args.config)
    plan = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "config": config,
        "execution_status": "PLANNED_NOT_EXECUTED",
        "required_next_components": [
            "SWE-bench task selector and Docker evaluator",
            "mini-SWE-agent adapter",
            "Agentless adapter",
            "local model server launcher",
            "normalized trace writer",
            "run accounting and failure taxonomy",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"Pilot plan written to {out}")
    print("No benchmark run was executed. Implement and validate adapters before scale-up.")


if __name__ == "__main__":
    main()
