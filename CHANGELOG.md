# Changelog

All notable changes to Vera are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `vera audit --share` flag: writes an anonymized, copy-pasteable `.share.md`
  snippet alongside the audit report, with a Vera attribution footer.
- `examples/` directory with a realistic transcript, audit report, and share
  snippet so the loop can be evaluated without running the CLI.
- Test suite under `tests/` (21 tests covering provenance, rules, audit
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
