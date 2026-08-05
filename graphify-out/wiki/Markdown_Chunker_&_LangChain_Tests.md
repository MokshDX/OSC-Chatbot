# Markdown Chunker & LangChain Tests

> 27 nodes

## Key Concepts

- **test_langchain_integration.py** (40 connections) — `tests/test_langchain_integration.py`
- **LangChainChunkerOptions** (14 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_document()** (11 connections) — `tests/test_langchain_integration.py`
- **MarkdownChunker** (10 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **test_chunk_ids_are_stable_across_runs()** (5 connections) — `tests/test_langchain_integration.py`
- **test_chunking_preserves_document_content()** (5 connections) — `tests/test_langchain_integration.py`
- **test_langchain_recursive_respects_the_size_budget()** (5 connections) — `tests/test_langchain_integration.py`
- **test_unbroken_text_is_still_split()** (5 connections) — `tests/test_langchain_integration.py`
- **test_markdown_chunker_records_the_heading_path()** (5 connections) — `tests/test_langchain_integration.py`
- **test_markdown_chunker_keeps_headings_in_the_chunk_text()** (5 connections) — `tests/test_langchain_integration.py`
- **parametrize** (4 connections)
- **test_langchain_chunkers_are_registered_and_satisfy_the_protocol()** (4 connections) — `tests/test_langchain_integration.py`
- **test_ordinals_are_contiguous()** (4 connections) — `tests/test_langchain_integration.py`
- **test_empty_document_produces_no_chunks()** (4 connections) — `tests/test_langchain_integration.py`
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **test_bridge_never_claims_native_citation_support()** (3 connections) — `tests/test_langchain_integration.py`
- **`ChunkerOptions` plus the settings only the LangChain splitters expose.** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Heading-aware splitting: structure first, then size. Two passes, because either…** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **test_the_bridges_are_registered_under_the_langchain_name()** (1 connections) — `tests/test_langchain_integration.py`
- **LangChain integration tests. Three surfaces, three concerns: * **Chunkers** —…** (1 connections) — `tests/test_langchain_integration.py`
- **Ingestion skips unchanged documents by hash; drifting ids would re-index all.** (1 connections) — `tests/test_langchain_integration.py`
- **Chunk text is quoted back as citation evidence, so no character may be…** (1 connections) — `tests/test_langchain_integration.py`
- **The reason for adopting the library: OSC's own chunker can overshoot by the…** (1 connections) — `tests/test_langchain_integration.py`
- **No separator exists in one long token; the hard fallback must catch it.** (1 connections) — `tests/test_langchain_integration.py`
- **A retrieval hit should say which section it came from without a second lookup.** (1 connections) — `tests/test_langchain_integration.py`
- *... and 2 more nodes in this community*

## Relationships

- [LangChain Text Splitters](LangChain_Text_Splitters.md) (8 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (7 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (7 shared connections)
- [LangChain Embedding Bridge](LangChain_Embedding_Bridge.md) (4 shared connections)
- [Chunker Registration](Chunker_Registration.md) (3 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (3 shared connections)
- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (3 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (1 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (1 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (1 shared connections)
- [Settings Schema](Settings_Schema.md) (1 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/langchain_splitters.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 112 (81%)
- INFERRED: 26 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*