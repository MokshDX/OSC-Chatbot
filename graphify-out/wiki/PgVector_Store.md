# PgVector Store

> 46 nodes

## Key Concepts

- **ChunkerOptions** (28 connections) — `src/osc_assistant/chunking/recursive.py`
- **RecursiveChunker** (24 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_chunking.py** (16 connections) — `tests/test_chunking.py`
- **IngestionPipeline** (13 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **_document()** (13 connections) — `tests/test_chunking.py`
- **InMemoryLoader** (11 connections) — `src/osc_assistant/ingestion/loaders.py`
- **test_osc_retrieval_is_usable_as_a_langchain_retriever()** (10 connections) — `tests/test_langchain_integration.py`
- **indexed()** (9 connections) — `tests/test_answerer.py`
- **indexed()** (9 connections) — `tests/test_retrieval.py`
- **test_a_populated_index_produces_no_note()** (9 connections) — `tests/test_server_lifecycle.py`
- **test_a_document_that_produced_no_chunks_is_still_visible()** (8 connections) — `tests/test_inspection.py`
- **indexed()** (7 connections) — `tests/test_inspection.py`
- **test_chunk_ids_are_stable_across_runs()** (5 connections) — `tests/test_chunking.py`
- **test_chunk_ids_change_when_content_changes()** (5 connections) — `tests/test_chunking.py`
- **test_document_metadata_is_denormalised_onto_chunks()** (5 connections) — `tests/test_chunking.py`
- **test_unbroken_text_is_still_split()** (5 connections) — `tests/test_chunking.py`
- **test_chunking_preserves_document_content()** (5 connections) — `tests/test_chunking.py`
- **test_short_document_is_a_single_chunk()** (4 connections) — `tests/test_chunking.py`
- **test_chunks_respect_the_size_budget()** (4 connections) — `tests/test_chunking.py`
- **test_ordinals_are_contiguous()** (4 connections) — `tests/test_chunking.py`
- **test_empty_document_produces_no_chunks()** (4 connections) — `tests/test_chunking.py`
- **test_fixed_chunker_overlaps_windows()** (4 connections) — `tests/test_chunking.py`
- **test_chunking_preserves_content_across_separator_kinds()** (4 connections) — `tests/test_chunking.py`
- **.validated()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- *... and 21 more nodes in this community*

## Relationships

- [Conversational Evaluator](Conversational_Evaluator.md) (20 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (6 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (3 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (3 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (3 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (2 shared connections)
- [Evaluation Framework ADR](Evaluation_Framework_ADR.md) (2 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (2 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (1 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (1 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/recursive.py`
- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `tests/test_answerer.py`
- `tests/test_chunking.py`
- `tests/test_inspection.py`
- `tests/test_langchain_integration.py`
- `tests/test_retrieval.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 142 (59%)
- INFERRED: 99 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*