# Fusion & Store Statistics

> 19 nodes · cohesion 0.12

## Key Concepts

- **memory.py** (30 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **IndexStatistics** (16 connections) — `src/osc_assistant/types.py`
- **MatchSource** (8 connections) — `src/osc_assistant/types.py`
- **fusion.py** (7 connections) — `src/osc_assistant/fusion.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **vectorstores/__init__.py** (4 connections) — `src/osc_assistant/providers/vectorstores/__init__.py`
- **.statistics()** (3 connections) — `src/osc_assistant/protocols.py`
- **.statistics()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_percentile()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.statistics()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **StrEnum** (2 connections)
- **Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…** (1 connections) — `src/osc_assistant/fusion.py`
- **Corpus-wide counts and chunk-size distribution.** (1 connections) — `src/osc_assistant/protocols.py`
- **Vector store providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/vectorstores/__init__.py`
- **register** (1 connections)
- **In-process vector store. Not a toy: this is what makes the test suite run…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Nearest-rank percentile over a pre-sorted list. Empty input is 0.** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Aggregate state of the index. Chunk length percentiles are here because chunk…** (1 connections) — `src/osc_assistant/types.py`
- **Where a retrieval hit came from. Recorded for tracing and evaluation.** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (6 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (5 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (5 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (4 shared connections)
- [In-Memory Vector Store](In-Memory_Vector_Store.md) (4 shared connections)
- [RRF Fusion & Source Rendering](RRF_Fusion_%26_Source_Rendering.md) (3 shared connections)
- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (3 shared connections)
- [Store Construction & Embedding Calls](Store_Construction_%26_Embedding_Calls.md) (3 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (3 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (2 shared connections)
- [Chunk Types & Document Chunks](Chunk_Types_%26_Document_Chunks.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)

## Source Files

- `src/osc_assistant/fusion.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/vectorstores/__init__.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 86 (93%)
- INFERRED: 6 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*