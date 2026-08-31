# Conversation Rules & Rewriting

> 7 nodes

## Key Concepts

- **follow_up_resolution / follow_up_lift** (4 connections) — `docs/engineering/architecture/evaluation-methodology.md`
- **Conversation Rules** (3 connections) — `AGENTS.md`
- **fast_llm (query rewriter and judge model)** (3 connections) — `config/default.yaml`
- **retrieval.rewrite_queries: true** (3 connections) — `config/default.yaml`
- **History Reaches Retrieval Only Through the Query Rewriter** (2 connections) — `docs/engineering/architecture/conversation.md`
- **context_switch_recovery / context_pollution** (2 connections) — `docs/engineering/architecture/evaluation-methodology.md`
- **faithfulness (LLM-as-judge, opt-in)** (1 connections) — `docs/engineering/architecture/evaluation-methodology.md`

## Relationships

- [Engineering Handbook](Engineering_Handbook.md) (1 shared connections)
- [Anthropic Adapter](Anthropic_Adapter.md) (1 shared connections)
- [Core Architecture Decisions](Core_Architecture_Decisions.md) (1 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (1 shared connections)

## Source Files

- `AGENTS.md`
- `config/default.yaml`
- `docs/engineering/architecture/conversation.md`
- `docs/engineering/architecture/evaluation-methodology.md`

## Audit Trail

- EXTRACTED: 18 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*