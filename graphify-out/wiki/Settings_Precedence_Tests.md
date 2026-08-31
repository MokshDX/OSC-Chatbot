# Settings Precedence Tests

> 27 nodes

## Key Concepts

- **MemoryVectorStore** (63 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_inspection.py** (18 connections) — `tests/test_inspection.py`
- **test_both_built_in_stores_offer_inspection()** (3 connections) — `tests/test_inspection.py`
- **test_chunk_size_percentiles_reflect_what_was_actually_stored()** (3 connections) — `tests/test_inspection.py`
- **test_a_chunk_can_be_fetched_by_id()** (3 connections) — `tests/test_inspection.py`
- **.document_chunks()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.get_chunk()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_statistics_report_the_corpus()** (2 connections) — `tests/test_inspection.py`
- **test_statistics_on_an_empty_store_do_not_divide_by_zero()** (2 connections) — `tests/test_inspection.py`
- **test_documents_can_be_listed_and_searched()** (2 connections) — `tests/test_inspection.py`
- **test_listing_is_paginated()** (2 connections) — `tests/test_inspection.py`
- **test_a_document_reports_its_chunks_in_order()** (2 connections) — `tests/test_inspection.py`
- **test_missing_records_return_none_rather_than_raising()** (2 connections) — `tests/test_inspection.py`
- **test_a_deleted_document_leaves_no_trace()** (2 connections) — `tests/test_inspection.py`
- **test_deleting_a_document_removes_its_chunks()** (2 connections) — `tests/test_retrieval.py`
- **test_hashes_are_recorded_for_incremental_sync()** (2 connections) — `tests/test_retrieval.py`
- **.__init__()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.setup()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.close()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.list_document_hashes()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.document_ids()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **A dictionary-backed `VectorStore`.** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Store inspection tests. `StoreInspector` is what the operational commands are…** (1 connections) — `tests/test_inspection.py`
- **The protocol is optional; a store that cannot support it is still a store. Both…** (1 connections) — `tests/test_inspection.py`
- *... and 2 more nodes in this community*

## Relationships

- [Quality Report Renderer](Quality_Report_Renderer.md) (14 shared connections)
- [Evaluation Framework ADR](Evaluation_Framework_ADR.md) (9 shared connections)
- [PgVector Store](PgVector_Store.md) (6 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (4 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (4 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (4 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (3 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (3 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (2 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (2 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/memory.py`
- `tests/test_inspection.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 119 (97%)
- INFERRED: 4 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*