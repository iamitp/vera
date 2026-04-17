from vera.cli import parse_captures


def test_no_captures_returns_empty():
    assert parse_captures("Hello world.") == []


def test_single_capture():
    resp = """Some response.

VERA-CAPTURE:
kind: RULE
content: no em dashes
"""
    out = parse_captures(resp)
    assert out == [("RULE", "no em dashes")]


def test_multiple_captures():
    resp = """Response.

VERA-CAPTURE:
kind: OBSERVED
content: user lives in Berlin

And more.

VERA-CAPTURE:
kind: INFERRED
content: user speaks German
"""
    out = parse_captures(resp)
    assert out == [
        ("OBSERVED", "user lives in Berlin"),
        ("INFERRED", "user speaks German"),
    ]


def test_malformed_capture_ignored():
    resp = """VERA-CAPTURE:
kind:
content:
"""
    assert parse_captures(resp) == []


def test_capture_block_requires_marker():
    resp = """kind: RULE
content: nope
"""
    assert parse_captures(resp) == []
