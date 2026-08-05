# Error Hierarchy & Protocol Seams

> 70 nodes

## Key Concepts

- **ComponentConfig** (64 connections) — `src/osc_assistant/registry.py`
- **protocols.py** (44 connections) — `src/osc_assistant/protocols.py`
- **errors.py** (38 connections) — `src/osc_assistant/errors.py`
- **EmbeddingModel** (33 connections) — `src/osc_assistant/protocols.py`
- **registries.py** (31 connections) — `src/osc_assistant/registries.py`
- **registry.py** (29 connections) — `src/osc_assistant/registry.py`
- **Reranker** (23 connections) — `src/osc_assistant/protocols.py`
- **embeddings/langchain_bridge.py** (18 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **embeddings/gemini.py** (15 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **embeddings/openai_compatible.py** (15 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **cross_encoder.py** (15 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **noop.py** (15 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **Registry** (15 connections) — `src/osc_assistant/registry.py`
- **local.py** (14 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **voyage.py** (14 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **test_registry.py** (10 connections) — `tests/test_registry.py`
- **UnknownComponentError** (8 connections) — `src/osc_assistant/errors.py`
- **embeddings/__init__.py** (7 connections) — `src/osc_assistant/providers/embeddings/__init__.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/cross_encoder.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **.create()** (5 connections) — `src/osc_assistant/registry.py`
- *... and 45 more nodes in this community*

## Relationships

- [Configuration Errors & Gemini Embeddings](Configuration_Errors_%26_Gemini_Embeddings.md) (23 shared connections)
- [LangChain Text Splitters](LangChain_Text_Splitters.md) (13 shared connections)
- [Startup Banner & Composition Root](Startup_Banner_%26_Composition_Root.md) (13 shared connections)
- [Settings Schema](Settings_Schema.md) (13 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (12 shared connections)
- [Faithfulness Judge & Answer Events](Faithfulness_Judge_%26_Answer_Events.md) (11 shared connections)
- [Vector Store Registration](Vector_Store_Registration.md) (8 shared connections)
- [Server Lifecycle & Startup Notes](Server_Lifecycle_%26_Startup_Notes.md) (8 shared connections)
- [Outbound LangChain Retriever](Outbound_LangChain_Retriever.md) (8 shared connections)
- [Container Lifecycle](Container_Lifecycle.md) (7 shared connections)
- [Markdown Chunker & LangChain Tests](Markdown_Chunker_%26_LangChain_Tests.md) (7 shared connections)
- [Anthropic Chat Adapter](Anthropic_Chat_Adapter.md) (6 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/errors.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/embeddings/__init__.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/langchain_bridge.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/openai_compatible.py`
- `src/osc_assistant/providers/embeddings/voyage.py`
- `src/osc_assistant/providers/reranking/cross_encoder.py`
- `src/osc_assistant/providers/reranking/noop.py`
- `src/osc_assistant/registries.py`
- `src/osc_assistant/registry.py`
- `tests/test_registry.py`

## Audit Trail

- EXTRACTED: 470 (93%)
- INFERRED: 36 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*