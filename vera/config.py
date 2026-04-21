"""Vera config: paths, provider selection, model choice."""
from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass

VERA_HOME = Path(os.environ.get("VERA_HOME", Path.home() / "vera"))
MEMORY_DIR = VERA_HOME / "memory"
AUDIT_DIR = VERA_HOME / "audit"
RULES_FILE = VERA_HOME / "rules.md"
PROVENANCE_LOG = VERA_HOME / "memory" / "_log.jsonl"
CONFIG_FILE = VERA_HOME / "config.yaml"

@dataclass
class Provider:
    name: str
    chat_model: str
    audit_model: str

def detect_provider() -> Provider:
    audit_override = os.environ.get("VERA_AUDIT_MODEL")
    if os.environ.get("ANTHROPIC_API_KEY"):
        return Provider(
            "anthropic",
            "claude-sonnet-4-6",
            audit_override or "claude-opus-4-6",
        )
    if os.environ.get("OPENAI_API_KEY"):
        return Provider("openai", "gpt-4o", audit_override or "gpt-4o")
    raise SystemExit("Set ANTHROPIC_API_KEY or OPENAI_API_KEY.")
