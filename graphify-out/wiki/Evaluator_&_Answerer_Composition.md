# Evaluator & Answerer Composition

> 26 nodes

## Key Concepts

- **RetrievalPipeline** (34 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Evaluator** (22 connections) — `src/osc_assistant/evaluation/runner.py`
- **Answerer** (18 connections) — `src/osc_assistant/generation/answerer.py`
- **FaithfulnessJudge** (14 connections) — `src/osc_assistant/evaluation/judge.py`
- **_settings()** (12 connections) — `tests/test_evaluation.py`
- **test_a_judge_failure_records_no_verdict_rather_than_a_wrong_one()** (10 connections) — `tests/test_evaluation.py`
- **_golden()** (9 connections) — `tests/test_evaluation.py`
- **test_the_judge_sees_the_passages_the_answer_was_built_from()** (8 connections) — `tests/test_evaluation.py`
- **test_a_generation_run_scores_citations_against_what_was_retrieved()** (7 connections) — `tests/test_evaluation.py`
- **test_a_missing_expected_fact_is_named_not_just_counted()** (7 connections) — `tests/test_evaluation.py`
- **test_a_retrieval_only_run_reports_no_generation_metrics()** (6 connections) — `tests/test_evaluation.py`
- **test_a_failing_provider_costs_one_case_not_the_whole_run()** (6 connections) — `tests/test_evaluation.py`
- **.__init__()** (5 connections) — `src/osc_assistant/evaluation/runner.py`
- **test_a_retrieval_run_scores_the_documents_it_found()** (5 connections) — `tests/test_evaluation.py`
- **test_the_configuration_that_produced_the_numbers_travels_with_them()** (5 connections) — `tests/test_evaluation.py`
- **.__init__()** (4 connections) — `src/osc_assistant/generation/answerer.py`
- **test_concurrency_does_not_change_the_result()** (4 connections) — `tests/test_evaluation.py`
- **._resolve_query()** (3 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **.answerer()** (2 connections) — `src/osc_assistant/container.py`
- **.__init__()** (2 connections) — `src/osc_assistant/evaluation/judge.py`
- **Scores one answer against the passages it was generated from.** (1 connections) — `src/osc_assistant/evaluation/judge.py`
- **Runs a golden set and scores it. Takes the pipelines rather than the…** (1 connections) — `src/osc_assistant/evaluation/runner.py`
- **Answers a question against the indexed corpus.** (1 connections) — `src/osc_assistant/generation/answerer.py`
- **Composes rewriting, search and reranking into one call.** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **Regression: `fact_match` used to read 1.0 for a run that generated nothing.…** (1 connections) — `tests/test_evaluation.py`
- *... and 1 more nodes in this community*

## Relationships

- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (11 shared connections)
- [Golden Set Loading & Evaluation Tests](Golden_Set_Loading_%26_Evaluation_Tests.md) (11 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (10 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (8 shared connections)
- [Stub Chat Model & Answerer Tests](Stub_Chat_Model_%26_Answerer_Tests.md) (6 shared connections)
- [Settings Schema](Settings_Schema.md) (4 shared connections)
- [Retrieval Pipeline](Retrieval_Pipeline.md) (4 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (3 shared connections)
- [Stub Embedding Model](Stub_Embedding_Model.md) (3 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (2 shared connections)
- [OSCRetriever()](OSCRetriever%28%29.md) (2 shared connections)
- [Tracing & Retrieval Instrumentation](Tracing_%26_Retrieval_Instrumentation.md) (2 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/evaluation/judge.py`
- `src/osc_assistant/evaluation/runner.py`
- `src/osc_assistant/generation/answerer.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `tests/test_evaluation.py`

## Audit Trail

- EXTRACTED: 168 (89%)
- INFERRED: 21 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*