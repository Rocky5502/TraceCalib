from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GenerationRequest:
    model: str
    messages: list[dict[str, Any]]
    temperature: float = 0.0
    max_tokens: int = 2048
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GenerationResponse:
    text: str
    model: str
    provider: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    request_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResponse:
        raise NotImplementedError
