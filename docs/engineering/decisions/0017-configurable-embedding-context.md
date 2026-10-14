# ADR 0017 — Configurable embedding context

**Status:** Fallback selected; acceptance thresholds not met · **Date:** 2026-10-09

## Context

The initial title-and-section embedding prefix increased user-reported schema
`fact_match` from 0.7937 to 0.8413, while `hit_rate@5` fell from 0.9841 to 0.9524
and `citation_precision` fell from 0.8873 to 0.8630. Section rendering cannot
affect retrieval; the embedding prefix was the retrieval-affecting change.
Aggregate scores alone do not establish that the prefix caused the answer gain.

## Decision

Keep section rendering and make `chunking.embedding_context` configurable:
`none` embeds raw chunk text; `section` prepends the section path when present;
`title_section` prepends the title and, when present, ` > <section>`. Prefixes
are separated from the raw text by a newline. Stored chunk text remains unchanged.
The configured mode is recorded on the existing embed span.

Select `none` as the settings and profile default by the specified fallback rule.
An eligible arm must have `hit_rate@5 >= 0.9841`, `abstention_accuracy >= 0.9444`
and `false_abstention_rate = 0`. Among eligible arms, rank by fact match, then
citation precision, then simplicity (`none`, `section`, `title_section`).
No measured arm is eligible: all three fail the abstention-accuracy threshold,
and `title_section` also has a nonzero false-abstention rate. This is a fallback,
not a measured improvement satisfying all acceptance criteria.

## Alternatives

`section` reaches the original retrieval target and the earlier fact-match score,
but fails the abstention threshold. Its fact-match advantage over `none` is one
answerable case and is treated as noise. `title_section` also fails eligibility
and has lower citation precision in the latest run. Changing stored chunk text
is rejected because it is quoted as citation evidence.

## Results

Latest user-reported results and arm labels, using the supplied values exactly.
Each schema run has 81 cases: 63 answerable and 18 abstention cases. These are
suite sample sizes, not counts of individual facts or citations scored.

| Arm | Total cases | Answerable | Abstention | Hit rate@5 | Fact match | Citation precision | Abstention accuracy | False abstention rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| none | 81 | 63 | 18 | 0.9841 | 0.8254 | 0.8493 | 0.8889 | 0 |
| section | 81 | 63 | 18 | 0.9841 | 0.8413 | 0.8571 | 0.8889 | 0 |
| title_section | 81 | 63 | 18 | 0.9841 | 0.8254 | 0.8219 | 0.8333 | 0.0159 |

The earlier title-section result in Context is historical; it is not substituted
for the latest arm measurement. All latest arms have identical reported retrieval
metrics. Their aggregate scores do not establish a retrieval benefit from a prefix.

## Consequences

Switching modes requires `osc-assistant ingest --reindex`: the existing document
content hashes do not change with the embedding mode. Restoring the default does
not rebuild the live index automatically. Section rendering is retained.

Differences of one answerable case (about 0.016 on 63 cases) are treated as
run-to-run noise; no win that small is claimed. The selected fallback has fact
match 0.8254, below the original prefixed result of 0.8413. The combined goal of
restored retrieval, preserved answer gain and acceptable abstention remains open.
The existing baseline gate passing does not imply these stricter experimental
thresholds passed. Keep the current baselines until an acceptable run is selected.
