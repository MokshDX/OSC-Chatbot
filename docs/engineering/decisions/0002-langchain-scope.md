# ADR 0002 — Adopt LangChain for undifferentiated work only

**Status:** Accepted · **Supersedes:** the outright rejection recorded in Phase 1 ·
**Date:** Phase 2

---

## Context

Requirement 7 of the original architecture asked for a pragmatic evaluation of
frameworks: *adopt LangChain/LlamaIndex if they genuinely improve the architecture,
reject them if not, on evidence rather than ideology.*

Phase 1 rejected LangChain outright, on the grounds that *"a framework would impose its
own document and retriever abstractions on top of ours, add a large transitive
dependency tree, and place an uncontrolled layer on the exact code path that most needs
tracing and tuning."*

Reviewing that in Phase 2 with more of the system built, the reasoning was found to be
**right about the framework and wrong about the libraries.** What the original
assessment treated as one decision was actually several, and two of the smaller ones
deserved a different answer.

The forces:

- Text splitting on the coarsest boundary that fits is a genuinely generic problem, and
  OSC's own implementation carried known defects.
- Writing an adapter per provider does not scale to the long tail (Bedrock, Vertex,
  Azure, Cohere, Mistral, Fireworks…).
- Other teams inside the company will build agents on frameworks OSC does not control,
  and will otherwise stand up a parallel index that drifts from this one.
- Against all three: the retrieval pipeline, the abstention policy and the citation
  contract are the parts most specific to OSC's requirements and most in need of being
  readable.

## Decision

**Adopt LangChain for undifferentiated work. Keep OSC's own code where OSC's design is
better.**

Adopted:

| What | Package | Why it is undifferentiated |
|---|---|---|
| Text splitting (`langchain_recursive`, `markdown`) | `langchain-text-splitters` | Generic problem, solved better elsewhere; heading-aware splitting would otherwise be written and maintained here |
| Provider reach (`langchain_bridge` for chat and embeddings) | `langchain-core` | One adapter covers the entire long tail by configuration |
| Outbound interoperability (OSC as a `BaseRetriever`) | `langchain-core` | OSC's value is the index, not the answer loop |

Refused:

| What | Why OSC's own is better |
|---|---|
| Vector store | The pgvector store fuses lexical and vector search with RRF **in SQL**, in one round trip. LangChain's `PGVector` does not |
| Retrieval pipeline | Six explicit, individually instrumented stages. LCEL would obscure the path most in need of reading |
| Answer loop | Abstention, citation policy and the streaming contract are the most OSC-specific parts of the system |
| Prompts | Frozen module constants, so the prefix stays byte-identical for caching and for attributable evaluation |
| Tracing | LangChain callbacks observe LangChain runs; most of this pipeline is not one. A tracer built on them would be blind to chunking, SQL fusion and abstention |
| Document type | `langchain_core.Document` at the boundary only |

**Dependency posture:** `langchain-core` and `langchain-text-splitters` are **core**
dependencies — both pure Python with no vendor SDK behind them, and both must be
importable for the registries to be complete. Every LangChain *integration* package
stays an install-time choice named by the operator in `options.class_path`.

## Alternatives considered

**Keep the total rejection.** Would have meant writing and maintaining a heading-aware
splitter, and an adapter per long-tail provider. Both are work with no OSC-specific
content — the definition of what a library should do.

**Adopt LangChain wholesale, including LCEL and `PGVector`.** Would have cost the SQL
fusion (the single best thing about the storage layer), made the retrieval path harder
to read, and put a framework on the code path the tracer exists to observe.

**LlamaIndex instead.** Stronger opinions about ingestion and indexing — which is
precisely the area where OSC's design is already deliberate. It would have taken over
more, not less.

**Use `init_chat_model` for the bridge** instead of naming a class by import path. It
lives in the `langchain` meta-package and would pull LangGraph in to save one line of
configuration.

## Consequences

**What it buys.**

- Two additional chunking strategies at zero maintenance cost, one of which
  (`markdown`) is heading-aware and well matched to the current corpus.
- The long tail of providers is reachable by configuration.
- Other teams can consume OSC's retrieval through a `BaseRetriever` and stay on the
  same index and tuning.

**What it costs.**

- **Two ways to reach a provider**, with different citation quality. A native adapter
  keeps provider-specific capabilities; the bridge produces marker-parsed citations.
- **Exposure to a fast-moving framework's release cadence.** Constrained to `>=1.0` and
  to two packages, which limits the blast radius but does not remove it.
- **Two of the four chunkers are unmeasured.** They cost no code, but "available" is not
  "better" — and the default is still `recursive` for the reason in
  [ADR 0006](0006-chunking-strategy.md).
- One more layer on the bridge path, invisible to the tracer's stage attribution.

**What must not change.** `integrations/` may import from the core; the core may **never**
import from `integrations/`. That one-way edge is what stops an outbound adapter from
becoming a dependency of the platform.
