# Logging Filters & Audit Stream

> 28 nodes

## Key Concepts

- **command** (11 connections)
- **ProfileOption** (10 connections)
- **JsonOption** (9 connections)
- **doctor()** (9 connections) — `src/osc_assistant/cli/diagnose.py`
- **logs()** (9 connections) — `src/osc_assistant/cli/diagnose.py`
- **help** (8 connections)
- **config()** (8 connections) — `src/osc_assistant/cli/diagnose.py`
- **documents()** (8 connections) — `src/osc_assistant/cli/diagnose.py`
- **document()** (8 connections) — `src/osc_assistant/cli/diagnose.py`
- **traces()** (8 connections) — `src/osc_assistant/cli/diagnose.py`
- **Option** (7 connections)
- **chunk()** (7 connections) — `src/osc_assistant/cli/diagnose.py`
- **providers()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **status()** (5 connections) — `src/osc_assistant/cli/diagnose.py`
- **Argument** (4 connections)
- **version()** (4 connections) — `src/osc_assistant/cli/diagnose.py`
- **VerboseOption** (1 connections)
- **min** (1 connections)
- **Check that every configured component is reachable and consistent. Runs the…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Print the fully resolved configuration and where it came from. Configuration is…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **List every registered provider, marking the ones this profile uses. Read from…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Summarise what is indexed: counts, chunk size distribution, formats.** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **List indexed documents with their chunk counts.** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Show one document's index record and how it chunked. Accepts a path fragment as…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- **Print one chunk in full — exactly the text the model was shown. The last step…** (1 connections) — `src/osc_assistant/cli/diagnose.py`
- *... and 3 more nodes in this community*

## Relationships

- [Test Doubles & Stubs](Test_Doubles_%26_Stubs.md) (16 shared connections)
- [AccessLock & BulkImportExport Schemas](AccessLock_%26_BulkImportExport_Schemas.md) (6 shared connections)

## Source Files

- `src/osc_assistant/cli/diagnose.py`

## Audit Trail

- EXTRACTED: 132 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*