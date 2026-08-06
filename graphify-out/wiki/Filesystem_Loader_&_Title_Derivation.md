# Filesystem Loader & Title Derivation

> 16 nodes · cohesion 0.17

## Key Concepts

- **FilesystemLoader** (18 connections) — `src/osc_assistant/ingestion/loaders.py`
- **._read()** (9 connections) — `src/osc_assistant/ingestion/loaders.py`
- **_derive_title()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Path** (4 connections)
- **test_unsupported_files_are_ignored_not_failed()** (4 connections) — `tests/test_parsers.py`
- **.load()** (3 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Path** (3 connections)
- **test_filesystem_loader_ids_are_stable()** (3 connections) — `tests/test_ingestion.py`
- **test_filesystem_loader_reads_a_tree()** (3 connections) — `tests/test_ingestion.py`
- **test_missing_corpus_directory_is_an_error()** (3 connections) — `tests/test_ingestion.py`
- **test_the_ingest_root_is_the_company_corpus_and_excludes_the_knowledge_base()** (3 connections) — `tests/test_ingestion.py`
- **.__init__()** (2 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Use the first Markdown heading as the title, else the filename. Titles are…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Loads documents from a directory tree, one parser per format. The Phase 1…** (1 connections) — `src/osc_assistant/ingestion/loaders.py`
- **Regression: the corpus boundary is enforced by two defaults agreeing.…** (1 connections) — `tests/test_ingestion.py`
- **A corpus directory holds images and archives. They are not errors.** (1 connections) — `tests/test_parsers.py`

## Relationships

- [Parser Registry & Parser Tests](Parser_Registry_%26_Parser_Tests.md) (7 shared connections)
- [Ingestion Pipeline & Loaders](Ingestion_Pipeline_%26_Loaders.md) (7 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (5 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (3 shared connections)
- [CLI Core Commands](CLI_Core_Commands.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/loaders.py`
- `tests/test_ingestion.py`
- `tests/test_parsers.py`

## Audit Trail

- EXTRACTED: 48 (76%)
- INFERRED: 15 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*