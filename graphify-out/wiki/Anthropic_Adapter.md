# Anthropic Adapter

> 25 nodes

## Key Concepts

- **SessionStore Protocol** (7 connections) — `docs/engineering/architecture/conversation.md`
- **Reciprocal Rank Fusion (RRF)** (7 connections) — `docs/engineering/architecture/retrieval.md`
- **Request Path** (6 connections) — `docs/engineering/architecture/overview.md`
- **ADR 0003 — Hybrid Retrieval with RRF Fused in SQL** (6 connections) — `docs/engineering/decisions/0003-hybrid-retrieval.md`
- **ADR 0013 — Conversational Memory Is Ephemeral, Process-Local and Bounded** (5 connections) — `docs/engineering/decisions/0013-ephemeral-session-memory.md`
- **Conversation** (4 connections) — `docs/engineering/decisions/0013-ephemeral-session-memory.md`
- **Hybrid Search** (4 connections) — `docs/engineering/architecture/retrieval.md`
- **InMemorySessionStore (bounded three ways)** (3 connections) — `docs/engineering/architecture/conversation.md`
- **Abstention Is a Code Path, Not a Prompt Instruction** (3 connections) — `docs/engineering/architecture/overview.md`
- **Protocols, Not Base Classes** (3 connections) — `docs/engineering/architecture/overview.md`
- **In-Process Protocol Test Doubles** (3 connections) — `docs/engineering/architecture/testing.md`
- **Bundled Chat UI** (3 connections) — `src/osc_assistant/api/static/index.html`
- **The complete Event Is Authoritative** (3 connections) — `src/osc_assistant/api/static/index.html`
- **Client Session Lifecycle** (3 connections) — `src/osc_assistant/api/static/index.html`
- **session_isolation metric** (2 connections) — `docs/engineering/architecture/evaluation-methodology.md`
- **Vendor Agnosticism Requirement** (2 connections) — `docs/engineering/architecture/overview.md`
- **Business Logic Never Imports a Provider** (2 connections) — `docs/engineering/architecture/overview.md`
- **InMemorySessionStore** (2 connections) — `docs/engineering/decisions/0013-ephemeral-session-memory.md`
- **SSE Frame Parsing Loop** (2 connections) — `src/osc_assistant/api/static/index.html`
- **Cormack, Clarke & Buettcher, Reciprocal Rank Fusion (SIGIR 2009)** (2 connections) — `docs/engineering/architecture/retrieval.md`
- **session: max_messages / max_sessions / idle_ttl_seconds** (1 connections) — `config/default.yaml`
- **Structural Session Isolation (unguessable token)** (1 connections) — `docs/engineering/architecture/conversation.md`
- **Minimal Hallucination Requirement** (1 connections) — `docs/engineering/architecture/overview.md`
- **One Datastore** (1 connections) — `docs/engineering/architecture/overview.md`
- **Instrumentation in Pipelines, Not Adapters** (1 connections) — `docs/engineering/architecture/overview.md`

## Relationships

- [LangChain Chat Bridge](LangChain_Chat_Bridge.md) (5 shared connections)
- [Measured Chunker Decision & IR Metrics](Measured_Chunker_Decision_%26_IR_Metrics.md) (4 shared connections)
- [Conversational Evaluation Tests](Conversational_Evaluation_Tests.md) (2 shared connections)
- [Conversation Rules & Rewriting](Conversation_Rules_%26_Rewriting.md) (1 shared connections)
- [CLI Tests](CLI_Tests.md) (1 shared connections)
- [LLM-as-Judge Faithfulness](LLM-as-Judge_Faithfulness.md) (1 shared connections)
- [Idempotency & Metric Honesty](Idempotency_%26_Metric_Honesty.md) (1 shared connections)
- [Embeddings & Vector Width](Embeddings_%26_Vector_Width.md) (1 shared connections)
- [Ingestion Tests](Ingestion_Tests.md) (1 shared connections)

## Source Files

- `config/default.yaml`
- `docs/engineering/architecture/conversation.md`
- `docs/engineering/architecture/evaluation-methodology.md`
- `docs/engineering/architecture/overview.md`
- `docs/engineering/architecture/retrieval.md`
- `docs/engineering/architecture/testing.md`
- `docs/engineering/decisions/0003-hybrid-retrieval.md`
- `docs/engineering/decisions/0013-ephemeral-session-memory.md`
- `src/osc_assistant/api/static/index.html`

## Audit Trail

- EXTRACTED: 61 (79%)
- INFERRED: 16 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*