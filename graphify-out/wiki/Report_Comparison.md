# Report Comparison

> 11 nodes

## Key Concepts

- **.run()** (6 connections) — `src/osc_assistant/evaluation/runner.py`
- **EvaluationReport** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **compare()** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **Any** (3 connections)
- **.to_dict()** (3 connections) — `src/osc_assistant/evaluation/runner.py`
- **test_compare_only_diffs_metrics_present_in_both_runs()** (2 connections) — `tests/test_evaluation.py`
- **GoldenSet** (1 connections)
- **One evaluation run: what was measured, under what configuration.** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **The on-disk shape. Stable, because baselines are compared against it.** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **Score every case in `golden`, at most `concurrency` at a time.** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **Metrics present in both runs, as (name, baseline, current). Only the…** (1 connections) — `src/osc_assistant/evaluation/runner.py`

## Relationships

- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (4 shared connections)
- [Answer & Citation Types](Answer_%26_Citation_Types.md) (2 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (2 shared connections)
- [Summarisation & Case Scoring](Summarisation_%26_Case_Scoring.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/runner.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 29 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*