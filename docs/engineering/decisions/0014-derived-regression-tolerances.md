# ADR 0014 — Regression tolerances are derived, not typed

**Status:** Accepted · **Date:** Phase 6

---

## Context

Phase 4 shipped a CI gate as three flags in the `Makefile`:

```
./osc eval --retrieval-only \
  --baseline evaluation/baselines/retrieval-default.json \
  --fail-under recall@5=0.90 --fail-under mrr=0.82
```

The comment above it said *"Thresholds are the committed baseline rounded down."* That
is an honest description of an arbitrary number. 0.90 was chosen because the baseline
was 0.932 and 0.90 is a round number below it; nothing about 0.90 corresponds to any
property of the measurement.

Three problems followed from that, and all three are the kind that surface only when
someone relies on the gate.

**The threshold does not track the suite.** A recall of 0.90 on the 86-case FAQ suite
and on a hypothetical 300-case suite mean different amounts of lost work, and the flag
cannot tell.

**It cannot distinguish noise from regression.** Retrieval is deterministic for a fixed
index; generation is sampled and scores differently on two runs of the same commit. One
flat threshold treats both identically, so it is either too tight for the sampled
metrics or too loose for the deterministic ones. It was set for the deterministic ones,
which is why generation metrics were simply not gated.

**Each metric is checked alone.** `precision@5` can be improved by returning fewer
results, which lowers recall. `abstention_accuracy` reaches 1.0 by abstaining at
everything, which empties `citation_coverage`. A per-metric threshold passes both moves.

## Decision

**No threshold is typed. Every tolerance is computed from the run it judges**, and each
kind of metric gets the treatment its noise behaviour warrants.

| Family | Tolerance | Justification |
|---|---|---|
| Retrieval, conversational retrieval | `1 / n` — one case | Deterministic for a fixed index, so there is no noise to absorb. The tolerance is a **materiality** threshold, and "more than one case was lost" is the only unit a person reading a red build can act on. |
| Generation, citations, abstention | `2 × √(p(1−p)/n)` | Two standard errors of a binomial proportion — the conventional approximate 95% interval. A drop inside it is indistinguishable from re-running the same commit. |
| Latency | 25% relative, **warning only** | Heavy-tailed and machine-dependent; no sample-size correction models a busy laptop. |
| Counts and totals | Not gated | They describe the run's size, not its quality. |

`n` is the number of cases that **actually contributed to that metric**, not the suite
size. `abstention_accuracy` over six cases is far noisier than `fact_match` over
forty-seven, and one tolerance for both is necessarily wrong for one of them.

**Trade-off guards** check pairs rather than metrics. Three pairings are guarded, each
naming a real way to game this suite:

| Improves | At the cost of | The gaming move |
|---|---|---|
| `precision@k` | `recall@k` | Return fewer results |
| `abstention_accuracy` | `citation_coverage` | Abstain more often |
| `latency_p50` | `recall@k` | Retrieve fewer candidates |

When both halves move beyond their own tolerances in opposite directions, the gate
blocks regardless of how good the improving half looks alone.

**The gate explains itself.** Every finding carries previous value, current value,
delta, the tolerance used, the sentence saying where that tolerance came from,
severity, the cases that changed from passing to failing, and the categories they span.
A gate that prints "recall@5 failed" is a gate someone overrides.

Reference for the interval: Brown, Cai & DasGupta, "Interval Estimation for a Binomial
Proportion", *Statistical Science* 16(2), 2001.
https://doi.org/10.1214/ss/1009213286

## Alternatives considered

**Keep `--fail-under`, add more flags.** Rejected: it scales the problem rather than
solving it, and every added flag is another number chosen because it looked round.

**Gate on generation metrics with a flat threshold.** The reason Phase 4 did not gate
them at all. A flat threshold wide enough to survive sampling noise on `fact_match` is
too wide to catch a real regression; the derived interval is what makes gating them
possible.

**Bootstrap confidence intervals instead of the normal approximation.** More correct at
small `n` and at proportions near 0 or 1, which is exactly where this suite sits
(`groundedness` is 1.0). Rejected for now on cost/benefit: it needs the per-case data
resampled hundreds of times per metric, and the normal approximation's known weakness
at p→1 is handled by the `MINIMUM_TOLERANCE` floor. Worth revisiting if the gate starts
producing arguments.

**A held-out set the gate runs against, separate from the tuning set.** The
methodologically correct answer to overfitting the golden set, and genuinely deferred
rather than dismissed. It needs roughly twice the curated cases to be worth doing.

## Consequences

**`--fail-under` is gone.** `./osc eval` gates by default against the committed
baseline for the suite, and `--no-gate` opts out. Existing invocations passing
`--fail-under` will fail with an unknown-option error rather than silently ignoring it.

**A small suite has wide tolerances, and this is visible.** `abstention_accuracy` over
six cases has a tolerance of roughly 0.385 — it would take a drop of more than two
cases in six to fail the gate. That is honest rather than good: the fix is more
abstention cases, and the number now says so instead of hiding behind a threshold that
happened to be below the baseline.

**`groundedness` is effectively zero-tolerance.** At p=1.0 the standard error is 0, so
the tolerance falls to the 0.005 floor and any real drop fails. Intended: a fabricated
citation is not a quality trade-off to be balanced.

**The gate can now block a change whose headline metric improved.** That is the point,
and it will eventually annoy someone whose precision win is genuine. The finding names
both metrics and both deltas, so the argument is about the evidence rather than about
the gate.

**Retrieval-only is what CI runs.** A gate must be deterministic; including generation
would let it change its mind between two runs of the same commit. The full run is still
gated when invoked, for a human deciding whether to commit a new baseline.
