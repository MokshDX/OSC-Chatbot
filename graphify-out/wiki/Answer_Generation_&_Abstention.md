# Answer Generation & Abstention

> 47 nodes · cohesion 0.07

## Key Concepts

- **retrieval/pipeline.py** (18 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Message** (18 connections) — `src/osc_assistant/types.py`
- **RetrievalPipeline** (16 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **QueryRewriter** (14 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **rewrite.py** (13 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **Answerer** (11 connections) — `src/osc_assistant/generation/answerer.py`
- **.stream()** (10 connections) — `src/osc_assistant/generation/answerer.py`
- **RetrievalResult** (10 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **._finalise()** (8 connections) — `src/osc_assistant/generation/answerer.py`
- **retrieval/__init__.py** (8 connections) — `src/osc_assistant/retrieval/__init__.py`
- **Answer** (8 connections) — `src/osc_assistant/types.py`
- **.answer()** (7 connections) — `src/osc_assistant/generation/answerer.py`
- **generation/__init__.py** (7 connections) — `src/osc_assistant/generation/__init__.py`
- **._abstention()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **._build_request()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **.__init__()** (6 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.retrieve()** (6 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **AnswerComplete** (5 connections) — `src/osc_assistant/generation/answerer.py`
- **RetrievalReady** (5 connections) — `src/osc_assistant/generation/answerer.py`
- **.rewrite()** (5 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **test_rewrite_failure_falls_back_to_the_original_question()** (5 connections) — `tests/test_retrieval.py`
- **.__init__()** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **.retrieval()** (3 connections) — `src/osc_assistant/container.py`
- **prompts.py** (3 connections) — `src/osc_assistant/generation/prompts.py`
- **._resolve_query()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- *... and 22 more nodes in this community*

## Relationships

- [Error Hierarchy](Error_Hierarchy.md) (16 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (12 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (7 shared connections)
- [Structured Logging](Structured_Logging.md) (6 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (5 shared connections)
- [Settings Schema](Settings_Schema.md) (4 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (3 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (3 shared connections)
- [Composition Root](Composition_Root.md) (2 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (2 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (2 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (2 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/generation/__init__.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/generation/prompts.py`
- `src/osc_assistant/retrieval/__init__.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `src/osc_assistant/types.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 222 (96%)
- INFERRED: 10 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*