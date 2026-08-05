# Retrieval Pipeline

> 12 nodes

## Key Concepts

- **retrieval/pipeline.py** (23 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **QueryRewriter** (15 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **retrieval/__init__.py** (10 connections) — `src/osc_assistant/retrieval/__init__.py`
- **RetrievalResult** (10 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.retrieval()** (3 connections) — `src/osc_assistant/container.py`
- **.__init__()** (2 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **.model_id()** (2 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **Retrieval: query rewriting, search and reranking.** (1 connections) — `src/osc_assistant/retrieval/__init__.py`
- **The retrieval pipeline: question in, ranked chunks out. rewrite -> search…** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Ranked chunks plus everything needed to explain how they were selected.…** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Turns a conversational turn into a standalone retrieval query.** (1 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **The model doing the rewriting, for traces and logs.** (1 connections) — `src/osc_assistant/retrieval/rewrite.py`

## Relationships

- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (11 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (4 shared connections)
- [Execution Tracing Core](Execution_Tracing_Core.md) (3 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (3 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (2 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)
- [Settings Schema](Settings_Schema.md) (2 shared connections)
- [Rank Fusion & Source Rendering](Rank_Fusion_%26_Source_Rendering.md) (2 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (1 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (1 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/retrieval/__init__.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/retrieval/rewrite.py`

## Audit Trail

- EXTRACTED: 64 (91%)
- INFERRED: 6 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*