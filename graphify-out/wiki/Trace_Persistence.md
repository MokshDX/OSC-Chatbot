# Trace Persistence

> 17 nodes

## Key Concepts

- **load_golden_set()** (18 connections) — `src/osc_assistant/evaluation/dataset.py`
- **Path** (11 connections)
- **_write()** (8 connections) — `tests/test_evaluation.py`
- **test_a_valid_golden_set_loads()** (4 connections) — `tests/test_evaluation.py`
- **test_duplicate_case_ids_are_rejected()** (4 connections) — `tests/test_evaluation.py`
- **test_an_unscoreable_case_is_rejected_rather_than_scored_zero()** (4 connections) — `tests/test_evaluation.py`
- **test_an_abstention_case_may_not_also_name_relevant_documents()** (4 connections) — `tests/test_evaluation.py`
- **test_malformed_yaml_is_an_operator_message_not_a_traceback()** (4 connections) — `tests/test_evaluation.py`
- **test_an_empty_golden_set_is_rejected()** (4 connections) — `tests/test_evaluation.py`
- **test_the_shipped_schema_suite_is_valid_and_declares_its_corpus()** (4 connections) — `tests/test_evaluation.py`
- **test_the_preserved_faq_suite_still_loads()** (4 connections) — `tests/test_evaluation.py`
- **test_the_two_suites_are_scored_against_different_corpora()** (4 connections) — `tests/test_evaluation.py`
- **test_a_missing_golden_set_names_the_file()** (3 connections) — `tests/test_evaluation.py`
- **Read and validate a golden set file. Raises: EvaluationError: The file is…** (1 connections) — `src/osc_assistant/evaluation/dataset.py`
- **`make eval` runs this file; a validation error here is a broken gate. Cheap to…** (1 connections) — `tests/test_evaluation.py`
- **The FAQ suite is kept runnable, not just kept on disk. Deleting evaluation…** (1 connections) — `tests/test_evaluation.py`
- **Their numbers are not comparable, and the files say so themselves.** (1 connections) — `tests/test_evaluation.py`

## Relationships

- [Answer & Citation Types](Answer_%26_Citation_Types.md) (11 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (3 shared connections)
- [Suite YAML Reading](Suite_YAML_Reading.md) (2 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (2 shared connections)

## Source Files

- `src/osc_assistant/evaluation/dataset.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 80 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*