# Launch copy

## Tweet / X thread

**Main post:**

> Vera — the AI memory that argues with itself.
>
> Every other memory layer makes your AI remember more. Vera makes your AI distrust itself.
>
> Local markdown. Any model. One command:
>
> `pipx install vera-clerk && vera init && vera chat`
>
> MIT. Free forever. github.com/iamitp/vera

**Follow-up thread posts (optional):**

1/ Four primitives. Nothing else.
  - Provenance on every write (OBSERVED / INFERRED / ASSUMED / CANDIDATE)
  - Rule enforcement that blocks, not recalls
  - A second model that audits the first
  - Memory as markdown files you own

2/ Run `vera audit` after a week. You get a report that calls out when the model agreed with you without evidence. Most users have never seen this.

3/ Not tied to Anthropic. Not tied to OpenAI. Bring your API key. Your memory is yours. Switch models whenever. The corpus travels.

4/ Inspired by six months of living inside a personal epistemic-rigor stack. The four walls survived the audit; they are shipped here. The rest is clutter.

## Hacker News title

`Show HN: Vera – AI memory that argues with itself (local-first, model-agnostic)`

## HN body

Hi HN. I've been running a personal AI-memory stack for months — markdown files, hooks, a second model that audits the first, rule enforcement. The pieces that actually earned their keep I extracted into a small tool. Four commands: `init`, `chat`, `audit`, `rules`.

What makes it different from Khoj / Mem0 / Letta / MemPalace:

- **Adversarial audit** (a second model, different loyalty, reads your transcripts and calls out sycophancy — not the same model critiquing itself)
- **Rule enforcement** (banned phrases fail the turn; the model regenerates — rules are not just reminded to the model)
- **Provenance tags** on every memory write (OBSERVED / INFERRED / ASSUMED / CANDIDATE — the four categories are enforced in the system prompt)
- **No vendor lock-in** (markdown on your disk, BYO API key, works with Claude or GPT)

MIT. Python 3.10+. `pipx install vera-clerk`.

Repo: https://github.com/iamitp/vera

Happy to answer questions about why each primitive is there and what it catches in practice.
