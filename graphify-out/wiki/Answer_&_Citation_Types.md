# Answer & Citation Types

> 36 nodes

## Key Concepts

- **test_evaluation.py** (51 connections) — `tests/test_evaluation.py`
- **Evaluator** (19 connections) — `src/osc_assistant/evaluation/runner.py`
- **_settings()** (12 connections) — `tests/test_evaluation.py`
- **RetrievalPipeline** (10 connections)
- **_golden()** (9 connections) — `tests/test_evaluation.py`
- **test_a_judge_failure_records_no_verdict_rather_than_a_wrong_one()** (7 connections) — `tests/test_evaluation.py`
- **test_a_retrieval_only_run_reports_no_generation_metrics()** (6 connections) — `tests/test_evaluation.py`
- **test_a_generation_run_scores_citations_against_what_was_retrieved()** (6 connections) — `tests/test_evaluation.py`
- **test_a_missing_expected_fact_is_named_not_just_counted()** (6 connections) — `tests/test_evaluation.py`
- **test_the_judge_sees_the_passages_the_answer_was_built_from()** (6 connections) — `tests/test_evaluation.py`
- **test_a_retrieval_run_scores_the_documents_it_found()** (5 connections) — `tests/test_evaluation.py`
- **test_the_configuration_that_produced_the_numbers_travels_with_them()** (5 connections) — `tests/test_evaluation.py`
- **test_a_failing_provider_costs_one_case_not_the_whole_run()** (4 connections) — `tests/test_evaluation.py`
- **test_concurrency_does_not_change_the_result()** (4 connections) — `tests/test_evaluation.py`
- **test_verdict_parsing_checks_unsupported_first_because_it_contains_supported()** (2 connections) — `tests/test_evaluation.py`
- **test_ndcg_separates_two_rankings_that_recall_and_mrr_cannot()** (2 connections) — `tests/test_evaluation.py`
- **test_ndcg_normalises_against_an_ideal_capped_at_k()** (2 connections) — `tests/test_evaluation.py`
- **test_ndcg_discounts_by_position_not_by_count()** (2 connections) — `tests/test_evaluation.py`
- **parametrize** (1 connections)
- **test_dedupe_preserves_rank_order_and_drops_repeats()** (1 connections) — `tests/test_evaluation.py`
- **test_recall_counts_relevant_documents_found_within_k()** (1 connections) — `tests/test_evaluation.py`
- **test_recall_of_a_case_with_no_relevant_documents_is_zero_not_undefined()** (1 connections) — `tests/test_evaluation.py`
- **test_precision_divides_by_k_not_by_results_returned()** (1 connections) — `tests/test_evaluation.py`
- **test_reciprocal_rank_is_the_inverse_of_the_first_relevant_position()** (1 connections) — `tests/test_evaluation.py`
- **test_hit_is_the_binary_form_of_recall()** (1 connections) — `tests/test_evaluation.py`
- *... and 11 more nodes in this community*

## Relationships

- [Trace Persistence](Trace_Persistence.md) (11 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (5 shared connections)
- [Summarisation & Case Scoring](Summarisation_%26_Case_Scoring.md) (5 shared connections)
- [Generation & Abstention Metrics](Generation_%26_Abstention_Metrics.md) (4 shared connections)
- [Evaluation Test Fixtures](Evaluation_Test_Fixtures.md) (3 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (3 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (2 shared connections)
- [Report Comparison](Report_Comparison.md) (2 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/runner.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 172 (98%)
- INFERRED: 4 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*