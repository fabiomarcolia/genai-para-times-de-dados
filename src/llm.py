from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests

from src.utils import env


@dataclass
class LLMResponse:
    text: str


def _ollama_generate(prompt: str) -> str:
    base_url = env("OLLAMA_BASE_URL", "http://localhost:11434")
    model = env("OLLAMA_MODEL", "llama3.1")
    r = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json().get("response", "")


def _openai_generate(prompt: str) -> str:
    # Implementação mínima (sem depender do SDK) via HTTP para manter o repo simples.
    # Você pode trocar pelo SDK oficial se preferir.
    api_key = env("OPENAI_API_KEY")
    model = env("OPENAI_MODEL", "gpt-4o-mini")
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": float(os.environ.get("TEMPERATURE", "0.2")),
            "max_tokens": int(os.environ.get("MAX_TOKENS", "600")),
        },
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]


def generate(prompt: str) -> LLMResponse:
    provider = os.environ.get("LLM_PROVIDER", "none").lower().strip()
    if provider == "none":
        return LLMResponse(text="")
    if provider == "ollama":
        return LLMResponse(text=_ollama_generate(prompt))
    if provider == "openai":
        return LLMResponse(text=_openai_generate(prompt))
    raise ValueError(f"Unknown LLM_PROVIDER={provider}")
