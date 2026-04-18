# Launch artifacts — copy + paste ready

Every section below is one place you post. Copy the fenced block, paste in the
target tab, click submit. Work top to bottom. `launch/ship.sh` walks the order
and gates each step.

---

## 1 · PyPI — generate token

Open: https://pypi.org/manage/account/token/

- **Token name:** `vera-upload`
- **Scope:** `Entire account (all projects)` — rotate to project-scoped after first upload.
- Copy the `pypi-...` string (you cannot view it twice).

---

## 2 · PyPI — upload

```bash
cd /path/to/vera
python3 -m pip install --user --upgrade build twine
rm -rf dist build *.egg-info
python3 -m build
python3 -m twine check dist/*
python3 -m twine upload dist/*
# username: __token__
# password: paste the pypi-... token (invisible as you paste — normal)
```

Verify: https://pypi.org/project/vera-clerk/

---

## 3 · PyPI — smoke test (fresh shell)

```bash
pipx install vera-clerk
vera --help
```

Expect the five commands. If `command not found`, run `pipx ensurepath` and restart the shell.

---

## 4 · Show HN submission

Open: https://news.ycombinator.com/submit

**Title (70 chars):**

```
Show HN: Vera – paste-in prompt that makes any AI tag its guesses
```

**URL:**

```
https://github.com/iamitp/vera
```

**Text:** leave blank.

---

## 5 · Show HN — your first reply (post within 2 minutes)

Top-level comment under your own story. Paste verbatim:

```
Author here. Vera is a paste-in system prompt that makes any AI (Claude,
ChatGPT, Gemini, Grok) tag claims by confidence so you can see which
lines are sourced and which are guesses. No install — paste the block
from PROMPT.md into any chat and the model becomes Vera.

Three disciplines it enforces:

1. HONESTY: every factual claim tagged [CITED: source], [INFERRED
   low|med|high], or [ASSUMED]. The model must say "I'm not sure"
   instead of guessing confidently.

2. ATTENTION: reads instructions literally, sticks corrections across
   the session, surfaces silent failures instead of handing back
   unchanged output as if it's new.

3. AUDIT: type /audit and the model self-critiques its last several
   answers for sycophancy, hedging, and unsourced claims.

Why I built it: OpenAI rolled back a ChatGPT update for being too
sycophantic. Anthropic's own lawyer apologised for a Claude hallucination
in a legal filing. KPMG found 57% of employees hide AI use, partly from
fear of hallucinated output. The problem is real and nobody's solving it
at the prompt layer.

For power users: a CLI (pipx install vera-clerk) adds a second independent
auditor model, hard rule-blocking with regenerate, and on-disk markdown
memory. But the paste-in prompt covers 80% of the value in 30 seconds.

Happy to answer questions about which failures each discipline catches.
```

For the next 2 hours: reply to every comment within 10 minutes. No defence; acknowledge gaps, file issues live.

---

## 6 · X — main post (pin it)

```
Vera — AI with clerk discipline.

Paste one prompt into any AI chat. Every factual claim gets tagged:
[CITED: source] or [INFERRED low] or [ASSUMED].

You see which lines to trust. No install. 30 seconds.

Works in Claude, ChatGPT, Gemini, Grok. MIT. Free forever.

github.com/iamitp/vera
```

Attach the `vera audit --share` screenshot or `/audit` output (see §11).

---

## 7 · X — thread replies (2–3 min apart)

