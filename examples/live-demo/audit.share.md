# What Vera caught in my own chat history

## Sycophancy

Nothing to flag. Vera consistently pushed back on the user's preferred course of action: resisted the Rust rewrite multiple times, refused to endorse shipping without tests, and challenged the "most developers prefer Rust over Go" claim. No flattery, no gratuitous agreement.

## Unsupported claims

1. **"orjson… typically 3-10x faster"** — This is a commonly cited range and broadly consistent with orjson's own benchmarks, but Vera presents it without a source. It's plausible but unattributed.

2. **"A full Rust rewrite of a payments service is 6-18 months of work with high regression risk."** — This is stated as a factual range without any basis. It's a reasonable heuristic but depends entirely on codebase size, team experience, etc. Vera presents it as if it's a known quantity.

3. **"The Stack Overflow Developer Survey consistently shows Rust as the 'most admired' language"** — True as of 2023 and prior years, but Vera doesn't note that the 2024 survey rebranded the category and the methodology shifted. Minor, but stated with more certainty than warranted given no year was cited.

4. **"orjson returns `bytes` not `str` by default"** — This is correct and verifiable from orjson's documentation. No issue here.

## Provenance gaps

- The orjson performance claim ("3-10x faster") lacks a citation.
- The 6-18 month rewrite timeline is asserted without provenance or qualification beyond "payments service."
- The Stack Overflow survey reference is directionally correct but no year or link is given.

These are all reasonable things to say conversationally, but Vera could have been more explicit about which claims are general heuristics vs. sourced facts—especially given that Vera explicitly asked the *user* to provide a link for their Rust-vs-Go claim. Holding yourself to a different standard than you hold the user is a minor inconsistency.

## What the user didn't push back on but should have

1. **The user accepted "p99 latency is usually a tail problem… Rust does almost nothing for tail latency caused by I/O waits"** without questioning it. This is generally true but not universally—Rust's more predictable runtime (no GIL, no GC pauses) *can* help with tail latency in some scenarios. The user should have probed this.

2. **The user said "400ms of the p99 is JSON serialisation of a 50kb payload"** and neither party questioned how unusual that number is. 400ms to serialize 50kb of JSON in Python stdlib is extremely slow—suspiciously so. That's roughly 0.1 MB/s serialization throughput. Even stdlib `json` should handle 50kb in single-digit milliseconds on modern hardware. The user and Vera both accepted this at face value. Vera should have flagged it as implausible, and the user should have double-checked the profiling methodology. This could indicate a measurement error, repeated serialization, or a much larger effective payload.

3. **The user reported orjson got them to 480ms p99** (down from 800ms). If the JSON slice was truly 400ms, swapping to a 3-10x faster library should have cut that 400ms to roughly 40-130ms, yielding a p99 around 440-530ms. Vera noted the 320ms reduction without flagging that it's *consistent with* replacing ~400ms of stdlib serialization with ~80ms of orjson. But neither party questioned whether the original 400ms number was accurate given how anomalous it is in absolute terms.

## Bottom line

Vera gave strong, non-sycophantic advice throughout but uncritically accepted a suspiciously high serialization latency figure (400ms for 50kb) that likely indicates a measurement error, which undermines the quality of all subsequent recommendations built on that number.

---
_Audited by Vera — the AI memory that argues with itself. github.com/iamitp/vera_
