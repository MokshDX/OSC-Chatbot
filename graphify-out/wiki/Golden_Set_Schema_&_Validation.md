# Golden Set Schema & Validation

> 39 nodes · cohesion 0.09

## Key Concepts

- **runner.py** (30 connections) — `src/osc_assistant/evaluation/runner.py`
- **GoldenSet** (17 connections) — `src/osc_assistant/evaluation/dataset.py`
- **evaluation/__init__.py** (16 connections) — `src/osc_assistant/evaluation/__init__.py`
- **GoldenCase** (14 connections) — `src/osc_assistant/evaluation/dataset.py`
- **dataset.py** (13 connections) — `src/osc_assistant/evaluation/dataset.py`
- **CaseResult** (13 connections) — `src/osc_assistant/evaluation/runner.py`
- **summarise()** (10 connections) — `src/osc_assistant/evaluation/runner.py`
- **document_key()** (8 connections) — `src/osc_assistant/evaluation/dataset.py`
- **unresolvable_documents()** (7 connections) — `src/osc_assistant/evaluation/dataset.py`
- **._score_answer()** (7 connections) — `src/osc_assistant/evaluation/runner.py`
- **._score_retrieval()** (7 connections) — `src/osc_assistant/evaluation/runner.py`
- **configuration_snapshot()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **.run()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **._evaluate_case()** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **._unique_ids()** (3 connections) — `src/osc_assistant/evaluation/dataset.py`
- **test_summarise_excludes_failed_cases_from_quality_means()** (3 connections) — `tests/test_evaluation.py`
- **test_summarise_scores_abstention_only_over_abstention_cases()** (3 connections) — `tests/test_evaluation.py`
- **field_validator** (2 connections)
- **._check_expectations()** (2 connections) — `src/osc_assistant/evaluation/dataset.py`
- **._normalise_paths()** (2 connections) — `src/osc_assistant/evaluation/dataset.py`
- **.referenced_documents()** (2 connections) — `src/osc_assistant/evaluation/dataset.py`
- **BaseModel** (2 connections)
- **.scored()** (2 connections) — `src/osc_assistant/evaluation/runner.py`
- **_ratio()** (2 connections) — `src/osc_assistant/evaluation/runner.py`
- **test_unresolvable_documents_finds_a_mistyped_path()** (2 connections) — `tests/test_evaluation.py`
- *... and 14 more nodes in this community*

## Relationships

- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (14 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (12 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (10 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (8 shared connections)
- [Evaluation Metrics](Evaluation_Metrics.md) (5 shared connections)
- [Evaluation Run Comparison](Evaluation_Run_Comparison.md) (3 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (2 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (2 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (1 shared connections)
- [Logging Subsystem Core](Logging_Subsystem_Core.md) (1 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/__init__.py`
- `src/osc_assistant/evaluation/dataset.py`
- `src/osc_assistant/evaluation/runner.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 189 (95%)
- INFERRED: 9 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*