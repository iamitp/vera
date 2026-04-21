"""Provenance tagging. Every autonomous memory write gets stamped."""
from __future__ import annotations
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal

ProvenanceKind = Literal[
    "OBSERVED", "INFERRED", "ASSUMED", "CANDIDATE", "RULE", "EXTERNAL", "MALFORMED",
]

SYSTEM_ADDENDUM = """
PROVENANCE RULES (non-negotiable). Every factual claim you write into memory
must be tagged with one of:
  [OBSERVED]   user said it verbatim this conversation
  [INFERRED]   your extrapolation (include confidence: low|med|high)
  [ASSUMED]    you guessed because you were not told
  [CANDIDATE]  auto-captured from an external source, unverified
  [RULE]       user-stated behavioural rule, binding
  [EXTERNAL]   from a tool or citeable source
Never write an untagged claim. If you are uncertain, use INFERRED or ASSUMED,
not OBSERVED. Provenance is the audit trail; lying in it is the one
unforgivable error.
""".strip()

def log_write(kind: ProvenanceKind, content: str, source: str, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(),
        "kind": kind,
        "source": source,
        "content": content[:2000],
    }
    with log_path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def log_usage(usage: dict, source: str, log_path: Path) -> None:
    """Append a USAGE entry (one per LLM call) to the provenance log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(),
        "kind": "USAGE",
        "source": source,
        "provider": usage.get("provider"),
        "model": usage.get("model"),
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "usd": usage.get("usd"),
    }
    with log_path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def spend_since(log_path: Path, days: int) -> tuple[float, int]:
    """Return (total_usd, call_count) for USAGE entries in the last N days.

    Unknown-cost calls (usd=None) contribute 0 USD but still count.
    """
    if not log_path.exists():
        return 0.0, 0
    cutoff = datetime.now() - timedelta(days=days)
    total = 0.0
    calls = 0
    for raw in log_path.read_text().splitlines():
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if entry.get("kind") != "USAGE":
            continue
        try:
            ts = datetime.fromisoformat(entry["ts"])
        except (KeyError, ValueError):
            continue
        if ts < cutoff:
            continue
        calls += 1
        usd = entry.get("usd")
        if isinstance(usd, (int, float)):
            total += usd
    return total, calls
