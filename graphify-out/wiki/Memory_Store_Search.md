# Memory Store Search

> 14 nodes

## Key Concepts

- **memory.py** (30 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_vector()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_keyword()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Vector** (3 connections)
- **.statistics()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_percentile()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_cosine_similarity()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_tokenize()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **register** (1 connections)
- **In-process vector store. Not a toy: this is what makes the test suite run…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Nearest-rank percentile over a pre-sorted list. Empty input is 0.** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`

## Relationships

- [In-Memory Vector Store](In-Memory_Vector_Store.md) (7 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (6 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (4 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (3 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [IndexStatistics](IndexStatistics.md) (2 shared connections)
- [DimensionMismatchError](DimensionMismatchError.md) (1 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (1 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)
- [Store Inspector](Store_Inspector.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/memory.py`

## Audit Trail

- EXTRACTED: 69 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*