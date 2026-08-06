# Parse Errors & Format Parsers

> 17 nodes · cohesion 0.21

## Key Concepts

- **parsers.py** (16 connections) — `src/osc_assistant/ingestion/parsers.py`
- **ParseError** (9 connections) — `src/osc_assistant/errors.py`
- **ParsedContent** (9 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_docx()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_html()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_pdf()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **parse_xlsx()** (6 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Path** (6 connections)
- **parse_text()** (5 connections) — `src/osc_assistant/ingestion/parsers.py`
- **A source file could not be turned into text. Raised per file and caught by the…** (1 connections) — `src/osc_assistant/errors.py`
- **Text extraction, one function per file format. A parser turns a file into plain…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Extract paragraphs and table cells from a Word document. Tables are included…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Extract cell values from an Excel workbook, one block per worksheet. A…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **The result of extracting one file. `title` is set only when the format declares…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Read a plain-text format (Markdown, reStructuredText, plain text).** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Extract readable text from HTML using the standard library. No dependency:…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Extract text from a PDF, page by page. Page boundaries become blank lines so…** (1 connections) — `src/osc_assistant/ingestion/parsers.py`

## Relationships

- [Parser Registry & Parser Tests](Parser_Registry_%26_Parser_Tests.md) (5 shared connections)
- [Whitespace Normalisation & Error Base](Whitespace_Normalisation_%26_Error_Base.md) (4 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (4 shared connections)
- [HTML Parser](HTML_Parser.md) (3 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (2 shared connections)
- [Doctor Health Checks](Doctor_Health_Checks.md) (1 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/ingestion/parsers.py`

## Audit Trail

- EXTRACTED: 67 (87%)
- INFERRED: 10 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*