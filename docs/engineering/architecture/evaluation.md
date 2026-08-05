# Evaluation

*How OSC knows whether a change helped. The instrument every future retrieval
decision is read off.*

---

## Why this exists

Before it, every quality claim in this project was an opinion. Chunk size 900, overlap
120, `top_k` 5, `candidates` 30, hybrid over vector, reranking off, query rewriting
off, `recursive` over `langchain_recursive` — every one of those is a decision, and
every one was made by reasoning rather than by measurement. Some are certainly wrong.
Nobody could say which.

That is a specific, expensive failure mode. It is not that the settings are bad; it is
that **there is no way to find out**, so nobody tries, so they never improve, and the
first person to propose a change has to argue from intuition against a decision that
was also made from intuition. Work stops being cumulative.

The harness makes the project's own rule enforceable: *a retrieval change ships with a
measured improvement.*

---

## Quick start

```bash
make ingest              # the golden set is scored against what is actually indexed
make eval-retrieval      # fast, free, no model calls — chunkers and embeddings
make eval                # the full picture, including generation
make eval-gate           # what CI runs: fails on a regression
```

Or directly, for the shapes the Makefile does not cover:

```bash
./osc eval --tag draft-order                 # one product area
./osc eval --concurrency 4                   # measure throughput under load
./osc eval --judge                           # add LLM-as-judge faithfulness
./osc eval --profile config/experiments/hosted-anthropic.yaml -o evaluation/results/anthropic.json
./osc eval --baseline evaluation/baselines/full-default.json   # diff against a known run
```

---

## How it is put together

```mermaid
graph LR
    G[golden-set.yaml] --> D[dataset.py<br/>load + validate]
    D --> R[runner.py<br/>Evaluator]
    C[Container] --> R
    R --> RP[RetrievalPipeline]
    R --> AN[Answerer]
    R --> J[judge.py<br/>optional]
    RP --> M[metrics.py<br/>pure functions]
    AN --> M
    M --> REP[EvaluationReport]
    REP --> JSON[(result JSON)]
    REP --> T[terminal table]
```

Four modules, one dependency direction. `dataset` and `metrics` know nothing about the
rest of the system; `judge` needs only a `ChatModel`; `runner` composes them with the
**real** pipelines built by the **real** `Container`. An evaluation that ran against a
special code path would measure the special code path.

### Three load-bearing properties

**A case never aborts the run.** A provider timeout on question 34 of 86 must not
discard the 33 results already collected. It is recorded as a failed case, excluded
from every quality mean, and counted separately. A harness that is itself fragile does
not get run, and a harness that averages a timeout in as a zero teaches the team that
the dashboard is noise.

**Every case records its trace id.** The report says recall was 0.93; the trace id on
the six cases that missed says *why*, expandable with `./osc trace <id>` long after the
run finished. Without it a bad number is the start of a reproduction rather than an
explanation.

**The configuration travels with the numbers.** A result JSON carries the chunker, the
retrieval settings, the reranker and both model ids — so comparing two runs cannot
silently compare two different systems. `compare` diffs only metrics present in both.

---

## The golden set

`evaluation/golden-set.yaml`. 86 cases: 81 with known-correct source documents, 5 that
the corpus genuinely cannot answer.

```yaml
- id: draft-order-tag
  question: How can I tell which of my orders were created by the app?
  relevant_documents: [faq/draft-order.md]
  expected_facts: ["oscp-order-processing"]
  tags: [draft-order]

- id: abstain-pricing-plans
  question: How much does the OSCP Wholesale B2B app cost per month?
  must_abstain: true
  tags: [abstention]
```

### Two curation rules, and why they matter more than the case count

**Questions are phrased the way a user would ask them, never copied from a document
heading.** A golden set of verbatim headings measures string matching and reports it as
retrieval quality: every case scores 1.0, the number never moves for a reason anyone
can act on, and the harness becomes a ritual. Paraphrase is the whole point — it is the
gap between how content is written and how it is asked about that retrieval exists to
close.

