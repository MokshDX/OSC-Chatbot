# Chat Model Interface

> 11 nodes · cohesion 0.18

## Key Concepts

- **ChatModel** (27 connections) — `src/osc_assistant/protocols.py`
- **.complete()** (4 connections) — `src/osc_assistant/protocols.py`
- **.stream()** (4 connections) — `src/osc_assistant/protocols.py`
- **.model_id()** (2 connections) — `src/osc_assistant/protocols.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/protocols.py`
- **StreamEvent** (1 connections)
- **A text-generating model.** (1 connections) — `src/osc_assistant/protocols.py`
- **The provider's identifier for the underlying model, for logs and traces.** (1 connections) — `src/osc_assistant/protocols.py`
- **True if the provider resolves citations itself from structured sources. When…** (1 connections) — `src/osc_assistant/protocols.py`
- **Generate a complete response.** (1 connections) — `src/osc_assistant/protocols.py`
- **Generate a response incrementally.** (1 connections) — `src/osc_assistant/protocols.py`

## Relationships

- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (5 shared connections)
- [Composition Root](Composition_Root.md) (3 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (3 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (2 shared connections)
- [Streaming & Response Types](Streaming_%26_Response_Types.md) (2 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (2 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (2 shared connections)
- [Structured Logging](Structured_Logging.md) (1 shared connections)
- [Chunker Registration](Chunker_Registration.md) (1 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (1 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (1 shared connections)
- [OpenAI-Compatible Chat Adapter](OpenAI-Compatible_Chat_Adapter.md) (1 shared connections)

## Source Files

- `src/osc_assistant/protocols.py`

## Audit Trail

- EXTRACTED: 38 (84%)
- INFERRED: 7 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*