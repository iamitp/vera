"""Vera CLI: init / chat / audit / rules."""
from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path
import click
from rich.console import Console
from rich.markdown import Markdown
from .config import VERA_HOME, MEMORY_DIR, AUDIT_DIR, RULES_FILE, PROVENANCE_LOG, detect_provider
from .provenance import SYSTEM_ADDENDUM, log_write
from .rules import ensure_rules, check_response, DEFAULT_RULES
from .llm import chat
from .audit import run_audit

console = Console()

def build_system(rules_text: str, memory_summary: str) -> str:
    return f"""You are Vera — a rigorously honest assistant with persistent memory
that the user owns as markdown files.

{SYSTEM_ADDENDUM}

USER'S STANDING RULES (binding — violations will be caught by the rule layer):
{rules_text}

USER'S MEMORY (recent):
{memory_summary if memory_summary else '(empty)'}

Behavioural contract:
- Be compact. The shortest useful answer wins.
- Do not agree because agreeing is easy. If you disagree, say so plainly.
- If you are unsure, say "I'm not sure" — do not guess confidently.
- At the end of any turn where the user stated a new rule or durable fact,
  append a block in this exact format:

    VERA-CAPTURE:
    kind: RULE|OBSERVED|INFERRED
    content: <one line>

  The CLI parses these captures and writes them to memory.
"""

def parse_captures(response: str) -> list[tuple[str, str]]:
    """Extract VERA-CAPTURE blocks from the model response."""
    out = []
    lines = response.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip() == "VERA-CAPTURE:":
            kind = content = ""
            for j in range(i+1, min(i+4, len(lines))):
                s = lines[j].strip()
                if s.startswith("kind:"):
                    kind = s.split(":",1)[1].strip()
                elif s.startswith("content:"):
                    content = s.split(":",1)[1].strip()
            if kind and content:
                out.append((kind, content))
            i += 3
        else:
            i += 1
    return out

def load_memory_summary() -> str:
    if not MEMORY_DIR.exists():
        return ""
    items = []
    for f in sorted(MEMORY_DIR.glob("*.md"))[-10:]:
        items.append(f"- {f.stem}: {f.read_text()[:200]}")
    return "\n".join(items)

@click.group()
def main():
    """Vera — AI memory that argues with itself."""
    pass

@main.command()
def init():
    """Create ~/vera/ with a starter rules file and empty memory."""
    VERA_HOME.mkdir(parents=True, exist_ok=True)
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_rules(RULES_FILE)
    console.print(f"[green]Vera initialised at {VERA_HOME}[/green]")
    console.print(f"Edit your rules: {RULES_FILE}")
    console.print(f"Run: [bold]vera chat[/bold] to start.")

@main.command()
def chat():
    """Interactive chat with provenance + rule enforcement."""
    provider = detect_provider()
    VERA_HOME.mkdir(parents=True, exist_ok=True)
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    rules_text = ensure_rules(RULES_FILE)
    transcript_path = MEMORY_DIR / f"{datetime.now():%Y-%m-%d_%H%M%S}.md"
    messages: list[dict] = []
    console.print(f"[dim]Vera · {provider.name}:{provider.chat_model} · {VERA_HOME}[/dim]")
    console.print("[dim]Ctrl-D to quit.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]you › [/bold cyan]")
        except EOFError:
            console.print()
            break
        if not user_input.strip():
            continue
        messages.append({"role": "user", "content": user_input})
        memory_summary = load_memory_summary()
        system = build_system(rules_text, memory_summary)

        for attempt in range(2):
            response = chat(provider, system, messages)
            violation = check_response(response, rules_text)
            if not violation:
                break
            messages_retry = messages + [
                {"role": "assistant", "content": response},
                {"role": "user", "content": violation},
            ]
            response = chat(provider, system, messages_retry)

        messages.append({"role": "assistant", "content": response})
        console.print()
        console.print(Markdown(response))
        console.print()

        # Capture user-stated facts / rules
        for kind, content in parse_captures(response):
            log_write(kind, content, source="chat", log_path=PROVENANCE_LOG)
            if kind == "RULE":
                with RULES_FILE.open("a") as f:
                    f.write(f"\n- \"{content}\" (captured {datetime.now():%Y-%m-%d})\n")
                rules_text = RULES_FILE.read_text()

        with transcript_path.open("a") as f:
            f.write(f"## you\n{user_input}\n\n## vera\n{response}\n\n")

@main.command()
def audit():
    """Run the adversarial auditor on recent transcripts."""
    provider = detect_provider()
    out = run_audit(provider, MEMORY_DIR)
    console.print(f"[green]Audit written:[/green] {out}")
    console.print()
    console.print(Markdown(out.read_text()))

@main.command()
def rules():
    """Print the active rules file."""
    console.print(Markdown(ensure_rules(RULES_FILE)))

@main.command()
def status():
    """Show Vera state."""
    console.print(f"Home: {VERA_HOME}")
    console.print(f"Rules: {RULES_FILE} ({'exists' if RULES_FILE.exists() else 'missing'})")
    console.print(f"Memory: {len(list(MEMORY_DIR.glob('*.md'))) if MEMORY_DIR.exists() else 0} transcripts")
    console.print(f"Audits: {len(list(AUDIT_DIR.glob('*.md'))) if AUDIT_DIR.exists() else 0} reports")

if __name__ == "__main__":
    main()
