# AssistantError Base & Loaders

> 20 nodes

## Key Concepts

- **ingestion/__init__.py** (20 connections) — `src/osc_assistant/ingestion/__init__.py`
- **loaders.py** (16 connections) — `src/osc_assistant/ingestion/loaders.py`
- **AssistantError** (11 connections) — `src/osc_assistant/errors.py`
- **._read()** (9 connections) — `src/osc_assistant/ingestion/loaders.py`
- **LoadFailure** (8 connections) — `src/osc_assistant/types.py`
- **IngestionReport** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **stable_document_id()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **_derive_title()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Path** (3 connections)
- **.load()** (3 connections) — `src/osc_assistant/ingestion/loaders.py`
- **.__init__()** (2 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Exception** (1 connections)
- **Base class for every error raised by this package.** (1 connections) — `src/osc_assistant/errors.py`
- **Corpus ingestion: connectors, text extraction, and the chunk/embed/store…** (1 connections) — `src/osc_assistant/ingestion/__init__.py`
- **Corpus connectors. A loader is any object with `load() ->…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Derive a stable id from a source URI. Hashed rather than slugified so the id is…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Use the first Markdown heading as the title, else the filename. Titles are…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **.succeeded()** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **What a sync did. Returned to the CLI and logged for the admin view.** (1 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **A source file a connector found but could not turn into a `Document`. Carries…** (1 connections) — `src/osc_assistant/types.py`

## Relationships

- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (11 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (6 shared connections)
- [Filesystem Loader & Corpus Boundary](Filesystem_Loader_%26_Corpus_Boundary.md) (5 shared connections)
- [Text Extraction Parsers](Text_Extraction_Parsers.md) (4 shared connections)
- [Parser Tests & Format Invariants](Parser_Tests_%26_Format_Invariants.md) (4 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (2 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (2 shared connections)
- [Chunker Registration](Chunker_Registration.md) (2 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (2 shared connections)
- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (1 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (1 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/ingestion/__init__.py`
- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `src/osc_assistant/types.py`

## Audit Trail

- EXTRACTED: 94 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*