# Startup Banner & Composition Root

> 16 nodes

## Key Concepts

- **container.py** (31 connections) — `src/osc_assistant/container.py`
- **StoreInspector** (21 connections) — `src/osc_assistant/protocols.py`
- **banner.py** (12 connections) — `src/osc_assistant/api/banner.py`
- **describe_startup()** (7 connections) — `src/osc_assistant/api/banner.py`
- **Protocol** (6 connections)
- **providers/__init__.py** (6 connections) — `src/osc_assistant/providers/__init__.py`
- **_inspector()** (4 connections) — `src/osc_assistant/cli/diagnose.py`
- **reranking/__init__.py** (4 connections) — `src/osc_assistant/providers/reranking/__init__.py`
- **_release()** (3 connections) — `src/osc_assistant/container.py`
- **Human-facing startup and shutdown reporting for the service. The structured…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Print where the service is listening and what it is running. Failures are…** (1 connections) — `src/osc_assistant/api/banner.py`
- **Composition root. The only module that knows both which providers exist and how…** (1 connections) — `src/osc_assistant/container.py`
- **Close a component if it offers a way to be closed. Probed rather than required…** (1 connections) — `src/osc_assistant/container.py`
- **Read-only introspection of what a store currently holds. Kept **separate from…** (1 connections) — `src/osc_assistant/protocols.py`
- **Provider implementations. Importing this package registers every built-in…** (1 connections) — `src/osc_assistant/providers/__init__.py`
- **Reranker providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/reranking/__init__.py`

## Relationships

- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (13 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (8 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (6 shared connections)
- [Settings Schema](Settings_Schema.md) (6 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (5 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (4 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (4 shared connections)
- [Store Inspector](Store_Inspector.md) (3 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (2 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (2 shared connections)
- [ChatModel Protocol](ChatModel_Protocol.md) (2 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)

## Source Files

- `src/osc_assistant/api/banner.py`
- `src/osc_assistant/cli/diagnose.py`
- `src/osc_assistant/container.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/__init__.py`
- `src/osc_assistant/providers/reranking/__init__.py`

## Audit Trail

- EXTRACTED: 93 (92%)
- INFERRED: 8 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*