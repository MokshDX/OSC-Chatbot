# Startup Banner & Lifecycle

> 8 nodes · cohesion 0.29

## Key Concepts

- **banner.py** (12 connections) — `src/osc_assistant/api/banner.py`
- **startup_notes()** (10 connections) — `src/osc_assistant/api/banner.py`
- **describe_startup()** (7 connections) — `src/osc_assistant/api/banner.py`
- **test_a_non_development_environment_is_called_out()** (5 connections) — `tests/test_server_lifecycle.py`
- **Human-facing startup and shutdown reporting for the service. The structured…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Print where the service is listening and what it is running. Failures are…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Conditions worth telling a developer about before their first request. Returned…** (1 connections) — `src/osc_assistant/api/banner.py`
- **A chat UI on an unauthenticated service is the state most easily mistaken for…** (1 connections) — `tests/test_server_lifecycle.py`

## Relationships

- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (6 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (4 shared connections)
- [Server Lifecycle Tests](Server_Lifecycle_Tests.md) (4 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (3 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (2 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (1 shared connections)
- [Trace Listing CLI](Trace_Listing_CLI.md) (1 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (1 shared connections)

## Source Files

- `src/osc_assistant/api/banner.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 38 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*