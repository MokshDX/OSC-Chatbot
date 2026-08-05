# Faithfulness Judge & Answer Events

> 46 nodes

## Key Concepts

- **types.py** (64 connections) — `src/osc_assistant/types.py`
- **answerer.py** (31 connections) — `src/osc_assistant/generation/answerer.py`
- **Message** (27 connections) — `src/osc_assistant/types.py`
- **judge.py** (15 connections) — `src/osc_assistant/evaluation/judge.py`
- **rewrite.py** (14 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **.stream()** (12 connections) — `src/osc_assistant/generation/answerer.py`
- **Role** (11 connections) — `src/osc_assistant/types.py`
- **._finalise()** (10 connections) — `src/osc_assistant/generation/answerer.py`
- **.answer()** (9 connections) — `src/osc_assistant/generation/answerer.py`
- **_bridge()** (9 connections) — `tests/test_langchain_integration.py`
- **._abstention()** (8 connections) — `src/osc_assistant/generation/answerer.py`
- **.is_faithful()** (6 connections) — `src/osc_assistant/evaluation/judge.py`
- **_annotate_generation()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **._build_request()** (6 connections) — `src/osc_assistant/generation/answerer.py`
- **.rewrite()** (6 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **RetrievalReady** (5 connections) — `src/osc_assistant/generation/answerer.py`
- **AnswerComplete** (5 connections) — `src/osc_assistant/generation/answerer.py`
- **test_bridge_streams_text_then_citations()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_reports_an_empty_completion_rather_than_abstaining()** (5 connections) — `tests/test_langchain_integration.py`
- **test_bridge_strips_a_leaked_reasoning_block()** (5 connections) — `tests/test_langchain_integration.py`
- **test_rewrite_failure_falls_back_to_the_original_question()** (5 connections) — `tests/test_retrieval.py`
- **.to_domain()** (4 connections) — `src/osc_assistant/api/schemas.py`
- **_parse_verdict()** (4 connections) — `src/osc_assistant/evaluation/judge.py`
- **_annotate_abstention()** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **test_bridge_translates_a_completion_and_parses_citations()** (4 connections) — `tests/test_langchain_integration.py`
- *... and 21 more nodes in this community*

## Relationships

- [Chat Request & Response Types](Chat_Request_%26_Response_Types.md) (22 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (15 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (11 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (11 shared connections)
- [Evaluator & Answerer Composition](Evaluator_%26_Answerer_Composition.md) (10 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (10 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (8 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (8 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (7 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (4 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (4 shared connections)
- [generation/__init__.py](generation-__init__.py.md) (4 shared connections)

## Source Files

- `src/osc_assistant/api/schemas.py`
- `src/osc_assistant/evaluation/judge.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `src/osc_assistant/types.py`
- `tests/test_langchain_integration.py`
- `tests/test_retrieval.py`

## Audit Trail

- EXTRACTED: 300 (98%)
- INFERRED: 5 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*