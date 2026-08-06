# Golden Set Loading & Evaluation Tests

> 25 nodes · cohesion 0.14

## Key Concepts

- **test_evaluation.py** (53 connections) — `tests/test_evaluation.py`
- **load_golden_set()** (15 connections) — `src/osc_assistant/evaluation/dataset.py`
- **Path** (8 connections)
- **_write()** (8 connections) — `tests/test_evaluation.py`
- **test_a_valid_golden_set_loads()** (4 connections) — `tests/test_evaluation.py`
- **test_an_abstention_case_may_not_also_name_relevant_documents()** (4 connections) — `tests/test_evaluation.py`
- **test_an_empty_golden_set_is_rejected()** (4 connections) — `tests/test_evaluation.py`
- **test_an_unscoreable_case_is_rejected_rather_than_scored_zero()** (4 connections) — `tests/test_evaluation.py`
- **test_duplicate_case_ids_are_rejected()** (4 connections) — `tests/test_evaluation.py`
- **test_malformed_yaml_is_an_operator_message_not_a_traceback()** (4 connections) — `tests/test_evaluation.py`
- **test_a_missing_golden_set_names_the_file()** (3 connections) — `tests/test_evaluation.py`
- **test_document_key_prefers_the_corpus_relative_path()** (3 connections) — `tests/test_evaluation.py`
- **test_verdict_parsing_checks_unsupported_first_because_it_contains_supported()** (3 connections) — `tests/test_evaluation.py`
- **Path** (1 connections)
- **Read and validate a golden set file. Raises: EvaluationError: The file is…** (1 connections) — `src/osc_assistant/evaluation/dataset.py`
- **parametrize** (1 connections)
- **Evaluation harness tests. The harness is the instrument every future retrieval…** (1 connections) — `tests/test_evaluation.py`
- **test_dedupe_preserves_rank_order_and_drops_repeats()** (1 connections) — `tests/test_evaluation.py`
- **test_hit_is_the_binary_form_of_recall()** (1 connections) — `tests/test_evaluation.py`
- **test_mean_of_nothing_is_zero_so_an_empty_run_stays_reportable()** (1 connections) — `tests/test_evaluation.py`
- **test_percentile_returns_an_observed_value_not_an_interpolation()** (1 connections) — `tests/test_evaluation.py`
- **test_precision_divides_by_k_not_by_results_returned()** (1 connections) — `tests/test_evaluation.py`
- **test_recall_counts_relevant_documents_found_within_k()** (1 connections) — `tests/test_evaluation.py`
- **test_recall_of_a_case_with_no_relevant_documents_is_zero_not_undefined()** (1 connections) — `tests/test_evaluation.py`
- **test_reciprocal_rank_is_the_inverse_of_the_first_relevant_position()** (1 connections) — `tests/test_evaluation.py`

## Relationships

- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (11 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (10 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (3 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (3 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (2 shared connections)
- [Noop Reranker & Evaluation Corpus](Noop_Reranker_%26_Evaluation_Corpus.md) (2 shared connections)
- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (1 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (1 shared connections)
- [Generation Package & Prompts](Generation_Package_%26_Prompts.md) (1 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (1 shared connections)
- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (1 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/dataset.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 129 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*