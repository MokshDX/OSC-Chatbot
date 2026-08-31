# Ingestion Loaders & Parsers

> 62 nodes

## Key Concepts

- **types.py** (69 connections) — `src/osc_assistant/types.py`
- **protocols.py** (44 connections) — `src/osc_assistant/protocols.py`
- **errors.py** (40 connections) — `src/osc_assistant/errors.py`
- **registries.py** (31 connections) — `src/osc_assistant/registries.py`
- **MissingDependencyError** (29 connections) — `src/osc_assistant/errors.py`
- **registry.py** (29 connections) — `src/osc_assistant/registry.py`
- **memory.py** (28 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **ConfigurationError** (25 connections) — `src/osc_assistant/errors.py`
- **embeddings/langchain_bridge.py** (18 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **embeddings/gemini.py** (15 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **embeddings/openai_compatible.py** (15 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **cross_encoder.py** (15 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **local.py** (14 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **voyage.py** (14 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **noop.py** (14 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **DimensionMismatchError** (9 connections) — `src/osc_assistant/errors.py`
- **UnknownComponentError** (8 connections) — `src/osc_assistant/errors.py`
- **embeddings/__init__.py** (7 connections) — `src/osc_assistant/providers/embeddings/__init__.py`
- **providers/__init__.py** (6 connections) — `src/osc_assistant/providers/__init__.py`
- **_instantiate()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **.__init__()** (5 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **.__init__()** (4 connections) — `src/osc_assistant/providers/llm/gemini.py`
- *... and 37 more nodes in this community*

## Relationships

- [Conversational Evaluator](Conversational_Evaluator.md) (30 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (18 shared connections)
- [Logging System Design](Logging_System_Design.md) (18 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (12 shared connections)
- [Chunker Registration](Chunker_Registration.md) (11 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (11 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (10 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (9 shared connections)
- [Logging Tests](Logging_Tests.md) (9 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (9 shared connections)
- [Default Local Profile](Default_Local_Profile.md) (9 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (8 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/__init__.py`
- `src/osc_assistant/providers/embeddings/__init__.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/openai_compatible.py`
- `src/osc_assistant/providers/embeddings/voyage.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/providers/llm/openai_compatible.py`
- `src/osc_assistant/providers/reranking/__init__.py`
- `src/osc_assistant/providers/reranking/cross_encoder.py`
- `src/osc_assistant/providers/reranking/noop.py`
- `src/osc_assistant/providers/vectorstores/__init__.py`
- `src/osc_assistant/providers/vectorstores/memory.py`
- `src/osc_assistant/registries.py`
- `src/osc_assistant/registry.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 507 (99%)
- INFERRED: 5 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*