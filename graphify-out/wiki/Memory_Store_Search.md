# Memory Store Search

> 7 nodes

## Key Concepts

- **.search_hybrid()** (6 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_vector()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **.search_keyword()** (5 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Vector** (3 connections)
- **_cosine_similarity()** (3 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **_tokenize()** (2 connections) — `src/osc_assistant/providers/vectorstores/memory.py`
- **Term-overlap scoring. Deliberately not BM25: this exists to make hybrid…** (1 connections) — `src/osc_assistant/providers/vectorstores/memory.py`

## Relationships

- [Settings Precedence Tests](Settings_Precedence_Tests.md) (3 shared connections)
- [Logging System Design](Logging_System_Design.md) (3 shared connections)
- [Ingestion Loaders & Parsers](Ingestion_Loaders_%26_Parsers.md) (2 shared connections)
- [Regression Gate Tests](Regression_Gate_Tests.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/vectorstores/memory.py`

## Audit Trail

- EXTRACTED: 25 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*