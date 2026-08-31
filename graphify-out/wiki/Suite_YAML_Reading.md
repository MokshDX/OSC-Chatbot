# Suite YAML Reading

> 9 nodes

## Key Concepts

- **load_conversational_set()** (10 connections) — `src/osc_assistant/evaluation/dataset.py`
- **_read_yaml_mapping()** (6 connections) — `src/osc_assistant/evaluation/dataset.py`
- **Path** (3 connections)
- **test_the_shipped_conversational_suite_is_valid()** (3 connections) — `tests/test_conversational_evaluation.py`
- **test_a_missing_conversational_set_names_the_file()** (2 connections) — `tests/test_conversational_evaluation.py`
- **Any** (1 connections)
- **Read a suite file, reporting the three ways it can fail to be one. Shared by…** (1 connections) — `src/osc_assistant/evaluation/dataset.py`
- **Read and validate a multi-turn golden set. Raises: EvaluationError: The file is…** (1 connections) — `src/osc_assistant/evaluation/dataset.py`
- **The suite the canonical command runs must load. A validation error here is a…** (1 connections) — `tests/test_conversational_evaluation.py`

## Relationships

- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (4 shared connections)
- [Trace Persistence](Trace_Persistence.md) (2 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (2 shared connections)
- [Document Loaders](Document_Loaders.md) (2 shared connections)

## Source Files

- `src/osc_assistant/evaluation/dataset.py`
- `tests/test_conversational_evaluation.py`

## Audit Trail

- EXTRACTED: 24 (86%)
- INFERRED: 4 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*