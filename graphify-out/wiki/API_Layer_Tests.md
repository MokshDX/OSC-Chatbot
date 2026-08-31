# API Layer Tests

> 54 nodes

## Key Concepts

- **test_api.py** (39 connections) — `tests/test_api.py`
- **TestClient** (27 connections)
- **_settings()** (7 connections) — `tests/test_api.py`
- **_development_client()** (7 connections) — `tests/test_api.py`
- **client()** (6 connections) — `tests/test_api.py`
- **_register_stub_providers()** (4 connections) — `tests/test_api.py`
- **Document** (4 connections)
- **test_malformed_requests_are_rejected()** (4 connections) — `tests/test_api.py`
- **test_health_reports_the_active_components()** (3 connections) — `tests/test_api.py`
- **test_ui_is_served_at_the_root()** (3 connections) — `tests/test_api.py`
- **test_chat_streams_sources_then_deltas_then_completion()** (3 connections) — `tests/test_api.py`
- **_parse_sse()** (3 connections) — `tests/test_api.py`
- **test_status_reports_what_is_indexed()** (3 connections) — `tests/test_api.py`
- **test_an_answer_carries_the_id_of_the_trace_that_produced_it()** (3 connections) — `tests/test_api.py`
- **test_traces_are_not_exposed_outside_development()** (3 connections) — `tests/test_api.py`
- **test_traces_are_listable_and_expandable_in_development()** (3 connections) — `tests/test_api.py`
- **test_an_unknown_trace_id_is_a_404()** (3 connections) — `tests/test_api.py`
- **test_every_response_carries_a_correlation_id()** (3 connections) — `tests/test_api.py`
- **test_closing_a_session_twice_is_not_an_error()** (3 connections) — `tests/test_api.py`
- **test_a_follow_up_in_a_session_is_answered_with_the_previous_turn()** (3 connections) — `tests/test_api.py`
- **test_a_question_with_no_session_carries_no_context()** (3 connections) — `tests/test_api.py`
- **test_a_closed_session_is_a_404_on_the_next_turn()** (3 connections) — `tests/test_api.py`
- **test_an_unknown_session_is_a_404_on_the_streaming_path_too()** (3 connections) — `tests/test_api.py`
- **test_supplying_both_a_session_and_a_history_is_rejected()** (3 connections) — `tests/test_api.py`
- **test_a_streamed_session_turn_is_remembered()** (3 connections) — `tests/test_api.py`
- *... and 29 more nodes in this community*

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (3 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (3 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (2 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)
- [Generation & Abstention Metrics](Generation_%26_Abstention_Metrics.md) (1 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (1 shared connections)
- [Document Loaders](Document_Loaders.md) (1 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (1 shared connections)

## Source Files

- `tests/test_api.py`

## Audit Trail

- EXTRACTED: 186 (98%)
- INFERRED: 3 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*