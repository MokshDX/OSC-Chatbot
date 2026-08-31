# Protocol Seams & Container

> 64 nodes

## Key Concepts

- **PgVectorStore** (43 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **test_pgvector_integration.py** (26 connections) — `tests/test_pgvector_integration.py`
- **._acquire()** (16 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **PgVectorOptions** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **populated()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_replace_document_supersedes_the_old_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **test_failed_replace_leaves_no_hash_without_chunks()** (7 connections) — `tests/test_pgvector_integration.py`
- **.setup()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **._migrate()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_chunk()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Any** (5 connections)
- **._assert_dimensions_match()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_document_summary()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **store()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_workspace_isolates_queries()** (5 connections) — `tests/test_pgvector_integration.py`
- **test_search_ignores_other_embedding_models()** (5 connections) — `tests/test_pgvector_integration.py`
- **.list_documents()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_document()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.document_chunks()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.get_chunk()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_register_codecs()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **embeddings()** (4 connections) — `tests/test_pgvector_integration.py`
- **test_statistics_are_scoped_to_the_workspace()** (4 connections) — `tests/test_pgvector_integration.py`
- **test_a_document_with_no_chunks_is_still_listed()** (4 connections) — `tests/test_pgvector_integration.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- *... and 39 more nodes in this community*

## Relationships

- [Logging System Design](Logging_System_Design.md) (15 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (11 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (10 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (6 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (4 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (4 shared connections)
- [Error Base Classes](Error_Base_Classes.md) (2 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `tests/test_pgvector_integration.py`

## Audit Trail

- EXTRACTED: 261 (99%)
- INFERRED: 2 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*