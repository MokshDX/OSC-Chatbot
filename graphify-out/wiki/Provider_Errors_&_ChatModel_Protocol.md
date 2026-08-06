# Provider Errors & ChatModel Protocol

> 22 nodes · cohesion 0.10

## Key Concepts

- **ProviderError** (33 connections) — `src/osc_assistant/errors.py`
- **ChatModel** (33 connections) — `src/osc_assistant/protocols.py`
- **ChatResponse** (28 connections) — `src/osc_assistant/types.py`
- **_ExplodingChatModel** (23 connections) — `tests/test_server_lifecycle.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/llm/gemini.py`
- **.complete()** (4 connections) — `src/osc_assistant/protocols.py`
- **.stream()** (4 connections) — `src/osc_assistant/protocols.py`
- **.complete()** (4 connections) — `tests/test_server_lifecycle.py`
- **.model_id()** (2 connections) — `src/osc_assistant/protocols.py`
- **.supports_citations()** (2 connections) — `src/osc_assistant/protocols.py`
- **.__init__()** (2 connections) — `src/osc_assistant/retrieval/rewrite.py`
- **An upstream provider (LLM, embeddings, reranker) failed.** (1 connections) — `src/osc_assistant/errors.py`
- **StreamEvent** (1 connections)
- **A text-generating model.** (1 connections) — `src/osc_assistant/protocols.py`
- **The provider's identifier for the underlying model, for logs and traces.** (1 connections) — `src/osc_assistant/protocols.py`
- **True if the provider resolves citations itself from structured sources. When…** (1 connections) — `src/osc_assistant/protocols.py`
- **Generate a complete response.** (1 connections) — `src/osc_assistant/protocols.py`
- **Generate a response incrementally.** (1 connections) — `src/osc_assistant/protocols.py`
- **register** (1 connections)
- **.model_id()** (1 connections) — `tests/test_server_lifecycle.py`
- **.supports_citations()** (1 connections) — `tests/test_server_lifecycle.py`
- **Fails partway through a stream, after deltas have already been sent.** (1 connections) — `tests/test_server_lifecycle.py`

## Relationships

- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (20 shared connections)
- [Protocol Seams & Embedding Errors](Protocol_Seams_%26_Embedding_Errors.md) (9 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (8 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (7 shared connections)
- [Grounded Prompt & LangChain Chat](Grounded_Prompt_%26_LangChain_Chat.md) (7 shared connections)
- [OpenAI-Compatible Chat Provider](OpenAI-Compatible_Chat_Provider.md) (5 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (5 shared connections)
- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (4 shared connections)
- [Container Lifecycle & E2E](Container_Lifecycle_%26_E2E.md) (4 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (4 shared connections)
- [Citation Grounding & Reasoning Models](Citation_Grounding_%26_Reasoning_Models.md) (2 shared connections)
- [OpenAI-Compatible Embeddings](OpenAI-Compatible_Embeddings.md) (2 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/llm/gemini.py`
- `src/osc_assistant/retrieval/rewrite.py`
- `src/osc_assistant/types.py`
- `tests/test_server_lifecycle.py`

## Audit Trail

- EXTRACTED: 109 (72%)
- INFERRED: 42 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*