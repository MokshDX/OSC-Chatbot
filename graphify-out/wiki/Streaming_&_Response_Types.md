# Streaming & Response Types

> 29 nodes · cohesion 0.12

## Key Concepts

- **ChatResponse** (21 connections) — `src/osc_assistant/types.py`
- **Usage** (21 connections) — `src/osc_assistant/types.py`
- **NativeCitationChatModel** (18 connections) — `tests/conftest.py`
- **FailingChatModel** (17 connections) — `tests/conftest.py`
- **CitationDelta** (16 connections) — `src/osc_assistant/types.py`
- **TextDelta** (16 connections) — `src/osc_assistant/types.py`
- **Citation** (15 connections) — `src/osc_assistant/types.py`
- **StreamEnd** (14 connections) — `src/osc_assistant/types.py`
- **.stream()** (12 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **.stream()** (8 connections) — `tests/conftest.py`
- **.stream()** (8 connections) — `tests/conftest.py`
- **.complete()** (5 connections) — `tests/conftest.py`
- **.complete()** (4 connections) — `tests/conftest.py`
- **.complete()** (4 connections) — `tests/conftest.py`
- **.stream()** (3 connections) — `tests/conftest.py`
- **StreamEvent** (3 connections)
- **StreamEvent** (1 connections)
- **Stream text, resolving citations from the accumulated answer at the end.…** (1 connections) — `src/osc_assistant/providers/llm/openai_compatible.py`
- **A reference from the answer back to the material that supports it. `index` is…** (1 connections) — `src/osc_assistant/types.py`
- **An incremental fragment of the answer.** (1 connections) — `src/osc_assistant/types.py`
- **A citation resolved mid-stream.** (1 connections) — `src/osc_assistant/types.py`
- **.__add__()** (1 connections) — `src/osc_assistant/types.py`
- **.model_id()** (1 connections) — `tests/conftest.py`
- **.supports_citations()** (1 connections) — `tests/conftest.py`
- **.__init__()** (1 connections) — `tests/conftest.py`
- *... and 4 more nodes in this community*

## Relationships

- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (23 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (21 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (13 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (12 shared connections)
- [OpenAI-Compatible Chat Adapter](OpenAI-Compatible_Chat_Adapter.md) (8 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (5 shared connections)
- [Rank Fusion & Citation Grounding](Rank_Fusion_%26_Citation_Grounding.md) (4 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (4 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (2 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (2 shared connections)
- [Embedding Model Interface](Embedding_Model_Interface.md) (1 shared connections)
- [Vector Store Interface](Vector_Store_Interface.md) (1 shared connections)

## Source Files

- `src/osc_assistant/providers/llm/openai_compatible.py`
- `src/osc_assistant/types.py`
- `tests/conftest.py`

## Audit Trail

- EXTRACTED: 149 (75%)
- INFERRED: 49 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*