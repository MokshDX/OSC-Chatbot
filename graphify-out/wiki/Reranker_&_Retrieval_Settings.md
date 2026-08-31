# Reranker & Retrieval Settings

> 23 nodes

## Key Concepts

- **report.py** (19 connections) — `src/osc_assistant/evaluation/report.py`
- **render_report()** (15 connections) — `src/osc_assistant/evaluation/report.py`
- **_render_categories()** (8 connections) — `src/osc_assistant/evaluation/report.py`
- **Any** (7 connections)
- **Console** (7 connections)
- **_render_scorecard()** (6 connections) — `src/osc_assistant/evaluation/report.py`
- **_render_gate()** (6 connections) — `src/osc_assistant/evaluation/report.py`
- **_render_header()** (5 connections) — `src/osc_assistant/evaluation/report.py`
- **_render_worst_cases()** (5 connections) — `src/osc_assistant/evaluation/report.py`
- **_bar()** (5 connections) — `src/osc_assistant/evaluation/report.py`
- **_render_errors()** (4 connections) — `src/osc_assistant/evaluation/report.py`
- **_fact_match()** (4 connections) — `src/osc_assistant/evaluation/report.py`
- **_format()** (3 connections) — `src/osc_assistant/evaluation/report.py`
- **_mean()** (3 connections) — `src/osc_assistant/evaluation/report.py`
- **_is_bounded()** (2 connections) — `src/osc_assistant/evaluation/report.py`
- **Renders an evaluation run as the quality report. Separate from `runner` and…** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **Print the full quality report for one run.** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **Every metric, grouped by concern, with a bar where a bar means something.** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **Per-tag performance, worst first. This is the section that turns a score into…** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **The individual cases that scored worst, with their trace ids. Abstention cases…** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **Regressions and improvements, each with the tolerance that judged it.** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **A proportional bar, but only for metrics that are proportions. Latency and…** (1 connections) — `src/osc_assistant/evaluation/report.py`
- **Fact match over the records that actually expect a fact. `None` rather than 0.0…** (1 connections) — `src/osc_assistant/evaluation/report.py`

## Relationships

- [Session Memory Tests](Session_Memory_Tests.md) (5 shared connections)
- [Golden Case Validators](Golden_Case_Validators.md) (4 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (3 shared connections)
- [Pure Metric Functions](Pure_Metric_Functions.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/report.py`

## Audit Trail

- EXTRACTED: 107 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*