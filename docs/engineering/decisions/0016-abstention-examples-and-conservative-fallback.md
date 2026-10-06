# ADR 0016 — Abstention examples and conservative fallback

**Status:** Measured; zero-false-abstention requirement not met · **Date:** 2026-10-04

## Context

About half of the earlier abstention failures were a measurement gap: the model
declined in cited prose, while the metric counted only architectural refusals.
The rest reflected actual unsupported answers. ADR 0015 introduced an explicit
refusal contract. The next target is schema `abstention_accuracy >= 0.90` with
`false_abstention_rate = 0`; recognising more refusals alone is insufficient.

## Decision

Keep `[[NO_ANSWER]]` as a fixed output marker and strengthen the frozen prompt
with two generic examples: an unstated detail and an unsupported premise.
The shared buffered/streaming finalizer recognises marker-only completions despite
surrounding whitespace, quotes, punctuation and stray citations, returning the
standard message, `abstained=True` and no citations.

A conservative deterministic fallback recognises source-absence prose only when
every visible sentence matches the short pattern list and no substantive partial
answer remains. Tests cover noisy markers, multiple refusal sentences, decimal
values, supported partial answers and ordinary negative claims containing similar
phrases. The detector is not a semantic evidence judge.

## Alternatives

An LLM judge on every answer adds latency and cost and is rejected. A relevance-score
threshold remains deferred pending calibration that demonstrates safe separation:
ADR 0015's overlapping cosine distributions do not justify a production cutoff.

## Results

User-reported schema measurements; dashes mean unreported, not zero.

| Run | Cases | Abstention accuracy | False abstention rate | Fact match | Hit rate@5 |
|---|---:|---:|---:|---:|---:|
| Historical baseline (6 abstention cases) | 61 | 0.6667 | — | — | — |
| Widened set, before this change | 81 | 0.8333 | 0 | 0.8254 | 0.9841 |
| Final reported run | 81 | 0.9444 | 0.0159 | 0.7937 | 0.9841 |

The final screenshot does not report the abstention-case denominator; 81 is the
previously supplied suite size. The 61-case and 81-case figures are **not directly
comparable** because the abstention set was widened. Single-run results vary a
little between runs; these measurements do not establish a repeatable causal gain.

## Consequences

Accuracy meets its target, but false abstentions violate the zero requirement and
fact match fell. Acceptance remains open; **do not refresh baselines from this
run**. Inspect the falsely refused case before attributing it to the prompt or
fallback. Aggregate metrics cannot identify that cause. An unusually worded real
refusal can still be missed. No evaluation was run or baseline modified during
this documentation phase.
