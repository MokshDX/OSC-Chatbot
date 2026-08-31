# Session Store Internals

> 19 nodes

## Key Concepts

- **settings.py** (38 connections) — `src/osc_assistant/settings.py`
- **container.py** (24 connections) — `src/osc_assistant/container.py`
- **_settings()** (10 connections) — `tests/test_e2e.py`
- **BaseModel** (9 connections)
- **ChunkingSettings** (8 connections) — `src/osc_assistant/settings.py`
- **osc_assistant/__init__.py** (6 connections) — `src/osc_assistant/__init__.py`
- **LoggingSettings** (4 connections) — `src/osc_assistant/settings.py`
- **ObservabilitySettings** (4 connections) — `src/osc_assistant/settings.py`
- **_release()** (3 connections) — `src/osc_assistant/container.py`
- **CorpusSettings** (3 connections) — `src/osc_assistant/settings.py`
- **DatabaseSettings** (3 connections) — `src/osc_assistant/settings.py`
- **ServerSettings** (2 connections) — `src/osc_assistant/settings.py`
- **OSC internal knowledge assistant. A provider-agnostic retrieval-augmented…** (1 connections) — `src/osc_assistant/__init__.py`
- **Composition root. The only module that knows both which providers exist and how…** (1 connections) — `src/osc_assistant/container.py`
- **Close a component if it offers a way to be closed. Probed rather than required…** (1 connections) — `src/osc_assistant/container.py`
- **Configuration. Layered, highest precedence first: process environment, then…** (1 connections) — `src/osc_assistant/settings.py`
- **Which directory is the answer corpus. This is configuration rather than a…** (1 connections) — `src/osc_assistant/settings.py`
- **Where logs are written, how long they are kept, and what may appear in them.…** (1 connections) — `src/osc_assistant/settings.py`
- **How much the system records about its own execution. Defaults are chosen for a…** (1 connections) — `src/osc_assistant/settings.py`

## Relationships

- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (6 shared connections)
- [Span Tree & Trace Core](Span_Tree_%26_Trace_Core.md) (6 shared connections)
- [PgVector SQL & Inspection](PgVector_SQL_%26_Inspection.md) (6 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (5 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (5 shared connections)
- [Document Loaders](Document_Loaders.md) (4 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (4 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (3 shared connections)
- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (3 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (3 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (3 shared connections)
- [API Layer Tests](API_Layer_Tests.md) (3 shared connections)

## Source Files

- `src/osc_assistant/__init__.py`
- `src/osc_assistant/container.py`
- `src/osc_assistant/settings.py`
- `tests/test_e2e.py`

## Audit Trail

- EXTRACTED: 118 (98%)
- INFERRED: 3 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*