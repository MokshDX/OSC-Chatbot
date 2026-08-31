# Logging System Design

> 20 nodes

## Key Concepts

- **ScoredChunk** (36 connections) — `src/osc_assistant/types.py`
- **pgvector.py** (30 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_to_scored_chunk()** (8 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **MatchSource** (8 connections) — `src/osc_assistant/types.py`
- **fusion.py** (7 connections) — `src/osc_assistant/fusion.py`
- **langchain.py** (7 connections) — `src/osc_assistant/integrations/langchain.py`
- **_encode_vector()** (7 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_vector()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **to_langchain_document()** (4 connections) — `src/osc_assistant/integrations/langchain.py`
- **.search_keyword()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Vector** (3 connections)
- **Reciprocal Rank Fusion. Combining a lexical and a vector ranking cannot be done…** (1 connections) — `src/osc_assistant/fusion.py`
- **LangChainDocument** (1 connections)
- **Exposing OSC to LangChain, rather than the other way round. Every other…** (1 connections) — `src/osc_assistant/integrations/langchain.py`
- **Translate one retrieval hit into a LangChain document. The score and the match…** (1 connections) — `src/osc_assistant/integrations/langchain.py`
- **PostgreSQL + pgvector store: the production default. One datastore holds chunk…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Render a vector in pgvector's literal form for the `::vector` cast.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Where a retrieval hit came from. Recorded for tracing and evaluation.** (1 connections) — `src/osc_assistant/types.py`
- **A chunk with a relevance score. Scores are only comparable within a single…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (18 shared connections)
- [Protocol Seams & Container](Protocol_Seams_%26_Container.md) (15 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (6 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (6 shared connections)
- [Regression Gate Tests](Regression_Gate_Tests.md) (4 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (4 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (4 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (4 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (3 shared connections)
- [Default Local Profile](Default_Local_Profile.md) (3 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (3 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (1 shared connections)

## Source Files

- `src/osc_assistant/fusion.py`
- `src/osc_assistant/integrations/langchain.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 128 (96%)
- INFERRED: 6 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*