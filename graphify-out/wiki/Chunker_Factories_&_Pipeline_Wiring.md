# Chunker Factories & Pipeline Wiring

> 13 nodes · cohesion 0.23

## Key Concepts

- **ComponentConfig** (64 connections) — `src/osc_assistant/registry.py`
- **Chunker** (25 connections) — `src/osc_assistant/protocols.py`
- **langchain_splitters.py** (23 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Protocol** (6 connections)
- **_build_langchain_recursive()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_build_markdown()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.__init__()** (4 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **.chunker()** (3 connections) — `src/osc_assistant/container.py`
- **register** (2 connections)
- **Chunkers backed by `langchain-text-splitters`. **Why adopt a library here, of…** (1 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Splits a document into retrievable units.** (1 connections) — `src/osc_assistant/protocols.py`
- **BaseModel** (1 connections)
- **Selects and configures one swappable component. `options` is intentionally…** (1 connections) — `src/osc_assistant/registry.py`

## Relationships

- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (16 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (13 shared connections)
- [Recursive & Markdown Splitting](Recursive_%26_Markdown_Splitting.md) (12 shared connections)
- [Component Registry](Component_Registry.md) (7 shared connections)
- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (5 shared connections)
- [LangChain Bridges & Splitters](LangChain_Bridges_%26_Splitters.md) (5 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (5 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (4 shared connections)
- [Store Construction & Embedding Calls](Store_Construction_%26_Embedding_Calls.md) (4 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (4 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (3 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (3 shared connections)

## Source Files

- `src/osc_assistant/chunking/langchain_splitters.py`
- `src/osc_assistant/container.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/registry.py`

## Audit Trail

- EXTRACTED: 116 (82%)
- INFERRED: 25 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*