# Dimension Guard & Match Source

> 12 nodes · cohesion 0.17

## Key Concepts

- **memory.py** (24 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **MatchSource** (8 connections) — `src/osc_assistant/types.py`
- **DimensionMismatchError** (6 connections) — `src/osc_assistant/errors.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.__init__()** (3 connections) — `src/osc_assistant/errors.py`
- **.__init__()** (2 connections) — `src/osc_assistant/errors.py`
- **.__init__()** (2 connections) — `src/osc_assistant/errors.py`
- **StrEnum** (2 connections)
- **The configured embedding model does not match the store's vector width.…** (1 connections) — `src/osc_assistant/errors.py`
- **register** (1 connections)
- **In-process vector store. Not a toy: this is what makes the test suite run…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Where a retrieval hit came from. Recorded for tracing and evaluation.** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Error Hierarchy](Error_Hierarchy.md) (8 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (6 shared connections)
- [Rank Fusion & Citation Grounding](Rank_Fusion_%26_Citation_Grounding.md) (3 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (3 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (2 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (2 shared connections)
- [Provider Registry](Provider_Registry.md) (1 shared connections)
- [Provider Package Registration](Provider_Package_Registration.md) (1 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (1 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 56 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*