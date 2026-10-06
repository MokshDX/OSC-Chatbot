# ADR 0015 — Explicit model abstention and an answerability guard

**Status:** Measured; milestone acceptance not met · **Date:** 2026-10-02

## Context

The committed schema baseline contains six must-abstain cases. Four are correctly
marked abstained; two contain citations and are marked answered. The Liquid snippet
response explicitly says the requested source is unavailable. The HTTP routes response
also says the routes are not listed, but first asserts that the module exposes no
routes. That assertion is unsupported: absence from a schema document does not prove
absence from the application. This is partly a recognition gap and partly a behaviour
gap, not evidence that both failures were harmless refusals.

Before this change, the answerer recognised no retrieved sources and uncited completions.
`min_score=0.0` accepts all returned hybrid RRF results; rank fusion scores are not
calibrated probabilities of answerability. The frozen system prompt requests prose
refusals, which can carry citations and evade the architectural flag.

## Experiment protocol (recorded before changing generation)

The pre-change implementation is repository commit
`f09ae5773d230c7a8b4bc8b15bd46ee31894e0dc`. The widened suites, source hashes and
eleven unchanged corpus hashes were recorded before changing generation. Runs use
the local `qwen3:8b` / `nomic-embed-text` profile, the same 80-chunk index and `top_k=5`.

1. Preserve all six original abstention cases. Add twelve, bringing the total to
   eighteen: six clearly unrelated questions and twelve near-domain questions overall.
   Add eight answerable look-alikes, including a negative answer and a partial answer.
   Add three conversational sessions (eight turns, three must-abstain).
2. Run the unchanged implementation on both widened suites. Store the raw reports
   untracked under `evaluation/results/abstention-before-*.json`; do not promote them.
3. Freeze one sentinel prompt before inspecting development results. Compare the
   sentinel implementation using `--baseline`. Consider a prose fallback only if
   measured gaps remain; consider a calibrated relevance gate only if still needed.
4. Do not inspect results for the four `holdout` cases until the implementation and
   prompt are frozen for the final measurement. Creating and corpus-checking their
   labels is curation, not tuning. The unchanged baseline may execute them, but its
   development summary must exclude them. Final reporting includes all eighteen.
5. Add the false-abstention summaries and derived regression guards. Run both full
   suites twice with the final implementation and report both, including errors and
   regressions. Only promote a baseline after the acceptance criteria are met.

### Corpus audit

Before adding cases, searched all eleven schema files using case-insensitive ripgrep
for `expirationDays|expir|retry|retries|backoff|smtp|port|LoyaltyRewards|loyalty|currency|
USD|EUR|region|backup|retention|sourdough|planet|jupiter|football|photosynthesis|submarine|
beethoven`, and inspected the relevant inventories and samples. No corpus file changed.

| New abstention case | Evidence for absence |
|---|---|
| email-retry-count | schema-7 lists templates and SMTP environment configuration; no retry policy or count anywhere in the corpus |
| draft-retention | schema-6 states a 15-minute reuse window, not deletion or retention; no deletion interval in the corpus |
| lock-expiration (holdout) | schema-10 inventory has no expiration field or default; no expirationDays match anywhere |
| email-port (holdout) | SMTP transport is named, but no numeric port is given anywhere |
| loyalty-module (holdout) | No LoyaltyRewards module or points-balance schema occurs in the corpus |
| fee-currency (holdout) | schema-8 has a 5.00 amount without a currency; USD in schema-2 is another module's sample and cannot establish this value |
| sourdough, jupiter, football, photosynthesis, submarine, beethoven | No matching subject or answer in the corpus; these are the six off-topic sanity controls |

Answerable controls are verified against schema-7 (SMTP/env, default constant,
template namespace/key), schema-6 (reuse constant, OPEN default), schema-10 (title
limit 200), and schema-8 (5.00 sample amount, collection expansion on save). The
compound email question intentionally has only a partial answer and must retain it.
The conversational additions reuse the audited retry, retention and submarine gaps.

