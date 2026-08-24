from __future__ import annotations

import httpx

from .base import BaseProvider, GenerationRequest, GenerationResponse


class OpenAICompatibleProvider(BaseProvider):
    """Small adapter for OpenAI-compatible Chat Completions endpoints.

    Suitable for local vLLM/TGI-style gateways and DeepSeek. OpenAI itself may
    use a dedicated Responses API adapter in the frozen implementation; this
    bootstrap client exists for provider-normalization smoke tests.
    """

    def __init__(self, name: str, base_url: str, api_key: str, timeout: float = 180.0):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        payload = {
            "model": request.model,
            "messages": request.messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            **request.extra,
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
        data = response.json()
        choice = data["choices"][0]
        usage = data.get("usage", {})
        return GenerationResponse(
            text=choice["message"].get("content", ""),
            model=data.get("model", request.model),
            provider=self.name,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
            request_id=response.headers.get("x-request-id") or data.get("id"),
            raw=data,
        )
