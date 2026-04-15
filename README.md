# Vera

**AI that admits when it's guessing.**

If you cite facts that matter — in decks, memos, papers, briefs, emails to your boss — you have probably been burned by an AI stating something confidently that turned out to be wrong. Vera makes your AI flag when it is guessing, cite when it is sure, and call out its own BS when you ask.

Paste Vera into Claude, ChatGPT, Gemini, or any AI chat. Zero install to try. To keep it on permanently, put the prompt into Custom Instructions for a Claude Project, a ChatGPT GPT, or a Gemini Gem, and every new chat in that container inherits it.

[**Try it in 30 seconds →**](PROMPT.md)

---

## What changes

Ask a regular AI a hard factual question and you get one paragraph of smooth prose. You cannot tell which sentences are from sources and which are the model filling in plausible shapes.

Ask Vera the same question and you get the same answer with every claim tagged. `[EXTERNAL: FOMC minutes October 2024]` on what it actually cites. `[INFERRED low]` on what it is extrapolating. `[ASSUMED]` on what it made up because it wasn't told. You can see which lines to trust on sight.

Type `/audit` after a few turns and the model reviews its own answers for sycophancy, hedging, and unsupported claims.

## Honest about the limits

Vera makes your AI more honest. It cannot make it perfect.

- The model can still fabricate the *thing inside* an `[EXTERNAL: ...]` tag (a plausible-sounding source that does not exist). For high-stakes claims, open the source yourself.
- Rule enforcement in the paste-in version is self-policed, not blocking. The model can drift, especially on long chats. The CLI version has hard regenerate-on-violation.
- Vera reduces the number of claims you have to check. It does not eliminate the need.

Nothing leaves your existing AI chat. The prompt is added instructions for the model you are already talking to. Your data does not go to a third-party service.

## Under the hood

- Every factual claim tagged: `[OBSERVED]`, `[INFERRED low|med|high]`, `[ASSUMED]`, `[EXTERNAL source]`.
- Sycophantic openers ("great question", "absolutely", "I'd be happy to") banned and regenerated.
- `/audit` produces a short structured self-critique.
- CLI version (below) adds a second model as the auditor, hard rule-blocking, and markdown memory on disk.

## Taste it in 30 seconds (no install, no API key)

If you already pay for Claude, ChatGPT, Gemini, or any other AI chat, you can feel what Vera does by pasting one block into a new chat. The model adopts the Vera persona for the rest of that conversation: provenance tags on every factual claim, banned phrases self-policed, a `/audit` command you can use at any time.

See [PROMPT.md](PROMPT.md) for the paste-in version. Use it as a chat message, or put it in Custom Instructions for a Claude Project / ChatGPT GPT / Gemini Gem and every chat in that container inherits it.

This version is lossy compared to the CLI. Self-audit is the same model critiquing itself, and enforcement is self-policed rather than blocking. It is the tasting session that tells you whether the idea is worth installing the real thing.

## Install the CLI (30 more seconds)

One line:

```bash
curl -sSf https://raw.githubusercontent.com/iamitp/vera/main/install.sh | bash
```

That bootstraps pipx if needed, installs Vera, and prints the two remaining steps: add an API key, then run `vera init` (a 3-question wizard that writes rules customised to you).

Already have pipx and a key? Three commands:

```bash
pipx install git+https://github.com/iamitp/vera
export ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY
vera init && vera chat
```

_(PyPI release coming: `pipx install vera-ai` once that lands.)_

## The CLI adds what the prompt cannot

- A **second model** with different loyalty runs the audit. Not the same model critiquing itself.
- Rule violations **fail the turn** and force a regenerate. Not self-policed.
- Memory is **markdown on your disk**, greppable, diff-able, sync-able, durable across chat deletion.
- Provenance is a **structured log** (`_log.jsonl`), not just tags inside prose.

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
