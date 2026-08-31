# FastAPI Routes & Session Endpoints

> 72 nodes

## Key Concepts

- **test_parsers.py** (20 connections) — `tests/test_parsers.py`
- **parse()** (18 connections) — `src/osc_assistant/ingestion/parsers.py`
- **ingestion/__init__.py** (16 connections) — `src/osc_assistant/ingestion/__init__.py`
- **loaders.py** (16 connections) — `src/osc_assistant/ingestion/loaders.py`
- **parsers.py** (16 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Path** (15 connections)
- **FilesystemLoader** (11 connections) — `src/osc_assistant/ingestion/loaders.py`
- **ParseError** (9 connections) — `src/osc_assistant/errors.py`
- **._read()** (9 connections) — `src/osc_assistant/ingestion/loaders.py`
- **ParsedContent** (9 connections) — `src/osc_assistant/ingestion/parsers.py`
- **_HtmlTextExtractor** (9 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Path** (6 connections)
- **parse_html()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_pdf()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_docx()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_xlsx()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_text()** (5 connections) — `src/osc_assistant/ingestion/parsers.py`
- **IngestionReport** (5 connections) — `src/osc_assistant/ingestion/pipeline.py`
- **stable_document_id()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **_derive_title()** (4 connections) — `src/osc_assistant/ingestion/loaders.py`
- **test_text_parser_preserves_content_exactly()** (4 connections) — `tests/test_parsers.py`
- **test_html_title_is_taken_from_the_document()** (4 connections) — `tests/test_parsers.py`
- **test_corrupt_binary_raises_parse_error_not_a_library_exception()** (4 connections) — `tests/test_parsers.py`
- **test_docx_extracts_paragraphs_and_table_cells()** (4 connections) — `tests/test_parsers.py`
- **test_xlsx_keeps_a_row_together_and_labels_it_with_its_sheet()** (4 connections) — `tests/test_parsers.py`
- *... and 47 more nodes in this community*

## Relationships

- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (9 shared connections)
- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (6 shared connections)
- [Conversational Evaluator](Conversational_Evaluator.md) (5 shared connections)
- [PgVector Store](PgVector_Store.md) (3 shared connections)
- [Error Base Classes](Error_Base_Classes.md) (2 shared connections)
- [Logging Tests](Logging_Tests.md) (2 shared connections)
- [Quality Report Renderer](Quality_Report_Renderer.md) (1 shared connections)
- [Settings Precedence Tests](Settings_Precedence_Tests.md) (1 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (1 shared connections)
- [Evaluation Framework ADR](Evaluation_Framework_ADR.md) (1 shared connections)
- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (1 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/ingestion/__init__.py`
- `src/osc_assistant/ingestion/loaders.py`
- `src/osc_assistant/ingestion/parsers.py`
- `src/osc_assistant/ingestion/pipeline.py`
- `tests/test_parsers.py`

## Audit Trail

- EXTRACTED: 273 (93%)
- INFERRED: 20 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*