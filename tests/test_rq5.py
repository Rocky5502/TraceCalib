import pandas as pd
import pytest

from tracecalib.evaluation.rq5 import summarize_portability


def test_rq5_retention_is_computed_against_in_family_reference() -> None:
    rows = []
    for mode, shift in [("in_family", 0.0), ("held_out", -0.08)]:
        for i in range(40):
            y = i % 2
            rows.append(
                {
                    "target_model": "model_a",
                    "access_regime": "local",
                    "evaluation_mode": mode,
                    "y_true": y,
                    "risk_score": max(0.01, min(0.99, 0.15 + 0.70 * y + shift)),
                    "success_cost_area": 0.8 if mode == "in_family" else 0.7,
                }
            )
    summary = summarize_portability(pd.DataFrame(rows))
    held = summary[summary.evaluation_mode == "held_out"].iloc[0]
    assert 0 < held.auroc_retention <= 1.0
    assert held.success_cost_area_delta == pytest.approx(-0.1)


def test_rq5_refuses_missing_contract_columns() -> None:
    with pytest.raises(ValueError, match="missing required RQ5 columns"):
        summarize_portability(pd.DataFrame({"y_true": [0, 1], "risk_score": [0.2, 0.8]}))
