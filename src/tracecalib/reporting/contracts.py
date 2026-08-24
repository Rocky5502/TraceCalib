from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class TableContract:
    name: str
    primary_key: tuple[str, ...]
    metrics: tuple[str, ...]
    rq: str | None = None


def load_contracts(path: str | Path = "configs/results.yaml") -> dict[str, TableContract]:
    with Path(path).open("r", encoding="utf-8") as handle:
        raw: dict[str, Any] = yaml.safe_load(handle)
    tables = raw.get("tables", {})
    contracts: dict[str, TableContract] = {}
    for name, spec in tables.items():
        contracts[name] = TableContract(
            name=name,
            primary_key=tuple(spec.get("primary_key", [])),
            metrics=tuple(spec.get("metrics", [])),
            rq=spec.get("rq"),
        )
    return contracts


def required_table_names() -> tuple[str, ...]:
    return tuple(load_contracts())
