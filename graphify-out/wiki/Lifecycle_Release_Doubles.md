# Lifecycle Release Doubles

> 10 nodes

## Key Concepts

- **_SyncClosableReranker** (23 connections) — `tests/test_server_lifecycle.py`
- **_ClosableEmbedding** (21 connections) — `tests/test_server_lifecycle.py`
- **.__init__()** (2 connections) — `tests/test_server_lifecycle.py`
- **.__init__()** (2 connections) — `tests/test_server_lifecycle.py`
- **.aclose()** (1 connections) — `tests/test_server_lifecycle.py`
- **.model_id()** (1 connections) — `tests/test_server_lifecycle.py`
- **.rerank()** (1 connections) — `tests/test_server_lifecycle.py`
- **.close()** (1 connections) — `tests/test_server_lifecycle.py`
- **Holds a resource, like the Voyage and OpenAI adapters do.** (1 connections) — `tests/test_server_lifecycle.py`
- **Closes synchronously, to prove both shapes are handled.** (1 connections) — `tests/test_server_lifecycle.py`

## Relationships

- [Recursive Chunker](Recursive_Chunker.md) (6 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (4 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (4 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (4 shared connections)
- [Evaluation Framework Rationale](Evaluation_Framework_Rationale.md) (4 shared connections)
- [OpenAI-Compatible Embeddings](OpenAI-Compatible_Embeddings.md) (2 shared connections)
- [Voyage Embeddings](Voyage_Embeddings.md) (2 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (2 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (2 shared connections)
- [Document Loaders](Document_Loaders.md) (2 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (2 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (2 shared connections)

## Source Files

- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 22 (41%)
- INFERRED: 32 (59%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*