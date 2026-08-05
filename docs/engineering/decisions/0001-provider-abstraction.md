# ADR 0001 — Five protocols as the swappability seams

**Status:** Accepted · **Date:** Phase 1

---

## Context

Every model in this system will be replaced. The chat model that is state of the art at
the time of writing will not be in eighteen months; the embedding model will be beaten
on MTEB within months; the vector store may need to move when the corpus outgrows one
machine.

The stated architectural requirements were explicit about it:

- Vendor-agnostic wherever practical; switching providers must require **configuration
  changes only**.
- Embeddings provider-agnostic and **independently swappable from the chat model**.
- The vector store must be replaceable without rewriting business logic.
- Design for experimentation — models, rerankers, chunkers and stores will be swapped
  frequently, and that must be cheap.
- **Avoid unnecessary abstractions.** Every abstraction must solve a real problem.

The last requirement is in tension with the first four, and resolving that tension is
what this decision is about. An abstraction per component is how codebases end up with
a factory for every noun.

## Decision

**Exactly five `Protocol` definitions**, in `protocols.py`, covering exactly the things
that are actually swapped: `ChatModel`, `EmbeddingModel`, `VectorStore`, `Reranker`,
`Chunker`. Plus one **optional** protocol, `StoreInspector`, for read-only
introspection.

Implementations satisfy them **structurally** — no base class, no inheritance, no
registration ceremony beyond one `REGISTRY.register(...)` line.

One rule enforces the property: **business logic imports `protocols` and `types` only,
and never imports a provider.** It is checkable with a grep.

`StoreInspector` is separate rather than part of `VectorStore` because every method on
`VectorStore` is one a new store *must* implement to be usable at all, whereas a hosted
vector database exposing no aggregate API should still be a perfectly good
`VectorStore`. Tooling probes for it with `isinstance` and reports its absence rather
than failing.

## Alternatives considered

**Abstract base classes.** Would work, and would force every provider — including
third-party objects and test doubles — to inherit from OSC's hierarchy. Structural
typing means a provider is compatible by virtue of its shape, which is what makes a
test double *indistinguishable* from a provider. See Consequences.

**Adopt a framework's abstractions (LangChain's `BaseChatModel`, `VectorStore`).**
Rejected here and revisited in [ADR 0002](0002-langchain-scope.md). Adopting them would
put an uncontrolled layer on the exact code path that most needs tracing and tuning, and
would tie the domain model to a framework's release cadence.

**No abstraction — call the SDKs directly.** Genuinely the right answer for a project
that will only ever use one provider. Not this one: the requirement to switch by
configuration is explicit, and the evaluation harness exists specifically to *compare*
providers.

**More protocols — one per component, including parsers.** Rejected. A parser is
selected by file extension and takes no options, so `PARSERS: dict[str, Parser]` is the
whole mechanism; a registry would be ceremony. The number of protocols is five because
five things are swapped, not because five is a good number.

## Consequences

**What it buys.**

- 37 registered providers across five registries. Adding one is a new file plus one
  import line — no pipeline change, no interface to inherit, no test to write.
- The chat and embedding models are genuinely independent, so upgrading one does not
  force a re-index.
- **The test suite is meaningful.** The API and CLI tests register in-process doubles
  through the ordinary registry — the same path a real provider takes — so "the whole
  stack can be retargeted by configuration alone" is asserted rather than assumed. This
  is the largest single payoff and it was not the original motivation.
- `./osc eval --profile <experiment>` compares providers with no code change, which is
  what makes [ADR 0005](0005-evaluation-framework.md) useful.

**What it costs.**

- **Protocols are enforced only statically.** Nothing at runtime checks that a
  registered provider satisfies `ChatModel`; the pipeline calls `complete()` and finds
  out. `mypy --strict` is what turns the convention into a check — which means the
  strict typecheck is load-bearing architecture, not hygiene.
- **A capability that only some providers have has nowhere natural to live.**
  `supports_citations` is on the protocol, and both paths produce the same `Citation`
  object, so nothing downstream can distinguish a verified citation from a parsed
  marker. That is a real, [documented
  limitation](../architecture/overview.md#where-the-architecture-is-weakest) and the
  direct price of a uniform interface.
- **Provider-specific tuning lives in untyped `options`.** `include_usage_in_stream`,
  `reasoning_effort` and `class_path` are dictionary keys, not fields. The alternative —
  a typed config per provider — would put provider knowledge back in the settings
  schema.
- Two ways to reach some providers (native adapter and LangChain bridge) with different
  citation quality.

**What must not change.** If a pipeline, route or CLI command ever imports a provider
module, the property this ADR exists to create is gone — silently, and with nothing
failing.
