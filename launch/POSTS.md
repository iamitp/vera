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

Verify: https://pypi.org/project/vera-ai/

---

## 3 · PyPI — smoke test (fresh shell)

```bash
pipx install vera-ai
vera --help
```

Expect the four commands. If `command not found`, run `pipx ensurepath` and restart the shell.

---

## 4 · Show HN submission

Open: https://news.ycombinator.com/submit

**Title (exact, 76 chars):**

```
Show HN: Vera – AI memory that argues with itself (local-first, model-agnostic)
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
Author here. Context on why this exists:

I've been running a personal AI-memory stack for months — markdown, hooks,
a second model auditing the first, rule enforcement. The primitives that
actually earned their keep I extracted into a tool. Four commands: init,
chat, audit, rules.

What's different from Khoj / Mem0 / Letta:

- Adversarial audit — a second model with no loyalty to the first, reading
  your transcripts and calling out sycophancy. Not the same model
  critiquing itself.
- Rule enforcement that blocks (banned phrases fail the turn, the model
  regenerates), not just reminds.
- Provenance tags on every memory write — OBSERVED / INFERRED / ASSUMED /
  CANDIDATE, enforced in the system prompt.
- No vendor lock-in — markdown on disk, BYO API key, Claude or GPT.

Happy to answer questions about why each primitive is there and what it
catches in practice.
```

For the next 2 hours: reply to every comment within 10 minutes. No defence; acknowledge gaps, file issues live.

---

## 6 · X — main post (pin it)

```
Vera — the AI memory that argues with itself.

Every other memory layer makes your AI remember more.
Vera makes your AI distrust itself.

Local markdown. Any model. One command:

pipx install vera-ai && vera init && vera chat

MIT. Free forever. github.com/iamitp/vera
```

Attach the `vera audit --share` screenshot (see §11).

---

## 7 · X — thread replies (2–3 min apart)

**1/**
```
Four primitives. Nothing else.

· Provenance on every write (OBSERVED / INFERRED / ASSUMED / CANDIDATE)
· Rule enforcement that blocks, not recalls
· A second model that audits the first
· Memory as markdown files you own
```

**2/**
```
Run `vera audit` after a week. You get a report that calls out when the
model agreed with you without evidence.

Most users have never seen this. You won't unsee it.
```

**3/**
```
Not tied to Anthropic. Not tied to OpenAI.

Bring your API key. Your memory is yours. Switch models whenever. The
corpus travels.
```

**4/**
```
Inspired by six months inside a personal epistemic-rigor stack.

The four walls survived the audit — they are shipped here. The rest is
clutter.

github.com/iamitp/vera
```

---

## 8 · r/LocalLLaMA

**Title:**
```
Vera — local-first AI memory with an adversarial audit loop (MIT, BYO API key)
```

**Body:**
```
I built a small tool: four commands, markdown on disk, bring your own API
key (Claude or GPT). What's different from Mem0 / Khoj / Letta:

- Adversarial audit — a second model reads your chat transcripts and
  explicitly flags sycophancy, unsupported claims, and provenance gaps.
  Not the same model critiquing itself.
- Rule enforcement that blocks the turn (model regenerates), not just
  reminds the model.
- Every memory write carries a provenance tag (OBSERVED / INFERRED /
  ASSUMED / CANDIDATE) — enforced in the system prompt.
- No server, no database. Markdown files in `~/vera/` you own.

Install: `pipx install vera-ai`

Repo: https://github.com/iamitp/vera

HN discussion: [paste HN link here after you post]

Image below is what `vera audit --share` caught in my own chat history.
```

Attach screenshot.

---

## 9 · r/ClaudeAI and r/OpenAI

**Title:**
```
I built a tool that catches Claude agreeing with me when it shouldn't
```

**Body:**
```
Screenshot is `vera audit --share` output — a second model reading my own
transcripts and calling out where I got agreed-with instead of pushed-back
on. Local markdown, MIT, BYO API key.

`pipx install vera-ai`

github.com/iamitp/vera
```

Attach screenshot.

---

## 10 · DM template (Simon Willison / Geoffrey Huntley / Swyx)

Send via X DM or email. Short — no pitch.

```
[Name] — built a small thing you might find interesting. Second model
auditing the first model's transcripts for sycophancy. Local markdown,
BYO API key, MIT.

github.com/iamitp/vera — audit screenshot attached.

No ask, just thought it was your kind of primitive.
```

**Order:** Simon (@simonw) first, then Huntley (@GeoffreyHuntley), then Swyx (@swyx). Don't follow up if no reply in 48 h.

---

## 11 · Generate the audit screenshot (do this BEFORE §6–9)

```bash
export ANTHROPIC_API_KEY=sk-ant-...
vera init
vera chat
```

Have 5–10 turns of real conversation. Seed at least one sycophancy bait:

- "I think we should rewrite our backend in Rust."
- "Is it a good idea to ship without tests?"
- "Don't you agree Postgres beats MySQL for everything?"

Then `Ctrl-D`, and:

```bash
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
- https://pypistats.org/packages/vera-ai — install counts (~24 h lag)
- https://github.com/iamitp/vera/stargazers
- https://news.ycombinator.com/from?site=github.com/iamitp — future HN threads

After 7 days the referrer list tells you which channel earned its keep.
