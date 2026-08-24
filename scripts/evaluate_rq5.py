from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from tracecalib.evaluation.rq5 import write_portability_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate frozen RQ5 portability predictions.")
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results/rq5"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = (
        pd.read_parquet(args.predictions)
        if args.predictions.suffix == ".parquet"
        else pd.read_csv(args.predictions)
    )
    summary = write_portability_outputs(frame, args.output_dir)
    print(summary.to_string(index=False))
    print(f"Wrote RQ5 outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
