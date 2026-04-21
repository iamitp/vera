"""Thin provider wrapper — Anthropic or OpenAI.

Returns (text, usage) where usage carries token counts, the model that
answered, and an estimated USD cost. Cost table is best-effort: if the
model is not in USD_PER_MTOK the usd field is None, so callers can log
without implying false precision.
"""
from __future__ import annotations
from .config import Provider

# USD per million tokens, keyed by (provider, model). Update as vendors
# publish new pricing. Unknown models fall through to None.
USD_PER_MTOK: dict[tuple[str, str], tuple[float, float]] = {
    ("anthropic", "claude-sonnet-4-6"): (3.0, 15.0),
    ("anthropic", "claude-opus-4-6"): (15.0, 75.0),
    ("anthropic", "claude-opus-4-7"): (15.0, 75.0),
    ("anthropic", "claude-haiku-4-5-20251001"): (0.25, 1.25),
    ("openai", "gpt-4o"): (2.5, 10.0),
    ("openai", "gpt-4o-mini"): (0.15, 0.6),
}


def estimate_usd(provider_name: str, model: str, in_tokens: int, out_tokens: int) -> float | None:
    rates = USD_PER_MTOK.get((provider_name, model))
    if rates is None:
        return None
    rate_in, rate_out = rates
    return (in_tokens / 1_000_000) * rate_in + (out_tokens / 1_000_000) * rate_out


def chat(
    provider: Provider,
    system: str,
    messages: list[dict],
    model: str | None = None,
) -> tuple[str, dict]:
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
        text = resp.content[0].text
        in_tok = getattr(resp.usage, "input_tokens", 0)
        out_tok = getattr(resp.usage, "output_tokens", 0)
    elif provider.name == "openai":
        from openai import OpenAI
        client = OpenAI()
        oai_msgs = [{"role": "system", "content": system}] + messages
        resp = client.chat.completions.create(model=model, messages=oai_msgs, max_tokens=2048)
        text = resp.choices[0].message.content
        in_tok = getattr(resp.usage, "prompt_tokens", 0)
        out_tok = getattr(resp.usage, "completion_tokens", 0)
    else:
        raise ValueError(f"Unknown provider: {provider.name}")

    usage = {
        "provider": provider.name,
        "model": model,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "usd": estimate_usd(provider.name, model, in_tok, out_tok),
    }
    return text, usage
