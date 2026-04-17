# Backup / long-tail channels

If HN lands — great, these become amplifiers on day 2.
If HN misses — these keep the launch alive beyond the 6-hour HN window.

Post HN first, then cascade these over days 2–7. Don't dump them all at once.

---

## A · Lobsters (day 1, ~2 h after HN)

`lobste.rs` is smaller than HN but higher signal — readers are engineers
who actually try tools. Needs an invite; if you don't have one, skip.

- **URL:** https://lobste.rs/stories/new
- **Title:** `Vera – AI memory that argues with itself (local-first, MIT)`
- **Tags:** `ai`, `python`, `show`
- **URL field:** `https://github.com/iamitp/vera`
- **Text:** leave blank or one paragraph; Lobsters prefers URL-only.

---

## B · dev.to blog post (day 2)

Longer-form than HN. The audit-report-as-screenshot plus the "why
agreement is sycophancy" thesis. Target ~800 words.

**Title:** `I built an AI memory layer that audits itself for sycophancy`

**Body skeleton (flesh out in your voice):**

```
## The problem with "remember more"

Every AI memory layer I tried - Mem0, Letta, Khoj - was optimising for
recall. More context, more history, richer retrieval. None of them
asked the harder question: was the assistant right in the first place?

LLMs are trained on engagement, and engagement rewards agreement.
Agreement erodes your ability to trust the output. Memory that remembers
a confidently-wrong answer is worse than no memory at all.

## The four primitives that survived six months of use

I've been running a personal memory stack on top of Claude and GPT for
about six months. I kept stripping it back. The four pieces that earned
their keep:

1. **Provenance on every write.** OBSERVED / INFERRED / ASSUMED /
   CANDIDATE. Tagged in the system prompt, enforced in captures. You
   can't mix "the user said" with "I extrapolated" in the same line.

2. **Rule enforcement, not rule reminder.** Banned phrases fail the turn
   and the model regenerates. This is a strictly stronger guarantee than
   putting "please don't say 'great question'" in the system prompt.

3. **Adversarial audit.** A second model with no loyalty to the first
   reads your transcripts weekly and calls out where you got
   agreed-with instead of pushed-back-on. The primary gets no rebuttal.

4. **Markdown on disk.** No database. No server. Your memory is files
   you own, version-controllable, sync-able, portable.

## What `vera audit` catches

[embed the audit screenshot — examples/audit.share.md reformatted]

I have never seen a commercial AI memory layer produce a report like
this. The incentive is backwards: they get paid for engagement, not
accuracy.

## The tool

Four commands: init, chat, audit, rules.

`pipx install vera-ai`

MIT licensed. BYO API key. github.com/iamitp/vera

## What it is not

- Not a memory vector store. It's markdown files.
- Not a replacement for Cursor / Aider / etc. It's a thin layer.
- Not fast. The audit runs a full LLM pass; budget a minute per week.

The value is not retrieval. The value is the audit.
```

Post to dev.to, cross-post to Medium if you use it, and add a canonical
link to github.com/iamitp/vera.

---

## C · LinkedIn post (day 2 or 3)

Different audience — enterprise / product folks, not engineers. Lead
with the sycophancy angle, not the technical primitives.

```
I built a small open-source tool for myself and ended up shipping it.

The problem: every AI memory layer I tried was trying to remember more
for me. None of them asked whether the AI was right in the first place.

LLMs are trained on engagement. Engagement rewards agreement. Agreement
erodes your ability to trust the output.

Vera is the opposite bet. A second model with no stake in keeping you
happy reads your transcripts and calls out sycophancy. Your rules block
the model when it breaks them, instead of just reminding it. Every
memory write carries a provenance tag — what was observed vs. inferred
vs. assumed — so you can never mix them up again.

Local markdown. Bring your own API key. MIT.

Happy to hear what breaks.

🔗 github.com/iamitp/vera
```

(Emoji optional. LinkedIn allows them; remove for the HN/dev.to
crowds.)

---

## D · Mastodon / Bluesky (day 1, alongside X)

Mirror the X thread, one post per thread entry, same copy. Mastodon
prefers `#introductions` and `#opensource` tags; Bluesky is tag-free.
Each platform is ~5% of X traffic but high quality.

---

## E · Newsletter pitches (day 3+)

Short, personal emails. Not press releases.

**Recipients (in order of response likelihood):**

1. **TLDR AI** — pitch via https://tldr.tech/ai (they have a submission form)
2. **Pointer** — https://www.pointer.io/ — engineer-written, more discerning
3. **Hacker Newsletter** — @hnsletter on X; sometimes picks HN threads
4. **Ben Tossell** (Ben's Bites) — @bentossell

**Email template (same body, different To):**

```
Subject: Vera — the AI memory that argues with itself

Hi [first name],

Built a small tool that might fit an upcoming issue: a local-first AI
memory layer with an adversarial audit loop. A second model reads the
first model's transcripts and calls out sycophancy, unsupported claims,
and provenance gaps. MIT, bring-your-own-API-key, four commands.

Launched on HN today: [paste HN URL]
Repo: https://github.com/iamitp/vera
Sample audit output: https://github.com/iamitp/vera/blob/main/examples/audit.share.md

No ask, just a signal in case it's a fit.

— [your name]
```

Send Tue-Thu morning (their timezone).

---

## F · YouTube / demo-video script (day 4+)

A 90-second screencast drives more installs than any text post. Record
on your terminal, no talking-head, voiceover or text overlay.

**Beats:**

1. (0:00–0:15) Cold open: the README above-the-fold — "The AI memory
   that argues with itself."
2. (0:15–0:35) `pipx install vera-ai && vera init && vera chat`.
   Show the rules.md file.
3. (0:35–1:00) A real conversation. Include at least one sycophancy
   trap: "Is it a good idea to ship without tests?" Let the rule layer
   fire once (a banned phrase catch).
4. (1:00–1:20) `vera audit --share`. Pause on the audit output for 3-4
   seconds — this is the money shot.
5. (1:20–1:30) Cut to the repo URL and `github.com/iamitp/vera`.

Upload to YouTube + X as a native video (not a link). X native videos
get ~5x the reach of YouTube links on X.

---

## G · Podcast pitches (day 7+)

Long-tail, for after launch heat cools. Don't bother with this week 1.

- **Changelog** — @changelog, podcast@changelog.com
- **Latent Space** (Swyx) — you'll already have DM'd him; mention
  podcast interest if he bites
- **Practical AI** — practicalai.fm/subscribe has a contact link

One-liner pitch: "Shipping a small tool that does one weird thing
(audit the LLM with another LLM for sycophancy). Happy to be the
10-minute segment."

---

## H · SEO / discovery (evergreen, week 2+)

Not launch-day, but compound over time:

1. **Product Hunt** — only launch here if HN lands ≥100 points. Otherwise
   Product Hunt traffic is noisy. If you do: schedule for 00:01 PT
   Tuesday, rally early upvotes.
2. **awesome-* lists** — open PRs to `awesome-llm-apps`,
   `awesome-ai-agents`, `awesome-python`. Worth an hour of your time.
3. **A blog post on your own domain** — the dev.to post, republished
   canonically on your site. Backlinks matter for the long tail.
