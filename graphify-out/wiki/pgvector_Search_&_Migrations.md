# pgvector Search & Migrations

> 16 nodes · cohesion 0.19

## Key Concepts

- **._acquire()** (11 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_scored_chunk()** (8 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_encode_vector()** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._migrate()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_vector()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._assert_dimensions_match()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_keyword()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Any** (3 connections)
- **Vector** (3 connections)
- **.delete_document()** (2 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Replace a document and its chunks in a single transaction. Delete-then-insert…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Apply unapplied migration files in filename order. A hand-rolled runner rather…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Fail loudly if the stored vector width disagrees with the active model.…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Render a vector in pgvector's literal form for the `::vector` cast.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`

## Relationships

- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (9 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (5 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (4 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (2 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (1 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/pgvector.py`

## Audit Trail

- EXTRACTED: 71 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*