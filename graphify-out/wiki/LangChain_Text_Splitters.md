# LangChain Text Splitters

> 28 nodes

## Key Concepts

- **Chunk** (34 connections) — `src/osc_assistant/types.py`
- **Chunker** (25 connections) — `src/osc_assistant/protocols.py`
- **langchain_splitters.py** (23 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **LangChainRecursiveChunker** (9 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **test_store_rejects_wrong_width_vectors()** (6 connections) — `tests/test_retrieval.py`
- **_require_splitters()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_build_langchain_recursive()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_build_markdown()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.split()** (4 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_heading_path()** (4 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.__init__()** (4 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.split()** (4 connections) — `src/osc_assistant/protocols.py`
- **Any** (3 connections)
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_section_metadata()** (3 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.document_chunks()** (3 connections) — `src/osc_assistant/protocols.py`
- **.get_chunk()** (3 connections) — `src/osc_assistant/protocols.py`
- **register** (2 connections)
- **Chunkers backed by `langchain-text-splitters`. **Why adopt a library here, of…** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **`RecursiveCharacterTextSplitter` behind the OSC `Chunker` protocol.** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Join whichever heading levels are present into a readable path.** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Every chunk of a document, in ordinal order.** (1 connections) — `src/osc_assistant/protocols.py`
- **One chunk with its full text — what the model was actually shown.** (1 connections) — `src/osc_assistant/protocols.py`
- **Splits a document into retrievable units.** (1 connections) — `src/osc_assistant/protocols.py`
- *... and 3 more nodes in this community*

## Relationships

- [Chunker Registration](Chunker_Registration.md) (13 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (13 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (8 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (7 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (5 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (4 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (3 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (3 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (3 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (2 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (2 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)

## Source Files

- `src/osc_assistant/chunking/langchain_splitters.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/types.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 141 (88%)
- INFERRED: 19 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*