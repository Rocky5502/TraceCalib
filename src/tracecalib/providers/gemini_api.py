from __future__ import annotations

import httpx

from .base import BaseProvider, GenerationRequest, GenerationResponse


class GeminiProvider(BaseProvider):
    name = "google"

    def __init__(self, api_key: str, timeout: float = 180.0):
        self.api_key = api_key
        self.timeout = timeout

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        contents = []
        system_text = []
        for message in request.messages:
            role = message.get("role")
            content = str(message.get("content", ""))
            if role == "system":
                system_text.append(content)
                continue
            contents.append({"role": "model" if role == "assistant" else "user", "parts": [{"text": content}]})
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            },
        }
        if system_text:
            payload["systemInstruction"] = {"parts": [{"text": "\n".join(system_text)}]}
        payload.update(request.extra)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{request.model}:generateContent"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, params={"key": self.api_key}, json=payload)
            response.raise_for_status()
        data = response.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        text = "".join(str(part.get("text", "")) for part in parts)
        usage = data.get("usageMetadata", {})
        return GenerationResponse(
            text=text,
            model=request.model,
            provider=self.name,
            input_tokens=usage.get("promptTokenCount"),
            output_tokens=usage.get("candidatesTokenCount"),
            request_id=response.headers.get("x-request-id"),
            raw=data,
        )
