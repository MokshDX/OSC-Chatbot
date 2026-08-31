# Conversational Report Shape

> 7 nodes

## Key Concepts

- **.run()** (6 connections) — `src/osc_assistant/evaluation/conversational.py`
- **ConversationalReport** (5 connections) — `src/osc_assistant/evaluation/conversational.py`
- **.to_dict()** (2 connections) — `src/osc_assistant/evaluation/conversational.py`
- **Any** (1 connections)
- **ConversationalSet** (1 connections)
- **One multi-turn evaluation run.** (1 connections) — `src/osc_assistant/evaluation/conversational.py`
- **Score every case, at most `concurrency` sessions at a time. Concurrency is over…** (1 connections) — `src/osc_assistant/evaluation/conversational.py`

## Relationships

- [Golden Set & Case Results](Golden_Set_%26_Case_Results.md) (2 shared connections)
- [Trace Configuration & Rendering](Trace_Configuration_%26_Rendering.md) (1 shared connections)
- [Document Loaders](Document_Loaders.md) (1 shared connections)
- [OpenAI-Compatible Provider](OpenAI-Compatible_Provider.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/conversational.py`

## Audit Trail

- EXTRACTED: 17 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*