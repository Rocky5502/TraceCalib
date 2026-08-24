from __future__ import annotations

import httpx

from .base import BaseProvider, GenerationRequest, GenerationResponse


class AnthropicProvider(BaseProvider):
    name = "anthropic"

    def __init__(self, api_key: str, timeout: float = 180.0):
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        system = None
        messages = []
        for message in request.messages:
            if message.get("role") == "system" and system is None:
                system = message.get("content", "")
            else:
                messages.append(message)
        payload = {
            "model": request.model,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
        if system:
            payload["system"] = system
        payload.update(request.extra)
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload)
            response.raise_for_status()
        data = response.json()
        text = "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
        usage = data.get("usage", {})
        return GenerationResponse(
            text=text,
            model=data.get("model", request.model),
            provider=self.name,
            input_tokens=usage.get("input_tokens"),
            output_tokens=usage.get("output_tokens"),
            request_id=data.get("id"),
            raw=data,
        )