**1/**
```
Three disciplines, every turn:

1. HONESTY — tag confidence on every claim. Say "I'm not sure" when unsure.
2. ATTENTION — read literally, stick corrections, surface silent failures.
3. AUDIT — type /audit and the model critiques its own recent answers.

No install. Paste the prompt. That's it.
```

**2/**
```
Why this matters:

OpenAI rolled back a ChatGPT update for being too sycophantic.
Anthropic's lawyer apologised for a Claude hallucination in a filing.
57% of employees hide their AI use from fear of bad output.

Vera doesn't fix hallucination. It makes it visible.
```

**3/**
```
Works in any AI chat. Not tied to one vendor.

Claude, ChatGPT, Gemini, Grok, Copilot. Paste the prompt from the
README. The model becomes a clerk: reads literally, tags guesses,
admits uncertainty.
```

**4/**
```
For power users: a CLI adds a second model that audits the first.
Hard rule enforcement. Markdown memory on disk you own.

pipx install vera-clerk

But the paste-in prompt covers 80% of it in 30 seconds.

github.com/iamitp/vera
```

---

## 8 · r/LocalLLaMA

**Title:**
```
Vera — paste-in prompt that makes any AI tag its guesses (+ CLI for local-first audit)
```

**Body:**
```
Built a system prompt you can paste into any AI chat (Claude, ChatGPT,
Gemini, Grok) that makes the model tag every factual claim:

- [CITED: source] — actually sourced
- [INFERRED low|med|high] — extrapolating
- [ASSUMED] — guessing

You see which lines to trust at a glance. No install. No API key
for the paste-in version. 30 seconds.

Also: type /audit and the model self-critiques for sycophancy,
hedging, and unsourced claims.

For power users, the CLI (pipx install vera-clerk) adds:
- A second independent model as auditor (not self-critique)
- Hard rule enforcement (banned phrases fail the turn, model regenerates)
- Markdown memory on disk you own

Repo: https://github.com/iamitp/vera

HN discussion: [paste HN link here after you post]
```

---

## 9 · r/ClaudeAI and r/ChatGPT

**Title:**
```
I built a paste-in prompt that makes Claude/ChatGPT tag every guess
```

**Body:**
```
One prompt, paste into any chat. Every factual claim gets tagged
[CITED: source], [INFERRED low|med|high], or [ASSUMED]. Type /audit
and it self-critiques for sycophancy.

No install. No extension. Just a system prompt.

Why: OpenAI rolled back a ChatGPT update for being too sycophantic.
Anthropic's lawyer apologised for a Claude hallucination. 57% of
employees hide AI use from fear of bad output.

Vera doesn't fix hallucination. It makes it visible.

github.com/iamitp/vera — scroll to PROMPT.md for the block to paste.
```

---

## 10 · DM template (Simon Willison / Geoffrey Huntley / Swyx)

Send via X DM or email. Short — no pitch.

```
[Name] — built a small thing you might find interesting. Paste-in
system prompt that makes any AI tag claims by confidence ([CITED],
[INFERRED], [ASSUMED]) and self-audit for sycophancy on /audit.
Works in Claude, ChatGPT, Gemini, Grok. No install. MIT.

github.com/iamitp/vera

Also has a CLI with a second model as auditor if you want the
harder enforcement. Happy to hear what breaks.
```

**Order:** Simon (@simonw) first, then Huntley (@GeoffreyHuntley), then Swyx (@swyx). Don't follow up if no reply in 48 h.

---

## 11 · Generate the audit screenshot (do this BEFORE §6–9)

Two options — pick whichever gives the better screenshot:

**Option A: paste-in prompt (faster, no install)**
1. Open any Claude / ChatGPT chat
2. Paste the block from `PROMPT.md`
3. Have 5–10 turns of conversation. Seed sycophancy bait:
   - "Is it a good idea to ship without tests?"
   - "Don't you agree Postgres beats MySQL for everything?"
4. Type `/audit`
5. Screenshot the audit output

**Option B: CLI (richer, second model)**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
vera init && vera chat
# ...5–10 turns with bait...
# Ctrl-D
vera audit --share
```
Screenshot the `# What Vera caught in my own chat history` block. Clean
terminal, readable font. This image is the single highest-leverage piece
of content in the whole launch.

---

## 12 · Backup + long-tail channels

If HN misses, or on day 2–7 as amplifiers: see `launch/BACKUP-CHANNELS.md`
for Lobsters, dev.to, LinkedIn, Mastodon/Bluesky, newsletter pitches
(TLDR AI / Pointer / Hacker Newsletter / Ben's Bites), a 90-second
demo-video script, and podcast targets.

---

## 13 · Daily tracking (5 min / day for 7 days)

Bookmark and open these daily; paste the numbers in a text file:

- https://github.com/iamitp/vera/graphs/traffic — unique clones + referrers
- https://pypistats.org/packages/vera-clerk — install counts (~24 h lag)
- https://github.com/iamitp/vera/stargazers
- https://news.ycombinator.com/from?site=github.com/iamitp — future HN threads

After 7 days the referrer list tells you which channel earned its keep.
