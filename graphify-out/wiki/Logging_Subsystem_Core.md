# Logging Subsystem Core

> 29 nodes · cohesion 0.10

## Key Concepts

- **logging.py** (29 connections) — `src/osc_assistant/logging.py`
- **configure_logging()** (12 connections) — `src/osc_assistant/logging.py`
- **LogRecord** (6 connections)
- **RedactionFilter** (5 connections) — `src/osc_assistant/logging.py`
- **_AuditOnly** (4 connections) — `src/osc_assistant/logging.py`
- **_ExcludeAudit** (4 connections) — `src/osc_assistant/logging.py`
- **JsonFormatter** (4 connections) — `src/osc_assistant/logging.py`
- **_NonDestructiveQueueHandler** (4 connections) — `src/osc_assistant/logging.py`
- **shutdown_logging()** (4 connections) — `src/osc_assistant/logging.py`
- **TraceContextFilter** (4 connections) — `src/osc_assistant/logging.py`
- **.format()** (3 connections) — `src/osc_assistant/logging.py`
- **log_directory()** (3 connections) — `src/osc_assistant/logging.py`
- **.filter()** (3 connections) — `src/osc_assistant/logging.py`
- **.filter()** (2 connections) — `src/osc_assistant/logging.py`
- **.filter()** (2 connections) — `src/osc_assistant/logging.py`
- **.prepare()** (2 connections) — `src/osc_assistant/logging.py`
- **Path** (2 connections)
- **.filter()** (2 connections) — `src/osc_assistant/logging.py`
- **Structured logging: what the system did, recorded durably. Tracing and logging…** (1 connections) — `src/osc_assistant/logging.py`
- **Renders records as single-line JSON.** (1 connections) — `src/osc_assistant/logging.py`
- **Stamps the active trace id onto every record. This is the seam between the two…** (1 connections) — `src/osc_assistant/logging.py`
- **Removes credentials, and reduces corpus text to a length unless allowed. A…** (1 connections) — `src/osc_assistant/logging.py`
- **A `QueueHandler` that does not discard the exception it was given. The stdlib…** (1 connections) — `src/osc_assistant/logging.py`
- **Routes only audit records to the audit file.** (1 connections) — `src/osc_assistant/logging.py`
- **Keeps audit records out of the operational stream. They would otherwise appear…** (1 connections) — `src/osc_assistant/logging.py`
- *... and 4 more nodes in this community*

## Relationships

- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (7 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (4 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (3 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (1 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (1 shared connections)
- [Golden Set Schema & Validation](Golden_Set_Schema_%26_Validation.md) (1 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (1 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (1 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (1 shared connections)
- [Shared Test Fixtures & Retrieval Tests](Shared_Test_Fixtures_%26_Retrieval_Tests.md) (1 shared connections)
- [Logging Tests & CLI Command Record](Logging_Tests_%26_CLI_Command_Record.md) (1 shared connections)
- [Search Strategies & Reranking](Search_Strategies_%26_Reranking.md) (1 shared connections)

## Source Files

- `src/osc_assistant/logging.py`

## Audit Trail

- EXTRACTED: 106 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*