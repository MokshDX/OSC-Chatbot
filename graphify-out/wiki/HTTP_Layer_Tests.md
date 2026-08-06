# HTTP Layer Tests

> 38 nodes · cohesion 0.09

## Key Concepts

- **test_api.py** (30 connections) — `tests/test_api.py`
- **TestClient** (18 connections)
- **_development_client()** (6 connections) — `tests/test_api.py`
- **client()** (5 connections) — `tests/test_api.py`
- **Document** (4 connections)
- **_settings()** (4 connections) — `tests/test_api.py`
- **test_malformed_requests_are_rejected()** (4 connections) — `tests/test_api.py`
- **_parse_sse()** (3 connections) — `tests/test_api.py`
- **_register_stub_providers()** (3 connections) — `tests/test_api.py`
- **test_an_answer_carries_the_id_of_the_trace_that_produced_it()** (3 connections) — `tests/test_api.py`
- **test_an_unknown_trace_id_is_a_404()** (3 connections) — `tests/test_api.py`
- **test_chat_streams_sources_then_deltas_then_completion()** (3 connections) — `tests/test_api.py`
- **test_every_response_carries_a_correlation_id()** (3 connections) — `tests/test_api.py`
- **test_health_reports_the_active_components()** (3 connections) — `tests/test_api.py`
- **test_status_reports_what_is_indexed()** (3 connections) — `tests/test_api.py`
- **test_traces_are_listable_and_expandable_in_development()** (3 connections) — `tests/test_api.py`
- **test_traces_are_not_exposed_outside_development()** (3 connections) — `tests/test_api.py`
- **test_ui_is_served_at_the_root()** (3 connections) — `tests/test_api.py`
- **fixture** (2 connections)
- **test_a_request_is_logged_with_its_outcome()** (2 connections) — `tests/test_api.py`
- **test_chat_abstains_when_nothing_is_retrieved()** (2 connections) — `tests/test_api.py`
- **test_chat_returns_a_cited_answer()** (2 connections) — `tests/test_api.py`
- **test_chat_returns_the_trace_when_asked()** (2 connections) — `tests/test_api.py`
- **test_history_is_accepted()** (2 connections) — `tests/test_api.py`
- **test_search_omits_the_trace_by_default()** (2 connections) — `tests/test_api.py`
- *... and 13 more nodes in this community*

## Relationships

- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (1 shared connections)
- [Diagnostic CLI Commands](Diagnostic_CLI_Commands.md) (1 shared connections)

## Source Files

- `tests/test_api.py`

## Audit Trail

- EXTRACTED: 132 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*