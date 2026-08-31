# Summarisation & Case Scoring

> 14 nodes

## Key Concepts

- **CaseResult** (10 connections) — `src/osc_assistant/evaluation/runner.py`
- **summarise()** (10 connections) — `src/osc_assistant/evaluation/runner.py`
- **._score_retrieval()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **._score_answer()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **._evaluate_case()** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **test_summarise_excludes_failed_cases_from_quality_means()** (3 connections) — `tests/test_evaluation.py`
- **test_summarise_scores_abstention_only_over_abstention_cases()** (3 connections) — `tests/test_evaluation.py`
- **GoldenCase** (3 connections)
- **.scored()** (2 connections) — `src/osc_assistant/evaluation/runner.py`
- **Answer** (1 connections)
- **ScoredChunk** (1 connections)
- **Everything one golden case produced, scored. Kept flat and JSON-serialisable on…** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **Whether this case contributed a measurement rather than an error.** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **Aggregate per-case results into the numbers a run is judged on. Two exclusions…** (1 connections) — `src/osc_assistant/evaluation/runner.py`

## Relationships

- [Answer & Citation Types](Answer_%26_Citation_Types.md) (5 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (3 shared connections)
- [OpenAI-Compatible Provider](OpenAI-Compatible_Provider.md) (3 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (1 shared connections)
- [Report Comparison](Report_Comparison.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/runner.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 53 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*