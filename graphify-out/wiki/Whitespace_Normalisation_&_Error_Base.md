# Whitespace Normalisation & Error Base

> 14 nodes · cohesion 0.15

## Key Concepts

- **ingestion/__init__.py** (19 connections) — `src/osc_assistant/ingestion/__init__.py`
- **loaders.py** (16 connections) — `src/osc_assistant/ingestion/loaders.py`
- **AssistantError** (10 connections) — `src/osc_assistant/errors.py`
- **normalize_whitespace()** (5 connections) — `src/osc_assistant/chunking/recursive.py`
- **IngestionReport** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **stable_document_id()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Exception** (1 connections)
- **Collapse runs of blank lines. Applied by loaders before chunking.** (1 connections) — `src/osc_assistant/chunking/recursive.py`
- **Base class for every error raised by this package.** (1 connections) — `src/osc_assistant/errors.py`
- **Corpus ingestion: connectors, text extraction, and the chunk/embed/store…** (1 connections) — `src/osc_assistant/ingestion/__init__.py`
- **Corpus connectors. A loader is any object with `load() ->…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Derive a stable id from a source URI. Hashed rather than slugified so the id is…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **.succeeded()** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **What a sync did. Returned to the CLI and logged for the admin view.** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (7 shared connections)
- [Filesystem Loader & Title Derivation](Filesystem_Loader_%26_Title_Derivation.md) (5 shared connections)
- [Parse Errors & Format Parsers](Parse_Errors_%26_Format_Parsers.md) (4 shared connections)
- [Parser Registry & Parser Tests](Parser_Registry_%26_Parser_Tests.md) (3 shared connections)
- [Ingestion Logging & Trace Persistence](Ingestion_Logging_%26_Trace_Persistence.md) (3 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Chunker Registration & Options](Chunker_Registration_%26_Options.md) (1 shared connections)
- [Recursive & Markdown Splitting](Recursive_%26_Markdown_Splitting.md) (1 shared connections)
- [FastAPI Application Assembly](FastAPI_Application_Assembly.md) (1 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (1 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (1 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (1 shared connections)

## Source Files

- `src/osc_assistant/chunking/recursive.py`
- `src/osc_assistant/errors.py`
- `src/osc_assistant/ingestion/__init__.py`
- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/pipeline.py`

## Audit Trail

- EXTRACTED: 67 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*