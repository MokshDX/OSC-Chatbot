# Chunking Strategies

> 41 nodes · cohesion 0.10

## Key Concepts

- **RecursiveChunker** (23 connections) — `src/osc_assistant/chunking/recursive.py`
- **ChunkerOptions** (22 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_chunking.py** (16 connections) — `tests/test_chunking.py`
- **_document()** (13 connections) — `tests/test_chunking.py`
- **chunking/__init__.py** (11 connections) — `src/osc_assistant/chunking/__init__.py`
- **FixedSizeChunker** (7 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/recursive.py`
- **_to_chunks()** (6 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_chunk_ids_are_stable_across_runs()** (5 connections) — `tests/test_chunking.py`
- **test_chunk_ids_change_when_content_changes()** (5 connections) — `tests/test_chunking.py`
- **test_chunking_preserves_document_content()** (5 connections) — `tests/test_chunking.py`
- **test_document_metadata_is_denormalised_onto_chunks()** (5 connections) — `tests/test_chunking.py`
- **test_unbroken_text_is_still_split()** (5 connections) — `tests/test_chunking.py`
- **_split_keeping_separator()** (4 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_chunking_preserves_content_across_separator_kinds()** (4 connections) — `tests/test_chunking.py`
- **test_chunks_respect_the_size_budget()** (4 connections) — `tests/test_chunking.py`
- **test_empty_document_produces_no_chunks()** (4 connections) — `tests/test_chunking.py`
- **test_fixed_chunker_overlaps_windows()** (4 connections) — `tests/test_chunking.py`
- **test_ordinals_are_contiguous()** (4 connections) — `tests/test_chunking.py`
- **test_short_document_is_a_single_chunk()** (4 connections) — `tests/test_chunking.py`
- **_chunk_id()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **.validated()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **_merge()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- *... and 16 more nodes in this community*

## Relationships

- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (14 shared connections)
- [Chunker Registration](Chunker_Registration.md) (10 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (3 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (2 shared connections)
- [HTTP Layer Tests](HTTP_Layer_Tests.md) (1 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/__init__.py`
- `src/osc_assistant/chunking/recursive.py`
- `tests/test_chunking.py`

## Audit Trail

- EXTRACTED: 140 (71%)
- INFERRED: 56 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*