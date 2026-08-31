# Test Doubles & Stubs

> 27 nodes

## Key Concepts

- **diagnose.py** (39 connections) — `src/osc_assistant/cli/diagnose.py`
- **Settings** (37 connections) — `src/osc_assistant/settings.py`
- **_run_checks()** (12 connections) — `src/osc_assistant/cli/diagnose.py`
- **Check** (10 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_store()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_chunker()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_reranker()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_llm()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_check_langchain()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **_traces_from()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **Path** (4 connections)
- **_check_corpus()** (4 connections) — `src/osc_assistant/cli/diagnose.py`
- **_redact()** (4 connections) — `src/osc_assistant/cli/diagnose.py`
- **Any** (3 connections)
- **_document_payload()** (3 connections) — `src/osc_assistant/cli/diagnose.py`
- **_fetch_traces()** (3 connections) — `src/osc_assistant/cli/diagnose.py`
- **_statistics_payload()** (2 connections) — `src/osc_assistant/cli/diagnose.py`
- **Trace** (2 connections)
- **.traces_are_exposed()** (2 connections) — `src/osc_assistant/settings.py`
- **.marker()** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **DocumentSummary** (1 connections)
- **Diagnostics and inspection: understanding the system without reading its…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **One diagnostic result. `status` is deliberately three-valued. A warning is a…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Report the LangChain versions in play. Both are core dependencies.** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Blank anything whose key suggests a credential. Name-based rather than value-…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- *... and 2 more nodes in this community*

## Relationships

- [Logging Filters & Audit Stream](Logging_Filters_%26_Audit_Stream.md) (16 shared connections)
- [RRF Fusion & Citation Parsing](RRF_Fusion_%26_Citation_Parsing.md) (9 shared connections)
- [Session Store Internals](Session_Store_Internals.md) (6 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (6 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (4 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (4 shared connections)
- [Chunking & Embedding Architecture](Chunking_%26_Embedding_Architecture.md) (3 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (2 shared connections)
- [Settings Validators](Settings_Validators.md) (2 shared connections)
- [Lifecycle Release Doubles](Lifecycle_Release_Doubles.md) (2 shared connections)
- [Core CLI Commands](Core_CLI_Commands.md) (1 shared connections)
- [FastAPI Routes & Session Endpoints](FastAPI_Routes_%26_Session_Endpoints.md) (1 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/settings.py`

## Audit Trail

- EXTRACTED: 158 (97%)
- INFERRED: 5 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*