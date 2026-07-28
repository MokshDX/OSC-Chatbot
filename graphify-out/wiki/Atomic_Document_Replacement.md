# Atomic Document Replacement

> 10 nodes · cohesion 0.22

## Key Concepts

- **Chunk** (20 connections) — `src/osc_assistant/types.py`
- **EmbeddedChunk** (19 connections) — `src/osc_assistant/types.py`
- **populated()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_store_rejects_wrong_width_vectors()** (6 connections) — `tests/test_retrieval.py`
- **.replace_document()** (4 connections) — `src/osc_assistant/protocols.py`
- **fixture** (2 connections)
- **Atomically replace a document and all of its chunks. Must be all-or-nothing.…** (1 connections) — `src/osc_assistant/protocols.py`
- **A retrievable span of a document. `title` and `source_uri` are denormalised…** (1 connections) — `src/osc_assistant/types.py`
- **A chunk paired with the vector produced for it, tagged with its model. The…** (1 connections) — `src/osc_assistant/types.py`
- **Mixing vector widths silently produces nonsense scores; it must raise.** (1 connections) — `tests/test_retrieval.py`

## Relationships

- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (7 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (6 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (4 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (4 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (3 shared connections)
- [Chunker Registration](Chunker_Registration.md) (3 shared connections)
- [Chunking Strategies](Chunking_Strategies.md) (3 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (2 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (2 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (2 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/types.py`
- `tests/test_pgvector_integration.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 52 (84%)
- INFERRED: 10 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*