# Document Loaders

> 32 nodes

## Key Concepts

- **test_conversational_evaluation.py** (30 connections) — `tests/test_conversational_evaluation.py`
- **ConversationalEvaluator** (19 connections) — `src/osc_assistant/evaluation/conversational.py`
- **GenerationSettings** (17 connections) — `src/osc_assistant/settings.py`
- **evaluator()** (11 connections) — `tests/test_conversational_evaluation.py`
- **test_a_failing_provider_costs_one_turn_not_the_whole_run()** (11 connections) — `tests/test_conversational_evaluation.py`
- **test_a_failed_turn_still_releases_its_session()** (11 connections) — `tests/test_conversational_evaluation.py`
- **_set()** (9 connections) — `tests/test_conversational_evaluation.py`
- **_settings()** (7 connections) — `tests/test_conversational_evaluation.py`
- **.__init__()** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **Document** (4 connections)
- **test_a_turn_records_the_context_it_was_answered_against()** (4 connections) — `tests/test_conversational_evaluation.py`
- **test_a_control_run_happens_only_for_the_turns_that_need_one()** (4 connections) — `tests/test_conversational_evaluation.py`
- **corpus()** (3 connections) — `tests/test_conversational_evaluation.py`
- **StubEmbeddingModel** (3 connections)
- **test_every_turn_of_a_case_is_scored()** (3 connections) — `tests/test_conversational_evaluation.py`
- **test_the_configuration_travels_with_the_numbers()** (3 connections) — `tests/test_conversational_evaluation.py`
- **test_a_report_round_trips_to_a_serialisable_dict()** (3 connections) — `tests/test_conversational_evaluation.py`
- **fixture** (2 connections)
- **test_a_case_needs_at_least_two_turns()** (2 connections) — `tests/test_conversational_evaluation.py`
- **test_an_opening_turn_may_not_require_context()** (2 connections) — `tests/test_conversational_evaluation.py`
- **test_a_turn_cannot_both_depend_on_and_be_independent_of_the_conversation()** (2 connections) — `tests/test_conversational_evaluation.py`
- **test_an_unscoreable_turn_is_rejected_rather_than_scored_zero()** (1 connections) — `tests/test_conversational_evaluation.py`
- **test_duplicate_case_ids_are_rejected()** (1 connections) — `tests/test_conversational_evaluation.py`
- **Multi-turn evaluation tests. The conversational harness has one property that…** (1 connections) — `tests/test_conversational_evaluation.py`
- **A one-turn "conversation" belongs in the single-turn suite.** (1 connections) — `tests/test_conversational_evaluation.py`
- *... and 7 more nodes in this community*

## Relationships

- [OpenAI-Compatible Provider](OpenAI-Compatible_Provider.md) (9 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (5 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (5 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (4 shared connections)
- [Generation & Abstention Metrics](Generation_%26_Abstention_Metrics.md) (4 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (3 shared connections)
- [StoreInspector Protocol](StoreInspector_Protocol.md) (3 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (2 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (2 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [Suite YAML Reading](Suite_YAML_Reading.md) (2 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (2 shared connections)

## Source Files

- `src/osc_assistant/evaluation/conversational.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/settings.py`
- `tests/test_conversational_evaluation.py`

## Audit Trail

- EXTRACTED: 161 (98%)
- INFERRED: 4 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*