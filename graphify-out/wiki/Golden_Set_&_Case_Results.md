# Golden Set & Case Results

> 31 nodes

## Key Concepts

- **logging.py** (31 connections) — `src/osc_assistant/logging.py`
- **retrieval/pipeline.py** (24 connections) — `src/osc_assistant/retrieval/pipeline.py`
- **runner.py** (19 connections) — `src/osc_assistant/evaluation/runner.py`
- **conversational.py** (18 connections) — `src/osc_assistant/evaluation/conversational.py`
- **ingestion/pipeline.py** (16 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **judge.py** (15 connections) — `src/osc_assistant/evaluation/judge.py`
- **rewrite.py** (14 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **get_logger()** (11 connections) — `src/osc_assistant/logging.py`
- **Role** (8 connections) — `src/osc_assistant/types.py`
- **mean_of()** (8 connections) — `src/osc_assistant/evaluation/metrics.py`
- **configuration_snapshot()** (8 connections) — `src/osc_assistant/evaluation/runner.py`
- **.is_faithful()** (6 connections) — `src/osc_assistant/evaluation/judge.py`
- **LoadFailure** (6 connections) — `src/osc_assistant/types.py`
- **FaithfulnessJudge** (4 connections) — `src/osc_assistant/evaluation/judge.py`
- **_parse_verdict()** (3 connections) — `src/osc_assistant/evaluation/judge.py`
- **StrEnum** (3 connections)
- **.__init__()** (2 connections) — `src/osc_assistant/evaluation/judge.py`
- **LLM-as-judge faithfulness scoring. Faithfulness asks whether every claim in an…** (1 connections) — `src/osc_assistant/evaluation/judge.py`
- **Scores one answer against the passages it was generated from.** (1 connections) — `src/osc_assistant/evaluation/judge.py`
- **Return True, False, or None when the judge could not be reached. `None` rather…** (1 connections) — `src/osc_assistant/evaluation/judge.py`
- **Read a one-word verdict out of whatever the model actually returned. Substring…** (1 connections) — `src/osc_assistant/evaluation/judge.py`
- **The ingestion pipeline: documents in, embedded chunks in the store. Idempotent…** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **Logger** (1 connections)
- **Structured logging: what the system did, recorded durably. Tracing and logging…** (1 connections) — `src/osc_assistant/logging.py`
- **The retrieval pipeline: question in, ranked chunks out. rewrite -> search…** (1 connections) — `src/osc_assistant/retrieval/pipeline.py`
- *... and 6 more nodes in this community*

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (12 shared connections)
- [Evaluation Runner Tests](Evaluation_Runner_Tests.md) (10 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (9 shared connections)
- [Suite Loading & Validation](Suite_Loading_%26_Validation.md) (9 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (6 shared connections)
- [Logging System Design](Logging_System_Design.md) (6 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (6 shared connections)
- [Session Memory Architecture](Session_Memory_Architecture.md) (6 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (5 shared connections)
- [OpenAI-Compatible Provider](OpenAI-Compatible_Provider.md) (5 shared connections)
- [LangChain Integration Tests](LangChain_Integration_Tests.md) (4 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (4 shared connections)

## Source Files

- `src/osc_assistant/evaluation/conversational.py`
- `src/osc_assistant/evaluation/judge.py`
- `src/osc_assistant/evaluation/metrics.py`
- `src/osc_assistant/evaluation/runner.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/logging.py`
- `src/osc_assistant/retrieval/pipeline.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 209 (100%)
- INFERRED: 1 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*