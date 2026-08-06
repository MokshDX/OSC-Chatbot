# Answer Generation & Faithfulness Judge

> 59 nodes · cohesion 0.07

## Key Concepts

- **types.py** (64 connections) — `src/osc_assistant/types.py`
- **answerer.py** (33 connections) — `src/osc_assistant/generation/answerer.py`
- **Message** (27 connections) — `src/osc_assistant/types.py`
- **retrieval/pipeline.py** (23 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **annotate()** (17 connections) — `src/osc_assistant/observability/trace.py`
- **judge.py** (15 connections) — `src/osc_assistant/evaluation/judge.py`
- **QueryRewriter** (15 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **rewrite.py** (14 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **Answer** (14 connections) — `src/osc_assistant/types.py`
- **.stream()** (12 connections) — `src/osc_assistant/generation/answerer.py`
- **current_trace_id()** (12 connections) — `src/osc_assistant/observability/trace.py`
- **._finalise()** (11 connections) — `src/osc_assistant/generation/answerer.py`
- **RetrievalResult** (11 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Role** (11 connections) — `src/osc_assistant/types.py`
- **retrieval/__init__.py** (10 connections) — `src/osc_assistant/retrieval/__init__.py`
- **.retrieve()** (10 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **._abstention()** (9 connections) — `src/osc_assistant/generation/answerer.py`
- **.answer()** (9 connections) — `src/osc_assistant/generation/answerer.py`
- **_audit_answer()** (7 connections) — `src/osc_assistant/generation/answerer.py`
- **annotate_text()** (7 connections) — `src/osc_assistant/observability/trace.py`
- **.get()** (7 connections) — `src/osc_assistant/observability/trace.py`
- **_annotate_generation()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **._build_request()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **.rewrite()** (6 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **AnswerComplete** (5 connections) — `src/osc_assistant/generation/answerer.py`
- *... and 34 more nodes in this community*

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (21 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (14 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (12 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (10 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (8 shared connections)
- [API Request & Response Schemas](API_Request_%26_Response_Schemas.md) (8 shared connections)
- [Logging Subsystem Core](Logging_Subsystem_Core.md) (7 shared connections)
- [LangChain Bridges & Splitters](LangChain_Bridges_%26_Splitters.md) (7 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (6 shared connections)
- [Trace Configuration & CLI Trace](Trace_Configuration_%26_CLI_Trace.md) (6 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (6 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (6 shared connections)

## Source Files

- `src/osc_assistant/evaluation/judge.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/logging.py`
- `src/osc_assistant/observability/trace.py`
- `src/osc_assistant/retrieval/__init__.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `src/osc_assistant/types.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 399 (96%)
- INFERRED: 16 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*