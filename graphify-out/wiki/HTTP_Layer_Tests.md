# HTTP Layer Tests

> 19 nodes · cohesion 0.16

## Key Concepts

- **test_api.py** (23 connections) — `tests/test_api.py`
- **TestClient** (8 connections)
- **client()** (6 connections) — `tests/test_api.py`
- **_register_stub_providers()** (5 connections) — `tests/test_api.py`
- **test_malformed_requests_are_rejected()** (4 connections) — `tests/test_api.py`
- **_parse_sse()** (3 connections) — `tests/test_api.py`
- **test_chat_streams_sources_then_deltas_then_completion()** (3 connections) — `tests/test_api.py`
- **test_health_reports_the_active_components()** (3 connections) — `tests/test_api.py`
- **fixture** (2 connections)
- **test_chat_abstains_when_nothing_is_retrieved()** (2 connections) — `tests/test_api.py`
- **test_chat_returns_a_cited_answer()** (2 connections) — `tests/test_api.py`
- **test_history_is_accepted()** (2 connections) — `tests/test_api.py`
- **test_search_returns_ranked_chunks()** (2 connections) — `tests/test_api.py`
- **parametrize** (1 connections)
- **HTTP layer tests. These run the real application — real container, real…** (1 connections) — `tests/test_api.py`
- **Validation happens at the trust boundary, before any provider is touched.** (1 connections) — `tests/test_api.py`
- **Decode a server-sent event stream into (event name, payload) pairs.** (1 connections) — `tests/test_api.py`
- **Register the doubles as ordinary providers. This is exactly how a new provider…** (1 connections) — `tests/test_api.py`
- **A running deployment must be able to say what it is configured with.** (1 connections) — `tests/test_api.py`

## Relationships

- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (5 shared connections)
- [Settings Schema](Settings_Schema.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)
- [Chunking Strategies](Chunking_Strategies.md) (1 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (1 shared connections)

## Source Files

- `tests/test_api.py`

## Audit Trail

- EXTRACTED: 70 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*