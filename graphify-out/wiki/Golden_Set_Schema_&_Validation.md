# Golden Set Schema & Validation

> 30 nodes

## Key Concepts

- **runner.py** (30 connections) — `src/osc_assistant/evaluation/runner.py`
- **evaluation/__init__.py** (16 connections) — `src/osc_assistant/evaluation/__init__.py`
- **GoldenCase** (14 connections) — `src/osc_assistant/evaluation/dataset.py`
- **CaseResult** (13 connections) — `src/osc_assistant/evaluation/runner.py`
- **summarise()** (10 connections) — `src/osc_assistant/evaluation/runner.py`
- **document_key()** (8 connections) — `src/osc_assistant/evaluation/dataset.py`
- **._score_retrieval()** (7 connections) — `src/osc_assistant/evaluation/runner.py`
- **._score_answer()** (7 connections) — `src/osc_assistant/evaluation/runner.py`
- **compare()** (7 connections) — `src/osc_assistant/evaluation/runner.py`
- **._evaluate_case()** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **._unique_ids()** (3 connections) — `src/osc_assistant/evaluation/dataset.py`
- **test_document_key_prefers_the_corpus_relative_path()** (3 connections) — `tests/test_evaluation.py`
- **test_summarise_excludes_failed_cases_from_quality_means()** (3 connections) — `tests/test_evaluation.py`
- **test_summarise_scores_abstention_only_over_abstention_cases()** (3 connections) — `tests/test_evaluation.py`
- **BaseModel** (2 connections)
- **._check_expectations()** (2 connections) — `src/osc_assistant/evaluation/dataset.py`
- **field_validator** (2 connections)
- **._normalise_paths()** (2 connections) — `src/osc_assistant/evaluation/dataset.py`
- **.scored()** (2 connections) — `src/osc_assistant/evaluation/runner.py`
- **_ratio()** (2 connections) — `src/osc_assistant/evaluation/runner.py`
- **test_compare_only_diffs_metrics_present_in_both_runs()** (2 connections) — `tests/test_evaluation.py`
- **Measurement for the retrieval and generation stack. The project's rule is that…** (1 connections) — `src/osc_assistant/evaluation/__init__.py`
- **model_validator** (1 connections)
- **The identity a golden set refers to a retrieved chunk's document by.…** (1 connections) — `src/osc_assistant/evaluation/dataset.py`
- **One question and what a correct system does with it.** (1 connections) — `src/osc_assistant/evaluation/dataset.py`
- *... and 5 more nodes in this community*

## Relationships

- [Evaluation CLI Command](Evaluation_CLI_Command.md) (20 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (11 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (7 shared connections)
- [Retrieval Metrics](Retrieval_Metrics.md) (5 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (4 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Settings Schema](Settings_Schema.md) (2 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (2 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (2 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/__init__.py`
- `src/osc_assistant/evaluation/dataset.py`
- `src/osc_assistant/evaluation/runner.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 146 (96%)
- INFERRED: 6 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*