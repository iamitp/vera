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
