# Architecture Decision Records

An ADR records **why** a significant decision was made, what else was considered, and
what it costs. The code says what was decided; only this says why.

## Why we keep them

Two failure modes they prevent, both expensive.

**Re-litigating settled questions.** Without a record, every new engineer who notices
that the vector store could be Pinecone has to be talked out of it from scratch — or is
not, and rewrites it. The ADR answers in two minutes.

**Reversing a decision without knowing its cost.** Several things in this codebase look
like omissions and are not: no LangChain in the retrieval pipeline, no OpenTelemetry
collector, no chunk-level relevance in the golden set. Each was chosen against a named
alternative for a stated reason. Changing one is fine — changing one *without knowing
what it was buying* is not.

## Format

Each record: **Context** (the forces at play) · **Decision** · **Alternatives
considered** · **Consequences** (what it costs, honestly).

## Rules

1. **ADRs are append-only.** Superseding one means writing a new record that says so,
   never editing the old one. Why a past decision was right *at the time* is itself
   information — it tells you which assumption changed.
2. **A record is written when the decision is made**, not reconstructed later.
3. **Consequences include the costs.** A record listing only benefits is advocacy, and
   nobody trusts it twice.

## The records

| # | Decision | Status |
|---|---|---|
| [0001](0001-provider-abstraction.md) | Five protocols as the swappability seams | Accepted |
| [0002](0002-langchain-scope.md) | Adopt LangChain for undifferentiated work only | Accepted (supersedes an earlier rejection) |
| [0003](0003-hybrid-retrieval.md) | Hybrid retrieval with RRF fused in SQL | Accepted |
| [0004](0004-persistent-tracing.md) | Persist traces to a bounded JSONL file | Accepted |
| [0005](0005-evaluation-framework.md) | An in-repo evaluation harness, not a third-party one | Accepted |
| [0006](0006-chunking-strategy.md) | Keep `recursive` as the default until measured | Accepted |
| [0007](0007-knowledge-corpus-layout.md) | Corpus root is `docs/company/`; split the FAQ by topic | Accepted |
| [0008](0008-content-level-deduplication.md) | Deduplicate by source, not by content — and detect, don't collapse | Accepted, with a known cost |
