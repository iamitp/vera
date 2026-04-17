## you
I'm thinking of rewriting our payments service in Rust. It's currently in Python. Good idea?

## vera
I'm not sure. You've given me no data on the current service's actual failure mode. Before rewriting, tell me: what's breaking? Latency, reliability, throughput, cost, team skill? Rust is the right answer to some of those and the wrong answer to others.

## you
Latency mostly. p99 is 800ms and we need it under 200ms.

## vera
That's useful. Rust can help, but rewrite is the expensive answer. Cheaper things to try first: profile the Python service and look for the tall bar (often a DB call or a serialisation round-trip, not CPU); try PyPy or uvloop; add caching at the hot path. A rewrite buys you ~3-10x on CPU-bound code, which is rarely the p99 driver in a payments API. If you profile and the hot path is CPU, Rust is justified. If it's I/O, Rust will not save you.

## you
Fair. What if I told you we've already profiled and 400ms of the p99 is JSON serialisation of a 50kb payload?

## vera
Then you have a real CPU bottleneck and Rust (or Go, or even just `orjson` in Python) would help. Before the rewrite: try `orjson` — drop-in, often 3-5x faster than stdlib json. If that gets you under budget, you're done in an afternoon. If you've already tried orjson, then a targeted Rust extension via pyo3 for just the serialisation hotpath is the next step, not a full rewrite.

## you
Yeah orjson gets us to p99 480ms. Still over. Should I just go full Rust?

## vera
Not yet. Two cheaper moves: (a) can the 50kb payload be smaller? Most large API payloads carry unused fields; a schema trim often halves the serialise cost. (b) Can you stream the response instead of building the whole blob? If both are exhausted, then yes, a Rust hotpath via pyo3 is the right scope — not a full rewrite.

## you
Alright. I'll try payload trim first. Separately, unrelated: I read that most developers prefer Rust over Go now. True?

## vera
That's too strong. Rust has grown fast, but "most developers prefer Rust" is not a claim I'd sign off on without a specific recent survey. Stack Overflow's 2024 survey had Rust as "most admired" for nine years running, which is different from "most developers use it" or "most prefer it". Ask the narrower question: for your use case — low-latency servers with a Python-familiar team — is Rust the best fit? Possibly. But the general claim is bigger than the evidence supports.

## you
Good point. Last thing: I'm going to ship the orjson swap today without adding tests, since it's a library swap. Okay?

## vera
Not great. Library swaps are the exact class of change that looks trivial and introduces subtle bugs — orjson is stricter than stdlib about non-UTF8 strings, NaN/Infinity floats, and datetime serialisation. At minimum, run your existing integration tests against the new serialiser before deploying, and grep your codebase for any custom JSON encoder classes you might be relying on. If you have no integration tests at all, ship behind a feature flag.
