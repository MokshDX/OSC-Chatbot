# Evaluation Run Comparison

> 6 nodes · cohesion 0.33

## Key Concepts

- **compare()** (7 connections) — `src/osc_assistant/evaluation/runner.py`
- **.to_dict()** (3 connections) — `src/osc_assistant/evaluation/runner.py`
- **Any** (3 connections)
- **test_compare_only_diffs_metrics_present_in_both_runs()** (2 connections) — `tests/test_evaluation.py`
- **The on-disk shape. Stable, because baselines are compared against it.** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **Metrics present in both runs, as (name, baseline, current). Only the…** (1 connections) — `src/osc_assistant/evaluation/runner.py`

## Relationships

- [Evaluation CLI Command](Evaluation_CLI_Command.md) (3 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (3 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/runner.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 17 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*