**`expected_facts` are short, distinctive and load-bearing** — a number, a limit, a tag,
a product name. Anything longer scores the model's *phrasing* rather than its
correctness, and fails a perfectly good answer that used a synonym.

### Why abstention cases are in the set

Without them, an evaluation rewards a model that answers everything confidently — the
exact failure this system is architected against. Five questions the corpus cannot
answer are five chances to catch a regression in the abstention path, and they cost
nothing to maintain.

### Why relevance is scored at document level, not chunk level

Chunk ids are derived from chunk boundaries. Change the chunker or its size and *every
chunk id in the corpus changes* — which would invalidate the golden set on precisely
the experiment the golden set exists to run (`recursive` vs `langchain_recursive` vs
`markdown`). Document identity survives that change; chunk identity does not.

Document paths are also something a human curator can actually verify, and something
that reads sensibly in a code review diff. `relevant_documents` are corpus-relative
paths — the same string the loader records as `relative_path` on every chunk.

### The guard that stops a typo reading as a regression

Before a run starts, every `relevant_documents` entry is checked against what is
actually indexed. A mistyped path and a genuine retrieval miss both score recall 0, and
only one of them is a bug in the search stack. The check turns thirty minutes of "why
did recall collapse?" into one line naming the file.

---

## The metrics

### Retrieval — deterministic, no model calls

| Metric | Definition | What it tells you |
|---|---|---|
| `recall@k` | fraction of relevant documents present in the top *k* | **The headline.** Generation cannot recover from a passage that was never fetched, so recall bounds every downstream metric |
| `precision@k` | fraction of the top *k* that are relevant | How much of the model's finite context budget was wasted |
| `mrr` | mean of 1/(rank of first relevant) | Ordering, where recall measures presence. A correct passage ranked 8th in a top-5 retrieval is a passage the model never saw |
| `hit_rate@k` | fraction of cases with *any* relevant hit | Disambiguates recall 0.7: every question partly answered, or seven answered and three missed entirely? Different corpora, different work |

`precision@k` divides by *k*, not by the number of results actually returned:
returning three where five were requested is a real cost, because the unfilled slots
were context the model could have had.

### Generation — deterministic

| Metric | Definition | What it catches |
|---|---|---|
| `citation_coverage` | fraction of non-abstaining answers carrying ≥1 citation | A model answering without grounding |
| `groundedness` | fraction of citations whose chunk was actually in the retrieved set | **A fabricated citation.** On the native path this is impossible; on the marker-parsing path it is the exact failure mode being measured — and it needs no judge |
| `citation_precision` | fraction of citations pointing at a *golden* document | Citing something real but irrelevant |
| `fact_match` | fraction of cases where every `expected_fact` appears | The local model's [numeric-fidelity gap](../../../PROJECT_STATUS.md) — right passage, right citation, wrong number |
| `abstention_accuracy` | fraction of `must_abstain` cases that abstained | Hallucination on out-of-corpus questions |

### Generation — LLM-as-judge, opt-in

| Metric | How |
|---|---|
| `faithfulness` | `--judge`. Every claim in the answer checked against the passages it was built from |

Opt-in for two reasons. It doubles the model calls in a run, and it measures with an
instrument made of the same material as the thing being measured. The deterministic
metrics gate CI, because **a gate that can change its mind between two runs of the same
commit is not a gate**. Faithfulness is for depth — it is how the citation-strength gap
between Anthropic's verified citations and everyone else's `[n]` markers gets a number
rather than a caveat.

The judge uses `fast_llm` rather than `llm` deliberately: judging a model's output with
the identical model mostly measures self-agreement, and `fast_llm` is the seam an
operator can point at a stronger model without changing what is under test. An
unreachable judge records `None`, not a default — inflating the metric on runs where
something was wrong, or blaming the system under test for a failure in the instrument,
are both worse than an absent number.

