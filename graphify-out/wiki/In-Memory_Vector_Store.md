# In-Memory Vector Store

> 32 nodes · cohesion 0.08

## Key Concepts

- **MemoryVectorStore** (72 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_inspection.py** (18 connections) — `tests/test_inspection.py`
- **indexed()** (7 connections) — `tests/test_inspection.py`
- **.replace_document()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_a_chunk_can_be_fetched_by_id()** (3 connections) — `tests/test_inspection.py`
- **test_both_built_in_stores_offer_inspection()** (3 connections) — `tests/test_inspection.py`
- **test_chunk_size_percentiles_reflect_what_was_actually_stored()** (3 connections) — `tests/test_inspection.py`
- **.delete_document()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.document_chunks()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.get_chunk()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **test_a_deleted_document_leaves_no_trace()** (2 connections) — `tests/test_inspection.py`
- **test_a_document_reports_its_chunks_in_order()** (2 connections) — `tests/test_inspection.py`
- **test_documents_can_be_listed_and_searched()** (2 connections) — `tests/test_inspection.py`
- **test_listing_is_paginated()** (2 connections) — `tests/test_inspection.py`
- **test_missing_records_return_none_rather_than_raising()** (2 connections) — `tests/test_inspection.py`
- **test_statistics_on_an_empty_store_do_not_divide_by_zero()** (2 connections) — `tests/test_inspection.py`
- **test_statistics_report_the_corpus()** (2 connections) — `tests/test_inspection.py`
- **test_deleting_a_document_removes_its_chunks()** (2 connections) — `tests/test_retrieval.py`
- **test_hashes_are_recorded_for_incremental_sync()** (2 connections) — `tests/test_retrieval.py`
- **.close()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.dimensions()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.document_ids()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.__init__()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.list_document_hashes()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.setup()** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- *... and 7 more nodes in this community*

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (14 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (13 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (13 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (4 shared connections)
- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (4 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (3 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (3 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (3 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (1 shared connections)
- [Citations & Native Citation Model](Citations_%26_Native_Citation_Model.md) (1 shared connections)
- [Noop Reranker & Evaluation Corpus](Noop_Reranker_%26_Evaluation_Corpus.md) (1 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/memory.py`
- `tests/test_inspection.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 141 (95%)
- INFERRED: 8 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*