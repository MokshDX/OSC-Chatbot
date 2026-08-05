# In-Memory Vector Store

> 28 nodes

## Key Concepts

- **MemoryVectorStore** (72 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_inspection.py** (18 connections) — `tests/test_inspection.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_both_built_in_stores_offer_inspection()** (3 connections) — `tests/test_inspection.py`
- **test_chunk_size_percentiles_reflect_what_was_actually_stored()** (3 connections) — `tests/test_inspection.py`
- **test_a_chunk_can_be_fetched_by_id()** (3 connections) — `tests/test_inspection.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.document_chunks()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.get_chunk()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_statistics_report_the_corpus()** (2 connections) — `tests/test_inspection.py`
- **test_statistics_on_an_empty_store_do_not_divide_by_zero()** (2 connections) — `tests/test_inspection.py`
- **test_documents_can_be_listed_and_searched()** (2 connections) — `tests/test_inspection.py`
- **test_listing_is_paginated()** (2 connections) — `tests/test_inspection.py`
- **test_a_document_reports_its_chunks_in_order()** (2 connections) — `tests/test_inspection.py`
- **test_missing_records_return_none_rather_than_raising()** (2 connections) — `tests/test_inspection.py`
- **test_a_deleted_document_leaves_no_trace()** (2 connections) — `tests/test_inspection.py`
- **.__init__()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.setup()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.close()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.list_document_hashes()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.document_ids()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **A dictionary-backed `VectorStore`.** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Replace a document and its chunks. Atomic by construction: the vectors are…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Store inspection tests. `StoreInspector` is what the operational commands are…** (1 connections) — `tests/test_inspection.py`
- *... and 3 more nodes in this community*

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (14 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (13 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (11 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (7 shared connections)
- [Store Inspector](Store_Inspector.md) (3 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (3 shared connections)
- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (2 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (2 shared connections)
- [conftest.py](conftest.py.md) (1 shared connections)
- [NoopReranker](NoopReranker.md) (1 shared connections)
- [DimensionMismatchError](DimensionMismatchError.md) (1 shared connections)
- [EmbeddedChunk](EmbeddedChunk.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/memory.py`
- `tests/test_inspection.py`

## Audit Trail

- EXTRACTED: 133 (97%)
- INFERRED: 4 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*