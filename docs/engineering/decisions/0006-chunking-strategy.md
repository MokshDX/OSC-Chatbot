# ADR 0006 — Keep `recursive` as the default chunker until a measurement says otherwise

**Status:** Accepted · **Date:** Phase 2, reaffirmed Phase 4

---

## Context

Four chunking strategies are registered: `recursive` and `fixed` (OSC's own), and
`langchain_recursive` and `markdown` (from `langchain-text-splitters`).

The default is `recursive`, and it has **two known defects**, both documented in the
source: a chunk can exceed its size budget by up to the overlap, and the overlap slice
can cut mid-word. `langchain_recursive` has neither. On the face of it the default
should change.

Two things argue against changing it on that basis alone.

**Switching invalidates the entire index.** Chunk ids are derived from chunk boundaries,
so a new chunker changes every id — while every *document* content hash still matches.
Ingestion sees unchanged documents, skips them, and leaves a stale index that looks
perfectly healthy. `--reindex` is required, and forgetting it produces a silent
wrong-state rather than an error.

**Neither defect has been shown to matter.** "Exceeds the budget by up to the overlap"
is 120 characters on a 900-character target. "Cuts mid-word" affects the overlap region
only, which is by definition duplicated text that also appears whole in an adjacent
chunk. Both are real; neither is obviously load-bearing for retrieval quality.

And the project's rule is explicit: **a retrieval change ships with a measured
improvement.** Until Phase 4 there was no way to measure one.

## Decision

**Keep `recursive` as the default.** Register the alternatives, test them, and change the
default only when an evaluation run shows a gain.

Chunk ids come from **one shared helper that every chunker uses**, so idempotent
ingestion behaves identically whichever strategy is configured — which is what makes
swapping them a fair experiment rather than a confounded one.

`fixed` is retained as a deliberately naive **evaluation baseline**: a strategy that
respects no structure at all is the control that says how much the structure-aware ones
are actually worth.

Default parameters — `chunk_size: 900`, `chunk_overlap: 120` — are sized against the
answer model's 4096-token context: roughly 225 tokens per chunk, five chunks of sources,
leaving room for the system prompt and the answer.

## Alternatives considered

**Switch to `langchain_recursive` immediately**, on the grounds that its edge cases are
strictly better. This is the tempting one, and it is *probably* right. It was rejected
because "probably right" is exactly the reasoning the measurement rule exists to
replace — and because adopting it without a number would set the precedent that the rule
applies to other people's changes.

**Switch to `markdown` immediately.** The corpus is now 17 topic-scoped Markdown files
whose H2 headings are the questions users ask; a heading-aware splitter should keep a
question and its answer in one chunk and record the heading path. That is a strong
hypothesis and it is *still a hypothesis*.

**Semantic chunking** (split where embedding similarity between adjacent sentences
drops). Interesting, materially more expensive at ingest time, and unmeasurable against
the same missing baseline. Deferred, not rejected.

**Token-based rather than character-based sizing.** More accurate against a context
window, and requires a tokenizer per model — a provider-specific dependency in the
chunking layer, which is exactly the coupling the architecture avoids. Characters are an
approximation that does not leak vendor knowledge into a provider-agnostic module.

**Remove `fixed` as dead code.** It has no production use and exists only as a baseline
for a harness that, until Phase 4, did not exist. Kept because that harness now does.

## Consequences

**What it buys.**

- No index churn on a change nobody could justify.
- Four strategies available, all tested (`test_chunking.py`,
  `test_langchain_integration.py` cover id stability, content preservation, size budget
  and heading metadata).
- The comparison is now a genuine experiment with a control.

**What it costs.**

- **The default has known defects** and everyone reading the code can see them, which is
  a persistent small tax on credibility.
- **Two registered chunkers have no measured value.** They cost no code to maintain, but
  carrying unmeasured options is how a configuration surface grows without anyone
  deciding to grow it.
- Chunk size is measured in characters, so the relationship to the model's real budget is
  approximate.

**The open item, and it is the top one.** Run the comparison:

```bash
./osc eval --retrieval-only -o evaluation/results/recursive.json
./osc ingest ./docs/company --reindex --profile config/experiments/markdown.yaml
./osc eval --retrieval-only --profile config/experiments/markdown.yaml \
  --baseline evaluation/results/recursive.json
```

Whichever wins becomes the default, with the number recorded here as a superseding ADR.
This is a Milestone A success criterion and the single highest-value use of the harness
on day one — it is a decision that has been waiting on a measurement for two phases.
