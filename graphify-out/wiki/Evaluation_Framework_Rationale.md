# Evaluation Framework Rationale

> 29 nodes

## Key Concepts

- **test_server_lifecycle.py** (30 connections) — `tests/test_server_lifecycle.py`
- **_settings()** (16 connections) — `tests/test_server_lifecycle.py`
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
- **_stub_providers()** (4 connections) — `tests/test_server_lifecycle.py`
- **test_an_unexpected_stream_failure_still_ends_the_stream()** (4 connections) — `tests/test_server_lifecycle.py`
- **test_an_unexpected_failure_does_not_leak_internals_to_the_client()** (4 connections) — `tests/test_server_lifecycle.py`
- **fixture** (2 connections)
- **test_every_adapter_that_owns_an_sdk_client_can_be_released()** (2 connections) — `tests/test_server_lifecycle.py`
- **Startup, shutdown and in-flight failure behaviour of the service. These cover…** (1 connections) — `tests/test_server_lifecycle.py`
- **A service that starts perfectly and abstains from everything looks broken. It…** (1 connections) — `tests/test_server_lifecycle.py`
- **A chat UI on an unauthenticated service is the state most easily mistaken for…** (1 connections) — `tests/test_server_lifecycle.py`
- **A condition worth interrupting a developer for belongs in the log as well.** (1 connections) — `tests/test_server_lifecycle.py`
- **A client told nothing waits forever. The handler previously caught only…** (1 connections) — `tests/test_server_lifecycle.py`
- **An unexpected exception's message is not part of the API contract.** (1 connections) — `tests/test_server_lifecycle.py`
- **`AssistantError` messages are written for operators and are safe to surface.** (1 connections) — `tests/test_server_lifecycle.py`
- **Only the vector store was closed before; provider HTTP clients leaked.** (1 connections) — `tests/test_server_lifecycle.py`
- *... and 4 more nodes in this community*

## Relationships

- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (7 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (6 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (6 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (5 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (4 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (4 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (4 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (3 shared connections)
- [PgVector Store](PgVector_Store.md) (2 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)
- [Document Loaders](Document_Loaders.md) (1 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (1 shared connections)

## Source Files

- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 127 (98%)
- INFERRED: 3 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*