## Decision

Use `[[NO_ANSWER]]` as the frozen system prompt's explicit refusal contract. A model
that cannot answer any part must emit only that token; a partial answer must state
the supported part and the missing part without the token. The prompt also prohibits
inferring that a feature does not exist merely because sources omit it.

The shared answer finalizer recognises the sentinel after removing a leading tagged
reasoning block, stray citation markers, whitespace, quotes and punctuation. It sets
`abstained=True`, uses the configured standard message, clears citations, preserves
retrieval and usage, and annotates `abstention_reason="model_declined"`. The policy
applies even with `require_citations=False`, and to native as well as parsed citations.
Streaming deltas remain provisional. The shipped UI already replaces them on
`AnswerComplete`; a Node-based test executes that client with split sentinel deltas
and verifies replacement and source removal. An interrupted stream emits no fabricated
completion.

Substantive text surrounding the token is preserved. This protects partial answers
and literal token mentions, including uncited answers when citations are optional.
Unmarked reasoning cannot be reliably distinguished from a partial answer with a
deterministic token parser; only explicitly tagged reasoning is removed. This is a
deliberately conservative limitation, not a semantic classifier.

After the sentinel-only development run missed three refusals, add a narrow prose
fallback: the entire visible response must match one of two explicit statements
that the sources do not specify/provide the requested information. Citation markers
are ignored, including doubled brackets. Multiple sentences, clause conjunctions,
quoted examples, application-level negative claims and substantive partial answers
are preserved. This deliberately misses more elaborate refusals; it is not a semantic
classifier. The prompt remains frozen. No extra model call is introduced.

No relevance threshold is added: the calibration below cannot recover the remaining
development failures without refusing answerable questions. The prompt's SHA-256 is now included in
evaluation configuration snapshots; comparison copies of the unchanged baseline have
the old prompt hash added from the recorded pre-change constant. Raw reports remain
untouched.

Add `false_abstention_rate` (and its `multi_turn_` counterpart) over successful
answerable observations, omitting it when there are none or generation did not run.
It is lower-is-better and uses ADR 0014's derived two-standard-error tolerance and
existing 0.005 floor, with the answerable denominator rather than the must-abstain
denominator. Both suites guard an abstention improvement paired with increased false
abstention. The gate's case attribution also treats a refusal of an answerable case
as a failure even when that case declares no expected-fact substrings.

The first sentinel schema process was launched before this reporting metric was
added. Its comparison copy is re-summarised from its untouched per-case records,
without another model call or any change to recorded abstention flags. Both raw
before reports likewise retain their original summaries. Reporting a new metric is
separate from changing the refusal policy.

### Alternatives

- Merely relabel cited prose refusals in the evaluator would improve a score without
  fixing the API, session history or UI. Recognition belongs in the answerer.
- An unrestricted substring search for the token would erase supported partial
  answers and quoted examples. Surrounding substantive text therefore wins.
- A broad prose-pattern detector risks treating valid negative answers as refusals;
  only whole-response patterns justified by the sentinel run are accepted.
- Another LLM call would add latency and another sampled decision on the hot path.
  There is no evidence justifying it yet.
- A guessed RRF cutoff would conflate rank fusion with answerability. The live
  submarine check returned five chunks at 0.015385–0.016393 with `min_score=0`.
  Retrieval settings remain unchanged.

## Measured results

The unchanged development slice has 77 cases (63 answerable, 14 must-abstain), excluding
the four held-out cases from inspection. It measured abstention 12/14 = 0.8571, false
abstention 0/63, fact match 0.7937, citation precision 0.8052, groundedness 1.0000 and
recall@5 0.9841. The two missed refusals were HTTP routes (an unsupported assertion
that none exist) and sourdough (a pure cited prose refusal).

The widened conversational baseline has 21 sessions / 54 turns, including six
must-abstain and 48 answerable turns. Abstention was 2/6 = 0.3333, false abstention
0/48, fact match 0.8864, citation precision 0.6719, groundedness 1.0000 and recall@5
0.9479. Three missed turns were straightforward cited refusals; the routes response
also suggested that no routes were exposed. Both runs had zero failed cases/turns.

