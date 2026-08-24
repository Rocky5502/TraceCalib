from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from .metrics import BinaryMetrics, binary_metrics


REQUIRED_COLUMNS = {
    "target_model",
    "access_regime",
    "evaluation_mode",
    "y_true",
    "risk_score",
}


@dataclass(frozen=True)
class PortabilityRow:
    target_model: str
    access_regime: str
    evaluation_mode: str
    n: int
    auroc: float
    auprc: float
    brier: float
    ece: float
    auroc_retention: float | None
    ece_degradation: float | None
    success_cost_area_delta: float | None


def _validate(frame: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"missing required RQ5 columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("RQ5 input is empty")
    invalid = set(frame["evaluation_mode"]) - {"in_family", "held_out", "api_portability"}
    if invalid:
        raise ValueError(f"unknown evaluation_mode values: {sorted(invalid)}")


def _metric_for(group: pd.DataFrame) -> BinaryMetrics:
    return binary_metrics(group["y_true"].astype(int), group["risk_score"].astype(float))


def summarize_portability(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize sealed RQ5 predictions without target-specific retuning.

    `in_family` rows provide the frozen local reference. `held_out` rows are
    leave-one-model-family-out predictions. `api_portability` rows are secondary
    black-box portability targets and may have no in-family reference.
    """
    _validate(frame)
    reference: dict[str, tuple[BinaryMetrics, float | None]] = {}
    for model, group in frame[frame["evaluation_mode"] == "in_family"].groupby("target_model"):
        metrics = _metric_for(group)
        sca = float(group["success_cost_area"].mean()) if "success_cost_area" in group else None
        reference[str(model)] = (metrics, sca)

    rows: list[PortabilityRow] = []
    keys = ["target_model", "access_regime", "evaluation_mode"]
    for (model, access, mode), group in frame.groupby(keys, sort=True):
        metrics = _metric_for(group)
        ref = reference.get(str(model))
        retention = None
        ece_delta = None
        sca_delta = None
        if ref is not None and mode != "in_family":
            ref_metrics, ref_sca = ref
            if ref_metrics.auroc != 0:
                retention = metrics.auroc / ref_metrics.auroc
            ece_delta = metrics.ece - ref_metrics.ece
            if "success_cost_area" in group and ref_sca is not None:
                sca_delta = float(group["success_cost_area"].mean()) - ref_sca
        elif mode == "in_family":
            retention = 1.0
            ece_delta = 0.0
            sca_delta = 0.0 if "success_cost_area" in group else None

        rows.append(
            PortabilityRow(
                target_model=str(model),
                access_regime=str(access),
                evaluation_mode=str(mode),
                n=metrics.n,
                auroc=metrics.auroc,
                auprc=metrics.auprc,
                brier=metrics.brier,
                ece=metrics.ece,
                auroc_retention=retention,
                ece_degradation=ece_delta,
                success_cost_area_delta=sca_delta,
            )
        )
    return pd.DataFrame([asdict(row) for row in rows])


def write_portability_outputs(frame: pd.DataFrame, output_dir: str | Path) -> pd.DataFrame:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary = summarize_portability(frame)
    summary.to_csv(out / "model_portability.long.csv", index=False)
    summary.to_json(out / "model_portability.json", orient="records", indent=2)
    return summary


def required_rq5_modes() -> tuple[str, ...]:
    return ("in_family", "held_out", "api_portability")


def local_target_models(config_models: Iterable[str]) -> tuple[str, ...]:
    return tuple(str(model) for model in config_models)
