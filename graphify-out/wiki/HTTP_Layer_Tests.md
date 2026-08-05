# HTTP Layer Tests

> 34 nodes

## Key Concepts

- **test_api.py** (33 connections) — `tests/test_api.py`
- **TestClient** (16 connections)
- **_development_client()** (7 connections) — `tests/test_api.py`
- **client()** (6 connections) — `tests/test_api.py`
- **_register_stub_providers()** (5 connections) — `tests/test_api.py`
- **api/__init__.py** (4 connections) — `src/osc_assistant/api/__init__.py`
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
- **fixture** (2 connections)
- **test_search_returns_ranked_chunks()** (2 connections) — `tests/test_api.py`
- **test_chat_returns_a_cited_answer()** (2 connections) — `tests/test_api.py`
- **test_chat_abstains_when_nothing_is_retrieved()** (2 connections) — `tests/test_api.py`
- **test_history_is_accepted()** (2 connections) — `tests/test_api.py`
- **test_search_returns_the_trace_when_asked()** (2 connections) — `tests/test_api.py`
- **test_search_omits_the_trace_by_default()** (2 connections) — `tests/test_api.py`
- **test_chat_returns_the_trace_when_asked()** (2 connections) — `tests/test_api.py`
- **parametrize** (1 connections)
- *... and 9 more nodes in this community*

## Relationships

- [HTTP API Layer](HTTP_API_Layer.md) (4 shared connections)
- [Settings Schema](Settings_Schema.md) (4 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (4 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (2 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (2 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (2 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (1 shared connections)
- [Chunker Registration](Chunker_Registration.md) (1 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (1 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (1 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/__init__.py`
- `tests/test_api.py`

## Audit Trail

- EXTRACTED: 126 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*