### Sentinel-only diagnosis and fallback attribution

The sentinel-only development slice scored **11/14 = 0.7857**, false abstention
**0/63**, fact match **0.8254**, citation precision **0.8289**, groundedness **1.0000**
and recall **0.9841**. Failures were the unsupported HTTP-route claim, a multi-sentence
Liquid-snippet refusal with related background, and a one-sentence email-retry refusal.

Replaying those exact recorded completions through the deterministic fallback changes
only the retry refusal: **12/14 = 0.8571**, false abstention **0/63**, citation precision
**0.8400**, with fact match, groundedness and retrieval unchanged. This isolates the
fallback's recognition effect without generation noise. It is explicitly a replay,
not a fresh live run. The final full live runs compare with `--baseline` and include
conversation-history effects that a replay cannot reproduce.

The first sentinel conversational run was invalid for acceptance: two turns failed
with `UnknownSessionError` after a long machine-idle interval exceeded the existing
3600-second session TTL. Its 52 successful turns scored abstention **3/5 = 0.6000**,
false abstention **0/47**, fact match **0.8605**, citation precision **0.7193**,
groundedness **1.0000** and recall **0.9255**. Do not compare that five-case abstention
denominator directly with the six-case baseline as evidence of a gain. The final runs
retain the same TTL; their worker prevents automatic idle sleep during measurement.

The final prompt and detector were frozen before inspecting the four held-out outputs.
Only then was the full unchanged baseline revealed: **14/18 = 0.7778**, false abstention
**0/63**, fact match **0.7937**, citation precision **0.7470**, groundedness **1.0000**,
recall **0.9841**. Sentinel-only was **13/18 = 0.7222**, false abstention **0/63**,
fact match **0.8254**, citation precision **0.7683**, groundedness **1.0000**, recall
**0.9841**. Holdout inspection did not trigger any prompt or detector changes.

For attribution, the full schema comparison after the candidate was frozen is:

| Metric | Widened before | (a) Sentinel only | (b) Frozen-output fallback replay |
|---|---:|---:|---:|
| Abstention accuracy (18 cases) | 0.7778 | 0.7222 | 0.8333 |
| False abstention rate (63 answerable) | 0.0000 | 0.0000 | 0.0000 |
| Fact match (63 fact-bearing) | 0.7937 | 0.8254 | 0.8254 |
| Citation precision | 0.7470 | 0.7683 | 0.8289 |
| Groundedness | 1.0000 | 1.0000 | 1.0000 |
| Recall@5 (63 answerable) | 0.9841 | 0.9841 | 0.9841 |

The full replay adds the retry and held-out expiration refusals. It still misses
the currency refusal containing a decimal, the mixed Liquid-snippet response, and
the unsupported HTTP-route claim. No pattern was changed after discovering the
held-out decimal case. Conversational output is not replayed as though it were a
live result: changed refusals change subsequent history. Its final live repetitions
provide the comparison instead. Step (c) below makes no production change.

### Relevance calibration (development cases only)

Top-1 vector cosine was measured through the configured embedding model and vector
store, independently of hybrid RRF. The observed distributions were:

| Group | n | Minimum | Q1 | Median | Q3 | Maximum |
|---|---:|---:|---:|---:|---:|---:|
| Answerable | 63 | 0.6030 | 0.6693 | 0.6951 | 0.7174 | 0.8578 |
| Must abstain | 14 | 0.4023 | 0.4691 | 0.5336 | 0.6372 | 0.6899 |

The highest cutoff preserving every answerable case is **0.6030083**. It recovers
**zero** remaining failures: HTTP routes scores **0.6878589**, Liquid snippet
**0.6898959**. A cutoff high enough to reject either removes **26/63 answerable cases**.
That violates both the zero false-abstention baseline's **0.005** tolerance and the
retrieval one-case tolerance **1/63 = 0.0159**. No cutoff is deployed and the observed
cosine values are not copied into hybrid `min_score`, which uses a different scale.

