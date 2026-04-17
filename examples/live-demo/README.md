# Live demo — 2026-04-17

Unlike `examples/` (which is hand-authored for didactic clarity), this folder
captures an actual end-to-end run:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
vera init --quick
vera chat < script.txt      # six-turn Rust-rewrite conversation
vera audit --share
```

- `transcript.md` — what Vera wrote during the chat.
- `audit.md` — what `vera audit` produced when a second Claude call reviewed it.
- `audit.share.md` — what `vera audit --share` emitted for copy-paste.

**What the auditor caught:** a suspiciously high serialization latency figure
(400ms for 50 KB JSON in Python) that neither Vera nor the user questioned.
A sycophantic AI would have built recommendations on top of that number. The
audit flagged it as implausible and worked out the implied throughput
(~0.1 MB/s, roughly 1000× slower than reasonable) — a real methodological
issue, not a writing-style critique.
