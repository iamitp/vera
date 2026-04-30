# Vera

**Archived. Final release: 0.1.1 on PyPI as `vera-clerk`. No further development planned.**

Vera was a personal-discipline experiment: a CLI that paired a primary LLM with a second-model auditor, enforced rules by regenerating on violation, and kept a markdown memory of what was captured. The four primitives (provenance, rules, audit, memory) and the reasoning behind each live in [`PROMPT.md`](PROMPT.md). The audit catch the tool produced on a real payments-service conversation is preserved at [`examples/live-demo/`](examples/live-demo/).

The project shipped a working MVP but did not find a user beyond its author. Subsequent work has moved to a different problem.

## The catch

One run against the Anthropic API, on a payments-service conversation [(full artifacts)](examples/live-demo/):

> **What the user didn't push back on but should have**
>
> The user said *"400ms of the p99 is JSON serialisation of a 50 kB payload"* and neither party questioned how unusual that number is. 400 ms to serialize 50 kB of JSON in Python stdlib is extremely slow, suspiciously so. That's roughly 0.1 MB/s serialization throughput. Even stdlib `json` should handle 50 kB in single-digit milliseconds on modern hardware. Vera should have flagged it as implausible. This could indicate a measurement error, repeated serialization, or a much larger effective payload.

The first model missed the implausible number. The auditor caught it, worked out the implied throughput, and pointed at three plausible root causes. That was the design in action: a second pass with different loyalty.

## Status

- PyPI: `vera-clerk` 0.1.1, marked archived. No further releases expected.
- Repository: archived on GitHub.
- `PROMPT.md` stands on its own; anyone is free to lift the discipline into their own work.

MIT licensed.