### Final decision

Acceptance criteria are not met. No committed baseline is promoted.

### Schema: final repeated measurements

| Metric | Before | Final run 1 | Final run 2 | Spread | Gate n (run 1 / 2) | Tolerance (run 1 / 2) |
|---|---:|---:|---:|---:|---:|---:|
| abstention_accuracy | 0.7778 | 0.8333 | 0.8333 | 0.8333–0.8333 | 18 / 18 | 0.1960 / 0.1960 |
| false_abstention_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000–0.0000 | 63 / 63 | 0.0050 / 0.0050 |
| fact_match | 0.7937 | 0.7937 | 0.7937 | 0.7937–0.7937 | 63 / 63 | 0.1020 / 0.1020 |
| citation_precision | 0.7470 | 0.8333 | 0.8684 | 0.8333–0.8684 | 66 / 66 | 0.1070 / 0.1070 |
| groundedness | 1.0000 | 1.0000 | 1.0000 | 1.0000–1.0000 | 66 / 66 | 0.0050 / 0.0050 |
| recall@5 | 0.9841 | 0.9841 | 0.9841 | 0.9841–0.9841 | 63 / 63 | 0.0159 / 0.0159 |

Gates vs widened baseline: [True, True]


- before: 81 observations; 0 errors; 14/18 correct abstentions; 0/63 false abstentions. Citation precision counts: 62/83; groundedness: 83/83; citation gate n: 67 answered observations.
- run1: 81 observations; 0 errors; 15/18 correct abstentions; 0/63 false abstentions. Citation precision counts: 60/72; groundedness: 72/72; citation gate n: 66 answered observations.
- run2: 81 observations; 0 errors; 15/18 correct abstentions; 0/63 false abstentions. Citation precision counts: 66/76; groundedness: 76/76; citation gate n: 66 answered observations.

### Conversational: final repeated measurements

| Metric | Before | Final run 1 | Final run 2 | Spread | Gate n (run 1 / 2) | Tolerance (run 1 / 2) |
|---|---:|---:|---:|---:|---:|---:|
| multi_turn_abstention_accuracy | 0.3333 | 0.8333 | 0.8333 | 0.8333–0.8333 | 6 / 6 | 0.3849 / 0.3849 |
| multi_turn_false_abstention_rate | 0.0000 | 0.0000 | 0.0000 | 0.0000–0.0000 | 48 / 48 | 0.0050 / 0.0050 |
| multi_turn_fact_match | 0.8864 | 0.8409 | 0.8864 | 0.8409–0.8864 | 44 / 44 | 0.0957 / 0.0957 |
| multi_turn_citation_precision | 0.6719 | 0.8421 | 0.8036 | 0.8036–0.8421 | 49 / 49 | 0.1341 / 0.1341 |
| multi_turn_groundedness | 1.0000 | 1.0000 | 1.0000 | 1.0000–1.0000 | 49 / 49 | 0.0050 / 0.0050 |
| multi_turn_recall@5 | 0.9479 | 0.9479 | 0.9271 | 0.9271–0.9479 | 48 / 48 | 0.0208 / 0.0208 |

Gates vs widened baseline: [True, False]

- Run 2 blocking regression: `follow_up_lift` 0.1666 → 0.1111, tolerance 0.0476.
- Run 2 blocking regression: `follow_up_resolution` 0.9444 → 0.8889, tolerance 0.0476.
- Run 2 blocking regression: `multi_turn_mrr` 0.8767 → 0.8455, tolerance 0.0208.
- Run 2 blocking regression: `multi_turn_ndcg@5` 0.8896 → 0.8610, tolerance 0.0208.

