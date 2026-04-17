# Ready-to-paste copy

All fields below are pre-filled against the live state of the repo (Pages live, v0.1.0 released, live-demo in `examples/live-demo/`). Order of posting is the same as `launch/POSTS.md`: HN first, X thread ~2 minutes later, then Reddit after HN has a link to reference, then DMs.

---

## 1. Show HN

**Submit URL:** https://news.ycombinator.com/submit

**Title (66 chars):**

```
Show HN: Vera – paste-in prompt that makes any AI tag its guesses
```

**URL:**

```
https://github.com/iamitp/vera
```

**Text:** leave blank.

---

## 2. Show HN — author reply (post within 2 minutes)

Top-level comment on your own story:

```
Author here. Vera is a paste-in system prompt that makes any AI chat (Claude, ChatGPT, Gemini, Grok) tag every factual claim by confidence — [CITED: source], [INFERRED low|med|high], or [ASSUMED] — so you see which lines to trust on sight. No install. 30 seconds. The prompt block lives in PROMPT.md.

Three disciplines it enforces every turn:

1. HONESTY — every factual claim tagged. Model says "I'm not sure" instead of guessing confidently.
2. ATTENTION — reads instructions literally, corrections stick across the session, silent edit failures surface instead of coming back as unchanged output dressed up as new.
3. AUDIT — type /audit and the model self-critiques its recent answers for sycophancy and unsourced claims.

Concrete example of what the /audit pass catches, from a real run against the Anthropic API this morning (full artifacts in examples/live-demo/):

The conversation was about rewriting a payments service in Rust. The user mentioned 400 ms of the p99 latency was JSON serialisation of a 50 kB payload. Neither the primary nor the user questioned this. On the audit pass, a second Claude call noticed it implies ~0.1 MB/s serialisation throughput — ~1000x too slow for stdlib json on modern hardware — and flagged it as likely measurement error with three candidate root causes.

A sycophantic AI would have accepted the number and built recommendations on top. That's the point.

For power users, a CLI (pipx install git+https://github.com/iamitp/vera@v0.1.0) adds a second independent auditor model, hard rule-blocking with regenerate, and on-disk markdown memory you can grep and sync. But the paste-in prompt covers 80% of the value in 30 seconds.

Happy to answer questions about which failures each discipline catches, why I didn't just ship an extension, or how it compares to guard-rails / constitutional-AI patterns.
```

---

## 3. X — main post (pin it)

```
Vera — AI with clerk discipline.

Paste one prompt into any AI chat. Every factual claim gets tagged:
[CITED: source] · [INFERRED low|med|high] · [ASSUMED]

You see which lines to trust. No install. 30 seconds.

Works in Claude, ChatGPT, Gemini, Grok. MIT.

github.com/iamitp/vera
```

Attach: screenshot of the audit.share.md from `examples/live-demo/audit.share.md` (the 400 ms JSON-serialisation catch is the money shot).

---

## 4. X — thread replies (2–3 min apart)

**1/**
```
Three disciplines, every turn:

1. HONESTY — tag confidence on every claim. Say "I'm not sure" when unsure.
2. ATTENTION — read literally, stick corrections, surface silent failures.
3. AUDIT — type /audit and the model critiques its own recent answers.

Paste the prompt. That's the install.
```

**2/**
```
Real example from this morning: a user said "400 ms of p99 is JSON serialisation of a 50 kB payload". Nobody questioned it.

The /audit pass worked out the implied throughput — ~0.1 MB/s, ~1000x too slow for stdlib json — and flagged it as measurement error.

A sycophantic AI would have accepted the number.
```

**3/**
```
Why this matters:

OpenAI rolled back a ChatGPT update for being too sycophantic.
Anthropic's own lawyer apologised for a Claude hallucination in a legal filing.
57% of employees hide their AI use from managers.

Vera doesn't fix hallucination. It makes it visible.
```

**4/**
```
For power users: a CLI adds a second independent model as the auditor, hard rule enforcement, and markdown memory on disk you own.

pipx install git+https://github.com/iamitp/vera@v0.1.0

But the paste-in prompt covers 80% of it in 30 seconds.

github.com/iamitp/vera
```

---

## 5. r/LocalLLaMA

**Title:**
```
Vera — paste-in prompt that makes any AI tag its guesses (+ CLI for local-first audit)
```

**Body:**
```
Built a system prompt you can paste into any AI chat (Claude, ChatGPT, Gemini, Grok) that makes the model tag every factual claim:

- [CITED: source] — actually sourced
- [INFERRED low|med|high] — extrapolating
- [ASSUMED] — guessing

You see which lines to trust at a glance. No install. No API key for the paste-in version. 30 seconds.

Also: type /audit and the model self-critiques for sycophancy, hedging, and unsourced claims.

Real example from a run against the Anthropic API this morning (examples/live-demo/ in the repo): the conversation was about a Rust rewrite, and the user said 400 ms of p99 was JSON serialisation of 50 kB. The /audit pass worked out the implied throughput (~0.1 MB/s, ~1000x too slow) and flagged it as likely measurement error.

For power users, the CLI (pipx install git+https://github.com/iamitp/vera@v0.1.0) adds:
- A second independent model as auditor (not self-critique)
- Hard rule enforcement (banned phrases fail the turn, model regenerates)
- Markdown memory on disk you own

Repo: https://github.com/iamitp/vera

HN discussion: [paste the HN link after you post]
```

---

## 6. r/ClaudeAI / r/ChatGPT / r/OpenAI

Use the r/LocalLLaMA body above, swap title to:

```
I built a paste-in prompt that makes Claude/ChatGPT tag every guess
```

---

## 7. DM template (Simon Willison / Geoffrey Huntley / Swyx)

```
[Name] — built a small thing you might find interesting. Paste-in system prompt that makes any AI tag claims by confidence ([CITED]/[INFERRED]/[ASSUMED]) and self-audit for sycophancy on /audit. Works in Claude, ChatGPT, Gemini, Grok. No install. MIT.

github.com/iamitp/vera

Real run from this morning caught an implausible latency number neither the primary nor the user questioned (examples/live-demo/). Also has a CLI with a second model as auditor if you want the harder version. Happy to hear what breaks.
```

Order: Simon (@simonw) first, then Huntley (@GeoffreyHuntley), then Swyx (@swyx). No follow-up if no reply in 48 h.

---

## 8. Lobsters (if you have an invite)

- **URL field:** https://github.com/iamitp/vera
- **Title:** `Vera – paste-in prompt that makes any AI tag its guesses (MIT)`
- **Tags:** `ai`, `python`, `show`
- **Text:** blank (Lobsters prefers URL-only).

---

## 9. Tracking (open these daily for a week)

- https://github.com/iamitp/vera/graphs/traffic
- https://github.com/iamitp/vera/stargazers
- https://pypistats.org/packages/vera-ai (once PyPI is live)
- https://news.ycombinator.com/from?site=github.com/iamitp

Paste the daily numbers into a text file. After 7 days the referrer list tells you which channel earned its keep.
