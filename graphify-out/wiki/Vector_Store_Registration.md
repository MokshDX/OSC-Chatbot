# Vector Store Registration

> 17 nodes

## Key Concepts

- **pgvector.py** (30 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **MatchSource** (8 connections) — `src/osc_assistant/types.py`
- **VectorStoreError** (6 connections) — `src/osc_assistant/errors.py`
- **.setup()** (6 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **vectorstores/__init__.py** (4 connections) — `src/osc_assistant/providers/vectorstores/__init__.py`
- **_register_codecs()** (4 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **_redact_dsn()** (3 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **StrEnum** (2 connections)
- **The vector store could not complete an operation.** (1 connections) — `src/osc_assistant/errors.py`
- **Vector store providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/vectorstores/__init__.py`
- **register** (1 connections)
- **PostgreSQL + pgvector store: the production default. One datastore holds chunk…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Open the pool and, unless disabled, apply pending migrations.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Decode JSONB into Python objects instead of raw strings.** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Strip the password from a DSN before it reaches a terminal or a log. Connection…** (1 connections) — `src/osc_assistant/providers/vectorstores/pgvector.py`
- **Where a retrieval hit came from. Recorded for tracing and evaluation.** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (8 shared connections)
- [pgvector Search & Migrations](pgvector_Search_%26_Migrations.md) (7 shared connections)
- [pgvector Store Interface](pgvector_Store_Interface.md) (5 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (3 shared connections)
- [Memory Store Search](Memory_Store_Search.md) (2 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (2 shared connections)
- [VectorStore Protocol](VectorStore_Protocol.md) (2 shared connections)
- [Store Inspector](Store_Inspector.md) (2 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (1 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (1 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (1 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/providers/vectorstores/__init__.py`
- `src/osc_assistant/providers/vectorstores/pgvector.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 74 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*