# pgvector Setup & Codecs

> 10 nodes · cohesion 0.22

## Key Concepts

- **pgvector.py** (25 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **VectorStoreError** (6 connections) — `src/osc_assistant/errors.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.setup()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_register_codecs()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **The vector store could not complete an operation.** (1 connections) — `src/osc_assistant/errors.py`
- **register** (1 connections)
- **PostgreSQL + pgvector store: the production default. One datastore holds chunk…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Open the pool and, unless disabled, apply pending migrations.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Decode JSONB into Python objects instead of raw strings.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`

## Relationships

- [Error Hierarchy](Error_Hierarchy.md) (6 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (5 shared connections)
- [pgvector Store & Integration Tests](pgvector_Store_%26_Integration_Tests.md) (5 shared connections)
- [Structured Logging](Structured_Logging.md) (2 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (2 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (2 shared connections)
- [Provider Package Registration](Provider_Package_Registration.md) (1 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (1 shared connections)
- [Dimension Guard & Match Source](Dimension_Guard_%26_Match_Source.md) (1 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`

## Audit Trail

- EXTRACTED: 48 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*