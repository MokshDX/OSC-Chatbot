# Recursive Chunker

> 31 nodes

## Key Concepts

- **ChunkerOptions** (31 connections) — `src/osc_assistant/chunking/recursive.py`
- **RecursiveChunker** (28 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_chunking.py** (16 connections) — `tests/test_chunking.py`
- **_document()** (13 connections) — `tests/test_chunking.py`
- **test_osc_retrieval_is_usable_as_a_langchain_retriever()** (10 connections) — `tests/test_langchain_integration.py`
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
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_overlap_must_be_smaller_than_chunk_size()** (3 connections) — `tests/test_chunking.py`
- **BaseModel** (1 connections)
- **Splits on the coarsest separator that keeps chunks under the target size. Falls…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Chunking tests. Chunk id stability is the load-bearing property here: ingestion…** (1 connections) — `tests/test_chunking.py`
- **Ingestion skips unchanged documents by hash; ids must not drift.** (1 connections) — `tests/test_chunking.py`
- *... and 6 more nodes in this community*

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (19 shared connections)
- [Chunker Registration](Chunker_Registration.md) (10 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (3 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (2 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (2 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (1 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)
- [OSCRetriever()](OSCRetriever%28%29.md) (1 shared connections)
- [NoopReranker](NoopReranker.md) (1 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (1 shared connections)
- [Settings Schema](Settings_Schema.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/recursive.py`
- `tests/test_chunking.py`
- `tests/test_inspection.py`
- `tests/test_langchain_integration.py`

## Audit Trail

- EXTRACTED: 99 (56%)
- INFERRED: 77 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*