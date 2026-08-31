# Error Hierarchy

> 53 nodes

## Key Concepts

- **test_langchain_integration.py** (40 connections) — `tests/test_langchain_integration.py`
- **LangChainChunkerOptions** (14 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **LangChainEmbeddingModel** (11 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **_document()** (11 connections) — `tests/test_langchain_integration.py`
- **_bridge()** (9 connections) — `tests/test_langchain_integration.py`
- **_embedding_bridge()** (7 connections) — `tests/test_langchain_integration.py`
- **LangChainChatOptions** (6 connections) — `src/osc_assistant/providers/llm/langchain_bridge.py`
- **._assert_width()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **test_chunk_ids_are_stable_across_runs()** (5 connections) — `tests/test_langchain_integration.py`
- **test_chunking_preserves_document_content()** (5 connections) — `tests/test_langchain_integration.py`
- **test_langchain_recursive_respects_the_size_budget()** (5 connections) — `tests/test_langchain_integration.py`
- **test_unbroken_text_is_still_split()** (5 connections) — `tests/test_langchain_integration.py`
- **test_markdown_chunker_records_the_heading_path()** (5 connections) — `tests/test_langchain_integration.py`
- **test_markdown_chunker_keeps_headings_in_the_chunk_text()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_streams_text_then_citations()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_reports_an_empty_completion_rather_than_abstaining()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_strips_a_leaked_reasoning_block()** (5 connections) — `tests/test_langchain_integration.py`
- **.embed_documents()** (4 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.embed_query()** (4 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **parametrize** (4 connections)
- **test_langchain_chunkers_are_registered_and_satisfy_the_protocol()** (4 connections) — `tests/test_langchain_integration.py`
- **test_ordinals_are_contiguous()** (4 connections) — `tests/test_langchain_integration.py`
- **test_empty_document_produces_no_chunks()** (4 connections) — `tests/test_langchain_integration.py`
- **test_bridge_translates_a_completion_and_parses_citations()** (4 connections) — `tests/test_langchain_integration.py`
- **.embed_documents()** (4 connections) — `tests/test_langchain_integration.py`
- *... and 28 more nodes in this community*

## Relationships

- [Conversational Evaluator](Conversational_Evaluator.md) (12 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (9 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (7 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (6 shared connections)
- [Logging Tests](Logging_Tests.md) (6 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (4 shared connections)
- [PgVector Store](PgVector_Store.md) (2 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (2 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (1 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (1 shared connections)
- [Logging System Design](Logging_System_Design.md) (1 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/langchain_splitters.py`
- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `src/osc_assistant/providers/llm/langchain_bridge.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 203 (90%)
- INFERRED: 23 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*