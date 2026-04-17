# Backup / long-tail channels

If HN lands — great, these become amplifiers on day 2.
If HN misses — these keep the launch alive beyond the 6-hour HN window.

Post HN first, then cascade these over days 2–7. Don't dump them all at once.

---

## A · Lobsters (day 1, ~2 h after HN)

`lobste.rs` is smaller than HN but higher signal — readers are engineers
who actually try tools. Needs an invite; if you don't have one, skip.

- **URL:** https://lobste.rs/stories/new
- **Title:** `Vera – paste-in prompt that makes any AI tag its guesses (MIT)`
- **Tags:** `ai`, `python`, `show`
- **URL field:** `https://github.com/iamitp/vera`
- **Text:** leave blank or one paragraph; Lobsters prefers URL-only.

---

## B · dev.to blog post (day 2)

Longer-form than HN. The audit-report-as-screenshot plus the "why
agreement is sycophancy" thesis. Target ~800 words.

**Title:** `I built a paste-in prompt that makes any AI tag its guesses`

**Body skeleton (flesh out in your voice):**

```
## The problem nobody's solving at the prompt layer

Every AI will confidently tell you wrong things. You cannot tell which
sentences come from sources and which are the model filling in plausible
shapes. OpenAI rolled back a ChatGPT update for being too sycophantic.
Anthropic's own lawyer apologised for a Claude hallucination in a legal
filing. 57% of employees hide their AI use from fear of bad output.

## Three disciplines, one paste

Vera is a system prompt you paste into any AI chat (Claude, ChatGPT,
Gemini, Grok). No install. No extension. 30 seconds. The model gets
three disciplines:

1. **HONESTY.** Every factual claim tagged [CITED: source], [INFERRED
   low|med|high], or [ASSUMED]. You see which lines to trust on sight.
   When unsure: "I'm not sure" instead of guessing with confidence.

2. **ATTENTION.** Reads instructions literally. Corrections stick across
   the session. Negations stay negated. Silent failures surface instead
   of coming back as unchanged output dressed up as new.

3. **AUDIT.** Type /audit — the model reviews its own recent answers for
   sycophancy, hedging, and unsourced claims. Quotes itself.

## What the audit catches

[embed the /audit screenshot]

Type /audit after a few turns and the model calls out where it agreed
too easily, hedged without saying so, or claimed without a source.

## The deeper path

For power users, a CLI (pipx install vera-ai) adds: a second
independent model as auditor (not self-critique), hard rule enforcement
(banned phrases fail the turn, model regenerates), and on-disk markdown
memory you can grep and sync.

But the paste-in prompt covers 80% of the value. Start there.

github.com/iamitp/vera — MIT licensed.
```

Post to dev.to, cross-post to Medium if you use it, and add a canonical
link to github.com/iamitp/vera.

---

## C · LinkedIn post (day 2 or 3)

Different audience — enterprise / product folks, not engineers. Lead
with the sycophancy angle, not the technical primitives.

```
Every AI will confidently tell you wrong things. You can't see which
lines are sourced and which are guesses. I built a solution at the
prompt layer.

Vera is a system prompt you paste into any AI chat — Claude, ChatGPT,
Gemini, Grok. No install. 30 seconds. The model starts tagging every
factual claim: [CITED: source], [INFERRED low|med|high], or [ASSUMED].

You see which lines to trust at a glance.

Type /audit and it self-critiques for sycophancy and unsourced claims.

Why: OpenAI rolled back a sycophantic ChatGPT update. Anthropic's
lawyer apologised for a Claude hallucination. 57% of employees hide
AI use from fear of bad output. The problem is real.

MIT. Works in any AI chat. github.com/iamitp/vera
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
