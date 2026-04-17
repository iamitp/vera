import json
from vera.provenance import log_write, SYSTEM_ADDENDUM


def test_log_write_appends_jsonl(tmp_path):
    log = tmp_path / "log.jsonl"
    log_write("OBSERVED", "user likes espresso", source="chat", log_path=log)
    log_write("INFERRED", "user probably in Europe", source="chat", log_path=log)

    lines = log.read_text().splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["kind"] == "OBSERVED"
    assert first["source"] == "chat"
    assert first["content"] == "user likes espresso"
    assert "ts" in first


def test_log_write_truncates_large_content(tmp_path):
    log = tmp_path / "log.jsonl"
    big = "x" * 5000
    log_write("CANDIDATE", big, source="tool", log_path=log)
    entry = json.loads(log.read_text())
    assert len(entry["content"]) == 2000


def test_log_write_creates_parent_dir(tmp_path):
    log = tmp_path / "nested" / "deep" / "log.jsonl"
    log_write("RULE", "no em dashes", source="user", log_path=log)
    assert log.exists()


def test_system_addendum_lists_all_kinds():
    for kind in ("OBSERVED", "INFERRED", "ASSUMED", "CANDIDATE", "RULE", "EXTERNAL"):
        assert f"[{kind}]" in SYSTEM_ADDENDUM
