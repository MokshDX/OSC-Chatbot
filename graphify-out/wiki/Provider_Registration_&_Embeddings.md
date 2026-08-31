# Provider Registration & Embeddings

> 43 nodes

## Key Concepts

- **evaluate_gate()** (32 connections) — `src/osc_assistant/evaluation/gate.py`
- **test_gate.py** (25 connections) — `tests/test_gate.py`
- **_report()** (22 connections) — `tests/test_gate.py`
- **_cases()** (8 connections) — `tests/test_gate.py`
- **test_a_smaller_sample_earns_a_wider_tolerance()** (5 connections) — `tests/test_gate.py`
- **test_precision_bought_with_recall_is_blocked()** (5 connections) — `tests/test_gate.py`
- **test_a_regression_names_the_cases_that_changed()** (5 connections) — `tests/test_gate.py`
- **test_the_report_serialises_with_its_reasoning_intact()** (5 connections) — `tests/test_gate.py`
- **test_a_deterministic_metric_tolerates_less_than_one_case()** (4 connections) — `tests/test_gate.py`
- **test_a_deterministic_metric_fails_when_more_than_one_case_is_lost()** (4 connections) — `tests/test_gate.py`
- **test_the_tolerance_rationale_explains_where_the_number_came_from()** (4 connections) — `tests/test_gate.py`
- **test_a_sampled_metric_tolerates_movement_inside_two_standard_errors()** (4 connections) — `tests/test_gate.py`
- **test_latency_is_reported_but_never_blocking()** (4 connections) — `tests/test_gate.py`
- **test_a_faster_run_is_an_improvement_not_a_regression()** (4 connections) — `tests/test_gate.py`
- **test_context_pollution_is_read_as_lower_is_better()** (4 connections) — `tests/test_gate.py`
- **test_an_honest_improvement_is_not_flagged_as_a_trade_off()** (4 connections) — `tests/test_gate.py`
- **test_counts_and_totals_are_not_gated()** (4 connections) — `tests/test_gate.py`
- **test_only_metrics_present_in_both_runs_are_compared()** (4 connections) — `tests/test_gate.py`
- **test_configuration_differences_are_surfaced()** (4 connections) — `tests/test_gate.py`
- **Any** (3 connections)
- **test_a_sampled_metric_fails_on_movement_outside_the_interval()** (3 connections) — `tests/test_gate.py`
- **_abstention_cases()** (3 connections) — `tests/test_gate.py`
- **test_latency_uses_a_relative_tolerance()** (3 connections) — `tests/test_gate.py`
- **test_abstaining_more_to_raise_abstention_accuracy_is_blocked()** (3 connections) — `tests/test_gate.py`
- **test_an_unchanged_run_passes_with_nothing_to_report()** (3 connections) — `tests/test_gate.py`
- *... and 18 more nodes in this community*

## Relationships

- [Session Memory Tests](Session_Memory_Tests.md) (6 shared connections)
- [Golden Case Validators](Golden_Case_Validators.md) (4 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (2 shared connections)

## Source Files

- `src/osc_assistant/evaluation/gate.py`
- `tests/test_gate.py`

## Audit Trail

- EXTRACTED: 188 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*