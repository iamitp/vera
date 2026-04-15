# Vera

**The AI memory that argues with itself.**

Every other AI memory layer makes your model remember more. Vera makes your model distrust itself.

- **Local-first.** Your memory is markdown on your disk. You own it.
- **Model-agnostic.** Bring your own API key — Claude, GPT, whatever.
- **Audit loop.** A second model reads the first model's transcripts and calls out sycophancy.
- **Rule enforcement, not rule recall.** Your rules block the model, they don't just remind it.
- **Provenance on every memory write.** `[OBSERVED]`, `[INFERRED]`, `[ASSUMED]`, `[CANDIDATE]` — never mixed.

## Install

```bash
pipx install git+https://github.com/iamitp/vera
export ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY
vera init
vera chat
```

_(PyPI release coming — `pipx install vera-ai` once that lands.)_

That's it.

## The four-command shape

```bash
vera init      # create ~/vera/ with starter rules
vera chat      # interactive chat; rules enforced, captures written to memory
vera audit     # second model audits recent transcripts, writes findings
vera rules     # print your active rules
vera status    # show paths + counts
```

## What the audit catches

Run `vera chat` for a week. Then `vera audit`. You will get a markdown report like:

```
## Sycophancy
Turn 3 — you asked "is this a good idea?" Vera said "yes, makes sense".
Vera cited no evidence. The user had not stated any supporting facts.
This is the agreement-for-agreement's-sake failure mode.

## Unsupported claims
Turn 7 — Vera asserted "most users prefer X" with no source. No
[EXTERNAL] tag. This is a provenance violation.

## Bottom line
Vera agreed too fast on turns 3 and 9. Push back on those.
```

You will not unsee this.

## Why this exists

Commercial AI is optimised for engagement. Engagement rewards agreement. Agreement erodes your ability to trust the output.

Vera is the opposite bet. It builds friction into the loop — a second model that has no stake in keeping you happy, and a rule layer that refuses to violate what you've said you want.

## Architecture

```
~/vera/
├── rules.md          # your rules (edit freely)
├── memory/           # transcripts + provenance log
│   ├── 2026-04-15_143022.md
│   └── _log.jsonl
└── audit/            # adversarial audit reports
    └── 2026-04-15.md
```

No databases. No servers. No vendor. Markdown and a JSON log. Version-control it, sync it, audit it yourself.

## Status

v0.1.0 — MVP. Ships the four primitives: provenance, rule enforcement, audit, portable memory. Expect rough edges. File issues freely.

MIT licensed.
