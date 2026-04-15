"""Provenance tagging. Every autonomous memory write gets stamped."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Literal

ProvenanceKind = Literal["OBSERVED", "INFERRED", "ASSUMED", "CANDIDATE", "RULE", "EXTERNAL"]

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
