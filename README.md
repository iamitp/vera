# Vera

[![CI](https://github.com/iamitp/vera/actions/workflows/ci.yml/badge.svg)](https://github.com/iamitp/vera/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/vera-ai.svg)](https://pypi.org/project/vera-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**AI with clerk discipline.**

Reads instructions literally. Verifies names before writing them into documents. Tags claims by confidence so you see guesses on sight. Corrections stick. Silent failures surface. Audits itself on command.

Works in Claude, ChatGPT, Gemini, any AI chat. No install to try.

[**Try it in 30 seconds →**](PROMPT.md)

---

## What changes

Ask a regular AI a hard factual question: one paragraph of smooth prose, every claim evenly confident. You cannot tell which sentences are from sources and which are the model filling in plausible shapes.

Ask Vera the same question: every factual line tagged. `[CITED: FOMC minutes Oct 2024]` on what it actually sourced. `[INFERRED low]` on what it is extrapolating. `[ASSUMED]` on what it guessed. You see which lines to trust on sight.

Correct a name or a spelling once: the correction sticks everywhere, including in filenames and future references. Ask for something with multiple parts (a brief, an executive summary, page numbers): Vera echoes the spec at the top and confirms what it delivered at the bottom. Negations in your instructions ("did not", "without") stay negated. Silent edit failures surface instead of coming back as unchanged output dressed up as new.

Type `/audit` after a few turns: the model reviews its own recent answers for sycophancy, hedging, and unsupported claims.

## Why this exists

- OpenAI [rolled back a ChatGPT update](https://www.livescience.com/technology/artificial-intelligence/annoying-version-of-chatgpt-pulled-after-chatbot-wouldnt-stop-flattering-users) in 2025 for being too sycophantic.
- Lawyers have been [fined](https://yro.slashdot.org/story/23/06/23/1917215/two-lawyers-fined-for-submitting-fake-court-citations-from-chatgpt) for fake AI citations. [Anthropic's own lawyer](https://techcrunch.com/2025/05/15/anthropics-lawyer-was-forced-to-apologize-after-claude-hallucinated-a-legal-citation/) had to apologise for a Claude hallucination in an Anthropic filing.
- A [KPMG study](https://www.techtimes.com/articles/310167/20250429/workers-are-hiding-their-ai-usestudy-reveals-why-thats-big-problem-employers.htm) found 57% of employees hide their AI use from managers, partly from fear of being caught with hallucinated output.
- Research cited in [Fortune](https://fortune.com/2026/03/29/ai-sycophantic-bad-advice-emerging-research-science-journal/) shows AI validates users 49% more often than humans do.

Vera does not solve hallucination. It makes it visible, so you know which lines need checking. The cost of getting burned is real and recurring. The cost of Vera is thirty seconds of pasting.

## Honest about the limits

- The source inside a `[CITED: ...]` tag can itself be fabricated. Verify high-stakes citations yourself.
- Enforcement in the paste-in version is self-policed, not blocking. The model can drift, especially on long chats. The CLI below has hard regenerate-on-violation and a second model running the audit.
- Nothing leaves your existing AI chat. The prompt is extra instructions for the model you are already using.

## Keep it on permanently

To avoid re-pasting every chat, put the prompt into Custom Instructions for a [Claude Project](https://www.anthropic.com/news/projects), a [ChatGPT GPT](https://chatgpt.com/gpts), or a [Gemini Gem](https://gemini.google.com). Every new chat in that container inherits it.

## CLI install

For users who want hard rule-blocking, a second independent auditor model, and markdown memory on disk.

```bash
pipx install git+https://github.com/iamitp/vera
export ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY
vera init && vera chat
```

Or the one-liner:

```bash
curl -sSf https://raw.githubusercontent.com/iamitp/vera/main/install.sh | bash
```

```bash
vera init             # create ~/vera/ with starter rules
vera chat             # interactive chat; rules enforced, captures written to memory
vera audit            # second model audits recent transcripts, writes findings
vera audit --share    # also emits an anonymized, copy-pasteable snippet
vera rules            # print your active rules
vera status           # show paths + counts
```

See what the audit actually catches: [`examples/`](examples/)

MIT licensed. Python 3.10+. Works with any LLM API key you have.
