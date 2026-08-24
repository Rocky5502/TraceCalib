from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from tracecalib.evaluation.rq5 import write_portability_outputs


def synthetic_fixture() -> pd.DataFrame:
    """Small deterministic fixture for plumbing tests only; never a research result."""
    rows = []
    models = ["qwen3_8b", "mistral_7b_instruct_v03", "gemma_3_12b_it"]
    for m_idx, model in enumerate(models):
        for mode_idx, mode in enumerate(("in_family", "held_out")):
            for idx in range(24):
                y = idx % 2
                base = 0.18 + 0.64 * y
                score = min(
                    0.98,
                    max(0.02, base - 0.04 * mode_idx + 0.005 * ((idx + m_idx) % 5)),
                )
                rows.append(
                    {
                        "target_model": model,
                        "access_regime": "local",
                        "evaluation_mode": mode,
                        "y_true": y,
                        "risk_score": score,
                        "success_cost_area": 0.70 - 0.02 * mode_idx,
                    }
                )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/smoke/rq5"))
    args = parser.parse_args()
    if "results" in args.output_dir.parts:
        raise SystemExit("Synthetic smoke fixtures may not be written under results/.")
    out = write_portability_outputs(synthetic_fixture(), args.output_dir)
    print(out.to_string(index=False))
    print("SMOKE ONLY - these values are synthetic and MUST NOT appear in the manuscript.")


if __name__ == "__main__":
    main()
