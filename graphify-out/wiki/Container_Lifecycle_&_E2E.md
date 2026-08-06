# Container Lifecycle & E2E

> 33 nodes · cohesion 0.06

## Key Concepts

- **Container** (60 connections) — `src/osc_assistant/container.py`
- **osc_assistant/__init__.py** (6 connections) — `src/osc_assistant/__init__.py`
- **.shutdown()** (4 connections) — `src/osc_assistant/container.py`
- **.__aenter__()** (3 connections) — `src/osc_assistant/container.py`
- **.fast_llm()** (3 connections) — `src/osc_assistant/container.py`
- **_release()** (3 connections) — `src/osc_assistant/container.py`
- **test_a_binary_format_is_answerable()** (3 connections) — `tests/test_e2e.py`
- **test_a_corpus_of_six_formats_indexes()** (3 connections) — `tests/test_e2e.py`
- **test_a_grounded_answer_cites_the_source_it_came_from()** (3 connections) — `tests/test_e2e.py`
- **test_a_question_the_corpus_cannot_answer_is_declined()** (3 connections) — `tests/test_e2e.py`
- **test_hybrid_retrieval_ranks_the_right_document_first()** (3 connections) — `tests/test_e2e.py`
- **test_the_run_is_fully_traced()** (3 connections) — `tests/test_e2e.py`
- **test_the_streamed_and_buffered_paths_agree_on_abstention()** (3 connections) — `tests/test_e2e.py`
- **.__aexit__()** (2 connections) — `src/osc_assistant/container.py`
- **.embeddings()** (2 connections) — `src/osc_assistant/container.py`
- **.ingestion()** (2 connections) — `src/osc_assistant/container.py`
- **.__init__()** (2 connections) — `src/osc_assistant/container.py`
- **.llm()** (2 connections) — `src/osc_assistant/container.py`
- **.reranker()** (2 connections) — `src/osc_assistant/container.py`
- **.startup()** (2 connections) — `src/osc_assistant/container.py`
- **Self** (1 connections)
- **A cheaper model for auxiliary steps such as query rewriting.** (1 connections) — `src/osc_assistant/container.py`
- **Release everything that was actually built. Only components whose…** (1 connections) — `src/osc_assistant/container.py`
- **Close a component if it offers a way to be closed. Probed rather than required…** (1 connections) — `src/osc_assistant/container.py`
- **Builds and owns the application's components.** (1 connections) — `src/osc_assistant/container.py`
- *... and 8 more nodes in this community*

## Relationships

- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (16 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (9 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (5 shared connections)
- [Startup Banner & Lifecycle](Startup_Banner_%26_Lifecycle.md) (4 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (4 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (3 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (3 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (2 shared connections)
- [Evaluator & Judge Composition](Evaluator_%26_Judge_Composition.md) (2 shared connections)
- [Store Construction & Embedding Calls](Store_Construction_%26_Embedding_Calls.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (2 shared connections)

## Source Files

- `src/osc_assistant/__init__.py`
- `src/osc_assistant/container.py`
- `tests/test_e2e.py`

## Audit Trail

- EXTRACTED: 117 (92%)
- INFERRED: 10 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*