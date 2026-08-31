# Session Memory Tests

> 19 nodes

## Key Concepts

- **gate.py** (18 connections) — `src/osc_assistant/evaluation/gate.py`
- **scored_records()** (8 connections) — `src/osc_assistant/evaluation/metrics.py`
- **numeric_summary()** (7 connections) — `src/osc_assistant/evaluation/metrics.py`
- **_judge_metric()** (6 connections) — `src/osc_assistant/evaluation/gate.py`
- **_outcomes()** (6 connections) — `src/osc_assistant/evaluation/gate.py`
- **_CaseOutcome** (5 connections) — `src/osc_assistant/evaluation/gate.py`
- **_sample_size()** (5 connections) — `src/osc_assistant/evaluation/gate.py`
- **_tolerance_for()** (4 connections) — `src/osc_assistant/evaluation/gate.py`
- **_regressed_cases()** (4 connections) — `src/osc_assistant/evaluation/gate.py`
- **Any** (2 connections)
- **Severity** (1 connections)
- **The regression gate: does this run still clear the trusted baseline? `--fail-…** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **The comparable skeleton of one case or turn, from either report shape.** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **Derive this metric's tolerance, its severity, and the sentence explaining both.** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **How many cases actually contributed to `name`. Using the suite size for…** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **Reduce per-case records to what a regression diff needs. Keyed by case id, or…** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **Cases that were right before and are wrong now, and the categories they span.…** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **The numeric entries of a result file's `summary`, as floats. Booleans are…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **The per-case records of a result file that actually produced a measurement.…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`

## Relationships

- [Golden Case Validators](Golden_Case_Validators.md) (7 shared connections)
- [Provider Registration & Embeddings](Provider_Registration_%26_Embeddings.md) (6 shared connections)
- [Reranker & Retrieval Settings](Reranker_%26_Retrieval_Settings.md) (5 shared connections)
- [Pure Metric Functions](Pure_Metric_Functions.md) (3 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/gate.py`
- `src/osc_assistant/evaluation/metrics.py`

## Audit Trail

- EXTRACTED: 74 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*