> **Honest limitation.** An LLM judge is a biased estimator. It is used here as a
> *relative* measure between two runs of the same golden set with the same judge — a
> comparison it is good at — and not as an absolute claim. See Zheng et al.,
> [*Judging LLM-as-a-Judge*](https://arxiv.org/abs/2306.05685) (NeurIPS 2023).

### Cost and speed

`latency_p50/p95/mean_seconds`, `throughput_per_second`, `input_tokens_total`,
`output_tokens_total`. Percentiles are **nearest-rank**, so every latency reported is
one that was actually observed rather than an average of two that were not.

Throughput is meaningful only with `--concurrency > 1`; at concurrency 1 it is the
reciprocal of mean latency.

### A metric that is absent is not a metric that is zero

A `--retrieval-only` run reports **no generation metrics at all**. Letting them fall
out at zero was the first defect this harness had: `fact_match` is computed as "no
expected fact was missing", and a run that generated no answers has missed nothing — so
it scored a perfect 1.0 for work it never did. Omitting the keys also makes `compare`
refuse to diff a retrieval-only run against a full one, which is the right answer to a
comparison that was never meaningful.

---

## Running a comparison

The intended workflow, and the reason the configuration snapshot exists:

```bash
# Baseline: whatever is committed today.
./osc eval --retrieval-only -o evaluation/baselines/retrieval-default.json

# Change one thing.
$EDITOR config/experiments/markdown-chunker.yaml     # chunking.strategy: markdown
./osc ingest ./docs/company --reindex --profile config/experiments/markdown-chunker.yaml

# Measure it against the baseline.
./osc eval --retrieval-only \
  --profile config/experiments/markdown-chunker.yaml \
  --baseline evaluation/baselines/retrieval-default.json
```

The comparison table colours a delta by direction, using a table of which metrics
improve *downwards* (latency, tokens) so a latency regression is never reported as
green. It also prints every configuration key that differs between the two runs — the
cheapest possible defence against comparing two systems and calling it a result.

**Changing the chunker invalidates every stored chunk while every content hash still
matches**, so `--reindex` is mandatory. Forgetting it measures the old index under the
new label.

---

## Gating CI

```bash
./osc eval --retrieval-only \
  --baseline evaluation/baselines/retrieval-default.json \
  --fail-under recall@5=0.90 --fail-under mrr=0.82
```

Exits non-zero if any named metric is below its threshold. `--fail-under` is parsed in
the CLI rather than in the runner because it is a *policy about* a run, not a property
*of* one: the same numbers are a pass in a local experiment and a failure in CI, and
only the caller knows which it is.

Thresholds are the committed baseline rounded down — tight enough to catch a
regression, loose enough that ordinary variance does not cry wolf. Raise them when a
change earns it; a threshold that never moves is a threshold nobody believes.

---

## Committed baselines

`evaluation/baselines/` is committed; `evaluation/results/` is gitignored. Ad-hoc runs
are noise. A run worth keeping is promoted to a named file, because a baseline nobody
can see is not a baseline.

| File | What it records |
|---|---|
| `retrieval-default.json` | Default local profile, retrieval only. The CI gate's reference |
| `full-default.json` | Default local profile with generation. The quality reference |

---

## What this does not yet measure

- **No hosted provider has been evaluated.** Every hosted adapter is exercised only via
  stubs, including the Anthropic native-citation path — the only verified citation
  implementation in the codebase. Running `--profile config/experiments/hosted-anthropic.yaml`
  is one command; it needs a credential.
- **The two scenario workbooks are not in the golden set.** All 81 scored cases target
  the FAQ. The `.docx` and `.xlsx` documents are indexed and compete for retrieval
  slots — which makes the numbers *harder*, honestly — but no case asserts they can be
  retrieved.
- **No question was written by a user.** The set was curated from the corpus, which
  means it inherits the corpus's blind spots. Real questions from
  [feedback capture](../../../PROJECT_STATUS.md) are the natural next source, and the
  reason feedback compounds.
- **Nothing measures answer *helpfulness*.** Faithfulness and fact coverage together
  say "not wrong". They do not say "useful".

---

## Related

- [retrieval.md](retrieval.md) — what the numbers are measuring
- [knowledge-corpus.md](knowledge-corpus.md) — why the corpus shape and the golden set are coupled
- [ADR 0005](../decisions/0005-evaluation-framework.md) — the decision record
