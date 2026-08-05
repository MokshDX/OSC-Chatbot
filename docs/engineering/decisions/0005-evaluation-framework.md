# ADR 0005 — An in-repo evaluation harness, not a third-party one

**Status:** Accepted · **Date:** Phase 4

---

## Context

Every quality claim in this project was an opinion. Chunk size 900, overlap 120,
`top_k` 5, `candidates` 30, hybrid over vector, reranking off, query rewriting off,
`recursive` over `langchain_recursive` — every one of those is a decision, every one was
made by reasoning rather than measurement, and some are certainly wrong. Nobody could
say which.

The cost is not that the settings are bad. It is that **there was no way to find out**,
so nobody tried, so they never improved, and anyone proposing a change had to argue from
intuition against a decision also made from intuition. Work stopped being cumulative.

The project's own rule — *a retrieval change ships with a measured improvement* — was
unenforceable, and had already blocked a change that was probably correct: the default
chunker stayed `recursive` despite `langchain_recursive` having strictly better edge
cases, because switching changes every chunk id in a live index and there was no golden
set to justify it.

Meanwhile the surface to evaluate had grown: four chunking strategies, two provider
tiers, a reranker of unknown value, and a documented but unquantified gap between
Anthropic's verified citations and every other provider's `[n]` markers.

## Decision

**Build the harness in-repo**, as `src/osc_assistant/evaluation/` — four modules with
one dependency direction — plus a curated golden set in `evaluation/golden-set.yaml` and
an `./osc eval` command.

Key sub-decisions, each of which could have gone the other way:

**It drives the real pipelines**, built by the real `Container`. An evaluation that ran
against a special code path would measure the special code path.

**Relevance is scored at document level, not chunk level.** Chunk ids are derived from
chunk boundaries, so changing the chunker changes every id in the corpus — which would
invalidate the golden set on precisely the experiment it exists to run. Document
identity survives that change. It is also what a human curator can verify and what reads
sensibly in a review diff.

**Deterministic metrics gate CI; the LLM judge is opt-in.** A gate that can change its
mind between two runs of the same commit is not a gate. `recall@k`, `mrr`,
`precision@k`, `groundedness`, `fact_match` and `abstention_accuracy` need no model
call. `faithfulness` does, and is behind `--judge`.

**`groundedness` is computed from ids, not judgement.** A citation whose chunk was not
in the retrieved set cannot have been read from a source, because the model was never
shown one. On the native citation path that is impossible; on the marker-parsing path it
is the exact failure mode being measured — and it is measurable with set arithmetic.

**Abstention cases are in the golden set.** Without them an evaluation rewards a model
that answers everything confidently, which is the failure this system is architected
against.

**The configuration snapshot travels in the result JSON**, so comparing two runs cannot
silently compare two different systems.

**A metric that is absent is not a metric that is zero.** A `--retrieval-only` run
reports no generation metrics at all, and `compare` diffs only the intersection.

## Alternatives considered

**RAGAS.** The obvious candidate: purpose-built RAG metrics including faithfulness and
context precision. Rejected on three grounds. It is LLM-judge-first, so the metrics that
should gate CI are the ones that are non-deterministic; adopting it would mean adopting
its data model on top of ours, on the code path we most want to read; and it pulls a
substantial dependency tree — including a second LLM abstraction — into a project whose
whole provider story is its own. The metrics themselves are twenty lines of set
arithmetic; the value in RAGAS is the judge prompts, and one judge prompt is not a
dependency.

**TruLens / DeepEval / promptfoo.** Same shape of objection: each brings an opinionated
runner and its own configuration surface, and each would need adapting to a system whose
pipelines are already composed by a container.

**LLM-judge everything.** Faster to write, and produces a number that moves between two
runs of the same commit. Unusable as a CI gate.

**Chunk-level relevance.** More precise, and self-invalidating on the first chunker
change.

**A `pytest` suite with quality assertions.** Conflates two questions. `make test` asks
whether the system is *correct*; `make eval` asks whether it is *good*. A system can
pass every test and answer every question badly, and a quality assertion that fails on a
model's ordinary variance would get marked `xfail` within a week.

## Consequences

**What it buys.**

- `make eval`, `make eval-retrieval`, `make eval-gate`. Committed baselines in
  `evaluation/baselines/`.
- A first measured baseline: `recall@5` 0.932, `mrr` 0.860 over 81 cases.
- Provider, chunker and reranker comparisons become two-command experiments, because
  `--profile` already retargets the whole stack.
- Every case carries a `trace_id`, so a bad number is expandable into a waterfall rather
  than being a starting point for a reproduction.
- A guard that refuses to run a golden set naming documents the index does not hold —
  because a mistyped path and a genuine retrieval miss both score zero, and only one is
  a bug in the search stack.

**What it costs.**

- **A golden set is a maintained asset.** Edit an FAQ answer and a case may need
  updating. This is the real ongoing cost and there is no way around it.
- **86 cases is small**, and none of the questions came from a real user — the set was
  curated from the corpus, so it inherits the corpus's blind spots. Feedback capture is
  the natural next source, and the reason feedback compounds.
- **`precision@k` is near its ceiling by construction** (most cases have one relevant
  document out of five slots). Useful relatively, misleading absolutely.
- **The LLM judge is a biased estimator.** Used as a *relative* measure between two runs
  with the same judge — a comparison it is good at — never as an absolute claim.
- **A full run takes minutes**, because it is 86 local model calls. Hence
  `--retrieval-only` for the fast loop and for the CI gate.
- **The two scenario workbooks are indexed but unscored.** They compete for retrieval
  slots, which makes the numbers honestly harder, but no case asserts them.

**One defect found by building it**, worth recording because it is the class of bug this
subsystem is most prone to: `fact_match` initially reported **1.0** for
`--retrieval-only` runs. It is computed as "no expected fact was missing", and a run
that generated no answers has missed nothing — a metric that was arithmetically correct
and factually a lie. `test_evaluation.py` holds the regression.
