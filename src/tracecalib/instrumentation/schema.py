from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class Stage(StrEnum):
    SPECIFICATION = "specification"
    RETRIEVAL = "retrieval"
    PLANNING = "planning"
    GENERATION = "generation"
    EXECUTION = "execution"
    REPAIR = "repair"
    OTHER = "other"


class RunStatus(StrEnum):
    COMPLETED_VALID_SUCCESS = "completed_valid_success"
    COMPLETED_VALID_AGENT_FAILURE = "completed_valid_agent_failure"
    INFRASTRUCTURE_FAILURE_RERUNNABLE = "infrastructure_failure_rerunnable"
    INFRASTRUCTURE_FAILURE_EXCLUDED = "infrastructure_failure_excluded"
    INVALID_TRACE = "invalid_trace"
    PROVIDER_FAILURE = "provider_failure"
    BUDGET_CANCELLED = "budget_cancelled"
    PROTOCOL_EXCLUSION = "protocol_exclusion"
    DUPLICATE_OR_LEAKAGE_EXCLUSION = "duplicate_or_leakage_exclusion"


class TraceEvent(BaseModel):
    schema_version: str = "0.1"
    run_id: str = Field(min_length=1)
    step_id: int = Field(ge=0)
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    progress: float = Field(ge=0.0, le=1.0)
    stage: Stage
    event_type: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    model_id: str = Field(min_length=1)
    provider: str
    task_id: str = Field(min_length=1)
    repository: str | None = None
    seed: int | None = None
    prompt_hash: str | None = None
    observation_hash: str | None = None
    tool_name: str | None = None
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    latency_ms: float | None = Field(default=None, ge=0)
    cumulative_cost_usd: float | None = Field(default=None, ge=0)
    uncertainty: dict[str, float] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def check_uncertainty_values(self) -> "TraceEvent":
        for key, value in self.uncertainty.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"uncertainty[{key!r}] must be numeric")
        return self


class RunRecord(BaseModel):
    schema_version: str = "0.1"
    run_id: str
    task_id: str
    repository: str
    dataset_revision: str
    agent_id: str
    agent_revision: str
    model_id: str
    model_revision: str | None = None
    provider: str
    condition: str
    seed: int
    requested_at_utc: datetime
    completed_at_utc: datetime | None = None
    status: RunStatus | None = None
    resolved: bool | None = None
    infrastructure_reason: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    tests_run: int = 0
    wall_seconds: float = 0.0
    estimated_cost_usd: float = 0.0
