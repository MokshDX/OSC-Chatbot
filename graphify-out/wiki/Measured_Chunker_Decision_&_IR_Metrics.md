# Measured Chunker Decision & IR Metrics

> 20 nodes

## Key Concepts

- **Six-Stage Retrieval Pipeline** (8 connections) — `docs/engineering/architecture/retrieval.md`
- **Query Rewriting (ON by default since Phase 6)** (7 connections) — `docs/engineering/architecture/retrieval.md`
- **Threshold Applied Before Reranking** (5 connections) — `docs/engineering/architecture/retrieval.md`
- **The Request Path (rewrite → retrieve → rerank → generate → cite → abstain)** (4 connections) — `PROJECT_STATUS.md`
- **abstention_accuracy 0.667 — The Weakest Measured Behaviour** (3 connections) — `PROJECT_STATUS.md`
- **Cold Control Design** (3 connections) — `PROJECT_STATUS.md`
- **Query Rewriting Turned On (ADR 0013)** (3 connections) — `PROJECT_STATUS.md`
- **Next Milestones and Success Criteria** (3 connections) — `PROJECT_STATUS.md`
- **Cross-Encoder Reranking (off by default, unmeasured)** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **follow_up_lift — 0.000 Off, +0.177 On** (3 connections) — `docs/engineering/architecture/retrieval.md`
- **Abstention Is Architectural, Not A Prompt** (2 connections) — `PROJECT_STATUS.md`
- **Session Memory (Phase 6 headline)** (2 connections) — `PROJECT_STATUS.md`
- **Not Yet Implemented (auth, ACLs, rate limiting, durable sessions)** (2 connections) — `PROJECT_STATUS.md`
- **precision@5 0.200 Is The Structural Maximum** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **OSC Exposed As A LangChain BaseRetriever** (2 connections) — `docs/engineering/technologies/langchain.md`
- **A Found Defect Gets a Regression Test in the Same Commit** (1 connections) — `docs/engineering/architecture/testing.md`
- **Conversational Evaluation Suite (18 sessions / 46 turns)** (1 connections) — `PROJECT_STATUS.md`
- **Uniform Corpus Access Control** (1 connections) — `docs/engineering/architecture/knowledge-corpus.md`
- **Retrieval Bounds Everything Downstream** (1 connections) — `docs/engineering/architecture/retrieval.md`
- **One-Way Dependency: integrations/ May Import Core, Core May Never Import integrations/** (1 connections) — `docs/engineering/technologies/langchain.md`

## Relationships

- [Ingestion Tests](Ingestion_Tests.md) (4 shared connections)
- [Anthropic Adapter](Anthropic_Adapter.md) (4 shared connections)
- [Embeddings & Vector Width](Embeddings_%26_Vector_Width.md) (2 shared connections)
- [LLM-as-Judge Faithfulness](LLM-as-Judge_Faithfulness.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `docs/engineering/architecture/knowledge-corpus.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/architecture/testing.md`
- `docs/engineering/technologies/langchain.md`

## Audit Trail

- EXTRACTED: 55 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*