from vera.audit import build_share_snippet, SHARE_FOOTER


SAMPLE = """# Vera Audit 2026-04-15 14:30

## Sycophancy
Turn 3 — primary agreed without evidence.

## Bottom line
Push back on turn 3.
"""


def test_build_share_snippet_strips_header(tmp_path):
    audit = tmp_path / "2026-04-15_1430.md"
    audit.write_text(SAMPLE)
    share_path, snippet = build_share_snippet(audit)

    assert "# Vera Audit 2026-04-15 14:30" not in snippet
    assert "# What Vera caught in my own chat history" in snippet
    assert "## Sycophancy" in snippet
    assert "## Bottom line" in snippet


def test_build_share_snippet_writes_sibling_file(tmp_path):
    audit = tmp_path / "2026-04-15_1430.md"
    audit.write_text(SAMPLE)
    share_path, snippet = build_share_snippet(audit)

    assert share_path.exists()
    assert share_path.name == "2026-04-15_1430.share.md"
    assert share_path.read_text() == snippet


def test_build_share_snippet_includes_attribution(tmp_path):
    audit = tmp_path / "a.md"
    audit.write_text(SAMPLE)
    _, snippet = build_share_snippet(audit)
    assert "github.com/iamitp/vera" in snippet
    assert SHARE_FOOTER.strip() in snippet


def test_build_share_snippet_handles_missing_header(tmp_path):
    audit = tmp_path / "a.md"
    audit.write_text("## Sycophancy\nTurn 1 flagged.\n")
    _, snippet = build_share_snippet(audit)
    assert "## Sycophancy" in snippet
    assert "Turn 1 flagged." in snippet


def test_build_share_snippet_scrubs_home_paths(tmp_path):
    audit = tmp_path / "a.md"
    audit.write_text(
        "# Vera Audit 2026-04-15 14:30\n\n"
        "## Provenance gaps\n"
        "Primary referenced /Users/alice/projects/payments/README.md verbatim.\n"
    )
    _, snippet = build_share_snippet(audit)
    assert "/Users/alice" not in snippet
    assert "~/…" in snippet


def test_build_share_snippet_scrubs_inline_timestamps(tmp_path):
    audit = tmp_path / "a.md"
    audit.write_text(
        "# Vera Audit 2026-04-15 14:30\n\n"
        "## Sycophancy\nSeen at 2026-04-15 14:28 in transcript.\n"
    )
    _, snippet = build_share_snippet(audit)
    assert "2026-04-15 14:28" not in snippet
    assert "[timestamp]" in snippet


def test_audit_cli_share_flag_writes_sibling(tmp_path, monkeypatch):
    from click.testing import CliRunner
    from vera import cli as cli_mod

    audit_dir = tmp_path / "audits"
    audit_dir.mkdir()
    report = audit_dir / "2026-04-15_1430.md"
    report.write_text(
        "# Vera Audit 2026-04-15 14:30\n\n## Sycophancy\nClean.\n"
    )

    monkeypatch.setattr(cli_mod, "run_audit", lambda provider, mem, **kw: report)
    monkeypatch.setattr(cli_mod, "detect_provider", lambda: object())
    monkeypatch.setattr(cli_mod, "MEMORY_DIR", tmp_path / "memory")

    runner = CliRunner()
    result = runner.invoke(cli_mod.main, ["audit", "--share"])
    assert result.exit_code == 0, result.output
    share_path = report.with_suffix(".share.md")
    assert share_path.exists()
    assert "# What Vera caught in my own chat history" in share_path.read_text()


def test_audit_cli_passes_flags_to_run_audit(tmp_path, monkeypatch):
    from click.testing import CliRunner
    from vera import cli as cli_mod

    captured = {}

    def fake_run_audit(provider, mem, **kw):
        captured.update(kw)
        out = tmp_path / "r.md"
        out.write_text("# Vera Audit now\n\nclean\n")
        return out

    monkeypatch.setattr(cli_mod, "run_audit", fake_run_audit)
    monkeypatch.setattr(cli_mod, "detect_provider", lambda: object())
    monkeypatch.setattr(cli_mod, "MEMORY_DIR", tmp_path / "memory")

    runner = CliRunner()
    result = runner.invoke(
        cli_mod.main,
        ["audit", "--last", "2", "--since", "2026-04-01", "--model", "claude-haiku-4-5-20251001"],
    )
    assert result.exit_code == 0, result.output
    assert captured["n"] == 2
    assert str(captured["since"]) == "2026-04-01"
    assert captured["model_override"] == "claude-haiku-4-5-20251001"


def test_audit_cli_rejects_bad_since(tmp_path, monkeypatch):
    from click.testing import CliRunner
    from vera import cli as cli_mod

    monkeypatch.setattr(cli_mod, "detect_provider", lambda: object())
    runner = CliRunner()
    result = runner.invoke(cli_mod.main, ["audit", "--since", "yesterday"])
    assert result.exit_code != 0
    assert "YYYY-MM-DD" in result.output


def test_select_transcripts_respects_last_and_since(tmp_path):
    import os
    from datetime import datetime, timedelta
    from vera.audit import _select_transcripts

    for name, days in [("a.md", 100), ("b.md", 60), ("c.md", 30), ("d.md", 5), ("e.md", 1)]:
        p = tmp_path / name
        p.write_text("x")
        ts = (datetime.now() - timedelta(days=days)).timestamp()
        os.utime(p, (ts, ts))

    picked = _select_transcripts(tmp_path, n=2, since=None)
    assert [p.name for p in picked] == ["d.md", "e.md"]

    cutoff = (datetime.now() - timedelta(days=45)).date()
    picked = _select_transcripts(tmp_path, n=10, since=cutoff)
    assert [p.name for p in picked] == ["c.md", "d.md", "e.md"]


def test_detect_provider_reads_vera_audit_model(monkeypatch):
    import importlib
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    monkeypatch.setenv("VERA_AUDIT_MODEL", "claude-haiku-4-5-20251001")
    import vera.config
    importlib.reload(vera.config)
    provider = vera.config.detect_provider()
    assert provider.audit_model == "claude-haiku-4-5-20251001"
