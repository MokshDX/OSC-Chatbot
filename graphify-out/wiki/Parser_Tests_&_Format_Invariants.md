# Parser Tests & Format Invariants

> 24 nodes

## Key Concepts

- **test_parsers.py** (20 connections) — `tests/test_parsers.py`
- **parse()** (18 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Path** (15 connections)
- **test_text_parser_preserves_content_exactly()** (4 connections) — `tests/test_parsers.py`
- **test_html_title_is_taken_from_the_document()** (4 connections) — `tests/test_parsers.py`
- **test_corrupt_binary_raises_parse_error_not_a_library_exception()** (4 connections) — `tests/test_parsers.py`
- **test_docx_extracts_paragraphs_and_table_cells()** (4 connections) — `tests/test_parsers.py`
- **test_xlsx_keeps_a_row_together_and_labels_it_with_its_sheet()** (4 connections) — `tests/test_parsers.py`
- **test_scanned_pdf_reports_that_it_has_no_text()** (4 connections) — `tests/test_parsers.py`
- **test_metadata_records_provenance()** (4 connections) — `tests/test_parsers.py`
- **test_html_parser_drops_script_and_style_but_keeps_prose()** (3 connections) — `tests/test_parsers.py`
- **test_unsupported_extension_is_rejected()** (3 connections) — `tests/test_parsers.py`
- **test_empty_xlsx_is_an_error_rather_than_an_unfindable_empty_document()** (3 connections) — `tests/test_parsers.py`
- **test_corrupt_xlsx_raises_parse_error_not_a_library_exception()** (3 connections) — `tests/test_parsers.py`
- **Extract `path` using the parser registered for its extension. Raises:…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **test_supported_extensions_are_lowercase_and_dotted()** (1 connections) — `tests/test_parsers.py`
- **Text extraction and multi-format loading tests. Two properties are load-bearing…** (1 connections) — `tests/test_parsers.py`
- **The invariant that makes a citation quotable: text in equals text out.** (1 connections) — `tests/test_parsers.py`
- **A format that declares its own title beats one derived from the filename.** (1 connections) — `tests/test_parsers.py`
- **Callers catch `ParseError`; a raw pypdf exception would escape that.** (1 connections) — `tests/test_parsers.py`
- **Policy documents keep the facts people ask about inside tables.** (1 connections) — `tests/test_parsers.py`
- **A spreadsheet's meaning is two-dimensional; retrieval is not. The row is the…** (1 connections) — `tests/test_parsers.py`
- **A page-image PDF parses cleanly and yields nothing. Indexing an empty document…** (1 connections) — `tests/test_parsers.py`
- **Provenance is denormalised onto every chunk, so it has to be right here.** (1 connections) — `tests/test_parsers.py`

## Relationships

- [Filesystem Loader & Corpus Boundary](Filesystem_Loader_%26_Corpus_Boundary.md) (9 shared connections)
- [Text Extraction Parsers](Text_Extraction_Parsers.md) (5 shared connections)
- [AssistantError Base & Loaders](AssistantError_Base_%26_Loaders.md) (4 shared connections)
- [Error Hierarchy & Protocol Seams](Error_Hierarchy_%26_Protocol_Seams.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/parsers.py`
- `tests/test_parsers.py`

## Audit Trail

- EXTRACTED: 102 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*