# Suite Loading & Validation

> 27 nodes

## Key Concepts

- **configure_logging()** (10 connections) — `src/osc_assistant/logging.py`
- **LogRecord** (6 connections)
- **RedactionFilter** (5 connections) — `src/osc_assistant/logging.py`
- **JsonFormatter** (4 connections) — `src/osc_assistant/logging.py`
- **TraceContextFilter** (4 connections) — `src/osc_assistant/logging.py`
- **_NonDestructiveQueueHandler** (4 connections) — `src/osc_assistant/logging.py`
- **_AuditOnly** (4 connections) — `src/osc_assistant/logging.py`
- **_ExcludeAudit** (4 connections) — `src/osc_assistant/logging.py`
- **shutdown_logging()** (4 connections) — `src/osc_assistant/logging.py`
- **.format()** (3 connections) — `src/osc_assistant/logging.py`
- **.filter()** (3 connections) — `src/osc_assistant/logging.py`
- **log_directory()** (3 connections) — `src/osc_assistant/logging.py`
- **.filter()** (2 connections) — `src/osc_assistant/logging.py`
- **.prepare()** (2 connections) — `src/osc_assistant/logging.py`
- **.filter()** (2 connections) — `src/osc_assistant/logging.py`
- **.filter()** (2 connections) — `src/osc_assistant/logging.py`
- **Path** (2 connections)
- **.__init__()** (1 connections) — `src/osc_assistant/logging.py`
- **Renders records as single-line JSON.** (1 connections) — `src/osc_assistant/logging.py`
- **Stamps the active trace id onto every record. This is the seam between the two…** (1 connections) — `src/osc_assistant/logging.py`
- **Removes credentials, and reduces corpus text to a length unless allowed. A…** (1 connections) — `src/osc_assistant/logging.py`
- **A `QueueHandler` that does not discard the exception it was given. The stdlib…** (1 connections) — `src/osc_assistant/logging.py`
- **Routes only audit records to the audit file.** (1 connections) — `src/osc_assistant/logging.py`
- **Keeps audit records out of the operational stream. They would otherwise appear…** (1 connections) — `src/osc_assistant/logging.py`
- **Install the logging stack. Safe to call more than once. Parameters are…** (1 connections) — `src/osc_assistant/logging.py`
- *... and 2 more nodes in this community*

## Relationships

- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (9 shared connections)
- [Logging System Design](Logging_System_Design.md) (1 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (1 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)

## Source Files

- `src/osc_assistant/logging.py`

## Audit Trail

- EXTRACTED: 74 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*