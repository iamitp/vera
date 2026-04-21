# Changelog

All notable changes to Vera are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.0] — 2026-04-21

Theme: visibility and control. 0.1.0 worked; 0.2.0 makes it durable
for week-over-week use.

### Added
- **Cost tracking.** `vera.llm.chat()` returns `(text, usage)` with token
  counts plus an estimated USD cost from a public rate table. Every LLM
  call (chat / chat-retry / audit) appends a `USAGE` entry to the
  provenance log. `vera status` prints `Spend (30d): $X.XX over N calls`
  when any USAGE entries exist.
- **Visible regenerate.** Rule violations no longer trigger a silent
  retry. A dim `⟲ regenerating: <violation>` line prints before attempt
  2; if the rule layer disagrees twice, a `⚠ rule layer disagreed
  twice` footer is appended to the response.
- **`vera prune`.** New command archives transcripts older than N days
  (default 90) into `MEMORY_DIR/_archive/`, always retaining the most
  recent `--keep` (default 50). Supports `--dry-run`. `vera status`
  surfaces archive counts.
- **Smarter memory summary.** `load_memory_summary()` now layers durable
  facts (deduped `RULE` / `OBSERVED` captures from the last 30 days)
  on top of headlines from the last 5 transcripts. No mid-word
  truncation.
- **Audit controls.** `vera audit --last N`, `--since YYYY-MM-DD`,
  `--model MODEL`, plus `VERA_AUDIT_MODEL` env var read in
  `detect_provider()`.
- **Lenient VERA-CAPTURE parsing.** Accepts markdown blockquotes, list
  bullets, indentation, case-insensitive keys, and blank-line
  separators. Malformed blocks produce a console warning plus a
  `MALFORMED` provenance entry instead of silently dropping.

### Changed
- `chat()` signature: now returns `(text, usage)`. All internal callers
  updated.
- `ProvenanceKind` widened to include `MALFORMED`.
- `load_memory_summary()` rewritten (backwards-compatible at call-site;
  output format changed).
- `run_audit()` signature: adds `n`, `since`, `model_override` kwargs.

### Fixed
- Install instructions across `README.md`, `LAUNCH.md`, `install.sh`,
  and `launch/READY-TO-PASTE.md` now consistently point at
  `pipx install vera-clerk` (PyPI) rather than the stale
  `git+https://github.com/iamitp/vera` form.

## [0.1.1] — Unreleased pre-0.2.0 work

### Added
- `vera audit --share` flag: writes an anonymized, copy-pasteable `.share.md`
  snippet alongside the audit report, with a Vera attribution footer.
- `examples/` directory with a realistic transcript, audit report, and share
  snippet so the loop can be evaluated without running the CLI.
- Test suite under `tests/` (24 tests covering provenance, rules, audit
  share-snippet, and VERA-CAPTURE parsing).
- GitHub Actions CI running pytest on Python 3.10 / 3.11 / 3.12 plus a
  build+twine-check job.
- `launch/POSTS.md` and `launch/BACKUP-CHANNELS.md` launch artifacts.
- `launch/ship.sh` interactive launcher.

## [0.1.0] — 2026-04-15

### Added
- Initial MVP: four primitives — provenance, rule enforcement, adversarial
  audit, portable markdown memory.
- `vera init`, `vera chat`, `vera audit`, `vera rules`, `vera status`.
- Anthropic and OpenAI provider support via environment variable.
- Starter rules file with default banned-phrase list and em-dash guard.
