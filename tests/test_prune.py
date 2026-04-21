import os
from datetime import datetime, timedelta
from pathlib import Path

from click.testing import CliRunner


def _make_transcript(dir_: Path, name: str, days_old: int) -> Path:
    dir_.mkdir(parents=True, exist_ok=True)
    p = dir_ / name
    p.write_text(f"## you\nhello\n\n## vera\nhi\n")
    ts = (datetime.now() - timedelta(days=days_old)).timestamp()
    os.utime(p, (ts, ts))
    return p


def _reload_cli_with_home(monkeypatch, home: Path):
    monkeypatch.setenv("VERA_HOME", str(home))
    import importlib
    import vera.config
    import vera.provenance
    import vera.audit
    import vera.cli
    # config reads env at import; reload the module graph that depends on it.
    importlib.reload(vera.config)
    importlib.reload(vera.provenance)
    importlib.reload(vera.audit)
    importlib.reload(vera.cli)
    return vera.cli


def test_prune_skips_when_under_keep_threshold(tmp_path, monkeypatch):
    cli = _reload_cli_with_home(monkeypatch, tmp_path)
    mem = cli.MEMORY_DIR
    for i in range(3):
        _make_transcript(mem, f"2026-01-0{i+1}.md", days_old=200)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["prune", "--older-than", "30", "--keep", "50"])
    assert result.exit_code == 0, result.output
    assert "nothing to archive" in result.output
    assert len(list(mem.glob("*.md"))) == 3


def test_prune_dry_run_does_not_move(tmp_path, monkeypatch):
    cli = _reload_cli_with_home(monkeypatch, tmp_path)
    mem = cli.MEMORY_DIR
    for i in range(10):
        _make_transcript(mem, f"old-{i:02d}.md", days_old=200)
    for i in range(5):
        _make_transcript(mem, f"new-{i:02d}.md", days_old=1)

    runner = CliRunner()
    result = runner.invoke(
        cli.main, ["prune", "--older-than", "30", "--keep", "3", "--dry-run"]
    )
    assert result.exit_code == 0, result.output
    assert "would archive" in result.output
    # Nothing moved on dry-run
    assert not (mem / cli.ARCHIVE_DIRNAME).exists()


def test_prune_moves_old_transcripts(tmp_path, monkeypatch):
    cli = _reload_cli_with_home(monkeypatch, tmp_path)
    mem = cli.MEMORY_DIR
    for i in range(8):
        _make_transcript(mem, f"old-{i:02d}.md", days_old=200)
    for i in range(3):
        _make_transcript(mem, f"new-{i:02d}.md", days_old=1)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["prune", "--older-than", "30", "--keep", "3"])
    assert result.exit_code == 0, result.output
    assert "Archived" in result.output
    archive = mem / cli.ARCHIVE_DIRNAME
    assert archive.exists()
    archived = list(archive.glob("*.md"))
    # 8 old minus 0 kept from the new-only tail: all 8 olds move, 3 news stay
    assert len(archived) == 8
    # Newest 3 are preserved
    remaining = {p.name for p in mem.glob("*.md")}
    assert remaining == {f"new-{i:02d}.md" for i in range(3)}


def test_prune_respects_keep_on_old_files(tmp_path, monkeypatch):
    cli = _reload_cli_with_home(monkeypatch, tmp_path)
    mem = cli.MEMORY_DIR
    # 10 old files, no new ones. keep=5 → only 5 oldest get moved.
    for i in range(10):
        _make_transcript(mem, f"old-{i:02d}.md", days_old=200)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["prune", "--older-than", "30", "--keep", "5"])
    assert result.exit_code == 0, result.output
    archive = mem / cli.ARCHIVE_DIRNAME
    assert len(list(archive.glob("*.md"))) == 5
    assert len(list(mem.glob("*.md"))) == 5


def test_status_shows_archive_count(tmp_path, monkeypatch):
    cli = _reload_cli_with_home(monkeypatch, tmp_path)
    mem = cli.MEMORY_DIR
    archive = mem / cli.ARCHIVE_DIRNAME
    _make_transcript(mem, "recent.md", days_old=1)
    _make_transcript(archive, "archived.md", days_old=200)

    runner = CliRunner()
    result = runner.invoke(cli.main, ["status"])
    assert result.exit_code == 0, result.output
    assert "Memory: 1 transcripts" in result.output
    assert "Archive: 1 transcripts" in result.output


def test_memory_summary_prefers_durable_facts(tmp_path, monkeypatch):
    cli = _reload_cli_with_home(monkeypatch, tmp_path)
    from vera.provenance import log_write
    log = cli.PROVENANCE_LOG
    log_write("RULE", "no em dashes ever", source="chat", log_path=log)
    log_write("OBSERVED", "user works in payments", source="chat", log_path=log)
    _make_transcript(cli.MEMORY_DIR, "2026-04-20.md", days_old=1)

    summary = cli.load_memory_summary()
    assert "Durable facts" in summary
    assert "[RULE] no em dashes ever" in summary
    assert "[OBSERVED] user works in payments" in summary
    assert "2026-04-20" in summary
