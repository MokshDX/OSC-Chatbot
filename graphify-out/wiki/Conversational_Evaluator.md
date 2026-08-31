# Conversational Evaluator

> 57 nodes

## Key Concepts

- **Document** (54 connections) — `src/osc_assistant/types.py`
- **ComponentConfig** (49 connections) — `src/osc_assistant/registry.py`
- **Chunk** (31 connections) — `src/osc_assistant/types.py`
- **langchain_splitters.py** (23 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **Chunker** (22 connections) — `src/osc_assistant/protocols.py`
- **recursive.py** (21 connections) — `src/osc_assistant/chunking/recursive.py`
- **chunking/__init__.py** (16 connections) — `src/osc_assistant/chunking/__init__.py`
- **to_chunks()** (12 connections) — `src/osc_assistant/chunking/recursive.py`
- **MarkdownChunker** (10 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **LangChainRecursiveChunker** (9 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **FixedSizeChunker** (7 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.split()** (6 connections) — `src/osc_assistant/chunking/recursive.py`
- **test_store_rejects_wrong_width_vectors()** (6 connections) — `tests/test_retrieval.py`
- **_require_splitters()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_build_langchain_recursive()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_build_markdown()** (5 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **.split()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **normalize_whitespace()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **_build_recursive()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **_build_fixed()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (4 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_heading_path()** (4 connections) — `src/osc_assistant/chunking/langchain_splitters.py`
- **_split_keeping_separator()** (4 connections) — `src/osc_assistant/chunking/recursive.py`
- **.split()** (4 connections) — `src/osc_assistant/protocols.py`
- *... and 32 more nodes in this community*

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (30 shared connections)
- [PgVector Store](PgVector_Store.md) (20 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (12 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (11 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (10 shared connections)
- [Protocol Seams & Container](Protocol_Seams_%26_Container.md) (10 shared connections)
- [ADR 0001 Protocol Seams](ADR_0001_Protocol_Seams.md) (7 shared connections)
- [Gemini Adapter](Gemini_Adapter.md) (6 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (6 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (5 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (4 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (4 shared connections)

## Source Files

- `src/osc_assistant/chunking/__init__.py`
- `src/osc_assistant/chunking/langchain_splitters.py`
- `src/osc_assistant/chunking/recursive.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/registry.py`
- `src/osc_assistant/types.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 332 (89%)
- INFERRED: 42 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*