import json
from datetime import datetime, timedelta

from vera.llm import estimate_usd, USD_PER_MTOK
from vera.provenance import log_usage, spend_since


def test_estimate_usd_known_model():
    in_rate, out_rate = USD_PER_MTOK[("anthropic", "claude-sonnet-4-6")]
    usd = estimate_usd("anthropic", "claude-sonnet-4-6", 1_000_000, 500_000)
    assert usd == in_rate + 0.5 * out_rate


def test_estimate_usd_unknown_model_returns_none():
    assert estimate_usd("anthropic", "made-up-model", 100, 100) is None


def test_log_usage_writes_expected_shape(tmp_path):
    log = tmp_path / "log.jsonl"
    usage = {
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
        "input_tokens": 1200,
        "output_tokens": 340,
        "usd": 0.0087,
    }
    log_usage(usage, source="chat", log_path=log)
    entry = json.loads(log.read_text().strip())
    assert entry["kind"] == "USAGE"
    assert entry["source"] == "chat"
    assert entry["provider"] == "anthropic"
    assert entry["model"] == "claude-sonnet-4-6"
    assert entry["input_tokens"] == 1200
    assert entry["output_tokens"] == 340
    assert entry["usd"] == 0.0087
    assert "ts" in entry


def test_spend_since_sums_usage_within_window(tmp_path):
    log = tmp_path / "log.jsonl"
    # one call today
    log_usage(
        {"provider": "anthropic", "model": "claude-sonnet-4-6",
         "input_tokens": 1000, "output_tokens": 1000, "usd": 0.018},
        source="chat", log_path=log,
    )
    # one old entry written manually
    old = datetime.now() - timedelta(days=60)
    with log.open("a") as f:
        f.write(json.dumps({
            "ts": old.isoformat(), "kind": "USAGE", "source": "chat",
            "provider": "anthropic", "model": "claude-sonnet-4-6",
            "input_tokens": 5000, "output_tokens": 5000, "usd": 0.09,
        }) + "\n")
    usd, calls = spend_since(log, days=30)
    assert calls == 1
    assert abs(usd - 0.018) < 1e-9


def test_spend_since_ignores_non_usage_entries(tmp_path):
    log = tmp_path / "log.jsonl"
    from vera.provenance import log_write
    log_write("OBSERVED", "hi", source="chat", log_path=log)
    usd, calls = spend_since(log, days=30)
    assert usd == 0.0
    assert calls == 0


def test_spend_since_handles_missing_log(tmp_path):
    log = tmp_path / "missing.jsonl"
    usd, calls = spend_since(log, days=30)
    assert usd == 0.0
    assert calls == 0


def test_spend_since_counts_unknown_usd_calls_but_adds_zero(tmp_path):
    log = tmp_path / "log.jsonl"
    log_usage(
        {"provider": "anthropic", "model": "mystery",
         "input_tokens": 100, "output_tokens": 100, "usd": None},
        source="chat", log_path=log,
    )
    usd, calls = spend_since(log, days=30)
    assert calls == 1
    assert usd == 0.0
