# Server Lifecycle Tests

> 25 nodes · cohesion 0.12

## Key Concepts

- **test_server_lifecycle.py** (30 connections) — `tests/test_server_lifecycle.py`
- **_settings()** (16 connections) — `tests/test_server_lifecycle.py`
- **exploding_client()** (7 connections) — `tests/test_server_lifecycle.py`
- **test_a_known_provider_failure_keeps_its_actionable_message()** (7 connections) — `tests/test_server_lifecycle.py`
- **test_shutdown_releases_every_component_that_was_built()** (7 connections) — `tests/test_server_lifecycle.py`
- **TestClient** (5 connections)
- **test_a_component_that_fails_to_close_does_not_break_shutdown()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_an_empty_index_is_reported_at_startup()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_embedding_vectors_are_unaffected_by_the_close_probe()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_shutdown_does_not_construct_what_was_never_used()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_startup_notes_reach_the_structured_log_too()** (5 connections) — `tests/test_server_lifecycle.py`
- **test_an_unexpected_failure_does_not_leak_internals_to_the_client()** (4 connections) — `tests/test_server_lifecycle.py`
- **test_an_unexpected_stream_failure_still_ends_the_stream()** (4 connections) — `tests/test_server_lifecycle.py`
- **test_every_adapter_that_owns_an_sdk_client_can_be_released()** (2 connections) — `tests/test_server_lifecycle.py`
- **Startup, shutdown and in-flight failure behaviour of the service. These cover…** (1 connections) — `tests/test_server_lifecycle.py`
- **A condition worth interrupting a developer for belongs in the log as well.** (1 connections) — `tests/test_server_lifecycle.py`
- **A client told nothing waits forever. The handler previously caught only…** (1 connections) — `tests/test_server_lifecycle.py`
- **An unexpected exception's message is not part of the API contract.** (1 connections) — `tests/test_server_lifecycle.py`
- **`AssistantError` messages are written for operators and are safe to surface.** (1 connections) — `tests/test_server_lifecycle.py`
- **Only the vector store was closed before; provider HTTP clients leaked.** (1 connections) — `tests/test_server_lifecycle.py`
- **`ingest` never builds a chat model; tearing one down would build it. That would…** (1 connections) — `tests/test_server_lifecycle.py`
- **Shutdown runs on the failure path too; it must not mask the original error.** (1 connections) — `tests/test_server_lifecycle.py`
- **A sanity check that the probe does not disturb a normal component.** (1 connections) — `tests/test_server_lifecycle.py`
- **Regression: `Container.shutdown()` probes for `aclose`/`close`, and an adapter…** (1 connections) — `tests/test_server_lifecycle.py`
- **A service that starts perfectly and abstains from everything looks broken. It…** (1 connections) — `tests/test_server_lifecycle.py`

## Relationships

- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (9 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (5 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (4 shared connections)
- [Startup Banner & Lifecycle](Startup_Banner_%26_Lifecycle.md) (4 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (4 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (4 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (4 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (3 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (3 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (2 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (2 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)

## Source Files

- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 115 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*