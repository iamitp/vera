"""Thin provider wrapper — Anthropic or OpenAI."""
from __future__ import annotations
from typing import Iterable
from .config import Provider

def chat(provider: Provider, system: str, messages: list[dict], model: str | None = None) -> str:
    model = model or provider.chat_model
    if provider.name == "anthropic":
        from anthropic import Anthropic
        client = Anthropic()
        resp = client.messages.create(
            model=model,
            max_tokens=2048,
            system=system,
            messages=messages,
        )
        return resp.content[0].text
    elif provider.name == "openai":
        from openai import OpenAI
        client = OpenAI()
        oai_msgs = [{"role": "system", "content": system}] + messages
        resp = client.chat.completions.create(model=model, messages=oai_msgs, max_tokens=2048)
        return resp.choices[0].message.content
    raise ValueError(f"Unknown provider: {provider.name}")
