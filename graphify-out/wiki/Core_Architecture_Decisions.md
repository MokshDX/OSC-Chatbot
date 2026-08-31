# Core Architecture Decisions

> 13 nodes

## Key Concepts

- **config/default.yaml — Default Local Profile** (7 connections) — `config/default.yaml`
- **Hybrid Retrieval by Default** (3 connections) — `README.md`
- **Fully Local Default Stack (Ollama + pgvector)** (3 connections) — `README.md`
- **llm: ollama / qwen3:8b** (3 connections) — `config/default.yaml`
- **embeddings: ollama / nomic-embed-text (768-d)** (3 connections) — `config/default.yaml`
- **Reciprocal Rank Fusion (fusion.py + SQL)** (2 connections) — `README.md`
- **min_score Applies Before Reranking** (2 connections) — `README.md`
- **reasoning_effort: none** (2 connections) — `config/default.yaml`
- **vector_store: pgvector** (2 connections) — `config/default.yaml`
- **reranker: noop (until measured)** (2 connections) — `config/default.yaml`
- **retrieval: hybrid, candidates 30, top_k 5, rrf_k 60** (2 connections) — `config/default.yaml`
- **generation: max_tokens 1500, require_citations true** (2 connections) — `config/default.yaml`
- **One Datastore (PostgreSQL holds everything)** (1 connections) — `README.md`

## Relationships

- [LangChain Splitters](LangChain_Splitters.md) (1 shared connections)
- [Knowledge Corpus Rules](Knowledge_Corpus_Rules.md) (1 shared connections)
- [Conversation Rules & Rewriting](Conversation_Rules_%26_Rewriting.md) (1 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (1 shared connections)

## Source Files

- `README.md`
- `config/default.yaml`

## Audit Trail

- EXTRACTED: 34 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*