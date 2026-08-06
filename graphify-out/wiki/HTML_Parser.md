# HTML Parser

> 10 nodes · cohesion 0.20

## Key Concepts

- **_HtmlTextExtractor** (9 connections) — `src/osc_assistant/ingestion/parsers.py`
- **.text()** (5 connections) — `src/osc_assistant/ingestion/parsers.py`
- **.handle_starttag()** (2 connections) — `src/osc_assistant/ingestion/parsers.py`
- **HTMLParser** (1 connections)
- **.handle_data()** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **.handle_endtag()** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **.__init__()** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **Any** (1 connections)
- **Collects visible text, discarding markup and non-content elements.** (1 connections) — `src/osc_assistant/ingestion/parsers.py`
- **The collected text, with each block element on its own line.** (1 connections) — `src/osc_assistant/ingestion/parsers.py`

## Relationships

- [Parse Errors & Format Parsers](Parse_Errors_%26_Format_Parsers.md) (3 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (1 shared connections)
- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (1 shared connections)

## Source Files

- `src/osc_assistant/ingestion/parsers.py`

## Audit Trail

- EXTRACTED: 21 (91%)
- INFERRED: 2 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*