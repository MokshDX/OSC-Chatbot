# Evaluation methodology

`evaluation.md` explains how the harness is built and how to run it. This page is
the reference for *what every number means* — the contract a metric has to satisfy
before it is allowed to gate a build.

Every metric below is documented against the same seven headings: **definition,
calculation, purpose, interpretation, limitations, baseline, regression criteria**.
A metric that cannot fill in all seven does not belong in the report, because a
number nobody can interpret is a number that gets argued about rather than acted on.

---

## The selection rule

The brief was to choose metrics that are defensible rather than to compute every
metric that exists. Three tests were applied, and a metric had to pass all three.

**Is it established?** Every retrieval metric here is from Manning, Raghavan &
Schütze's *Introduction to Information Retrieval* (2008) or Järvelin & Kekäläinen
(2002). Nothing was invented where a standard exists.

**Does it change a decision?** MAP was considered and rejected: with a golden set
where most questions have exactly one relevant document, MAP degenerates to MRR and
would be a second name for a number already reported. A metric that always agrees
with another metric is noise in the report.

**Can it be computed honestly here?** Answer *correctness* in the general sense —
"is this a good answer to the question?" — cannot be, without either a reference
answer per case (which fossilises the model's phrasing) or an LLM judge treated as
ground truth (which it is not). It is decomposed instead into `fact_match`,
`groundedness` and `citation_precision`, each of which is set arithmetic or
substring matching and reproducible from a recorded run.

### What is deliberately not measured

| Not measured | Why |
|---|---|
| MAP | Degenerates to MRR on a mostly-single-relevant-document set |
| BLEU / ROUGE against reference answers | Scores phrasing, not correctness; a correct answer in different words fails |
| Semantic answer similarity | Needs a reference answer, and inherits the embedding model being evaluated |
| Human preference | No annotators; a fabricated preference score would be worse than none |
| Recall of the corpus as a whole | Unknowable without exhaustive annotation of all 11 documents against 61 questions |

---

## Retrieval metrics

All four are computed **over documents, not chunks**, and all four are
**deterministic**: given one index and one configuration, the same query returns the
same ranking. That property is what allows their regression tolerance to be a
materiality threshold rather than a noise allowance (see *Regression gates* below).

Document-level relevance is a deliberate choice with a cost. Chunk ids derive from
chunk boundaries, so changing the chunker changes every chunk id in the corpus —
which would invalidate the golden set on precisely the experiment the golden set
exists to run. Document identity survives a re-chunk; chunk identity does not.

### `recall@k`

| | |
|---|---|
| **Definition** | Fraction of a question's relevant documents that appear in the top *k* results. |
| **Calculation** | `\|relevant ∩ retrieved[:k]\| / \|relevant\|`, averaged over cases that name relevant documents. |
| **Purpose** | The ceiling on everything downstream. Generation cannot recover from a passage that was never fetched, so recall bounds citation, grounding and factual accuracy simultaneously. |
| **Interpretation** | "Could the model possibly have got this right?" A recall of 0.98 means that for 98% of expected evidence, the model had the chance. |
| **Limitations** | Says nothing about *ordering* — a relevant document at rank 5 and at rank 1 score identically. Blind to relevant documents the curator did not think of, which inflates it slightly. |
| **Baseline** | **0.982** (schema suite, k=5, markdown chunker) |
| **Regression criteria** | Blocking. Tolerance `1/n` — one case out of the scored 55. |

### `precision@k`

| | |
|---|---|
| **Definition** | Fraction of the top *k* results that are relevant. |
| **Calculation** | `\|relevant ∩ retrieved[:k]\| / k`. Divided by *k*, not by the number returned. |
| **Purpose** | The cost side of recall. Every irrelevant chunk in the prompt is context budget spent on nothing and one more thing for the model to be distracted by. |
| **Interpretation** | **Structurally capped on this suite, and must be read that way.** Most questions have exactly one relevant document, so with `k=5` the maximum achievable `precision@5` is 0.2. The observed 0.200 is therefore a *perfect* score, not a bad one. This is the metric in the report most likely to be misread. |
| **Limitations** | The cap above makes cross-suite comparison meaningless. Only comparable between runs at the same *k* on the same suite. |
| **Baseline** | **0.200** (at the structural maximum) |
| **Regression criteria** | Blocking, and additionally guarded: an improvement in precision that coincides with a recall regression is blocked as a trade-off, because returning fewer results raises one and lowers the other. |

### `mrr` (mean reciprocal rank)

| | |
|---|---|
| **Definition** | Mean of `1 / (rank of the first relevant result)`, or 0 when none is present. |
| **Calculation** | Averaged over cases naming relevant documents; positions are 1-based over deduplicated documents. |
| **Purpose** | Measures ordering where recall measures presence. The prompt budget is finite, and a correct passage ranked eighth in a top-5 retrieval is a passage the model never saw. |
| **Interpretation** | 1.0 means the right document was always first. 0.5 means it was typically second. |
| **Limitations** | Only sees the *first* relevant result; a question with three relevant documents scores 1.0 if the first is at rank 1, regardless of where the other two land. That gap is why nDCG is also reported. |
| **Baseline** | **0.897** |
| **Regression criteria** | Blocking. Tolerance `1/n`. |

### `ndcg@k`

| | |
|---|---|
| **Definition** | Normalised discounted cumulative gain: every relevant document contributes, discounted logarithmically by its rank. |
| **Calculation** | `Σ 1/log₂(i+1)` over relevant hits in the top *k*, divided by the same sum for a perfect ranking, with the ideal **capped at k**. Binary relevance, so the `2^rel − 1` and plain-`rel` formulations coincide. |
| **Purpose** | The metric that separates two rankings recall and MRR cannot tell apart — the same three relevant documents at ranks 1,2,3 versus 1,4,5. |
| **Interpretation** | 1.0 means every relevant document is packed at the top. Falls as relevant material is pushed toward the `top_k` boundary. |
| **Limitations** | Binary relevance loses the distinction between "answers the question" and "mentions it". Graded relevance was rejected: asking a curator for 0–3 grades produces numbers with more precision than the judgement behind them. |
| **Baseline** | **0.918** |
| **Regression criteria** | Blocking. Tolerance `1/n`. |
| **Source** | Järvelin & Kekäläinen, *ACM TOIS* 20(4), 2002. https://doi.org/10.1145/582415.582418 |

### `hit_rate@k`

| | |
|---|---|
| **Definition** | Fraction of questions for which *any* relevant document appears in the top *k*. |
| **Calculation** | Binary per case, then averaged. |
| **Purpose** | Disambiguates a mean recall. 0.7 recall can mean "every question partly answered" or "seven answered and three missed entirely", and those need completely different work. |
| **Interpretation** | Read *with* recall. `hit_rate ≈ recall` means most questions have one relevant document. A large gap means multi-document questions are being partly served. |
| **Limitations** | Coarse by construction — it is the binary form of recall and adds nothing on a single-relevant-document suite. |
| **Baseline** | **0.982** |
| **Regression criteria** | Blocking. Tolerance `1/n`. |

---

## Generation metrics

Deterministic in *computation* but measuring a **sampled** process: the model can
answer the same question differently twice. That is why their regression tolerance
is a statistical interval rather than a materiality threshold.

### `groundedness`

| | |
|---|---|
| **Definition** | Fraction of citations whose cited chunk was actually in the retrieved set. |
| **Calculation** | `\|{citations with chunk_id ∈ retrieved}\| / \|citations\|`. Set arithmetic over ids. **No model is involved.** |
| **Purpose** | Detects a citation pointing at something the model was never shown — a fabricated reference. On the Anthropic native-citation path this is structurally impossible; on the marker-parsing path every other provider uses, it is the exact failure being measured. |
| **Interpretation** | Anything below 1.0 means the answer contains a reference the system cannot substantiate, which is worse than an uncited answer because it looks trustworthy. |
| **Limitations** | Proves the chunk was *present*, not that it *supports* the claim. That stronger property needs the judge (`faithfulness`). |
| **Baseline** | **1.000** |
| **Regression criteria** | Blocking, and effectively zero-tolerance: at p=1.0 the binomial standard error is 0, so the tolerance falls to the 0.005 floor. Any real drop fails. This is intended — a fabricated citation is not a quality trade-off. |

### `citation_coverage`

| | |
|---|---|
| **Definition** | Fraction of answered (non-abstained) cases carrying at least one citation. |
| **Calculation** | Mean of `citations > 0` over answered cases. |
| **Purpose** | The counterweight to abstention. Without it, a system could reach perfect abstention accuracy by declining everything. |
| **Interpretation** | With `require_citations: true` this is 1.0 by construction — an uncited answer becomes an abstention. Its value is as the *paired* metric in the abstention trade-off guard. |
| **Limitations** | Says nothing about whether the citation is the right one; that is `citation_precision`. |
| **Baseline** | **1.000** |
| **Regression criteria** | Blocking. Guarded against abstention: a rise in `abstention_accuracy` alongside a fall here is blocked as a trade-off. |

### `citation_precision`

| | |
|---|---|
| **Definition** | Fraction of citations pointing at a document the golden set marks relevant. |
| **Calculation** | `\|{grounded citations whose document ∈ relevant}\| / \|citations\|`. |
| **Purpose** | Distinguishes "cited something real" from "cited the right thing". |
| **Interpretation** | Deflated by design on multi-topic answers: an answer that correctly cites two documents where the curator listed one scores 0.5 without being wrong. Read as a trend across runs, not as an absolute. |
| **Limitations** | Inherits the golden set's blind spots more than any other metric here. |
| **Baseline** | **0.871** |
| **Regression criteria** | Blocking, two standard errors. |

### `fact_match`

| | |
|---|---|
| **Definition** | Fraction of cases whose answer contains every one of its `expected_facts`. |
| **Calculation** | Case-insensitive substring match, over cases that declare expected facts. All-or-nothing per case. |
| **Purpose** | The closest deterministic proxy for factual correctness. Facts are chosen to be short, distinctive and unguessable — `adt`, `registractionForm`, `IDEMPOTENCY_WINDOW_MS` — so a match is evidence of retrieval and extraction rather than of plausible generation. |
| **Interpretation** | The headline answer-quality number. Below 1.0 means the model had the passage (recall is 0.982) and did not carry the fact through. |
| **Limitations** | **Substring matching is brittle in one direction and blind in the other.** A correct answer that writes `oscp.adt` when the fact is `adt` passes; one that writes the value in a table cell the model reformatted may fail. It cannot detect a correct fact stated in a wrong context. It is a floor on correctness, not a measure of it. |
| **Baseline** | **0.782** |
| **Regression criteria** | Blocking, two standard errors. At p=0.78 over 47 fact-bearing cases that is ≈0.12 — wide, honestly reflecting that this is a sampled metric on a small suite. |

### `abstention_accuracy`

| | |
|---|---|
| **Definition** | Fraction of `must_abstain` cases where the system declined. |
| **Calculation** | Mean of `abstained` over abstention cases only. |
| **Purpose** | Without it, an evaluation rewards a model that answers everything confidently. This is the metric that makes "minimal hallucinations" measurable rather than aspirational. |
| **Interpretation** | **The weakest number in the current baseline.** 0.667 means two of six unanswerable questions got an answer. |
| **Limitations** | Six cases is a small sample — one case is worth 0.167, so the tolerance is necessarily wide (≈0.385). It measures only *whether* the system declined, not whether it declined for the right reason. |
| **Baseline** | **0.667** |
| **Regression criteria** | Blocking, two standard errors. Guarded: a rise here alongside a fall in `citation_coverage` is blocked, since abstaining more often improves this metric while making the system less useful. |

### `faithfulness` — LLM-as-judge, opt-in

| | |
|---|---|
| **Definition** | Fraction of answers a judge model rules fully supported by the passages shown. |
| **Calculation** | One call per answered case to the configured `fast_llm`, parsed to `supported` / `unsupported`. Enabled only with `--judge`. |
| **Purpose** | The one property no set-arithmetic metric reaches: whether the cited passage actually *supports* the claim, as opposed to merely being present. |
| **Interpretation** | Directional evidence, never ground truth. |
| **Limitations** | **Documented rather than papered over.** It is non-deterministic; it can change its mind between two runs of the same commit. Judge models are known to favour their own outputs, which is why the judge runs on `fast_llm` — a separate seam an operator can point at a stronger, different model — rather than on the model under evaluation. On the default profile both happen to be `qwen3:8b`, so **the local-profile faithfulness number measures self-agreement and should not be quoted**; point `fast_llm` elsewhere before trusting it. |
| **Baseline** | Not committed. |
| **Regression criteria** | **Never gates.** A gate that can change its mind between two runs of the same commit is not a gate. |

---

## Conversational metrics

The design point of this group is that **no number here is reported without its
control**. A follow-up that gets answered proves nothing on its own — it may have
retrieved the right document by keyword luck — so every turn flagged
`requires_context` or `context_switch` is run twice, once in the session and once
cold, and the pair is the measurement.

### `follow_up_resolution` / `follow_up_resolution_no_context` / `follow_up_lift`

| | |
|---|---|
| **Definition** | Hit rate on context-dependent turns, in-session and cold, and the difference. |
| **Calculation** | `hit_rate@k` over turns marked `requires_context`; the control repeats the same question against an empty session, retrieval only. `lift = in_session − cold`. |
| **Purpose** | The only honest measure of what conversational memory contributes. |
| **Interpretation** | **The lift is the number that matters; the absolute is not.** A high `follow_up_resolution` with a lift of zero means the follow-ups resolve without memory — a defect in the golden set, not evidence of a working feature. A negative lift means the conversation made retrieval *worse*. |
| **Limitations** | Measures resolution at the **retrieval** stage only. History reaches retrieval solely through the query rewriter; it reaches *generation* as prompt context regardless, so a zero lift with `rewrite_queries: false` is expected and does not mean the model saw no context. |
| **Baseline** | See *Measured baseline* in `PROJECT_STATUS.md` §1. |
| **Regression criteria** | Blocking, tolerance `1/n` over context-dependent turns. |

### `context_switch_recovery` / `context_pollution`

| | |
|---|---|
| **Definition** | Hit rate on standalone turns that follow an unrelated topic, and how far that falls below the cold control. |
| **Calculation** | `pollution = max(0, cold − in_session)`. Floored at zero: doing better than cold is not "negative harm". |
| **Purpose** | The opposite failure from follow-up resolution — history dragging retrieval back to the previous topic. |
| **Interpretation** | Here the control is the **benchmark to match, not to beat**. A standalone question should retrieve exactly as well mid-conversation as it does cold. `context_pollution` of 0 is the target. |
| **Limitations** | Only detects pollution that changes *which documents* are retrieved. Pollution that degrades the answer while retrieval stays correct is invisible here. |
| **Baseline** | See `PROJECT_STATUS.md` §1. |
| **Regression criteria** | Blocking, `1/n`. Lower is better, and the gate reads it that way. |

### `session_isolation`

| | |
|---|---|
| **Definition** | Fraction of turns answered against exactly their own conversation and nothing else. |
| **Calculation** | Turn *n* must see exactly `min(2(n−1), max_messages)` messages. Exact integer comparison, no model. |
| **Purpose** | Detects one session's state reaching another's, under the concurrency a real service runs at. |
| **Interpretation** | Expected to be 1.000. Like `groundedness`, the value is that it stops being 1.0 the day something breaks. |
| **Limitations** | Detects *volume* leakage, not content substitution — a store that returned the right count of the wrong messages would pass. That failure is covered by tests rather than by a metric. **An alternative was rejected**: comparing retrieved documents across cases looks correct and is not, because with 11 documents and `k=5` nearly every turn legitimately retrieves something another case also expects, so it would report a catastrophic leak on a perfectly isolated system. |
| **Baseline** | **1.000** |
| **Regression criteria** | Blocking, floor tolerance. Any drop is a real leak. |

### Multi-turn retrieval and generation metrics

`multi_turn_recall@k`, `multi_turn_ndcg@k`, `multi_turn_mrr`,
`multi_turn_groundedness`, `multi_turn_fact_match`,
`multi_turn_abstention_accuracy` and the rest are the **same functions** applied
per turn. They are prefixed rather than merged so that a single-turn regression and
a conversational one are distinguishable, and they mean exactly what their
single-turn counterparts mean above.

---

## System metrics

### `latency_p50` / `latency_p95` / `latency_mean`

Nearest-rank percentiles, not interpolated: every reported value is a latency that
was actually observed. **Reported, never blocking** — a developer's laptop
compiling something else while `make eval` runs is not a quality regression, and
failing a build for it would be a lie. Tolerance is relative (25%). Note that under
`--concurrency > 1` these measure per-case wall time under contention, which is
useful as a load signal and is not the same as single-request latency.

### `throughput_per_second`, `input_tokens_total`, `output_tokens_total`

Descriptive, and **excluded from gating entirely**: they measure the size and shape
of the run, not its quality. A suite that grew by ten cases would otherwise fail the
gate for using more input tokens. Tokens are the cost signal that makes a
prompt-budget change visible; throughput is what makes a concurrency change visible.

### `cases_scored` / `turns_scored` / error count

Failed cases are **excluded from every quality mean** and reported separately as a
count. Averaging a provider timeout in as a zero would let an unrelated
infrastructure problem read as a retrieval regression, which is the fastest way to
teach a team to ignore the dashboard.

---

## Regression gates

Implemented in `src/osc_assistant/evaluation/gate.py`. No threshold is typed by
hand; every tolerance is derived from the run it is applied to.

| Metric family | Tolerance | Why this and not a round number |
|---|---|---|
| Retrieval, conversational retrieval | `1 / n` — one case | Deterministic for a fixed index, so there is no noise to absorb. The tolerance is a *materiality* threshold, and "more than one case was lost" is the only unit a person reading a red build can act on. |
| Generation, abstention, citations | `2 × √(p(1−p)/n)` | Two standard errors of a binomial proportion — the conventional approximate 95% interval. A drop inside it is indistinguishable from re-running the same commit, and a gate that fires on noise is one people re-run until it passes. |
| Latency | 25% relative, **warning only** | Heavy-tailed and machine-dependent; no sample-size correction models a busy laptop. |
| Counts and totals | Not gated | They describe the run's size, not its quality. |

`n` is the number of cases that **actually contributed to that metric**, not the
suite size: `abstention_accuracy` over six cases is far noisier than `fact_match`
over forty-seven, and one tolerance for both would necessarily be wrong for one of
them.

Standard error of a proportion: Brown, Cai & DasGupta, "Interval Estimation for a
Binomial Proportion", *Statistical Science* 16(2), 2001.
https://doi.org/10.1214/ss/1009213286

### Trade-off guards

Checking thresholds one at a time cannot see a metric that improved because another
collapsed. Three pairings are guarded, each naming a real way to game this suite:

| Improves | At the cost of | The gaming move |
|---|---|---|
| `precision@k` | `recall@k` | Return fewer results |
| `abstention_accuracy` | `citation_coverage` | Abstain more often |
| `latency_p50` | `recall@k` | Retrieve fewer candidates |

When both halves move beyond their own tolerances in opposite directions, the gate
blocks regardless of how good the improving half looks alone.

### What the gate reports

Per regressed metric: previous value, current value, delta, the tolerance used, the
sentence explaining where that tolerance came from, severity, the **cases that
changed from passing to failing** (not every currently-failing case — that list is
identical on a good run and a bad one), and the categories those cases span.

---

## Related

- `evaluation.md` — how the harness is built and how to run it
- ADR 0005 — why the framework was built in-repo rather than adopting RAGAS
- ADR 0011 — the schema-first knowledge corpus
- ADR 0012 — the measured chunker decision
- ADR 0013 — ephemeral session memory
