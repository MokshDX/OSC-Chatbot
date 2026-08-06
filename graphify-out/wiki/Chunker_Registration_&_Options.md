# Chunker Registration & Options

> 31 nodes · cohesion 0.15

## Key Concepts

- **ChunkerOptions** (31 connections) — `src/osc_assistant/chunking/recursive.py`
- **RecursiveChunker** (28 connections) — `src/osc_assistant/chunking/recursive.py`
- **chunking/__init__.py** (18 connections) — `src/osc_assistant/chunking/__init__.py`
- **test_chunking.py** (16 connections) — `tests/test_chunking.py`
- **_document()** (13 connections) — `tests/test_chunking.py`
- **pipeline()** (7 connections) — `tests/test_ingestion.py`
- **test_chunk_ids_are_stable_across_runs()** (5 connections) — `tests/test_chunking.py`
- **test_chunk_ids_change_when_content_changes()** (5 connections) — `tests/test_chunking.py`
- **test_chunking_preserves_document_content()** (5 connections) — `tests/test_chunking.py`
- **test_document_metadata_is_denormalised_onto_chunks()** (5 connections) — `tests/test_chunking.py`
- **test_unbroken_text_is_still_split()** (5 connections) — `tests/test_chunking.py`
- **test_chunking_preserves_content_across_separator_kinds()** (4 connections) — `tests/test_chunking.py`
- **test_chunks_respect_the_size_budget()** (4 connections) — `tests/test_chunking.py`
- **test_empty_document_produces_no_chunks()** (4 connections) — `tests/test_chunking.py`
- **test_fixed_chunker_overlaps_windows()** (4 connections) — `tests/test_chunking.py`
- **test_ordinals_are_contiguous()** (4 connections) — `tests/test_chunking.py`
- **test_short_document_is_a_single_chunk()** (4 connections) — `tests/test_chunking.py`
- **.validated()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **.__init__()** (3 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_overlap_must_be_smaller_than_chunk_size()** (3 connections) — `tests/test_chunking.py`
- **Chunking strategies. Imported for registration side effects.** (1 connections) — `src/osc_assistant/chunking/__init__.py`
- **BaseModel** (1 connections)
- **Splits on the coarsest separator that keeps chunks under the target size. Falls…** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Chunking tests. Chunk id stability is the load-bearing property here: ingestion…** (1 connections) — `tests/test_chunking.py`
- *... and 6 more nodes in this community*

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (16 shared connections)
- [Recursive & Markdown Splitting](Recursive_%26_Markdown_Splitting.md) (14 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (4 shared connections)
- [LangChain Bridges & Splitters](LangChain_Bridges_%26_Splitters.md) (3 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (2 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (2 shared connections)
- [Noop Reranker & Evaluation Corpus](Noop_Reranker_%26_Evaluation_Corpus.md) (2 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (1 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (1 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (1 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (1 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/__init__.py`
- `src/osc_assistant/chunking/recursive.py`
- `tests/test_chunking.py`
- `tests/test_ingestion.py`

## Audit Trail

- EXTRACTED: 114 (62%)
- INFERRED: 70 (38%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*