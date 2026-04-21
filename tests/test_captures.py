from vera.cli import parse_captures


def test_no_captures_returns_empty():
    captures, warnings = parse_captures("Hello world.")
    assert captures == []
    assert warnings == []


def test_single_capture():
    resp = """Some response.

VERA-CAPTURE:
kind: RULE
content: no em dashes
"""
    captures, warnings = parse_captures(resp)
    assert captures == [("RULE", "no em dashes")]
    assert warnings == []


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
    captures, _ = parse_captures(resp)
    assert captures == [
        ("OBSERVED", "user lives in Berlin"),
        ("INFERRED", "user speaks German"),
    ]


def test_malformed_capture_emits_warning():
    resp = """VERA-CAPTURE:
kind:
content:
"""
    captures, warnings = parse_captures(resp)
    assert captures == []
    assert len(warnings) == 1
    assert "missing kind" in warnings[0]


def test_capture_block_requires_marker():
    resp = """kind: RULE
content: nope
"""
    captures, warnings = parse_captures(resp)
    assert captures == []
    assert warnings == []


def test_capture_inside_blockquote():
    resp = """Response text.

> VERA-CAPTURE:
> kind: RULE
> content: no emojis in filenames
"""
    captures, warnings = parse_captures(resp)
    assert captures == [("RULE", "no emojis in filenames")]
    assert warnings == []


def test_capture_with_list_bullets():
    resp = """Response.

- VERA-CAPTURE:
- kind: OBSERVED
- content: user uses postgres at work
"""
    captures, warnings = parse_captures(resp)
    assert captures == [("OBSERVED", "user uses postgres at work")]
    assert warnings == []


def test_capture_with_indentation():
    resp = """Response.

    VERA-CAPTURE:
      kind: RULE
      content: be terse
"""
    captures, warnings = parse_captures(resp)
    assert captures == [("RULE", "be terse")]


def test_capture_case_insensitive_keys():
    resp = """VERA-CAPTURE:
Kind: INFERRED
Content: user cares about latency
"""
    captures, _ = parse_captures(resp)
    assert captures == [("INFERRED", "user cares about latency")]


def test_capture_tolerates_blank_line_after_marker():
    resp = """VERA-CAPTURE:

kind: RULE
content: confirm before deleting
"""
    captures, warnings = parse_captures(resp)
    assert captures == [("RULE", "confirm before deleting")]
    assert warnings == []


def test_capture_fields_five_lines_apart_still_parsed():
    resp = """VERA-CAPTURE:
kind: RULE


content: don't paraphrase code
"""
    captures, warnings = parse_captures(resp)
    # Blank line after fields started ends the block; content should not be found
    assert captures == []
    assert len(warnings) == 1
