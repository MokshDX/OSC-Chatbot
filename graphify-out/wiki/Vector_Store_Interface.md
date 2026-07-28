# Vector Store Interface

> 15 nodes · cohesion 0.13

## Key Concepts

- **VectorStore** (31 connections) — `src/osc_assistant/protocols.py`
- **.search_keyword()** (3 connections) — `src/osc_assistant/protocols.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/protocols.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **.document_ids()** (2 connections) — `src/osc_assistant/protocols.py`
- **.list_document_hashes()** (2 connections) — `src/osc_assistant/protocols.py`
- **.setup()** (2 connections) — `src/osc_assistant/protocols.py`
- **Remove a document and every chunk belonging to it.** (1 connections) — `src/osc_assistant/protocols.py`
- **Map document id to stored content hash, for incremental sync.** (1 connections) — `src/osc_assistant/protocols.py`
- **Every document id currently indexed.** (1 connections) — `src/osc_assistant/protocols.py`
- **Lexical search. Return `[]` if the store has no lexical index.** (1 connections) — `src/osc_assistant/protocols.py`
- **Persistence and retrieval of embedded chunks. Implementations that cannot do…** (1 connections) — `src/osc_assistant/protocols.py`
- **Prepare the store (connect, create collections). Idempotent.** (1 connections) — `src/osc_assistant/protocols.py`
- **The vector width this store is configured to hold.** (1 connections) — `src/osc_assistant/protocols.py`
- **.close()** (1 connections) — `src/osc_assistant/protocols.py`

## Relationships

- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (4 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (3 shared connections)
- [Composition Root](Composition_Root.md) (2 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (2 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (2 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (2 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (1 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (1 shared connections)
- [Chunker Registration](Chunker_Registration.md) (1 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`

## Audit Trail

- EXTRACTED: 45 (87%)
- INFERRED: 7 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*