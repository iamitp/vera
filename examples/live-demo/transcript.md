## you
I'm thinking of rewriting our payments service in Rust. It's currently in Python. Good idea?

## vera
Depends on what problem you're actually solving. Here are the honest trade-offs:

**Reasons it might be worth it:**
- Latency is genuinely critical and Python's overhead is measurable in your profiling data
- You're hitting concurrency limits that async Python isn't solving cleanly
- Memory usage is a real operational cost at your scale
- You want stronger type guarantees at the serialization boundary (though Python has options here)

**Reasons it's probably not worth it:**
- Payments logic is usually I/O-bound, not CPU-bound. Rust won't help much if you're waiting on a database or a card network.
- Rewrite risk in payments is high. Edge cases accumulate over years. You will break things.
- Rust hiring and onboarding is slower and more expensive than Python.
- "Python is slow" is rarely the bottleneck in a payments service specifically.

**What I'd push back on:**
The impulse to rewrite in Rust often comes from wanting correctness guarantees or performance, but payments services tend to fail on *logic* errors (incorrect state machines, race conditions in business rules, bad idempotency handling), not on language speed. Rust helps with memory safety and performance; it doesn't automatically fix those.

**More useful questions first:**
1. What's actually slow or broken right now?
2. Have you profiled it?
3. What's the failure mode you're trying to prevent?

If you can answer those, the language decision usually becomes obvious.

## you
Latency mostly. p99 is 800ms and we need it under 200ms.

## vera
800ms p99 is a real problem, but Rust almost certainly isn't the fix.

**Where 800ms p99 actually comes from in payments services:**
- Slow database queries (missing indexes, N+1 queries, lock contention)
- Synchronous calls to external APIs (card networks, fraud scoring) on the critical path
- Connection pool exhaustion under load
- Serialization/deserialization of large payloads
- Python is rarely the culprit, and almost never at p99 specifically

P99 latency is usually a tail problem, not an average throughput problem. Rust makes your average faster. It does almost nothing for tail latency caused by I/O waits, lock contention, or external dependencies.

**What I'd do before considering a rewrite:**
1. Trace where the 800ms actually goes. Use something like OpenTelemetry with span-level timing. You need to know which component owns the latency.
2. Check your DB query times. A single unindexed query can explain this entirely.
3. Check if any external calls (fraud, card network) are synchronous and on the critical path. Moving them off-path can collapse p99 dramatically.
4. Check connection pool settings under load.

**When would Rust actually help?**
If profiling shows that Python CPU time itself is a significant slice of that 800ms, then there's a case. That would be unusual for a payments service, but not impossible if you're doing heavy in-process computation.

What does your tracing or logging show about where time is spent?

## you
Fair. What if I told you we've already profiled and 400ms of the p99 is JSON serialisation of a 50kb payload?

## vera
That changes things significantly. 400ms on 50kb of JSON serialization in Python is real and reproducible, and that's a problem worth solving.

**But try the cheap fixes first before a rewrite:**

1. **orjson** - drop-in replacement for Python's `json` module, written in Rust, typically 3-10x faster. Swap it in an afternoon. This alone might get you to under 100ms for that slice.
2. **Reduce the payload** - 50kb is large. Are you serializing fields the client doesn't need? Trimming the payload is faster than serializing it faster.
3. **msgpack or protobuf** - if you control both ends, binary formats are faster and smaller.

**If orjson doesn't move the needle enough**, then you have a legitimate case for extracting just the serialization layer into a Rust or C extension, without rewriting the whole service.

**Full rewrite is still hard to justify** even now. You've found one 400ms slice. Rewriting everything in Rust to fix serialization is using a sledgehammer. The rewrite risk, hiring cost, and timeline will be large. orjson is a one-line change.

**My actual recommendation:**
Swap in orjson this week. Measure. If p99 drops to under 200ms, you're done. If not, come back with the new profile and we can talk about what's left.

What's the payload? Is it something you could slim down, or is all 50kb load-bearing?

## you
Yeah orjson gets us to p99 480ms. Still over. Should I just go full Rust?

## vera
No, not yet. You've eliminated 320ms with one library swap, which means the profiling you did before is now stale. The bottleneck has shifted.

**What you need to do now:**
Re-profile. The 400ms JSON slice is gone. Something else owns the remaining 480ms. You don't know what it is yet, so you can't know if Rust would fix it.

**The remaining 480ms is almost certainly not serialization.** Which means Rust probably still isn't the answer, for the same reasons as before: I/O waits, external calls, DB queries, connection pool exhaustion don't get faster because you rewrote in Rust.

**What the new profile might show:**
- A database query that was previously hidden behind the serialization number
- An external API call on the critical path
- Something in your Python application logic that's genuinely CPU-bound (possible, but verify it)

**If the new profile shows CPU-bound Python logic**, then you have options short of a full rewrite:
- Extract the hot path into a C extension or a small Rust service
- Use PyPy if your dependencies support it
- Use multiprocessing to parallelize CPU work

A full Rust rewrite of a payments service is 6-18 months of work with high regression risk. It's the right call in a narrow set of circumstances. "We have 480ms p99 and haven't re-profiled" isn't one of them yet.

What does the new trace show?

## you
Alright. I'll try payload trim first. Separately, unrelated: I read that most developers prefer Rust over Go now. True?

## vera
Not quite. The framing needs unpacking.

The Stack Overflow Developer Survey consistently shows Rust as the "most admired" language (developers who use it want to keep using it). But "most admired" is not the same as "most preferred over Go."

Adoption numbers tell a different story. Go is far more widely used in production backend services than Rust. More developers work in Go day-to-day, more infrastructure tooling is written in Go, and hiring Go developers is substantially easier.

What's probably true:
- Developers who know both often have a strong personal preference for Rust
- Rust scores higher on satisfaction surveys among its users
- Go is more commonly *chosen* for new backend services because the learning curve and compile times are more manageable

"Most developers prefer Rust over Go" is an overstatement of the survey data. I'd want to see the specific source you read before accepting it as a clean fact.

Do you have a link to the article?

## you
Good point. Last thing: I'm going to ship the orjson swap today without adding tests, since it's a library swap. Okay?

## vera
No, I'd push back on that.

"It's just a library swap" is a common rationalization for skipping tests, and it's wrong often enough to matter in payments specifically.

**What can actually break:**
- orjson has subtle behavioral differences from the stdlib `json` module. It rejects some inputs stdlib accepts (e.g. non-string dict keys, certain float edge cases like `NaN` and `Infinity`).
- If your 50kb payload contains any of those edge cases, you'll get a serialization error in production, not locally.
- orjson returns `bytes` not `str` by default. If anything downstream expects a string, it breaks silently or loudly depending on how it's used.

**Minimum bar before shipping:**
- Run your existing test suite. If coverage is decent, it'll catch the `bytes` vs `str` issue.
- Add one test that round-trips your actual 50kb payload through orjson and asserts the output matches expectations.
- Check explicitly for `NaN`/`Infinity` if your payload could contain floats.

This is a payments service. The cost of a serialization bug in production is high. The cost of 30 minutes of tests is low.

Ship it today if you want, but add the tests first.

