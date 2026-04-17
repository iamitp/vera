#!/usr/bin/env python3
"""Verify docs/index.html embeds the current PROMPT.md fenced block.

The landing page ships the prompt as an inline JS template literal.
If PROMPT.md is edited without updating docs/index.html, phone visitors
copy a stale prompt. This check fails CI in that case.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROMPT_MD = REPO / "PROMPT.md"
LANDING = REPO / "docs" / "index.html"

FENCE_RE = re.compile(r"```\n(.*?)\n```", re.DOTALL)
JS_PROMPT_RE = re.compile(r"const PROMPT = `(.*?)`;", re.DOTALL)


def extract_prompt_md() -> str:
    text = PROMPT_MD.read_text()
    match = FENCE_RE.search(text)
    if not match:
        sys.exit(f"{PROMPT_MD}: no fenced prompt block found")
    return match.group(1).strip()


def extract_landing_prompt() -> str:
    text = LANDING.read_text()
    match = JS_PROMPT_RE.search(text)
    if not match:
        sys.exit(f"{LANDING}: no `const PROMPT = ...` template literal found")
    return match.group(1).strip()


def main() -> int:
    md = extract_prompt_md()
    js = extract_landing_prompt()
    if md == js:
        print("PROMPT.md and docs/index.html are in sync.")
        return 0
    print("PROMPT.md and docs/index.html have diverged.", file=sys.stderr)
    print("Update docs/index.html `const PROMPT = `...`` to match PROMPT.md.", file=sys.stderr)
    print("", file=sys.stderr)
    import difflib
    diff = difflib.unified_diff(
        md.splitlines(), js.splitlines(),
        fromfile="PROMPT.md", tofile="docs/index.html",
        lineterm="",
    )
    print("\n".join(diff), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
