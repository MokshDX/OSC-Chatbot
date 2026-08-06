# Store Construction & Embedding Calls

> 29 nodes · cohesion 0.07

## Key Concepts

- **VectorStore** (33 connections) — `src/osc_assistant/protocols.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.vector_store()** (4 connections) — `src/osc_assistant/container.py`
- **Vector** (4 connections)
- **.replace_document()** (4 connections) — `src/osc_assistant/protocols.py`
- **.search_hybrid()** (4 connections) — `src/osc_assistant/protocols.py`
- **.embed_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.embed_query()** (3 connections) — `src/osc_assistant/protocols.py`
- **.search_keyword()** (3 connections) — `src/osc_assistant/protocols.py`
- **.search_vector()** (3 connections) — `src/osc_assistant/protocols.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/protocols.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/protocols.py`
- **.list_document_hashes()** (2 connections) — `src/osc_assistant/protocols.py`
- **.setup()** (2 connections) — `src/osc_assistant/protocols.py`
- **Build the store, injecting values it cannot know on its own. Vector width, the…** (1 connections) — `src/osc_assistant/container.py`
- **Remove a document and every chunk belonging to it.** (1 connections) — `src/osc_assistant/protocols.py`
- **Map document id to stored content hash, for incremental sync.** (1 connections) — `src/osc_assistant/protocols.py`
- **Every document id currently indexed.** (1 connections) — `src/osc_assistant/protocols.py`
- **Lexical search. Return `[]` if the store has no lexical index.** (1 connections) — `src/osc_assistant/protocols.py`
- **Combined lexical and vector search, fused into a single ranking.** (1 connections) — `src/osc_assistant/protocols.py`
- **Embed corpus text. Returns one vector per input, in order.** (1 connections) — `src/osc_assistant/protocols.py`
- **Embed a search query.** (1 connections) — `src/osc_assistant/protocols.py`
- **Persistence and retrieval of embedded chunks. Implementations that cannot do…** (1 connections) — `src/osc_assistant/protocols.py`
- **Prepare the store (connect, create collections). Idempotent.** (1 connections) — `src/osc_assistant/protocols.py`
- *... and 4 more nodes in this community*

## Relationships

- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (4 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (4 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (4 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (3 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (3 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (3 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (1 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (1 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (1 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`

## Audit Trail

- EXTRACTED: 81 (90%)
- INFERRED: 9 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*