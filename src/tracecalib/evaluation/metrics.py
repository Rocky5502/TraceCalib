from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score


@dataclass(frozen=True)
class BinaryMetrics:
    auroc: float
    auprc: float
    brier: float
    ece: float
    n: int


def expected_calibration_error(
    y_true: Iterable[int], y_score: Iterable[float], *, bins: int = 10
) -> float:
    """Compute equal-width expected calibration error for probabilities in [0, 1]."""
    y = np.asarray(list(y_true), dtype=float)
    p = np.asarray(list(y_score), dtype=float)
    if y.shape != p.shape:
        raise ValueError("y_true and y_score must have identical shape")
    if y.size == 0:
        raise ValueError("at least one observation is required")
    if np.any((p < 0.0) | (p > 1.0)):
        raise ValueError("probabilities must lie in [0, 1]")
    edges = np.linspace(0.0, 1.0, bins + 1)
    ids = np.minimum(np.digitize(p, edges[1:-1], right=True), bins - 1)
    ece = 0.0
    for idx in range(bins):
        mask = ids == idx
        if not np.any(mask):
            continue
        ece += float(mask.mean()) * abs(float(p[mask].mean()) - float(y[mask].mean()))
    return float(ece)


def binary_metrics(y_true: Iterable[int], y_score: Iterable[float], *, bins: int = 10) -> BinaryMetrics:
    y = np.asarray(list(y_true), dtype=int)
    p = np.asarray(list(y_score), dtype=float)
    if y.size == 0:
        raise ValueError("at least one observation is required")
    if len(np.unique(y)) < 2:
        raise ValueError("AUROC/AUPRC require both outcome classes")
    return BinaryMetrics(
        auroc=float(roc_auc_score(y, p)),
        auprc=float(average_precision_score(y, p)),
        brier=float(brier_score_loss(y, p)),
        ece=expected_calibration_error(y, p, bins=bins),
        n=int(y.size),
    )
