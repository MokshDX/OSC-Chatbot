# Composition Root & Settings

> 29 nodes

## Key Concepts

- **test_ingestion.py** (18 connections) — `tests/test_ingestion.py`
- **IngestionPipeline** (11 connections)
- **Document** (10 connections)
- **MemoryVectorStore** (8 connections)
- **pipeline()** (5 connections) — `tests/test_ingestion.py`
- **test_prune_disabled_leaves_other_documents_alone()** (5 connections) — `tests/test_ingestion.py`
- **test_unreadable_documents_are_not_pruned()** (5 connections) — `tests/test_ingestion.py`
- **test_genuinely_removed_documents_are_still_pruned_alongside_failures()** (5 connections) — `tests/test_ingestion.py`
- **test_reindex_forces_work_the_content_hash_says_is_unnecessary()** (5 connections) — `tests/test_ingestion.py`
- **Path** (4 connections)
- **test_documents_are_indexed()** (4 connections) — `tests/test_ingestion.py`
- **test_reingesting_unchanged_documents_does_no_work()** (4 connections) — `tests/test_ingestion.py`
- **test_edited_document_is_reindexed()** (4 connections) — `tests/test_ingestion.py`
- **test_removed_documents_are_pruned()** (4 connections) — `tests/test_ingestion.py`
- **test_one_bad_document_does_not_abort_the_sync()** (4 connections) — `tests/test_ingestion.py`
- **test_a_sync_reports_the_trace_that_produced_it()** (4 connections) — `tests/test_ingestion.py`
- **test_the_configured_corpus_root_cannot_reach_the_engineering_knowledge_base()** (4 connections) — `tests/test_ingestion.py`
- **StubEmbeddingModel** (3 connections)
- **test_filesystem_loader_reads_a_tree()** (2 connections) — `tests/test_ingestion.py`
- **test_filesystem_loader_ids_are_stable()** (2 connections) — `tests/test_ingestion.py`
- **test_missing_corpus_directory_is_an_error()** (2 connections) — `tests/test_ingestion.py`
- **fixture** (1 connections)
- **Ingestion tests. Idempotency is the property that matters: a re-run over an…** (1 connections) — `tests/test_ingestion.py`
- **Partial ingestion must not delete the rest of the corpus.** (1 connections) — `tests/test_ingestion.py`
- **Regression: a file that fails to parse is still present at the source. Pruning…** (1 connections) — `tests/test_ingestion.py`
- *... and 4 more nodes in this community*

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (1 shared connections)
- [Shared Test Fixtures](Shared_Test_Fixtures.md) (1 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (1 shared connections)

## Source Files

- `tests/test_ingestion.py`

## Audit Trail

- EXTRACTED: 120 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*