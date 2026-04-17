from vera.rules import DEFAULT_RULES, ensure_rules, check_response


def test_ensure_rules_creates_file_with_default(tmp_path):
    rules_file = tmp_path / "rules.md"
    text = ensure_rules(rules_file)
    assert rules_file.exists()
    assert text == DEFAULT_RULES
    assert "# Vera Rules" in text


def test_ensure_rules_reads_existing(tmp_path):
    rules_file = tmp_path / "rules.md"
    rules_file.write_text("# Custom\n- \"banana\"\n")
    text = ensure_rules(rules_file)
    assert "banana" in text
    assert "# Vera Rules" not in text


def test_check_response_clean_is_none():
    assert check_response("Here is the answer.", DEFAULT_RULES) is None


def test_check_response_catches_banned_phrase():
    resp = "Great question! Here's what I think."
    violation = check_response(resp, DEFAULT_RULES)
    assert violation is not None
    assert "great question" in violation
    assert "Regenerate" in violation


def test_check_response_catches_multiple_violations():
    resp = "Great question — you're right, absolutely."
    violation = check_response(resp, DEFAULT_RULES)
    assert violation is not None
    assert "great question" in violation
    assert "you're right" in violation
    assert "absolutely" in violation


def test_check_response_catches_em_dash():
    resp = "Here is one thing — and another."
    violation = check_response(resp, DEFAULT_RULES)
    assert violation is not None
    assert "em dash" in violation


def test_check_response_case_insensitive():
    resp = "GREAT QUESTION that was."
    assert check_response(resp, DEFAULT_RULES) is not None


def test_check_response_ignores_em_dash_when_rule_absent():
    custom = "# Rules\n- \"bad\"\n"
    resp = "A — B"
    assert check_response(resp, custom) is None
