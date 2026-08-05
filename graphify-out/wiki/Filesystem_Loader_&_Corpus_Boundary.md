# Filesystem Loader & Corpus Boundary

> 14 nodes

## Key Concepts

- **FilesystemLoader** (18 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Path** (4 connections)
- **test_failures_are_cleared_in_place_between_runs()** (4 connections) — `tests/test_parsers.py`
- **test_unsupported_files_are_ignored_not_failed()** (4 connections) — `tests/test_parsers.py`
- **test_filesystem_loader_reads_a_tree()** (3 connections) — `tests/test_ingestion.py`
- **test_filesystem_loader_ids_are_stable()** (3 connections) — `tests/test_ingestion.py`
- **test_missing_corpus_directory_is_an_error()** (3 connections) — `tests/test_ingestion.py`
- **test_the_ingest_root_is_the_company_corpus_and_excludes_the_knowledge_base()** (3 connections) — `tests/test_ingestion.py`
- **test_loader_reads_every_supported_format()** (3 connections) — `tests/test_parsers.py`
- **test_one_unreadable_file_does_not_abort_the_sync()** (3 connections) — `tests/test_parsers.py`
- **Loads documents from a directory tree, one parser per format. The Phase 1…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Regression: the corpus boundary is enforced by two defaults agreeing.…** (1 connections) — `tests/test_ingestion.py`
- **The pipeline is handed this list before iteration and reads it after, so a re-…** (1 connections) — `tests/test_parsers.py`
- **A corpus directory holds images and archives. They are not errors.** (1 connections) — `tests/test_parsers.py`

## Relationships

- [Parser Tests & Format Invariants](Parser_Tests_%26_Format_Invariants.md) (9 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (5 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (4 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (3 shared connections)
- [CLI Commands — ask, ingest, search](CLI_Commands_%E2%80%94_ask%2C_ingest%2C_search.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/loaders.py`
- `tests/test_ingestion.py`
- `tests/test_parsers.py`

## Audit Trail

- EXTRACTED: 34 (65%)
- INFERRED: 18 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*