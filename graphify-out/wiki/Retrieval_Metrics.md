# Retrieval Metrics

> 19 nodes

## Key Concepts

- **metrics.py** (9 connections) — `src/osc_assistant/evaluation/metrics.py`
- **mean_of()** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **mean()** (4 connections) — `src/osc_assistant/evaluation/metrics.py`
- **percentile()** (3 connections) — `src/osc_assistant/evaluation/metrics.py`
- **dedupe()** (2 connections) — `src/osc_assistant/evaluation/metrics.py`
- **recall_at_k()** (2 connections) — `src/osc_assistant/evaluation/metrics.py`
- **precision_at_k()** (2 connections) — `src/osc_assistant/evaluation/metrics.py`
- **reciprocal_rank()** (2 connections) — `src/osc_assistant/evaluation/metrics.py`
- **hit_at_k()** (2 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Retrieval and generation metrics. Every function here is pure: same inputs,…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Collapse repeats while preserving rank order. Retrieval returns chunks and…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Fraction of the relevant documents that appear in the top `k`. The headline…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Fraction of the top `k` results that are relevant. Divided by `k` rather than…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **1 / (rank of the first relevant result), or 0.0 if none is present. Averaged…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Whether any relevant document appears in the top `k`. The binary form of…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Arithmetic mean, defined as 0.0 on an empty sequence. Returning 0.0 rather than…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **Nearest-rank percentile of `values`. Nearest-rank rather than interpolated:…** (1 connections) — `src/osc_assistant/evaluation/metrics.py`
- **T** (1 connections)
- **Mean of `extract` over `items`, rounded, and 0.0 when there are none.** (1 connections) — `src/osc_assistant/evaluation/runner.py`

## Relationships

- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (5 shared connections)

## Source Files

- `src/osc_assistant/evaluation/metrics.py`
- `src/osc_assistant/evaluation/runner.py`

## Audit Trail

- EXTRACTED: 41 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*