# Parser Registry & Parser Tests

> 28 nodes · cohesion 0.13

## Key Concepts

- **test_parsers.py** (20 connections) — `tests/test_parsers.py`
- **parse()** (18 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Path** (15 connections)
- **test_corrupt_binary_raises_parse_error_not_a_library_exception()** (4 connections) — `tests/test_parsers.py`
- **test_docx_extracts_paragraphs_and_table_cells()** (4 connections) — `tests/test_parsers.py`
- **test_failures_are_cleared_in_place_between_runs()** (4 connections) — `tests/test_parsers.py`
- **test_html_title_is_taken_from_the_document()** (4 connections) — `tests/test_parsers.py`
- **test_metadata_records_provenance()** (4 connections) — `tests/test_parsers.py`
- **test_scanned_pdf_reports_that_it_has_no_text()** (4 connections) — `tests/test_parsers.py`
- **test_text_parser_preserves_content_exactly()** (4 connections) — `tests/test_parsers.py`
- **test_xlsx_keeps_a_row_together_and_labels_it_with_its_sheet()** (4 connections) — `tests/test_parsers.py`
- **test_corrupt_xlsx_raises_parse_error_not_a_library_exception()** (3 connections) — `tests/test_parsers.py`
- **test_empty_xlsx_is_an_error_rather_than_an_unfindable_empty_document()** (3 connections) — `tests/test_parsers.py`
- **test_html_parser_drops_script_and_style_but_keeps_prose()** (3 connections) — `tests/test_parsers.py`
- **test_loader_reads_every_supported_format()** (3 connections) — `tests/test_parsers.py`
- **test_one_unreadable_file_does_not_abort_the_sync()** (3 connections) — `tests/test_parsers.py`
- **test_unsupported_extension_is_rejected()** (3 connections) — `tests/test_parsers.py`
- **Extract `path` using the parser registered for its extension. Raises:…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Text extraction and multi-format loading tests. Two properties are load-bearing…** (1 connections) — `tests/test_parsers.py`
- **A spreadsheet's meaning is two-dimensional; retrieval is not. The row is the…** (1 connections) — `tests/test_parsers.py`
- **A page-image PDF parses cleanly and yields nothing. Indexing an empty document…** (1 connections) — `tests/test_parsers.py`
- **The pipeline is handed this list before iteration and reads it after, so a re-…** (1 connections) — `tests/test_parsers.py`
- **Provenance is denormalised onto every chunk, so it has to be right here.** (1 connections) — `tests/test_parsers.py`
- **The invariant that makes a citation quotable: text in equals text out.** (1 connections) — `tests/test_parsers.py`
- **A format that declares its own title beats one derived from the filename.** (1 connections) — `tests/test_parsers.py`
- *... and 3 more nodes in this community*

## Relationships

- [Filesystem Loader & Title Derivation](Filesystem_Loader_%26_Title_Derivation.md) (7 shared connections)
- [Parse Errors & Format Parsers](Parse_Errors_%26_Format_Parsers.md) (5 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (3 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/parsers.py`
- `tests/test_parsers.py`

## Audit Trail

- EXTRACTED: 110 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*