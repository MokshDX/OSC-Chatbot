# OpenAI-Compatible Provider

> 32 nodes

## Key Concepts

- **TurnResult** (15 connections) — `src/osc_assistant/evaluation/conversational.py`
- **summarise_conversation()** (15 connections) — `src/osc_assistant/evaluation/conversational.py`
- **._evaluate_turn()** (7 connections) — `src/osc_assistant/evaluation/conversational.py`
- **._score()** (6 connections) — `src/osc_assistant/evaluation/conversational.py`
- **._evaluate_case()** (5 connections) — `src/osc_assistant/evaluation/conversational.py`
- **._add_control()** (5 connections) — `src/osc_assistant/evaluation/conversational.py`
- **mean()** (5 connections) — `src/osc_assistant/evaluation/metrics.py`
- **test_follow_up_lift_is_the_difference_between_the_pair()** (4 connections) — `tests/test_conversational_evaluation.py`
- **test_a_negative_lift_is_reported_rather_than_clamped()** (4 connections) — `tests/test_conversational_evaluation.py`
- **test_context_pollution_measures_falling_below_the_cold_control()** (4 connections) — `tests/test_conversational_evaluation.py`
- **test_beating_the_control_on_a_switch_is_not_negative_pollution()** (4 connections) — `tests/test_conversational_evaluation.py`
- **test_failed_turns_are_excluded_from_quality_means()** (4 connections) — `tests/test_conversational_evaluation.py`
- **_session_isolation()** (4 connections) — `src/osc_assistant/evaluation/conversational.py`
- **ratio()** (4 connections) — `src/osc_assistant/evaluation/metrics.py`
- **percentile()** (4 connections) — `src/osc_assistant/evaluation/metrics.py`
- **ConversationalCase** (3 connections)
- **ConversationalTurn** (3 connections)
- **Answer** (1 connections)
- **The lift must come from the two measurements, not from the in-session one.…** (1 connections) — `tests/test_conversational_evaluation.py`
- **The conversation making retrieval *worse* is a real outcome. Clamping it to…** (1 connections) — `tests/test_conversational_evaluation.py`
- **For a context switch the control is the benchmark to match, not to beat.** (1 connections) — `tests/test_conversational_evaluation.py`
- **Pollution is floored at zero: doing better than cold is not "negative harm".** (1 connections) — `tests/test_conversational_evaluation.py`
- **Averaging a provider timeout in as a zero lets an outage read as a regression.** (1 connections) — `tests/test_conversational_evaluation.py`
- **.scored()** (1 connections) — `src/osc_assistant/evaluation/conversational.py`
- **One scored turn. Flat and JSON-serialisable, like `CaseResult`.** (1 connections) — `src/osc_assistant/evaluation/conversational.py`
- *... and 7 more nodes in this community*

## Relationships

- [Document Loaders](Document_Loaders.md) (9 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (5 shared connections)
- [Pure Metric Functions](Pure_Metric_Functions.md) (3 shared connections)
- [Summarisation & Case Scoring](Summarisation_%26_Case_Scoring.md) (3 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (2 shared connections)
- [Conversational Report Shape](Conversational_Report_Shape.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/conversational.py`
- `src/osc_assistant/evaluation/metrics.py`
- `tests/test_conversational_evaluation.py`

## Audit Trail

- EXTRACTED: 91 (82%)
- INFERRED: 20 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*