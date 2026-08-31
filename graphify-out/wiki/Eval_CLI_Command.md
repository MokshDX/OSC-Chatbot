# Eval CLI Command

> 31 nodes

## Key Concepts

- **ChatModel** (29 connections) — `src/osc_assistant/protocols.py`
- **DocumentSummary** (19 connections) — `src/osc_assistant/types.py`
- **StoreInspector** (16 connections) — `src/osc_assistant/protocols.py`
- **IndexStatistics** (14 connections) — `src/osc_assistant/types.py`
- **Protocol** (7 connections)
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **._summarise()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.statistics()** (3 connections) — `src/osc_assistant/protocols.py`
- **.list_documents()** (3 connections) — `src/osc_assistant/protocols.py`
- **.get_document()** (3 connections) — `src/osc_assistant/protocols.py`
- **.document_chunks()** (3 connections) — `src/osc_assistant/protocols.py`
- **.get_chunk()** (3 connections) — `src/osc_assistant/protocols.py`
- **.statistics()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.list_documents()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.get_document()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_percentile()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.model_id()** (2 connections) — `src/osc_assistant/protocols.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/protocols.py`
- **A text-generating model.** (1 connections) — `src/osc_assistant/protocols.py`
- **The provider's identifier for the underlying model, for logs and traces.** (1 connections) — `src/osc_assistant/protocols.py`
- **True if the provider resolves citations itself from structured sources. When…** (1 connections) — `src/osc_assistant/protocols.py`
- **Read-only introspection of what a store currently holds. Kept **separate from…** (1 connections) — `src/osc_assistant/protocols.py`
- **Corpus-wide counts and chunk-size distribution.** (1 connections) — `src/osc_assistant/protocols.py`
- **Indexed documents, newest first. `search` matches title or source URI.** (1 connections) — `src/osc_assistant/protocols.py`
- **One document's index record, or None if it is not indexed.** (1 connections) — `src/osc_assistant/protocols.py`
- *... and 6 more nodes in this community*

## Relationships

- [Conversational Evaluator](Conversational_Evaluator.md) (11 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (10 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (6 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (5 shared connections)
- [Logging System Design](Logging_System_Design.md) (4 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (4 shared connections)
- [Protocol Seams & Container](Protocol_Seams_%26_Container.md) (4 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (3 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (3 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (3 shared connections)
- [Default Local Profile](Default_Local_Profile.md) (3 shared connections)
- [Conversation Turn Orchestration](Conversation_Turn_Orchestration.md) (2 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 111 (80%)
- INFERRED: 28 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*