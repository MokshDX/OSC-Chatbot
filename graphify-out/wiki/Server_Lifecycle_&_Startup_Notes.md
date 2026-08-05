# Server Lifecycle & Startup Notes

> 35 nodes

## Key Concepts

- **test_server_lifecycle.py** (30 connections) — `tests/test_server_lifecycle.py`
- **_ExplodingChatModel** (23 connections) — `tests/test_server_lifecycle.py`
- **_settings()** (16 connections) — `tests/test_server_lifecycle.py`
- **startup_notes()** (10 connections) — `src/osc_assistant/api/banner.py`
- **.stream()** (7 connections) — `tests/test_server_lifecycle.py`
- **exploding_client()** (7 connections) — `tests/test_server_lifecycle.py`
- **test_a_known_provider_failure_keeps_its_actionable_message()** (7 connections) — `tests/test_server_lifecycle.py`
- **test_shutdown_releases_every_component_that_was_built()** (7 connections) — `tests/test_server_lifecycle.py`
- **test_an_empty_index_is_reported_at_startup()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_a_non_development_environment_is_called_out()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_startup_notes_reach_the_structured_log_too()** (5 connections) — `tests/test_server_lifecycle.py`
- **TestClient** (5 connections)
- **test_shutdown_does_not_construct_what_was_never_used()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_a_component_that_fails_to_close_does_not_break_shutdown()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_embedding_vectors_are_unaffected_by_the_close_probe()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_an_unexpected_stream_failure_still_ends_the_stream()** (4 connections) — `tests/test_server_lifecycle.py`
- **test_an_unexpected_failure_does_not_leak_internals_to_the_client()** (4 connections) — `tests/test_server_lifecycle.py`
- **test_every_adapter_that_owns_an_sdk_client_can_be_released()** (2 connections) — `tests/test_server_lifecycle.py`
- **Conditions worth telling a developer about before their first request. Returned…** (1 connections) — `src/osc_assistant/api/banner.py`
- **.model_id()** (1 connections) — `tests/test_server_lifecycle.py`
- **.supports_citations()** (1 connections) — `tests/test_server_lifecycle.py`
- **StreamEvent** (1 connections)
- **Startup, shutdown and in-flight failure behaviour of the service. These cover…** (1 connections) — `tests/test_server_lifecycle.py`
- **A service that starts perfectly and abstains from everything looks broken. It…** (1 connections) — `tests/test_server_lifecycle.py`
- **A chat UI on an unauthenticated service is the state most easily mistaken for…** (1 connections) — `tests/test_server_lifecycle.py`
- *... and 10 more nodes in this community*

## Relationships

- [Settings Schema](Settings_Schema.md) (14 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (8 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (8 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (6 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (6 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (5 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (4 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (3 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (2 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (2 shared connections)
- [_stub_providers()](_stub_providers%28%29.md) (2 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/banner.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 150 (89%)
- INFERRED: 19 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*