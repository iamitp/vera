"""Vera CLI: init / chat / audit / rules / prune / status."""
from __future__ import annotations
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
import click
from rich.console import Console
from rich.markdown import Markdown
from .config import VERA_HOME, MEMORY_DIR, AUDIT_DIR, RULES_FILE, PROVENANCE_LOG, detect_provider
from .provenance import SYSTEM_ADDENDUM, log_write, log_usage, spend_since
from .rules import ensure_rules, check_response, DEFAULT_RULES
from .llm import chat as _llm_chat
from .audit import run_audit, build_share_snippet

ARCHIVE_DIRNAME = "_archive"

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

_CAPTURE_LEADER = re.compile(r"^[\s>\-*]*")


def _strip_leader(line: str) -> str:
    """Drop leading whitespace, blockquote '>', and list bullets."""
    return _CAPTURE_LEADER.sub("", line).strip()


def parse_captures(response: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Extract VERA-CAPTURE blocks from the model response.

    Returns (captures, warnings). A malformed block (marker present but
    kind or content missing within the next 6 lines) adds a warning
    instead of silently dropping. Accepts blockquote and list prefixes
    and arbitrary indentation around the marker and its fields.
    """
    out: list[tuple[str, str]] = []
    warnings: list[str] = []
    lines = response.splitlines()
    i = 0
    while i < len(lines):
        stripped = _strip_leader(lines[i])
        if stripped == "VERA-CAPTURE:":
            kind = content = ""
            scanned = 0
            for j in range(i + 1, min(i + 7, len(lines))):
                s = _strip_leader(lines[j])
                if not s:
                    # Blank line between marker and first field is tolerated;
                    # blank line after we've started reading fields ends the block.
                    if kind or content:
                        break
                    continue
                if s.lower().startswith("kind:"):
                    kind = s.split(":", 1)[1].strip()
                elif s.lower().startswith("content:"):
                    content = s.split(":", 1)[1].strip()
                else:
                    # Non-field line ends the block.
                    break
                scanned = j - i
            if kind and content:
                out.append((kind, content))
            else:
                warnings.append(
                    f"VERA-CAPTURE at line {i+1} missing "
                    f"{'kind' if not kind else 'content'}"
                )
            i += max(scanned, 1)
        else:
            i += 1
    return out, warnings

def _truncate_line(text: str, limit: int = 160) -> str:
    line = text.strip().splitlines()[0] if text.strip() else ""
    return line if len(line) <= limit else line[:limit].rstrip() + "…"


def _recent_durable_facts(log_path: Path, days: int = 30, limit: int = 20) -> list[str]:
    """Return deduped RULE / OBSERVED entries from the last N days."""
    if not log_path.exists():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    seen: set[str] = set()
    out: list[tuple[datetime, str, str]] = []
    for raw in log_path.read_text().splitlines():
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if entry.get("kind") not in ("RULE", "OBSERVED"):
            continue
        try:
            ts = datetime.fromisoformat(entry["ts"])
        except (KeyError, ValueError):
            continue
        if ts < cutoff:
            continue
        content = _truncate_line(str(entry.get("content", "")))
        if not content or content in seen:
            continue
        seen.add(content)
        out.append((ts, entry["kind"], content))
    out.sort(key=lambda x: x[0], reverse=True)
    return [f"[{k}] {c}" for _, k, c in out[:limit]]


def load_memory_summary() -> str:
    """Compose the memory-summary block the chat system prompt sees.

    Two layers: durable facts (RULE / OBSERVED captures in the last 30 days,
    deduped) plus headlines from the last 5 transcripts. No mid-word
    truncation — one line per entry, 160-char cap.
    """
    parts: list[str] = []
    facts = _recent_durable_facts(PROVENANCE_LOG)
    if facts:
        parts.append("Durable facts (recent captures):")
        parts.extend(f"- {f}" for f in facts)

    if MEMORY_DIR.exists():
        recent = sorted(MEMORY_DIR.glob("*.md"))[-5:]
        if recent:
            parts.append("")
            parts.append("Recent transcripts:")
            for f in recent:
                first = _truncate_line(f.read_text())
                parts.append(f"- {f.stem}: {first}" if first else f"- {f.stem}: (empty)")
    return "\n".join(parts)

@click.group()
def main():
    """Vera — AI memory that argues with itself."""
    pass

@main.command()
@click.option("--quick", is_flag=True, help="Skip the wizard, write default rules only.")
def init(quick):
    """Interactive setup: three questions, then you have personalised rules."""
    VERA_HOME.mkdir(parents=True, exist_ok=True)
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    if quick or not sys.stdin.isatty():
        ensure_rules(RULES_FILE)
        console.print(f"[green]Vera initialised at {VERA_HOME}[/green]")
        console.print(f"Edit your rules: {RULES_FILE}")
        console.print(f"Run: [bold]vera chat[/bold] to start.")
        return

    if RULES_FILE.exists():
        if not click.confirm(f"{RULES_FILE} exists. Re-run the wizard (overwrites)?", default=False):
            console.print(f"[dim]Kept existing rules. Run: [bold]vera chat[/bold][/dim]")
            return

    console.print("[bold]Vera setup[/bold] — three quick questions so your rules actually fit you.\n")
    use = click.prompt("1. What do you use AI for most (one line)", type=str).strip()
    stop = click.prompt("2. One thing you want AI to stop doing", type=str).strip()
    banned_raw = click.prompt(
        "3. Phrases you never want to see (comma-separated, or blank)",
        default="", show_default=False,
    ).strip()
    banned = [p.strip() for p in banned_raw.split(",") if p.strip()]

    personalised = DEFAULT_RULES.rstrip() + "\n"
    personalised += "\n## Your profile (the system reads this on every turn)\n"
    personalised += f"- Primary use: {use}\n"
    personalised += f"- Asked to stop: {stop}\n"
    if banned:
        personalised += "\n## Your custom banned phrases\n"
        for phrase in banned:
            personalised += f'- "{phrase}"\n'
    RULES_FILE.write_text(personalised)

    console.print(f"\n[green]Vera initialised at {VERA_HOME}[/green]")
    console.print(f"[dim]  Rules: {RULES_FILE} (edit freely — your rules, your binding)[/dim]\n")
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

        response, usage = _llm_chat(provider, system, messages)
        log_usage(usage, source="chat", log_path=PROVENANCE_LOG)
        violation = check_response(response, rules_text)
        if violation:
            console.print(f"[dim]⟲ regenerating: {violation}[/dim]")
            messages_retry = messages + [
                {"role": "assistant", "content": response},
                {"role": "user", "content": violation},
            ]
            response, usage = _llm_chat(provider, system, messages_retry)
            log_usage(usage, source="chat-retry", log_path=PROVENANCE_LOG)
            second_violation = check_response(response, rules_text)
            if second_violation:
                response = (
                    f"{response}\n\n"
                    f"> ⚠ rule layer disagreed twice: {second_violation}"
                )

        messages.append({"role": "assistant", "content": response})
        console.print()
        console.print(Markdown(response))
        console.print()

        # Capture user-stated facts / rules
        captures, capture_warnings = parse_captures(response)
        for kind, content in captures:
            log_write(kind, content, source="chat", log_path=PROVENANCE_LOG)
            if kind == "RULE":
                with RULES_FILE.open("a") as f:
                    f.write(f"\n- \"{content}\" (captured {datetime.now():%Y-%m-%d})\n")
                rules_text = RULES_FILE.read_text()
        for warn in capture_warnings:
            console.print(f"[dim]warning: malformed capture skipped — {warn}[/dim]")
            log_write("MALFORMED", warn, source="chat", log_path=PROVENANCE_LOG)

        with transcript_path.open("a") as f:
            f.write(f"## you\n{user_input}\n\n## vera\n{response}\n\n")

@main.command()
@click.option(
    "--share",
    "share_flag",
    is_flag=True,
    help="Also emit an anonymized, copy-pasteable snippet suitable for social media.",
)
@click.option("--last", "last_n", type=int, default=5,
              help="Audit the last N transcripts by mtime (default 5).")
@click.option("--since", "since_str", type=str, default=None,
              help="Only audit transcripts touched on/after YYYY-MM-DD.")
@click.option("--model", "model_override", type=str, default=None,
              help="Override the audit model. Also reads VERA_AUDIT_MODEL.")
def audit(share_flag: bool, last_n: int, since_str: str | None, model_override: str | None):
    """Run the adversarial auditor on recent transcripts."""
    provider = detect_provider()
    since = None
    if since_str:
        try:
            since = datetime.strptime(since_str, "%Y-%m-%d").date()
        except ValueError:
            raise click.BadParameter("--since must be YYYY-MM-DD")
    out = run_audit(
        provider, MEMORY_DIR,
        n=last_n, since=since, model_override=model_override,
    )
    console.print(f"[green]Audit written:[/green] {out}")
    console.print()
    console.print(Markdown(out.read_text()))
    if share_flag:
        share_path, snippet = build_share_snippet(out)
        console.print()
        console.print(f"[green]Shareable snippet written:[/green] {share_path}")
        console.print("[dim]Copy below and post wherever. No paths, no timestamps.[/dim]\n")
        console.print(Markdown(snippet))

@main.command()
def rules():
    """Print the active rules file."""
    console.print(Markdown(ensure_rules(RULES_FILE)))

@main.command()
@click.option("--older-than", "older_than_days", type=int, default=90,
              help="Archive transcripts older than N days (default 90).")
@click.option("--keep", type=int, default=50,
              help="Always keep at least N most-recent transcripts (default 50).")
@click.option("--dry-run", is_flag=True, help="Show what would be moved, don't move.")
def prune(older_than_days: int, keep: int, dry_run: bool):
    """Archive old transcripts into MEMORY_DIR/_archive/ to cap disk growth."""
    if not MEMORY_DIR.exists():
        console.print(f"[dim]No memory dir at {MEMORY_DIR}; nothing to prune.[/dim]")
        return
    archive_dir = MEMORY_DIR / ARCHIVE_DIRNAME
    transcripts = sorted(MEMORY_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime)
    if len(transcripts) <= keep:
        console.print(
            f"[dim]{len(transcripts)} transcripts ≤ keep={keep}; nothing to archive.[/dim]"
        )
        return
    cutoff = datetime.now() - timedelta(days=older_than_days)
    # Newest `keep` (by mtime) are never moved; consider only the older tail.
    tail = transcripts[:-keep] if keep > 0 else transcripts
    to_archive = [t for t in tail if datetime.fromtimestamp(t.stat().st_mtime) < cutoff]
    if not to_archive:
        console.print(
            f"[dim]No transcripts older than {older_than_days} days beyond the last {keep}.[/dim]"
        )
        return
    if dry_run:
        console.print(
            f"[yellow]Dry run — would archive {len(to_archive)} transcripts "
            f"to {archive_dir}:[/yellow]"
        )
        for t in to_archive:
            console.print(f"  {t.name}")
        return
    archive_dir.mkdir(parents=True, exist_ok=True)
    for t in to_archive:
        t.rename(archive_dir / t.name)
    console.print(
        f"[green]Archived {len(to_archive)} transcripts to {archive_dir}[/green]"
    )


@main.command()
def status():
    """Show Vera state."""
    console.print(f"Home: {VERA_HOME}")
    console.print(f"Rules: {RULES_FILE} ({'exists' if RULES_FILE.exists() else 'missing'})")
    console.print(f"Memory: {len(list(MEMORY_DIR.glob('*.md'))) if MEMORY_DIR.exists() else 0} transcripts")
    archive_dir = MEMORY_DIR / ARCHIVE_DIRNAME
    if archive_dir.exists():
        console.print(f"Archive: {len(list(archive_dir.glob('*.md')))} transcripts")
    console.print(f"Audits: {len(list(AUDIT_DIR.glob('*.md'))) if AUDIT_DIR.exists() else 0} reports")
    usd, calls = spend_since(PROVENANCE_LOG, days=30)
    if calls:
        console.print(f"Spend (30d): ${usd:.2f} over {calls} calls")

if __name__ == "__main__":
    main()
