# Protocol Seams & Embedding Errors

> 31 nodes · cohesion 0.11

## Key Concepts

- **protocols.py** (44 connections) — `src/osc_assistant/protocols.py`
- **errors.py** (38 connections) — `src/osc_assistant/errors.py`
- **EmbeddingModel** (33 connections) — `src/osc_assistant/protocols.py`
- **registries.py** (31 connections) — `src/osc_assistant/registries.py`
- **registry.py** (29 connections) — `src/osc_assistant/registry.py`
- **embeddings/gemini.py** (15 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **embeddings/openai_compatible.py** (15 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **local.py** (14 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **voyage.py** (14 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **embeddings/__init__.py** (7 connections) — `src/osc_assistant/providers/embeddings/__init__.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/local.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/embeddings/voyage.py`
- **.dimensions()** (2 connections) — `src/osc_assistant/protocols.py`
- **_make_factory()** (2 connections) — `src/osc_assistant/providers/embeddings/openai_compatible.py`
- **Exception hierarchy for the assistant. A single root (`AssistantError`) lets…** (1 connections) — `src/osc_assistant/errors.py`
- **.model_id()** (1 connections) — `src/osc_assistant/protocols.py`
- **The five seams of the system. Every swappable component is defined here as a…** (1 connections) — `src/osc_assistant/protocols.py`
- **A text embedding model. Document and query embedding are separate methods…** (1 connections) — `src/osc_assistant/protocols.py`
- **Vector width. Must match the vector store's configured dimension.** (1 connections) — `src/osc_assistant/protocols.py`
- **register** (1 connections)
- **Google Gemini embedding provider.** (1 connections) — `src/osc_assistant/providers/embeddings/gemini.py`
- **Embedding providers. Imported for registration side effects.** (1 connections) — `src/osc_assistant/providers/embeddings/__init__.py`
- **register** (1 connections)
- **Local embedding provider backed by `sentence-transformers`. Present for two…** (1 connections) — `src/osc_assistant/providers/embeddings/local.py`
- *... and 6 more nodes in this community*

## Relationships

- [Error Hierarchy & Embedding Providers](Error_Hierarchy_%26_Embedding_Providers.md) (19 shared connections)
- [Chunker Factories & Pipeline Wiring](Chunker_Factories_%26_Pipeline_Wiring.md) (16 shared connections)
- [Reranker Protocol & Provider Registration](Reranker_Protocol_%26_Provider_Registration.md) (11 shared connections)
- [Answer Generation & Faithfulness Judge](Answer_Generation_%26_Faithfulness_Judge.md) (10 shared connections)
- [Provider Errors & ChatModel Protocol](Provider_Errors_%26_ChatModel_Protocol.md) (9 shared connections)
- [Component Registry](Component_Registry.md) (7 shared connections)
- [VectorStore Errors & Inspection](VectorStore_Errors_%26_Inspection.md) (7 shared connections)
- [Citation Parsing & Gemini Chat](Citation_Parsing_%26_Gemini_Chat.md) (6 shared connections)
- [Fusion & Store Statistics](Fusion_%26_Store_Statistics.md) (6 shared connections)
- [Composition Root & Settings Models](Composition_Root_%26_Settings_Models.md) (6 shared connections)
- [Evaluation CLI Command](Evaluation_CLI_Command.md) (4 shared connections)
- [Anthropic Adapter & Retrieval Pipeline](Anthropic_Adapter_%26_Retrieval_Pipeline.md) (4 shared connections)

## Source Files

- `src/osc_assistant/errors.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/embeddings/__init__.py`
- `src/osc_assistant/providers/embeddings/gemini.py`
- `src/osc_assistant/providers/embeddings/local.py`
- `src/osc_assistant/providers/embeddings/openai_compatible.py`
- `src/osc_assistant/providers/embeddings/voyage.py`
- `src/osc_assistant/registries.py`
- `src/osc_assistant/registry.py`

## Audit Trail

- EXTRACTED: 265 (96%)
- INFERRED: 10 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*