| Context metric | Before | Final 1 | Final 2 |
|---|---:|---:|---:|
| follow_up_resolution | 0.9444 | 0.9444 | 0.8889 |
| follow_up_resolution_no_context | 0.7778 | 0.7778 | 0.7778 |
| follow_up_lift | 0.1666 | 0.1666 | 0.1111 |
| context_switch_recovery | 0.8571 | 0.8571 | 0.8571 |
| context_switch_recovery_no_context | 0.8571 | 0.8571 | 0.8571 |
| context_pollution | 0.0000 | 0.0000 | 0.0000 |
| session_isolation | 1.0000 | 1.0000 | 1.0000 |

- before: 54 observations; 0 errors; 2/6 correct abstentions; 0/48 false abstentions. Citation precision counts: 43/64; groundedness: 64/64; citation gate n: 52 answered observations.
- run1: 54 observations; 0 errors; 5/6 correct abstentions; 0/48 false abstentions. Citation precision counts: 48/57; groundedness: 57/57; citation gate n: 49 answered observations.
- run2: 54 observations; 0 errors; 5/6 correct abstentions; 0/48 false abstentions. Citation precision counts: 45/56; groundedness: 56/56; citation gate n: 49 answered observations.


Remaining misses are listed without changing their labels or the frozen detector:

- schema run 1: missed refusals abstain-http-routes, abstain-liquid-snippet-source, abstain-fee-currency; false refusals none.
- schema run 2: missed refusals abstain-http-routes, abstain-liquid-snippet-source, abstain-fee-currency; false refusals none.
- conversational run 1: missed refusals convo-abstain-after-relevant-history:3; false refusals none.
- conversational run 2: missed refusals convo-abstain-after-relevant-history:3; false refusals none.

Generation tolerances use `max(0.005, 2*sqrt(p*(1-p)/n))`, where `p` is the
widened before value and `n` is the successful contributing sample in that run.
Retrieval uses `max(0.005, 1/n)`. A schema refusal changes accuracy by 1/18
= 0.0556; a false refusal changes its rate by 1/63 = 0.0159. The corresponding
conversational units are 1/6 = 0.1667 and 1/48 = 0.0208 when no turn failed.
At a zero false-refusal baseline, the 0.005 floor rejects even one new false
refusal. Two repetitions describe observed spread, not population certainty.

The replay isolates recognition: it relabels explicit refusals already present
in the model output. The prompt changes model behaviour, but the independent
live samples cannot attribute every score change to that instruction. Removing
citations on recognised refusals also raises citation precision mechanically;
that is not proof of better citation selection on supported answers.

Existing committed baselines remain historical evidence. Their six-case
numbers are not the before measurement for this experiment. The original report commands saved complete JSON,
then exited nonzero because Windows' redirected console encoding rejected Unicode
report bars. Subsequent commands set `PYTHONIOENCODING=utf-8`; this was a presentation
failure, not an evaluation failure.

### Metric denominators

Citation precision and groundedness pool citation counts. Their inherited ADR 0014
gate uses the number of answered observations as its approximate sample size, not
the number of citations. The final tables label that value **Gate n** and report the
underlying citation numerators and denominators separately.

### Verification portability

The pre-change hermetic run found a Windows-only provenance failure: the filesystem
loader emitted backslashes for nested relative paths. Recording `.as_posix()` restores
its existing tested contract without changing corpus content or reindexing. The
Makefile now selects `Scripts` on Windows and `bin` elsewhere; `./osc` recognises the
Windows virtualenv launcher. GNU Make was downloaded into ignored local tooling;
no application dependency was added. Integration and E2E use dedicated test databases.

`make verify` reports **493 passed, one failed**. Ruff and strict mypy pass across
67 source files. The remaining failure is the unchanged live test
`test_the_streamed_and_buffered_paths_agree_on_abstention`: separate model calls
returned a sentinel and a cited prose refusal ("not addressed in the provided
sources"), respectively. Shared-policy unit tests pass, but model contract compliance
is not deterministic. The test was not weakened and the detector was not amended
after the holdout was opened. `make eval-gate` passes against the existing retrieval
baseline; latency warnings are non-blocking. This is not a green full verification.
