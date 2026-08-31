# Default Local Profile

> 17 nodes

## Key Concepts

- **Reranker** (20 connections) — `src/osc_assistant/protocols.py`
- **CrossEncoderReranker** (7 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **.rerank()** (3 connections) — `src/osc_assistant/protocols.py`
- **CrossEncoderOptions** (3 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **.__init__()** (3 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **.rerank()** (2 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **.model_id()** (1 connections) — `src/osc_assistant/protocols.py`
- **A second-stage relevance model applied to retrieval candidates.** (1 connections) — `src/osc_assistant/protocols.py`
- **Return the `top_k` most relevant candidates, most relevant first.** (1 connections) — `src/osc_assistant/protocols.py`
- **BaseModel** (1 connections)
- **.model_id()** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **._score()** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **register** (1 connections)
- **Adapter over a `sentence-transformers` CrossEncoder.** (1 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **register** (1 connections)

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (9 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (4 shared connections)
- [Eval CLI Command](Eval_CLI_Command.md) (3 shared connections)
- [Logging System Design](Logging_System_Design.md) (3 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (1 shared connections)
- [Recursive Chunker](Recursive_Chunker.md) (1 shared connections)
- [Memory Vector Store](Memory_Vector_Store.md) (1 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (1 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (1 shared connections)
- [Evaluation Framework ADR](Evaluation_Framework_ADR.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/reranking/cross_encoder.py`
- `src/osc_assistant/providers/reranking/noop.py`

## Audit Trail

- EXTRACTED: 49 (86%)
- INFERRED: 8 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*