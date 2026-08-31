# Evaluation Runner Tests

> 39 nodes

## Key Concepts

- **answerer.py** (35 connections) — `src/osc_assistant/generation/answerer.py`
- **Message** (22 connections) — `src/osc_assistant/types.py`
- **.stream()** (12 connections) — `src/osc_assistant/generation/answerer.py`
- **._finalise()** (11 connections) — `src/osc_assistant/generation/answerer.py`
- **RetrievalResult** (11 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Answerer** (10 connections) — `src/osc_assistant/generation/answerer.py`
- **.retrieve()** (10 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.answer()** (9 connections) — `src/osc_assistant/generation/answerer.py`
- **._abstention()** (9 connections) — `src/osc_assistant/generation/answerer.py`
- **generation/__init__.py** (7 connections) — `src/osc_assistant/generation/__init__.py`
- **_audit_answer()** (7 connections) — `src/osc_assistant/generation/answerer.py`
- **Answer** (7 connections) — `src/osc_assistant/types.py`
- **_annotate_generation()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **._build_request()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **audit()** (5 connections) — `src/osc_assistant/logging.py`
- **RetrievalReady** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **AnswerComplete** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **_annotate_abstention()** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **prompts.py** (3 connections) — `src/osc_assistant/generation/prompts.py`
- **.as_sources()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **._resolve_query()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **AnswerEvent** (2 connections)
- **Answer generation: prompts, citation policy and abstention.** (1 connections) — `src/osc_assistant/generation/__init__.py`
- **Answer generation: the composition of retrieval and a chat model. This is the…** (1 connections) — `src/osc_assistant/generation/answerer.py`
- **Emitted before generation so the client can render sources immediately.** (1 connections) — `src/osc_assistant/generation/answerer.py`
- *... and 14 more nodes in this community*

## Relationships

- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (10 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (10 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (9 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (7 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (6 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (4 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (4 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (2 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (2 shared connections)
- [Document Loaders](Document_Loaders.md) (2 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (2 shared connections)
- [Conversation Turn Orchestration](Conversation_Turn_Orchestration.md) (2 shared connections)

## Source Files

- `src/osc_assistant/generation/__init__.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/generation/prompts.py`
- `src/osc_assistant/logging.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 201 (97%)
- INFERRED: 6 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*