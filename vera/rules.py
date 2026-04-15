"""Rule enforcement layer. Rules block, not remind."""
from __future__ import annotations
from pathlib import Path
from typing import Optional

DEFAULT_RULES = """# Vera Rules

These rules are enforced on every assistant response. Violations fail the turn
and the model is asked to regenerate. Edit freely — your rules, your binding.

## Banned phrases
- "great question"
- "absolutely"
- "I'd be happy to"
- "you're right"
- "I notice"
- "in today's world"
- "needless to say"

## Style
- No em dashes (—). Use commas or periods.
- No emojis unless user uses them first.
- Start with the answer, not a preamble.

## Epistemic
- Do not claim certainty without evidence. Say "I'm not sure" when you're not.
- If you are agreeing because agreeing is easy, name the disagreement first.
"""

def ensure_rules(path: Path) -> str:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(DEFAULT_RULES)
    return path.read_text()

def check_response(response: str, rules_text: str) -> Optional[str]:
    """Returns violation message if a banned phrase is found, else None."""
    lower = response.lower()
    violations = []
    for line in rules_text.splitlines():
        line = line.strip()
        if line.startswith("- \"") and line.endswith("\""):
            phrase = line[3:-1].lower()
            if phrase in lower:
                violations.append(phrase)
    if "—" in response and "No em dashes" in rules_text:
        violations.append("em dash")
    if not violations:
        return None
    return "Rule violations: " + ", ".join(violations) + ". Regenerate without these."
