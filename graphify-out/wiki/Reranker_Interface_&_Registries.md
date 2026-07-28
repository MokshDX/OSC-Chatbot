# Reranker Interface & Registries

> 14 nodes · cohesion 0.18

## Key Concepts

- **registries.py** (25 connections) — `src/osc_assistant/registries.py`
- **registry.py** (22 connections) — `src/osc_assistant/registry.py`
- **Reranker** (21 connections) — `src/osc_assistant/protocols.py`
- **noop.py** (13 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **_build()** (5 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **.rerank()** (3 connections) — `src/osc_assistant/protocols.py`
- **.reranker()** (2 connections) — `src/osc_assistant/container.py`
- **A second-stage relevance model applied to retrieval candidates.** (1 connections) — `src/osc_assistant/protocols.py`
- **Return the `top_k` most relevant candidates, most relevant first.** (1 connections) — `src/osc_assistant/protocols.py`
- **.model_id()** (1 connections) — `src/osc_assistant/protocols.py`
- **register** (1 connections)
- **Pass-through reranker: the default. Reranking is a real accuracy gain but costs…** (1 connections) — `src/osc_assistant/providers/reranking/noop.py`
- **The registries for every swappable component. Kept in one small module so that…** (1 connections) — `src/osc_assistant/registries.py`
- **A minimal registry so new providers are additions, never edits. This exists to…** (1 connections) — `src/osc_assistant/registry.py`

## Relationships

- [Error Hierarchy](Error_Hierarchy.md) (13 shared connections)
- [Component Config & Registry Tests](Component_Config_%26_Registry_Tests.md) (5 shared connections)
- [Chunker Registration](Chunker_Registration.md) (4 shared connections)
- [Cross-Encoder Reranker](Cross-Encoder_Reranker.md) (4 shared connections)
- [In-Memory Store & Noop Reranker](In-Memory_Store_%26_Noop_Reranker.md) (4 shared connections)
- [Structured Logging](Structured_Logging.md) (3 shared connections)
- [Gemini Chat Adapter](Gemini_Chat_Adapter.md) (3 shared connections)
- [Hybrid Search Scoring](Hybrid_Search_Scoring.md) (3 shared connections)
- [Provider Registry](Provider_Registry.md) (3 shared connections)
- [Composition Root](Composition_Root.md) (2 shared connections)
- [Atomic Document Replacement](Atomic_Document_Replacement.md) (2 shared connections)
- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (2 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/protocols.py`
- `src/osc_assistant/providers/reranking/noop.py`
- `src/osc_assistant/registries.py`
- `src/osc_assistant/registry.py`

## Audit Trail

- EXTRACTED: 91 (93%)
- INFERRED: 7 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*