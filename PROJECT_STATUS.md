# PROJECT_STATUS.md

**Project:** OSC Internal Knowledge Assistant
**Status:** Phase 6 — a measured, observable, durably logged, **conversational** knowledge engine on an authoritative corpus; Alpha, not production-ready
**Last updated:** 2026-08-31
**Audience:** a senior engineer, or a future Claude session, joining with zero context

Read this file first, then `README.md` for how to run it, then `claude.md` for the
engineering standards this repository is held to. `docs/engineering/` is the
engineering knowledge base — architecture, technologies and decision records, written
to explain *why* rather than *what*. `graphify-out/` holds a generated, agent-crawlable
map of the codebase.

---

## 1. Executive summary

A provider-agnostic retrieval-augmented **conversational** assistant over OSC's
internal documents. Employees ask a question; the system retrieves supporting
passages from an indexed corpus, generates an answer grounded in them, attaches
citations back to the sources, declines to answer rather than guessing when the
corpus does not support one — and remembers the conversation, so follow-ups resolve
against what was said before.

Three constraints distinguish it.

**Vendor agnosticism.** The chat model, embedding model, reranker, vector store and
chunking strategy are each selected by configuration and swappable independently.
Business logic depends on five `Protocol` definitions and never imports a provider
module. 37 providers are registered today; adding one is a new file plus one import
line — and via the LangChain bridge, most of the remaining ecosystem is reachable
with no new file at all.

**Observability.** Every significant stage of ingestion and question answering is a
timed span, one *turn* produces one trace, and that trace survives the process that
made it. Alongside it, a persistent structured log records what happened across
*every* execution — rotating, retained, and joined to the traces by `trace_id`.

**Measurement.** Every quality claim below is a number produced by `make eval`
against curated golden sets, not an opinion. Baselines are committed to
`evaluation/baselines/` and a regression fails the gate.

**Where it stands.** The full path runs against real infrastructure: the schema
corpus is parsed, chunked, embedded and stored in PostgreSQL with pgvector.
Questions retrieve by hybrid search and are answered by Qwen3 through Ollama, with
citations back to the source file. Sessions hold conversation history in the
answering process. **445 tests pass in one command** — `make verify` — covering the
hermetic, pgvector and end-to-end tiers in a single pytest invocation. `ruff` and
`mypy --strict` clean across 67 source files.

### Measured baseline

Default local profile, **schema corpus** (11 documents / 80 chunks), `markdown`
chunking, `top_k=5`, query rewriting on. Committed to `evaluation/baselines/`.

**Single-turn** — `suites/schema.yaml`, 55 scored + 6 abstention:

| | | | |
|---|---|---|---|
| `recall@5` | **0.982** | `groundedness` | **1.000** |
| `hit_rate@5` | **0.982** | `citation_coverage` | **1.000** |
| `ndcg@5` | **0.918** | `citation_precision` | 0.875 |
| `mrr` | **0.897** | `fact_match` | 0.782 |
| `precision@5` | 0.200 ᵃ | `abstention_accuracy` | **0.667** ᵇ |
| `latency_p50` | 8.3 s | tokens in/out | 63.6k / 2.2k |

**Conversational** — `suites/conversational.yaml`, 18 sessions / 46 turns:

| | | | |
|---|---|---|---|
| `follow_up_resolution` | **0.941** | `context_pollution` | **0.000** |
| ↳ cold control | 0.765 | `context_switch_recovery` | 0.857 |
| ↳ **lift** | **+0.177** | `session_isolation` | **1.000** |

ᵃ At the structural maximum: most questions have one relevant document, so with
`k=5` no ranking can exceed 0.2. ᵇ **The weakest number in the system** — two of six
unanswerable questions still got an answer.

These are the *committed baseline* values. A verification re-run of the same commit
scored `fact_match` 0.800 rather than 0.782 — a two-case difference, well inside the
derived tolerance of ±0.12, and a working illustration of why generation metrics get
a statistical interval rather than a threshold. Every deterministic retrieval metric
reproduced exactly.

**These numbers are not comparable to Phase 5's.** The corpus changed (§5.1), so the
Phase 5 figures (recall@5 0.932, `fact_match` 0.90, `abstention_accuracy` 0.80) are
FAQ-suite numbers and are preserved as such in `evaluation/baselines/faq-*.json`
rather than overwritten.

**Two things were changed on evidence this phase**, both following the project's own
baseline → change → measure → keep/reject rule:

* **`markdown` replaced `recursive` as the default chunker** (+0.073 recall@5). The
  schema documents are mostly tables, and `recursive` was splitting them mid-row and
  mid-word. All four strategies were measured; the table is in ADR 0012.
* **Query rewriting was turned on** (`follow_up_lift` 0.000 → +0.177). It is the only
  path by which conversation history reaches retrieval, and the cold-control design
  is what made its absence a number rather than a suspicion.

**Where it does not stand.** There is still no authentication, no per-document access
control and no rate limiting. Conversation memory does not survive a restart, which
makes sticky sessions a prerequisite for running more than one replica. Answer quality
is bounded by an 8B local model — `abstention_accuracy` of 0.667 is the number that
would most embarrass this system in front of a user, and `fact_match` of 0.782 the
one that would most disappoint them.

**The honest one-line summary:** a working, verified, thoroughly observable,
measurable and now genuinely conversational knowledge engine on a local stack — a
credible Alpha, one authentication story and one abstention pass away from being
defensible in production.

---

## 2. Original project goals

From `claude.md` (the repository's engineering handbook) and the approved
architecture:

**Product goal.** An internal knowledge assistant for OSC employees that answers
questions from OSC's own documents, designed to grow into a broader enterprise AI
knowledge platform supporting multiple knowledge sources and document formats.

**Stated priorities**, in the handbook's own order: accuracy, minimal
hallucinations, maintainability, scalability, modular architecture, developer
experience. Engineering decisions optimise for correctness → reliability →
maintainability → readability → scalability → performance → development speed.

**Architectural requirements:**

1. Vendor-agnostic wherever practical; switching providers must require
   configuration changes only.
2. Embeddings provider-agnostic and independently swappable from the chat model.
3. The vector store must be replaceable. PostgreSQL + pgvector is the preferred
   default; migrating elsewhere must not require rewriting business logic.
4. Design for experimentation — models, rerankers, chunkers and stores will be
   swapped frequently, and that must be cheap.
5. Avoid unnecessary abstractions. Every abstraction must solve a real problem.
6. New providers are plug-in additions rather than edits to business logic.
7. Evaluate frameworks pragmatically — adopt LangChain/LlamaIndex if they genuinely
   improve the architecture, reject them if not, on evidence rather than ideology.

**Non-functional targets set during design** (now partly measured — see §11):
time-to-first-token < 2s p95, full answer < 10s p95, faithfulness ≥ 95%, retrieval
recall@10 ≥ 90%, full index rebuildable unattended in < 4h.

**Status against those targets, as of Phase 6.** `recall@5` is 0.982 on the schema
suite, so the recall target is met at a *stricter* k than it was set at (it was 0.932
on the Phase 5 FAQ corpus). The latency targets are not met on
the local stack — `latency_p50` is 8.3s at concurrency 1 against a 10s *p95* target —
and that is a statement about an 8B model on a laptop rather than about the
architecture. Whether
the latency target is wrong for this deployment, or the deployment is wrong for the
target, is a decision that now has numbers behind it.

---

## 3. Current architecture

```
connectors ──▶ parse ──▶ chunk ──▶ embed ──▶ vector store
                                                  │
question ──▶ rewrite ──▶ search ──▶ rerank ──▶ generate ──▶ answer + citations

            every stage above is a timed span in one trace
            every stage above is scored by `make eval`
```

### The five seams

Everything swappable is a `Protocol` in `src/osc_assistant/protocols.py`.
Implementations satisfy them **structurally** — no base class, no inheritance:

| Protocol | Responsibility |
|---|---|
| `ChatModel` | `complete()` / `stream()`; declares `supports_citations` |
| `EmbeddingModel` | `embed_documents()` / `embed_query()`; declares `dimensions` |
| `VectorStore` | `replace_document()`, `delete_document()`, three search methods, hash listing |
| `Reranker` | `rerank(query, candidates, top_k)` |
| `Chunker` | `split(document) -> list[Chunk]` |

Plus one **optional** protocol, `StoreInspector`, added in iteration 2. It carries
read-only introspection — statistics, document listing, chunk lookup — and is
deliberately *not* part of `VectorStore`: every method on `VectorStore` is one a new
store must implement to be usable at all, whereas a hosted vector database exposing
no aggregate API should still be a perfectly good `VectorStore`. Tooling probes for
it with `isinstance` and reports its absence rather than failing. Both built-in
stores implement it.

`types.py` holds the only vocabulary shared across modules, all frozen dataclasses.
**Business logic imports `protocols` and `types` only. It never imports a
provider.** That single rule is what makes vendor-agnosticism real rather than
aspirational, and it is checkable with a grep.

### Wiring

`registries.py` holds five `Registry` instances mapping a provider name to a
factory. A provider module registers itself on import; `providers/__init__.py`
imports the sub-packages; `container.py` (the composition root) imports that package
once. Nothing in the call path imports every possible implementation.

`Container` builds components lazily via `cached_property`, so `ingest` never
constructs a chat model and therefore never needs an LLM credential. It injects into
the vector store the values the store cannot know itself — vector width and the
active embedding model id, both derived from the embedding model.

Shutdown releases every component that was *actually built*: `cached_property`
stores into the instance `__dict__`, so its presence there is exactly the record of
what was constructed. Components are probed for `aclose()` or `close()` rather than
being required to have one, because most providers hold no resource (§5).

### Request path

1. **Authenticate** — *not implemented.* See §8.
2. **Rewrite** (`retrieval/rewrite.py`) — resolves conversational references into a
   standalone query using the configured *fast* model. Best-effort: any failure
   falls back to the original question and records why on the span.
3. **Retrieve** (`retrieval/pipeline.py`) — vector, keyword, or hybrid. Hybrid runs
   both and fuses with Reciprocal Rank Fusion; the pgvector store implements the
   same formula in SQL so both stores rank identically.
4. **Rerank** — `noop` by default; `cross_encoder` available.
5. **Generate** (`generation/answerer.py`) — builds a `ChatRequest` with the frozen
   system prompt and the retrieved chunks as `sources`.
6. **Cite** — Anthropic passes sources as structured documents and receives verified
   per-span citations. Every other provider renders sources into the prompt and
   parses `[n]` markers back out. Both paths produce the same `Citation` shape.
7. **Abstain** — no retrieval hits means the model is never called. No citations
   means the answer is treated as ungrounded.

### Observability layer

`observability/` is three modules with one dependency direction: `trace` collects,
`store` persists, `render` presents; the package `__init__` is the only place that
composes them.

- **`trace.py`** — a context-var span tree. `span()` outside a trace returns a
  detached span that records nothing, so instrumented code carries no `if tracing`
  branches. `trace()` nested inside another trace *extends* it rather than forking,
  which is what lets `retrieve` be both a whole operation (`./osc search`) and a
  stage of a larger one (`./osc ask`). Bounded by `max_spans_per_trace`, with the
  dropped count recorded so totals stay accurate past the cap.
- **`store.py`** — a bounded, append-only JSONL log so a trace outlives the process
  that made it. Rotation, not rewriting: appending is O(1). Writing never raises —
  instrumentation that can break the thing it observes is a liability.
- **`render.py`** — the waterfall and one-line summary. Bars are positioned by
  offset and sized by duration, so "these ran back to back" and "this one dominated"
  are distinguishable at a glance.

Instrumentation lives in the pipelines, not the adapters. Every provider call is
made from a pipeline, so wrapping the call sites covers all 37 providers without a
single adapter importing the tracer — and a new provider is traced the day it is
written.

### Ingestion path

`ingestion/parsers.py` maps a file extension to an extraction function:
Markdown/text read directly, HTML through the standard library's `html.parser`, PDF
through `pypdf` (per page, retaining `page_count`), `.docx` through `python-docx`
(including table cells). Parsers extract and never rewrite: chunk text is quoted
back as citation evidence, so invented text would make that evidence a forgery.

`FilesystemLoader` records any file it cannot read in `failures`, which the pipeline
treats as **present but unreadable** rather than deleted (§13).

### Storage

One PostgreSQL database holds chunk text, embeddings (`pgvector`), the lexical index
(a generated `tsvector` column) and document metadata. `migrations/001_init.sql` is
applied by a forward-only runner in `pgvector.py`; the embedding dimension is
substituted into the DDL at migration time. The HNSW index is created only when that
dimension is ≤ 2000. Every table carries a `workspace_id` partition key.

---

## 4. LangChain integration — what was adopted and what was not

Requirement 7 asked for a pragmatic evaluation. Iteration 1 rejected LangChain
outright; iteration 2 revised that on a narrower reading of the evidence, and the
revision is worth recording honestly.

**The original rejection was right about the framework and wrong about the
libraries.** "A framework would impose its own document and retriever abstractions
on top of ours, add a large transitive dependency tree, and place an uncontrolled
layer on the exact code path that most needs tracing and tuning" — all still true,
and all still the reason LangChain does not own the retrieval pipeline, the vector
store, the prompts or the answer loop. What the original assessment treated as one
decision was actually several, and two of the smaller ones deserved a different
answer.

The rule applied: **adopt LangChain for undifferentiated work, keep OSC's own code
where OSC's design is better.**

### Adopted

**Text splitting** (`chunking/langchain_splitters.py`). `langchain-text-splitters`
supplies `langchain_recursive` and `markdown`. Splitting text on the coarsest
boundary that fits is a genuinely generic problem; OSC's own implementation carried
known rough edges (a chunk can exceed its budget by up to the overlap, and the
overlap slice can cut mid-word); and heading-aware splitting would otherwise have to
be written and maintained here. The `markdown` strategy splits on structure first and
packs to size second, recording the heading path on each chunk's metadata.

Chunk ids come from the same shared helper the built-in chunkers use, so idempotent
ingestion behaves identically whichever strategy is configured.

**Provider reach** (`providers/{llm,embeddings}/langchain_bridge.py`). One adapter
wraps any LangChain `BaseChatModel` or `Embeddings` behind OSC's protocols, making
Bedrock, Vertex, Azure, Cohere, Mistral, Fireworks and the rest reachable by
configuration rather than by writing an adapter each time. This creates a deliberate
two-tier provider strategy: native adapters are the default path and keep
provider-specific capabilities (Anthropic's verified citations, the reasoning
controls on the OpenAI-compatible family); the bridge covers the long tail at the
cost of marker-parsed citations and one more layer.

The class is named by import path rather than resolved by `init_chat_model`, which
lives in the `langchain` meta-package and would pull LangGraph in to save one line
of configuration.

**Outbound interoperability** (`integrations/langchain.py`). OSC's retrieval pipeline
presented as a LangChain `BaseRetriever`. OSC's value is the indexed corpus and how
it is retrieved, not the answer loop, and teams inside the company will build agents
on frameworks OSC does not control — making the retriever consumable means they use
the same index and tuning rather than standing up a parallel one that drifts.

### Not adopted, with reasons

| Component | Why OSC's own is better |
|---|---|
| Vector store | The pgvector store fuses lexical and vector search with RRF **in SQL**, in one round trip. LangChain's PGVector does not. |
| Retrieval pipeline | Six explicit stages, each instrumented and independently testable. LCEL would obscure the path most in need of reading. |
| Answer loop | Abstention, the citation policy and the streaming contract are the parts most specific to OSC's requirements. |
| Prompts | Frozen module constants, precisely so the prefix stays byte-identical. A template engine has nothing to add to a constant. |
| Tracing | LangChain callbacks observe LangChain runs; most of this pipeline is not one. A tracer built on them would be blind to chunking, SQL fusion and the abstention decision. |
| Document type | `langchain_core.Document` at the boundary only. Domain types stay frozen dataclasses with no framework in them. |

### Dependency posture

`langchain-core` and `langchain-text-splitters` are **core** dependencies: both are
pure Python with no vendor SDK behind them, and both must be importable for the
registries to be complete. Every LangChain *integration* package
(`langchain-anthropic`, `langchain-aws`, …) remains an install-time choice named by
the operator in `options.class_path`. This preserves the existing principle — the
core runtime is small, vendor SDKs are extras.

**The default chunker is now `markdown`, from `langchain-text-splitters`** — the
clearest vindication of the adoption rule above. Splitting text on the coarsest
boundary that fits is undifferentiated work; the library does it better than the
implementation written here; and the switch was settled by a measurement rather than
by preference (recall@5 0.909 → 0.982 across four strategies, ADR 0012). It was
deliberately deferred for two phases because switching changes every chunk id in a
live index and the project's rule is that a retrieval change ships with a measured
improvement — there was no golden set until Phase 4, and it was not spent until
Phase 6.

---

## 5. What changed in this iteration (Phase 6)

The brief was to turn a measured single-turn engine into a measured *conversational*
one, on an authoritative corpus, with one command for correctness and one for quality.
Five things were built, and two settings were changed on evidence.

### 5.1 The knowledge source moved to `docs/company/schema/`

Eleven module persistence-schema documents — metafield inventories, metaobject field
tables, Prisma models, sample payloads — became the production corpus. The FAQ and
scenario documents stay on disk and left the index (ADR 0011).

**This invalidated the Phase 5 baseline**, and that is stated rather than hidden: the
86-case FAQ golden set and both its baselines measure a different system. They are
preserved as a runnable second suite (`suites/faq.yaml`, its own workspace) because
deleting evaluation cases when the corpus moves is how a benchmark becomes a story —
and because it is the only suite over *prose*, which makes it the control when a
retrieval change is suspected of being specific to tables and JSON.

The corpus root also stopped being three literals kept equal by hand (`Makefile`,
`doctor`, the startup banner) and became one setting, `corpus.root` (ADR 0010). The
regression test that asserted two literals agreed now asserts the property those
literals existed to protect.

### 5.2 Session memory — the headline

`conversation.py`: a `SessionStore` Protocol, an `InMemorySessionStore` bounded by
message count, session count and idle TTL, and a `Conversation` that defines what one
turn is. New endpoints `POST /api/sessions` and `DELETE /api/sessions/{id}`;
`session_id` on `/api/chat`, mutually exclusive with client-supplied `history`. The
bundled UI now holds a session id rather than a transcript and deletes it on
`pagehide`.

**Memory is deliberately ephemeral** (ADR 0013). The audit stream already holds one
durable record per answered question, which is what a compliance question actually
wants, without keeping user text in a second place with its own retention story.

The pieces were mostly already there and unused — `Answerer` and `QueryRewriter` both
took `history` — so this was less a feature than the missing place for the
conversation to live.

**A defect found by writing the test for it:** the `session_context` span recorded
nothing, because `Conversation` loaded history *before* opening the trace and
`span()` outside a trace is detached by design. The failure was invisible in the
answer and total in the trace.

**A second defect found by the end-to-end suite:** `last_active_at` advanced only on
`record()`, so a session idle for almost its whole TTL could pass the history read,
spend ten seconds generating, and then expire at the write — discarding a turn after
the model call had been paid for. Reading history now counts as activity.

### 5.3 Conversational evaluation, with cold controls

`suites/conversational.yaml` — 18 sessions, 46 turns covering reference resolution,
context retention across three and four turns, context switching, irrelevant history,
in-conversation abstention, clarification and recovery.

**The design decision that makes it worth having is the control run.** A follow-up
that gets answered proves nothing on its own — it may have retrieved the right
document by keyword luck. Every turn marked `requires_context` or `context_switch` is
run twice, once in the session and once cold, and the pair is the measurement.

That design immediately paid for itself. `follow_up_resolution` was 0.765 and looked
healthy; the cold control was **also 0.765**, so the lift was exactly **0.000** —
conversational memory was contributing nothing to retrieval. Turning on query
rewriting moved the lift to +0.177. Without the control, a working-looking number
would have hidden a feature that did not work.

`session_isolation` measures context *size* per turn rather than comparing retrieved
documents. The document-overlap version looks correct and is not: with 11 documents
and `k=5`, nearly every turn legitimately retrieves something another case expects, so
it would report a catastrophic leak on a perfectly isolated system.

### 5.4 A mature evaluation system

* **nDCG@k added** — the one metric that separates rankings `recall` and `mrr` cannot
  (three relevant documents at ranks 1,2,3 versus 1,4,5).
* **`evaluation/gate.py`** — regression gates whose tolerances are *derived*, not
  typed: `1/n` for deterministic retrieval metrics, two binomial standard errors for
  sampled generation metrics, relative and non-blocking for latency, and three
  explicit trade-off guards (ADR 0014). `--fail-under` is gone.
* **`evaluation/report.py`** — the quality report: scorecard grouped by concern with
  bars only where a bar means something, category performance worst-first, weakest
  cases with trace ids, and the gate's findings with the tolerance that judged them.
* **`docs/engineering/architecture/evaluation-methodology.md`** — every metric's
  definition, calculation, purpose, interpretation, **limitations**, baseline and
  regression criteria, plus what is deliberately *not* measured and why.

**A defect found by reading the report:** abstention cases name no relevant documents,
so their recall is 0 by construction, and the category table ranked them as the
system's worst-performing area — permanently, for a reason unrelated to retrieval.
The same class of lie as `fact_match` scoring 1.0 on a retrieval-only run. They now
render as a dash.

### 5.5 Two canonical commands

`make verify` runs **every** tier — hermetic, pgvector and end-to-end — in one pytest
invocation, so there is one summary line, one exit code and one list of failures.
That needed `OSC_E2E_DSN` split out from `OSC_TEST_DSN`, because the two tiers need
different databases and with one variable only one could be pointed at the right place.

`make eval` runs both suites, gates both against their committed baselines, and exits
non-zero on a regression.

### 5.6 Changed on evidence

| Change | Evidence | Recorded in |
|---|---|---|
| Default chunker `recursive` → `markdown` | recall@5 0.909 → **0.982**, all four strategies measured | ADR 0012 |
| `rewrite_queries` false → **true** | `follow_up_lift` 0.000 → **+0.177**, single-turn bit-identical | ADR 0013, config comment |

Both required `--reindex` or a full re-measure, and both were rejected-or-kept on a
before/after number rather than on plausibility.

---

## 5b. What changed in Phase 4

The brief was maturity and measurement. Three things were built: the evaluation
framework, a corpus restructured around real company documents, and the engineering
knowledge base — followed in Phase 5 by persistent logging and audit.

**Read this section knowing that Phase 6 superseded two of its decisions.** The corpus
it describes (`docs/company/`, the 17-file FAQ) is no longer the production corpus
(§5.1, ADR 0011), and the `--fail-under` gate it describes has been replaced by derived
tolerances (ADR 0014). The reasoning is kept because it is still the reasoning — what
changed is the corpus, not whether splitting a 633-line FAQ was the right call.

### 5.1 The evaluation framework — the headline

`src/osc_assistant/evaluation/` (four modules), `evaluation/golden-set.yaml`
(86 curated cases), `./osc eval`, and three Makefile targets. *That file is now
`evaluation/suites/faq.yaml`; the package is seven modules.*

It drives the **real** pipelines built by the **real** `Container`, because an
evaluation that ran against a special code path would measure the special code path.
Full design and rationale: `docs/engineering/architecture/evaluation.md` and
ADR 0005.

| Decision | Reason |
|---|---|
| **Built in-repo, not RAGAS/TruLens/DeepEval** | Each is LLM-judge-first, so the metrics that should gate CI are the non-deterministic ones; each imposes its own data model on the code path we most want to read; and the metrics themselves are twenty lines of set arithmetic. The value in those tools is the judge prompts, and one prompt is not a dependency |
| **Relevance scored at document level** | Chunk ids derive from chunk boundaries, so changing the chunker changes every id — invalidating the golden set on precisely the experiment it exists to run |
| **Deterministic metrics gate CI; the judge is `--judge`** | A gate that can change its mind between two runs of the same commit is not a gate |
| **`groundedness` from ids, not judgement** | A citation whose chunk was not in the retrieved set cannot have been read from a source. Set arithmetic, no model |
| **Abstention cases in the golden set** | Without them an evaluation rewards a model that answers everything confidently |
| **Configuration snapshot in every result** | So comparing two runs cannot silently compare two different systems |

**A defect found by building it**, recorded because it is the class of bug this
subsystem is most prone to: `fact_match` initially reported **1.0** on
`--retrieval-only` runs. It is computed as "no expected fact was missing", and a run
that generated no answers has missed nothing — arithmetically correct, factually a
lie. Fixed by omitting generation metrics entirely from a retrieval-only run;
`test_evaluation.py` holds the regression.

### 5.2 The knowledge corpus, restructured around real company documents

The seed corpus was replaced with production content: the OSCP Wholesale B2B advance
FAQ plus four scenario documents. That forced two decisions (ADR 0007).

**The ingest root moved from `docs/` to `docs/company/`.** The engineering knowledge
base had to live somewhere, and with the old root an employee asking "how does OSC
handle refunds?" could have been answered from an ADR about reciprocal rank fusion,
with a correct citation, confidently. The failure mode is invisible — retrieval
succeeds, grounding succeeds, the citation is right, the universe is wrong. An
exclusion list would fail open; a directory boundary fails safe.

**The 633-line FAQ was split into 17 topic files**, all 89 questions preserved
verbatim. The reason is measurement: with a single-document corpus, `recall@k` is 1.0
for every answerable question and the retrieval metrics measure nothing. Citations
also improved from *"Advance FAQ"* to *"Tax Display"*.

Also: an `.xlsx` parser (`openpyxl`, read-only, one block per sheet, cells tab-joined
per row) because two of the four scenario documents were otherwise invisible; and
`./osc doctor` no longer reports dotfiles as unparseable corpus. Doctor went from
8 ok / 1 warn to **9 ok / 0 warn**.

### 5.3 The engineering knowledge base

`docs/engineering/` — 8 architecture pages, 6 technology pages and 8 ADRs, with
Mermaid diagrams and authoritative references. It exists because `PROJECT_STATUS.md`
answers *what the system is* and the code answers *what it does*, and neither answers
*why it is built this way* — the question that actually costs time on handover.

### 5.4 Persistent logging and audit (Phase 5)

`logging.py` grew from a 68-line formatter into the logging system: rotating file
persistence, retention, an audit stream, TRACE-level pipeline detail, trace
correlation and redaction. Full design in
`docs/engineering/architecture/logging.md` and ADR 0009.

**The load-bearing decision is that coverage came from the span stream, not from new
call sites.** Every stage of OSC is already a `span()` with structured attributes, so
one hook in `trace.py`'s span-exit path emits a TRACE record per stage — giving
`retrieve`, `embed_query`, `search`, `threshold`, `rerank`, `generate`, `finalise`,
`load_hashes`, `document`, `chunk`, `embed`, `store` and `prune` their log lines with
**no modification to any pipeline, provider, chunker, store, or the evaluation and
LangChain layers**. The alternative would have been a second set of instrumentation
drifting from the first.

What the span stream cannot supply is *which command produced it* — every command
initialises identically, so a day of history is a run of indistinguishable
`settings.resolved` records. `load()` emits one `cli.command` record naming the
command and its flags; the positional tail is payload and appears only under
`capture_payloads`, because `osc ask "<a real question>"` puts user text on the
command line.

| Concern | Mechanism | Why |
|---|---|---|
| Persistence, rotation, retention | stdlib `RotatingFileHandler` | Disk bounded by `max_bytes * (backup_count + 1)`; oldest deleted, not archived |
| Non-blocking writes | stdlib `QueueHandler`/`QueueListener` | A log call enqueues; disk I/O is on a background thread |
| Trace correlation | a `logging.Filter` on the tracer's context var | Any log line expands into a waterfall with `./osc trace <id>` |
| Redaction | a `logging.Filter` on the queue entry | Applies identically to console and file |
| TRACE level | `addLevelName(5, ...)` | Somewhere to put per-stage detail that would be unbearable at DEBUG |

Two streams: `.osc/logs/osc.log` (operational) and `.osc/logs/audit.log` (one record
per answered question, longer retention, pinned at INFO so a coarser root level
cannot silence it). New command: `./osc logs [--audit] [-f]`.

**Four defects found by running it, all silent, none caught by construction:**

- **`QueueHandler.prepare()` strips `exc_info`** to make records picklable across a
  process boundary. Our queue is thread-local, so the stripping bought nothing and
  silently deleted every traceback. Fixed with a `prepare()` override.
- **The redaction heuristic redacted token counts.** `input_tokens` contains
  "token", so every cost measurement became `[redacted]` — found by reading a real
  audit record, not by a test. Fixed with a `NEVER_REDACT` allowlist.
- **The test suite wrote into the developer's real log.** `test_cli.py` purges every
  `OSC_*` variable to prove the commands retarget through configuration alone, which
  also purged the isolation `conftest` installed; it re-applied the trace directory
  and not the log directory. Found by watching `.osc/logs/osc.log` grow during
  `make check`. Both overrides now sit adjacent under a comment naming both.
- **File logging could not be disabled from the environment.** An environment
  variable is always a string, so `OSC_LOGGING__DIRECTORY=null` created a directory
  named `null` and an empty value wrote `osc.log` into the working directory. That is
  the documented setting for a containerised deployment, and a container configures
  through the environment. Fixed with a `field_validator` mapping empty/`null`/`none`
  to `None`.

All four now have regression tests. The lesson recorded in ADR 0009: the failure
modes of a logging system are silent, and the only way to find them is to read the
output of a real run.

---

## 5c. What changed in Phase 3

### The observability gap that was actually there

The in-memory ring buffer works for the server — the process is long-lived, so
`/api/traces` answers "what did that request just do?" with no storage. It does not
work for the CLI, where the process exits the moment the answer is printed. A
developer who did not think to pass `--explain` had no way back to the trace, and
`./osc trace` could only read from a running server.

**Alternatives evaluated**, before choosing:

| Option | Rejected because |
|---|---|
| Re-run with `--explain` | A generation is not deterministic. Re-running produces *a* trace, not *the* trace — and the answer under investigation is usually the odd one. It also costs a full model call and cannot explain a failure that already happened in CI. |
| A `traces` table in PostgreSQL | Puts write load on the primary datastore for a debugging feature, and makes tracing unavailable in exactly the situation where it is most wanted: when the database is what is broken. |
| OpenTelemetry + collector | Right destination once traces leave the host, wrong answer for reading a trace in a terminal. `Span` stays OTel-shaped so that remains an exporter, not a rewrite. |
| A daemon or socket | A background process to read a trace is worse than the problem. |

**Chosen: a bounded, append-only JSONL log** (`observability/store.py`), plus
**auto-explain on failure**, which needs no persistence at all. The file is the
smallest thing that outlives a process; it needs no service, schema or migration; it
works identically for the CLI, the server and CI; and it uses exactly the payload
the HTTP endpoint already serves, so one parser and one renderer cover both sources.

### Everything else

| Area | Change |
|---|---|
| **Traces** | `./osc traces` lists from the persisted log with `--name`, `--failed` and `--slower-than` filters; `./osc trace [id]` expands one, defaulting to the most recent. `--url` still reads from a running service. |
| **Failure reporting** | A failed command prints its trace before the error. `AssistantError` — the project's vocabulary for operator problems — is reported as a message, not a traceback; anything else keeps its traceback, because for a bug the frames are the point. |
| **Error translation** | `PgVectorStore.setup()` now wraps connection failures in `VectorStoreError` with the DSN (password redacted). Untranslated, a stopped database surfaced as a bare `OSError` traceback in the CLI and **bypassed the API's error handler entirely** — the most common operational failure was also the worst reported. |
| **CLI coherence** | Commands grouped into three `--help` panels by purpose. `traces`/`trace` now mirrors `documents`/`document`. `version` added. |
| **Server experience** | A human summary on **stderr** — URLs, active components, warnings — while structured JSON continues to stdout untouched, so `serve > run.log` still yields a clean parseable log. Startup notes (empty index, mixed embedding models, non-development environment without auth) are both printed and logged. |
| **SSE robustness** | The stream handler caught only `AssistantError`, so an unexpected exception closed the connection with **no terminal event** and left the UI spinning forever. Every exit now emits one; unexpected exceptions get a stable client message with the detail in the log. |
| **Lifecycle** | `Container.shutdown()` released only the vector store; provider HTTP clients leaked. It now releases every component that was built, probing for `aclose`/`close`, and never constructs one that was not. |
| **Naming** | `provider: local` meant an OpenAI-compatible server in `llm` and sentence-transformers in `embeddings`. Renamed to `openai_local`, with `local` kept as a working alias. |
| **Packaging** | `py.typed` added and shipped, so consumers see the annotations. |
| **Test hygiene** | Trace persistence is isolated per test in `conftest`, so the suite no longer writes into the repository. |

---

## 6. Repository structure

```
src/osc_assistant/
├── protocols.py            the five seams + optional StoreInspector
├── types.py                domain vocabulary — the largest shared surface
├── registries.py           five Registry instances
├── registry.py             generic Registry[T] + ComponentConfig
├── settings.py             layered config: env > .env > YAML profile
├── errors.py               AssistantError hierarchy
├── fusion.py               Reciprocal Rank Fusion (reference implementation)
├── grounding.py            source rendering, citation parsing, reasoning-model hygiene
├── container.py            composition root + lifecycle
├── logging.py              the logging system: rotation, audit, redaction, queue
├── observability/          trace.py · store.py · render.py
├── cli/                    __init__ · _shared · core · diagnose
├── providers/
│   ├── llm/                anthropic · openai_compatible · gemini · langchain_bridge
│   ├── embeddings/         openai_compatible · voyage · gemini · local · langchain_bridge
│   ├── reranking/          noop · cross_encoder
│   └── vectorstores/       pgvector · memory
├── chunking/               recursive.py · langchain_splitters.py
├── ingestion/              parsers.py · loaders.py · pipeline.py
├── retrieval/              pipeline.py · rewrite.py
├── generation/             answerer.py · prompts.py
├── conversation.py         SessionStore · InMemorySessionStore · Conversation
├── evaluation/             dataset · metrics · judge · runner · conversational · gate · report
├── integrations/           langchain.py — OSC exposed outward
└── api/                    app.py · schemas.py · sse.py · banner.py · static/index.html

tests/                      445 tests across 23 files
migrations/001_init.sql     schema, with a dimension-conditional HNSW index
docs/company/schema/        THE CORPUS — 11 documents, authoritative (corpus.root)
docs/company/{faq,scenarios}/  on disk, deliberately NOT indexed
docs/engineering/           the engineering knowledge base — NOT ingested
evaluation/suites/          schema.yaml · conversational.yaml · faq.yaml (preserved)
evaluation/baselines/       committed reference runs (results/ is gitignored)
config/                     default.yaml + 4 experiment profiles
osc                         the CLI wrapper — no .venv paths anywhere
graphify-out/               generated knowledge graph
```

**A third rule, and Phase 6 changed how it is enforced:** the corpus is
`corpus.root` — `docs/company/schema/` — and `docs/engineering/` is not. The root used
to be three literals kept equal by hand; it is now one setting, read by `ingest`,
`doctor` and the startup banner (ADR 0010). Do not reintroduce a second default.

**One rule to preserve:** business logic imports `protocols` and `types` only. If a
pipeline, route or CLI command ever imports a provider module, the vendor-agnosticism
this project is built around has been broken.

**A second, newer rule:** `integrations/` may import from the core, and the core may
never import from `integrations/`. That one-way dependency is what stops an outbound
adapter from becoming a dependency of the platform.

### What the knowledge graph says about this structure

Current build, 2026-09-01, an incremental update after this phase: **2651 nodes,
5469 edges, 171 communities**, all 171 named, with a clean health check (no dangling,
missing or collapsed edges).

The new subsystems are visible as their own clusters rather than smeared across
existing ones — *In-Memory Session Store*, *Session Memory Architecture*, *Session
Store Internals*, *Conversation Turn Orchestration*, *Conversational Evaluator*,
*Regression Gate Engine* and *Quality Report Renderer* are each distinct communities.
That is what a genuinely new subsystem should look like, and it was true of the
logging and evaluation subsystems when they were added.

**The graph earned its keep this phase.** Its extraction pass flagged four
documentation contradictions that no test could catch: `retrieval.md` still
documenting query rewriting as off while `overview.md` said on;
`chunking-and-embeddings.md` and `langchain.md` still calling `recursive` the default
and the chunker comparison "the open item"; and three pockets of `PROJECT_STATUS.md`
contradicting its own §5. All four are fixed. It also surfaced an import cycle in
`evaluation/`, which led to `mean_of` moving to `metrics.py` where its own purity rule
says it belongs.

**Node count went down and edge count went up** in the preceding full rebuild, which
is the finding worth keeping. The build before it reported 2086/4572; the 2026-08-05
rebuild reported 1981/4624 — density 2.19 → 2.33 edges per node. The earlier build
derived its document nodes structurally (heading stubs); the rebuild extracted them
semantically, so 429 stubs were replaced by 324 concepts that carry rationale
attributes, external citations and hyperedges. A smaller, denser, more meaningful
graph. `to_json`'s shrink guard correctly refused the write until the reduction was
verified.

`MemoryVectorStore` (72 edges), `Document` (70), `StubEmbeddingModel` (69),
`ComponentConfig` (65) and `Container` (60) are the architectural hubs —
configuration, the corpus record and the composition root are what the system routes
through, which matches the intended design. An *earlier* build reported
`StubEmbeddingModel`, a **test double**, as the single most connected node in the
codebase, ahead of every real component: the graph's way of saying that the test
suite, not production wiring, was what exercised every seam. Real components lead
now. The doubles are still central and should be — they are how the protocol layer is
proven.

**Two gaps closed in the 2026-08-05 rebuild**, both previously invisible rather than
known:

- `graphifyy[office]` — the four `.docx`/`.xlsx` scenario documents were being
  reported as `skipped_sensitive` and silently dropped. They are 82 of the production
  index's 193 chunks, so the graph had been blind to roughly 42% of the real corpus.
- `graphifyy[sql]` — `migrations/001_init.sql` now contributes nodes, so the storage
  schema no longer has to be read from raw SQL.

**On graph health.** The current diagnostic is clean: **0 dangling-endpoint edges, 0
missing endpoints, 0 self-loops, 0 collapsed edges** across 4952 edges. That is the
incremental path resolving every new endpoint against the graph it merges into.

The full-rebuild path does not report zero, and the difference is worth knowing
rather than treating as a regression. That build's diagnostic reported 273
dangling-endpoint edges, of which 245 (90%) were `imports`/`imports_from` edges
pointing at third-party packages and stdlib modules — `pkg_pydantic`, `pathlib`,
`typing`, `json`. Those are the graph correctly declining to invent nodes for things
outside the scanned corpus, not information loss. Roughly 17 edges (0.3%) were
genuine cross-chunk semantic references that failed to resolve, which is the real and
small cost of parallel extraction. The "collapsed" edges an undirected simple `Graph`
reports are multi-edges such as `evaluate_eval → typer.Option ×8` at one source line
merging — expected, not corruption.

**One caveat stands.** Community *labels* are hand-written, and a rebuild that changes
the community set silently renames every changed community by its hub until they are
rewritten. `graphify label --backend=ollama` would automate it but requires the
`openai` package, which is not installed. All 105 labels in the current build were
written by hand after the merge.

---

## 7. Completed milestones

| # | Milestone | Evidence |
|---|---|---|
| 1 | Five-protocol seam layer | `protocols.py`; no provider import in any pipeline (grep-verifiable) |
| 2 | Registry + composition root | 37 registered providers across 5 registries |
| 3 | 15 chat providers | `anthropic` (native citations), `gemini`, an OpenAI-compatible adapter serving 12 names, and the LangChain bridge |
| 4 | 12 embedding providers | openai-compatible family, `voyage`, `gemini`, `local`, LangChain bridge |
| 5 | 3 vector store names | `pgvector`/`postgres` (production) and `memory`; identical RRF ranking |
| 6 | 4 chunking strategies | `recursive`, `fixed`, `langchain_recursive`, `markdown` |
| 7 | Layered configuration | env > `.env` > YAML profile; four experiment profiles |
| 8 | Idempotent ingestion | content-hash skip, incremental re-index, pruning, per-document failure isolation, `--reindex` escape hatch |
| 9 | Hybrid retrieval | BM25-equivalent `tsvector` + pgvector cosine, fused by RRF in SQL |
| 10 | Grounded generation with citations | Anthropic native path + marker-parsing fallback, one `Citation` shape |
| 11 | Abstention policy | no hits → no model call; no citations → ungrounded; identical in both modes |
| 12 | HTTP API + SSE streaming | health, status, search, chat, traces |
| 13 | Multi-format parsing | 8 extensions, one function per format, verified against a real corpus |
| 14 | PostgreSQL layer verified | 18 integration tests against a real database |
| 15 | Fully local default stack | Ollama + pgvector; no credential, no corpus text off-host |
| 16 | **Execution tracing** | every stage timed; one trace per request; nested traces merge correctly |
| 17 | **Trace persistence** | bounded JSONL log; traces outlive the process; `traces`/`trace` commands |
| 18 | **Operational CLI** | 14 commands in three groups; `doctor`, `status`, `config`, document and chunk inspection |
| 19 | **Store inspection** | `StoreInspector` on both stores; SQL aggregates and percentiles |
| 20 | **LangChain integration** | two chunkers, two provider bridges, one outbound retriever — all scoped (§4) |
| 21 | **End-to-end smoke test** | 9 tests driving the real stack; the old manual verification table, executed |
| 22 | **Human/machine output split** | stderr banner, stdout JSON; both audiences served without compromise |
| 23 | Chat UI | one static page, streaming over SSE, honouring the authoritative-`complete` contract |
| 24 | **Evaluation framework** | 4 modules, 86-case golden set, 11 metrics, `./osc eval`, committed baselines, CI gate |
| 25 | **Measured quality baseline** | *(Phase 4, FAQ corpus)* recall@5 0.932 · mrr 0.860 · groundedness 1.00 · fact_match 0.90 |
| 26 | **Knowledge corpus restructure** | real company documents; corpus/engineering split; 17-file FAQ; `.xlsx` support |
| 27 | **Engineering knowledge base** | 9 architecture pages, 6 technology pages, 9 ADRs |
| 28 | **Persistent logging** | rotating files, retention, async writes, TRACE level, trace correlation, redaction |
| 29 | **Audit trail** | one record per answered question, separate stream and retention |
| 30 | **Schema-first knowledge corpus** | `corpus.root` is one setting; 11 authoritative documents; FAQ preserved as a runnable suite |
| 31 | **Session memory** | `SessionStore` seam, bounded in-memory store, session endpoints, UI holding a session id |
| 32 | **Conversational evaluation** | 18 sessions / 46 turns, every context-dependent turn run against a cold control |
| 33 | **Derived regression gates** | tolerances computed from the run; three trade-off guards; verified exit 1 on a real regression |
| 34 | **The quality report** | scorecard by concern, category performance worst-first, weakest cases with trace ids |
| 35 | **Two canonical commands** | `make verify` (445 tests, one invocation) and `make eval` (both suites, gated) |
| 36 | **Measured chunker decision** | all four strategies compared; `markdown` adopted, +0.073 recall@5 (ADR 0012) |
| 37 | **Measured rewriting decision** | `follow_up_lift` 0.000 → +0.177; single-turn verified unaffected |

---

## 8. Not yet implemented

Ordered by how much each blocks a production release.

1. **Authentication (OIDC).** No identity anywhere. `/api/chat` and `/api/search`
   accept arbitrary unauthenticated input. Intended design: OIDC against OSC's IdP,
   with group membership feeding access control.
2. **Per-document access control.** ACLs resolved at index time and enforced as a
   SQL predicate at query time, so an unauthorised chunk is never retrieved. No ACL
   column, no principal resolution, no filtering exists. Phase 1 was scoped to
   company-wide-readable content specifically to avoid needing this yet.
3. **Rate limiting and concurrency bounds.** A request can hold a connection for the
   full 120s provider timeout. Nothing caps requests per user.
4. **Durable conversation persistence.** Conversation memory exists and works
   (§5.2) but lives in the answering process: it does not survive a restart, and
   behind more than one replica a client's next turn may reach a process that never
   heard of its session. **Sticky sessions or a shared store is a prerequisite for
   horizontal scaling.** The `SessionStore` Protocol is the seam; ADR 0013 is why it
   is ephemeral for now.
5. **Feedback capture.** No thumbs, no comments — so the golden set cannot yet be fed
   by real user questions, which is the natural way for it to grow past 86 cases.
7. **Connectors beyond the filesystem.** Confluence, Drive, SharePoint. The loader
   shape (`load() -> AsyncIterator[Document]`) is established and used.
8. **Deployment artefacts.** No Dockerfile for the service, no IaC, no CI pipeline.
   `docker-compose.yml` covers only the development database.
9. **Trace export.** Traces are local. A collector, and an OTel exporter, is the
   next step once more than one process matters.

---

## 9. Technical debt

Ordered by impact. Items closed in this iteration are listed first, because a future
session should not re-derive them.

### Closed in Phase 6 (this iteration)

- **The corpus root was three literals kept equal by hand** — `Makefile`,
  `cli/diagnose.py` and `api/banner.py`. Now one setting, `corpus.root` (ADR 0010).
  The regression test that compared two of the three literals now asserts the
  property they existed to protect, and covers the third, which it never did.
- **The default chunker was an unmeasured guess** — and a bad one for this corpus.
  `recursive` split schema tables mid-row and mid-word; one chunk of `schema.md`
  began `ormId`. Measured against three alternatives, `markdown` adopted (ADR 0012).
- **Conversational memory reached generation and not retrieval, invisibly.** With
  `rewrite_queries: false` a follow-up was generated with full context and retrieved
  for as if standalone. The cold-control design turned this from a suspicion into
  `follow_up_lift = 0.000`, and rewriting is now on.
- **The `session_context` span recorded nothing.** `Conversation` loaded history
  before opening the trace, and `span()` outside a trace is detached by design — so
  the one stage that distinguishes "answered as if it were a first question" from
  "answered badly" was absent from every trace. Found by the test written for it.
- **A session could expire during its own turn.** `last_active_at` advanced only on
  `record()`, so a session idle for almost its whole TTL passed the history read,
  spent ten seconds generating, and failed at the write — discarding a turn after the
  model call was paid for. Found by the end-to-end suite; reading now counts as
  activity.
- **The category table ranked abstention cases as the worst-performing area.** They
  name no relevant documents, so their recall is 0 by construction. Permanently
  misleading, and the same class of lie as `fact_match` scoring 1.0 on a
  retrieval-only run. They now render as a dash.
- **`--output` with two suites silently overwrote the first result.** Now refused.
- **CI gate thresholds were round numbers typed by hand** — "the baseline rounded
  down". Replaced by tolerances derived from the run (ADR 0014).

### Closed in Phase 4

- **No evaluation harness** — built (§5.1). Every setting in `config/default.yaml` is
  still an educated guess, but they are now *measurable* guesses.
- **`fact_match` scored 1.0 for work never done** — a defect in the new harness,
  found and fixed before the baseline was committed.
- **The end-to-end suite ingested the production corpus path** (`CORPUS =
  Path("docs")`), so it asserted against company documents anyone could edit *and*
  swept `docs/engineering/` into its index — the knowledge base being retrieved,
  which is the exact failure the corpus split exists to prevent. It now generates its
  own six-format corpus in `tmp_path`, including a hand-assembled minimal PDF so that
  PDF text extraction is still proven without adding a rendering dependency. Runtime
  fell from 139s to 22s as a side effect. A regression test now asserts the Makefile
  and CLI corpus roots agree and that the knowledge base is not reachable from the
  corpus root.
- **The default local stack leaked an HTTP client per container.**
  `Container.shutdown()` probes each component for `aclose`/`close`, but the
  OpenAI-compatible chat and embedding adapters — what `provider: ollama` resolves to
  — owned an `AsyncOpenAI` client and exposed neither, so they were silently exempt
  from the mechanism whose docstring claimed the leak was fixed. Only `voyage` and
  `pgvector` of eight adapters implemented their side of it. `aclose()` added to the
  OpenAI-compatible and Anthropic adapters, with a structural regression test.
- **The corpus and the repository's own documentation shared an ingest root** — split
  (§5.2). This was latent rather than active; writing the knowledge base activated it.
- **Two `.xlsx` corpus documents were unparseable** — `openpyxl` parser added; they
  contribute 82 of the index's 193 chunks.
- **`./osc doctor` reported `.DS_Store` as a corpus problem** — dotfiles skipped.
  A warning an operator learns to ignore defeats the warning.
- **Retrieval metrics were structurally impossible** — a one-document corpus makes
  `recall@k` 1.0 for every answerable question. The FAQ split fixed the measurement,
  not just the presentation.

### Closed in Phase 3

- **CLI traces died with the process** — persisted trace log (§5b).
- **A failing command produced a raw traceback** — `AssistantError` reported as a
  message; trace printed on failure.
- **asyncpg exceptions escaped untranslated** — now `VectorStoreError`, with the
  DSN password redacted. This also fixed the API, which could not handle them either.
- **The SSE stream could end with no terminal event** — every exit now emits one.
- **Provider resources were never released** — `Container.shutdown()` closes what
  it built.
- **`provider: local` meant two different things** — renamed to `openai_local`,
  alias retained.
- **`settings.py` had zero tests** — 10 tests pin the four-layer precedence.
- **`RetrievalResult` was the only unfrozen dataclass** — frozen.
- **No `py.typed` marker** — added and shipped.
- **The end-to-end path was not automated** — `make test-e2e`, 9 tests.
- **The test suite wrote into the working directory** — isolated in `conftest`.

### P1 — fix before real traffic

**Endpoints are unauthenticated, unbounded and unthrottled.** Documented as
deferred, which is fine as a plan and not fine as a release state. The service now
*says so* at every startup when `environment != development`, but the constraint
still lives in prose rather than in the code path. *Smallest fix:* refuse to start
when `environment != "development"` and no auth is configured. Ten lines.

**Every retrieval and generation setting is still an educated guess** — but now a
measurable one. Chunk size, `top_k`, `rrf_k`, the reasoning budget and the choice of
chunking strategy have never been tuned against the golden set. The harness exists;
the tuning pass has not been run. This is now the cheapest high-value work in the
project, and it is Milestone C.

**`latency_p95` is 92.9 s.** Measured under `--concurrency 2` against a single Ollama
instance, so it is partly contention and partly cold start — the slowest case took
223 s for 197 output tokens. But the provider timeout is 120 s, which means the
observed p95 is within a factor of 1.3 of the point where requests start failing
rather than merely being slow. Nothing caps concurrency today.

**The two scenario workbooks are 42% of the index.** 82 of 193 chunks come from the
two `.xlsx` files, and they compete for retrieval slots against the FAQ. Four of the
six recall failures retrieved a spreadsheet chunk in place of the FAQ document that
answers the question. Whether that is bad chunking of tabular data, bad ranking, or a
golden set that under-specifies its relevant documents is not yet determined — and it
is exactly the kind of question the harness now makes answerable.

**34 of 193 chunks (17.6%) are exact duplicates**, and nothing detects it.
`OSCP_B2B_Scenario_Document.docx` and `OSCP_B2B_Scenario_Document-1.docx` differ at
the byte level but extract to byte-identical text (content hash `54314756e14a2f4f`),
so they index as two documents of 34 chunks each. Duplicate chunks compete for the
same `top_k = 5` slots, which is a plausible contributor to the recall failures above.
`content_hash` answers "has *this* document changed?", never "is this the same as
*another* document?" — see ADR 0008. *Smallest fix:* a `duplicates` check in
`./osc doctor` grouping indexed documents by content hash. Roughly ten lines; the
store already exposes `list_document_hashes()`. Deleting the duplicate file is the
corpus owner's call, not ours.

**Logs are process-local and unshipped.** Same limitation the trace store has and
the same answer: an exporter, once more than one host matters. The queue is also
unbounded, so a pathological burst grows memory rather than dropping records —
deliberate, since dropping a diagnostic to bound memory trades away the thing you
are reading, and the rotating file already bounds disk. Records queued at a
`SIGKILL` are lost; that is the price of not blocking on `fsync`.

**Rotation is size-based, so retention windows are not predictable.** Disk is
bounded (~60 MB operational, ~210 MB audit at defaults) but "exactly the last 30
days" is not a guarantee this policy can make. See ADR 0009.

**The integration suite shares the application database.** Isolation is by
`workspace_id` and it is honoured, but a run against a production DSN would write to
production. The new e2e suite takes a separate database, which is the right pattern;
the pgvector suite should follow it.

### P2 — maintainability

**`api/app.py` uses `response_model=None` on `/chat`**, dropping the JSON branch
from the OpenAPI schema. Splitting into `/chat` and `/chat/stream` is the fix, and
it is an API break the bundled UI would have to follow — deferred deliberately
rather than overlooked.

**Speculative code with no consumer.**
- `providers/{llm,embeddings}/gemini.py` — ~330 lines and a `google-genai`
  dependency reaching a service the `gemini_openai` preset already reaches through
  an adapter that is already shipped and tested.
- `FixedSizeChunker` — an evaluation baseline for an evaluation harness that does
  not exist. Now joined by two LangChain chunkers that are also unmeasured, though
  those at least cost no code to maintain.

**No OCR path for scanned PDFs.** They are detected and rejected with a clear
message rather than silently indexed as empty, which is the right failure. But a
real internal corpus contains scans.

**Trace reads are whole-file.** `TraceStore._read_backwards` reads both files to
serve twenty summaries. Bounded by `max_trace_file_bytes` and fine at 5 MB; marked
with a `ponytail:` comment naming seek-from-end as the upgrade if that limit rises.

### Minor

- `container.py` imports `RecursiveChunker` purely for a registration side effect.
- `pgvector/pgvector:pg16` is a moving tag in `docker-compose.yml`; pin the digest.
- ~~The UI does not send conversation history~~ — closed in Phase 6. It holds a
  server-side `session_id` and deletes it on `pagehide`; query rewriting is on by
  default, on a measured lift (§5.2, §5.6).

---

## 10. Known limitations

**Citation strength differs by provider, silently.** Anthropic returns citations
verified against the source text. Every other provider — including the local default
and the LangChain bridge — asserts them via `[n]` markers that a model can emit for
an unsupported claim. Both produce the same `Citation` object, so nothing downstream
can tell the difference. A deliberate trade-off for vendor agnosticism. The harness
that would measure the gap now exists and has never been pointed at a hosted
provider — that is one command and one credential away, and it is the highest-value
unrun experiment in the repository.

**Prompt injection is mitigated, not eliminated.** Source bodies can no longer close
the data delimiter (it carries a per-request nonce), but a document can still contain
persuasive text. Nothing prevents a corpus document from arguing with the system
prompt — only from impersonating it.

**Retrieval quality is measured and strong.** `recall@5` 0.982 over 55 scored cases
on the schema corpus. The single miss is `bulk-variant-rules-key`, where `priceRule`
is described in both `schema-2.md` and `schema-6.md` and the golden set names one.
Part measurement finding, part curation finding.

`precision@5` of 0.200 looks alarming and is not: most cases have exactly one relevant
document out of five slots, so the ceiling *is* 0.2 — the observed value is a perfect
score. It is useful as a *relative* measure across runs and misleading as an absolute
one, and it is the metric in the report most likely to be misread.

**Answer quality is the weaker half.** `fact_match` 0.782 with `recall@5` 0.982 means
the passage was retrieved and the fact did not survive into the answer roughly one
time in five. That gap is the 8B model, not the search stack, and it is the clearest
argument for the unrun hosted-provider comparison above.

**Abstention is the weakest measured behaviour, and it got worse on the new corpus.**
`abstention_accuracy` is **0.667** — four of six, down from 0.80 on the FAQ suite. Two
of six questions the corpus cannot answer received an answer anyway. The architectural
guarantee (no retrieval hits → the model is never called) is solid; what fails is the
case where retrieval *does* return plausible-looking schema documents and the model
writes something from them. Six cases is also a small enough sample that the derived
gate tolerance is ±0.385, which is honest rather than reassuring: **more abstention
cases is the single highest-value addition to the golden set.**

**Conversational memory does not survive a restart**, and behind more than one replica
a client's next turn may reach a process that never heard of its session. Sticky
sessions or a shared store is a prerequisite for horizontal scaling (ADR 0013).

**History reaches retrieval only through query rewriting**, which costs one `fast_llm`
call per follow-up on the critical path. With rewriting off, conversational memory
contributes exactly nothing to retrieval — measured, not asserted.

*The paragraph below is the Phase 5 finding, retained because the mechanism it
describes is unchanged:* `abstention_accuracy` was The fifth (`abstain-woocommerce`) did not trip the architectural
abstention because retrieval returned hits; instead the model correctly wrote *"The
sources provided do not mention compatibility with WooCommerce or BigCommerce."* That
is the right answer, scored as a miss. The architectural guarantee (no hits → no model
call) is solid; the prose self-abstention is a model behaviour with no guarantee behind
it, and the metric currently cannot distinguish them.

**The local answer model misreads figures.** Observed directly: asked for expense
approval thresholds, `qwen3:8b` rendered "500 to 2,500 EUR" as "50,000 to 2,500 EUR"
while citing the correct passage. Retrieval was right, the citation was right, the
number was wrong. This is the central honest caveat of the local stack. `fact_match`
is now 0.90, and all three failures were retrieval or omission rather than
transcription — so the gap is quantified but not yet reproduced under measurement.

**Citation precision is 0.732 while groundedness is 1.00.** Every citation the model
emitted pointed at a chunk it was actually shown — no fabrication. But roughly a
quarter of citations point at a document the golden set does not consider relevant,
which is what citing all five sources indiscriminately looks like.

**Answers are limited by a 4096-token context.** Ollama loads `qwen3:8b` with a
4096-token window, capping the corpus sent to the model at five chunks. Since the
chunker changed (ADR 0012) the median chunk is 278 characters rather than 826, so
`top_k=5` is now roughly a third of the context it used to be — **`top_k` has not
been re-tuned and is the most obvious next experiment.** Two variables were
deliberately not moved at once.

**Traces are process-local and lossy.** The persisted log is bounded and lives on
one host. It answers "what happened recently, here". It does not answer "what
happened last Tuesday across the fleet" — that needs the exporter in §8.

**Trace text may contain corpus content.** Questions, rewritten queries and answers
are recorded by default. `observability.capture_text: false` retains every timing,
count and stage while reducing text to a length. The HTTP trace endpoints are
additionally refused outside `environment: development`, and that check is not
overridable by configuration.

**Ingestion assumes a single writer.** `_prune` reads the document-hash map once at
the start of a sync and deletes anything absent at the end.

**Chunk overlap can exceed the size budget** in the built-in `recursive` chunker.
No longer on the default path — `markdown` is the default since ADR 0012 — but
`recursive` is still registered and still has the defect.

---

## 11. Testing status

```
make verify     445 tests · unit + pgvector + end-to-end · one invocation · ~42s  ✅
                ruff clean · mypy --strict clean across 67 source files

make eval       61 single-turn cases + 18 conversations / 46 turns          ✅
make eval-gate  passes on the committed baseline; exits 1 on a regression   ✅ verified
```

**`make verify` asks whether the system is correct. `make eval` asks whether it is
good.** They are different questions and a system can pass every test while answering
every question badly, which is why evaluation is a separate command and not a test
file.

`make verify` runs every tier in a **single** pytest invocation — one summary line,
one exit code, one list of failures — which required splitting `OSC_E2E_DSN` out from
`OSC_TEST_DSN` because the two tiers need different databases. Verified stable across
three consecutive runs.

| File | Covers |
|---|---|
| `test_conversation.py` | **New.** Session creation, isolation, closure and cleanup; history trimmed from the oldest end; LRU eviction; idle expiry; **reading history postpones expiry so a turn cannot outlive itself**; follow-ups reaching generation in both modes; abstentions recorded as turns; a failed stream recording nothing; **the `session_context` span existing at all** |
| `test_conversational_evaluation.py` | **New.** Multi-turn dataset validation; per-turn scoring; **the cold control running only for turns that need one**; lift computed from the pair and honest when negative; pollution floored at zero; a failed turn costing one turn and still releasing its session |
| `test_gate.py` | **New.** Derived tolerances for deterministic and sampled metrics; smaller samples earning wider tolerances; latency reported but never blocking; **all three trade-off guards**; regression attribution down to the individual turn; counts excluded from gating |
| `test_evaluation.py` | Metrics against worked examples incl. **nDCG separating rankings recall and MRR cannot**; golden-set validation and its rejection cases; failed cases excluded from means; retrieval-only omits generation metrics; **the shipped suites load and declare their corpora** |
| `test_api.py` | Health, status, search, chat (both modes), SSE ordering, trace endpoints and their environment gate; **session open/close/404, isolation over HTTP, `session_id` with `history` rejected** |
| `test_e2e.py` | Six formats indexed from a corpus it generates itself; idempotency; hybrid ranking; a cited answer; abstention; both modes agreeing; the run fully traced; **the whole session lifecycle against live Ollama and PostgreSQL** |
| `test_logging.py` | Creation, rotation, retention and the disk ceiling; console/file level separation; trace-id correlation; the span bridge on and off; credential and payload redaction; audit isolation; tracebacks surviving the queue; token counts not read as credentials |
| `test_cli.py` | Every operational command; doctor's pass/warn/fail behaviour; trace commands across process boundaries; operator-error reporting; help grouping |
| `test_langchain_integration.py` | Both chunkers (id stability, content preservation, size budget, heading metadata); the chat and embedding bridges; the outbound retriever |
| `test_pgvector_integration.py` | Migrations, tsvector, SQL fusion, cascade delete, JSONB, workspace isolation, transaction rollback, inspection SQL |
| `test_fusion_and_grounding.py` | RRF ordering/dedup; citation marker parsing; **prompt-injection containment** |
| `test_trace_store.py` | Cross-process readability, rotation, malformed lines, unwritable directories, round-trip fidelity |
| `test_observability.py` | Span tree shape, nested-trace merging, error capture, span cap, text redaction |
| `test_retrieval.py` | Store contract, all three strategies, top_k, reranking, rewriting, **min_score applied pre-rerank** |
| `test_parsers.py` | Every format, content preservation, corrupt and scanned files, **failure isolation** |
| `test_ingestion.py` | Idempotency, change detection, pruning, **unreadable-file prune exemption**, `--reindex`, **the knowledge base unreachable from `corpus.root`** |
| `test_chunking.py` | Size budget, id stability, **content preservation** |
| `test_server_lifecycle.py` | Startup notes, **in-flight stream failure emits a terminal event**, shutdown releases components without constructing unused ones |
| `test_inspection.py` | `StoreInspector` contract on the memory store; empty-store edge cases |
| `test_answerer.py` | Abstention in both modes, citation policy, streaming reassembly |
| `test_settings.py` | Four-layer precedence, nested env merge, malformed profiles, trace exposure gate |
| `test_reasoning_models.py` | `<think>` stripping, exhausted-budget error, reasoning markers never becoming citations |
| `test_registry.py` | Registration, override, unknown-provider error |

**What the suite is good at.** It runs the *real* pipelines against in-process
implementations of the protocols. The API and CLI tests register those doubles
through the ordinary registry — the same path a new provider takes — so "the whole
stack can be retargeted by configuration alone" is asserted, not assumed. Several
tests are regressions for defects actually found and reproduced, including three
found in this phase.

**Remaining gaps:**

1. **No hosted provider has ever been called.** Every hosted adapter is exercised
   only via stubs — including the Anthropic native-citation path, the only verified
   citation implementation in the codebase. Running
   `./osc eval --profile config/experiments/hosted-anthropic.yaml --suite schema` is
   one command and needs one credential.
2. **No load or concurrency test.** `./osc eval --concurrency N` is the closest thing
   and was not built for that purpose, though it is what produced the p95 figures.
3. **Session memory is tested single-process only.** The failure that matters at
   scale — a client's next turn reaching a replica that never heard of its session —
   is a property of a deployment this suite cannot construct.
4. **One end-to-end assertion is deliberately tolerant.** Whether a live 8B model
   abstains is not deterministic, so the E2E abstention tests assert
   `abstained or not citations`. Asserting it strictly produced a test that passed in
   isolation and failed in a full run; the strict form is covered against stubs.
5. **The Gemini adapters still hold an unreleasable client.** `genai.Client` exposes
   no async close in the installed surface and is an optional extra.
6. **No question was written by a real user.** Both suites were curated from the
   corpus, so they inherit its blind spots.

## 12. Configuration and environment

**Runtime:** Python 3.12+. PostgreSQL 16+ with `pgvector`.

```bash
make install                    # venv + dev extras
./osc doctor                    # is everything reachable?
```

**Configuration layers**, highest precedence first: process environment → `.env` →
YAML profile (`config/default.yaml`, overridable with `OSC_PROFILE`). Any value is
addressable from the environment with `OSC_` and `__` for nesting.
`./osc config` prints what was actually resolved, with credentials redacted.

**Defaults (all local):** Ollama `qwen3:8b` with reasoning disabled, Ollama
`nomic-embed-text` (768-d), pgvector, `noop` reranker, **`markdown` chunking**
(900/120), hybrid retrieval (30 candidates → top 5), 1500 max completion tokens,
**query rewriting on**, ephemeral sessions (20 messages / 1000 sessions / 1h idle),
tracing on and persisted to `.osc/`.

**Reference environment as verified:** PostgreSQL 18.4 with pgvector 0.8.2; Ollama
0.32.5 serving `qwen3:8b` at a 4096-token context and `nomic-embed-text`.

**Four constraints that will bite:**
- Changing the embedding model changes the vector width, fixed in the DDL at
  migration time. It requires a new database and a full re-index.
- pgvector cannot build an HNSW index above 2000 dimensions; above it search
  degrades to an exact scan.
- The prompt budget is sized for a 4096-token context.
- Changing the chunker invalidates every stored chunk while every content hash
  still matches. Use `./osc ingest --reindex`.

---

## 13. Important design decisions

**Protocols, not base classes.** Structural typing means a provider is compatible by
virtue of its shape. A test double is indistinguishable from a provider — which is
what makes the API and CLI tests meaningful.

**One datastore.** PostgreSQL holds chunk text, embeddings, lexical index and
metadata. A chunk and its vector cannot drift apart, there is one backup, and hybrid
retrieval is one round trip.

**Hybrid retrieval by default.** Internal corpora are dense with acronyms, codenames
and error strings that semantic search handles badly, and paraphrase that keyword
search handles badly. Avoiding a known failure mode, not premature optimisation.

**Abstention is architectural, not a prompt.** No hits → no model call. In streaming
mode the final `complete` event is authoritative.

**Frozen prompts.** Module constants with no interpolation. Anything dynamic would
break prefix caching and make evaluation results unattributable.

**`workspace_id` from day one.** The only speculative design in the codebase, and
defended: adding a partition key to a populated corpus is a data migration.

**Text extraction is a plain dict of functions, not a registry.** A parser is
selected by file extension and takes no options, so `PARSERS: dict[str, Parser]` is
the whole mechanism.

**Inspection is a separate, optional protocol.** Discussed in §3. The last change to
`VectorStore` removed a method rather than adding one; that direction is worth
protecting.

**Instrumentation in pipelines, not adapters.** Discussed in §3.

**Human output on stderr, machine output on stdout.** The two audiences are served
by two streams rather than by compromising one. `serve > run.log` yields a clean
parseable log while the terminal still shows where the service is listening.

**Operator errors are messages; bugs are tracebacks.** `AssistantError` is the
project's vocabulary for problems an operator must fix, and each carries an
actionable message. A traceback buries it under frames describing our call stack
rather than their problem. Anything else keeps its frames, because for a bug the
frames are the point.

### Defects found and fixed, by session

**This session:** asyncpg exceptions escaping untranslated (which also bypassed the
API error handler); the SSE stream ending with no terminal event on an unexpected
exception; provider resources never released.

**Previous session:** retrieval-only runs produced no trace, because only the
answerer opened one.

**Earlier:** metadata double-encoded in PostgreSQL; pruning could delete an
unreadable-but-present document; the migration would have failed on the previous
default embedding model; prompt injection via source bodies; ingestion could
permanently lose a document; the chunker silently corrupted document text.

---

## 14. Recommended implementation order

The ordering principle is unchanged — **make the system verifiable before making it
bigger.** Measurement existed but was unspent for two phases; Phase 6 spent part of it,
and the binding constraint has moved again.

1. **Widen the abstention cases, then fix abstention.** `abstention_accuracy` is
   **0.667** — the weakest measured behaviour in the system and the one that most
   directly contradicts the product's stated priority of minimal hallucinations. Six
   cases is also too few for the metric to be trustworthy: the derived gate tolerance
   is ±0.385, so it would take a drop of more than two cases to fail. **Add cases
   first**, re-baseline honestly, then fix. `min_score` is 0.0 today, so retrieval
   happily returns five chunks for a question about submarines — that is the first
   hypothesis to test.
2. **Re-tune `top_k`.** The chunker change (ADR 0012) cut the median chunk from 826 to
   278 characters, so `top_k=5` is now roughly a third of the context it used to be.
   Two variables were deliberately not moved at once; this is the owed half.
3. **One hosted-provider run.** `./osc eval --profile config/experiments/hosted-anthropic.yaml`
   is one command and one credential. It would put a number on the
   verified-versus-parsed citation gap — the only unmeasured claim in the architecture
   — and separate "the 8B model is the ceiling" from "the pipeline is the ceiling" for
   `fact_match` 0.782.
4. **Add authentication (OIDC).** The first hard blocker to exposing the service.
   Group membership from the IdP is also the input to item 6.
5. **Production start-up guard.** Refuse to start when `environment != development`
   and no auth is configured. Ten lines, and the constraint becomes enforced rather
   than announced. Cheap enough to land alongside item 4.
6. **Add per-document ACLs.** Only after auth exists.
7. **A reranker decision**, with the measured delta. `cross_encoder` is registered,
   tested and never scored.
8. **Feedback capture.** The raw material for growing the golden sets past curated
   questions — and the natural source of the abstention cases item 1 needs.
9. **Durable session storage**, when a second replica is on the horizon. The
   `SessionStore` Protocol is the seam; nothing above it changes.
10. **Second connector.** The loader shape is established and has a parser layer
    behind it; this proves both.
11. **Deployment artefacts and trace export.** Dockerfile, CI (running `make verify`
    and `make eval-gate`), and an OTel exporter once traces need to leave the host.

**Closed by Phase 6, previously on this list:** the chunker comparison (ADR 0012), the
query-rewriting decision (ADR 0013), and conversation memory itself.

**Deliberately late:** a richer web client, multi-tenancy beyond the partition key,
additional providers (the bridge covers the long tail). **Deliberately absent:**
fine-tuning, agentic tool use, a knowledge-graph layer.

---

## 15. Next milestones with success criteria

### Milestone A — Evaluation harness — **DONE**
*Delivered in Phase 4; the two open criteria closed in Phase 6.*

| Criterion | Status |
|---|---|
| `make eval` prints retrieval and generation metrics and writes a comparable JSON | ✅ |
| A pull request that drops recall below a threshold fails CI | ✅ `make eval-gate`, verified exit 1 — but no CI runs it yet |
| Baseline numbers for the default profile are committed | ✅ `evaluation/baselines/` |
| The local model's numeric-fidelity gap is quantified | ✅ `fact_match` 0.782 |
| At least one provider comparison run end to end | ❌ still needs a credential |
| **A chunker comparison is recorded** with a decision and a number | ✅ **ADR 0012** — all four measured, `markdown` adopted |

### Milestone A′ — Spend the harness — **mostly done**
*Phase 6.*

| Criterion | Status |
|---|---|
| A recorded chunker decision with a before/after number | ✅ ADR 0012 |
| A recorded decision on query rewriting | ✅ ADR 0013 / config — kept, `follow_up_lift` +0.177 |
| A recorded reranker decision, with the measured delta | ❌ `cross_encoder` still unmeasured |
| A recorded decision on `top_k` and `rrf_k` | ❌ **and now more urgent** — `markdown` chunks are a third the size, so five of them is a third the context it used to be |
| One hosted-provider run | ❌ needs a credential |

### Milestone B — Authentication
*Estimated 2–3 days.*

OIDC against OSC's IdP. Tokens validated server-side; the resolved principal set
attached to every request and carried into retrieval so ACL filtering has somewhere
to plug in.

**Success criteria**
- An unauthenticated request to `/api/chat` or `/api/search` returns 401.
- A valid token yields an answer, and the user and group ids appear in the
  structured log **and on the trace** for that request.
- Starting with `OSC_ENVIRONMENT=production` and no auth configured exits non-zero.
- Rate limiting per authenticated principal, with a test that a burst is rejected.

### Milestone B′ — Abstention and answer quality
*Estimated 1–2 days. No new architecture.*

Promoted above Milestone C because it is where the measured numbers are weakest and
because it needs no credential and no new component.

**Success criteria**
- `abstention_accuracy` ≥ 0.90, **on a golden set with at least 15 abstention cases**
  — six is too few for the metric to be trustworthy, and widening the sample is half
  the work. Adding cases must come first, so the baseline is re-measured honestly
  rather than improved by shrinking the denominator.
- A recorded decision on whether the abstention failure is a prompt problem or a
  threshold problem, with a before/after number. `min_score` is 0.0 today, so
  retrieval returns five chunks for a question about submarines.
- `fact_match` ≥ 0.85, or a written explanation of why the 8B model is the ceiling —
  supported by one hosted-provider run.

### Milestone C — Retrieval quality pass
*Estimated 3–5 days. Requires Milestone A.*

**Success criteria**
- Faithfulness ≥ 95% and recall@5 ≥ 95% on the schema suite (recall@5 is already
  **0.982**, so this criterion is met at the retrieval end), or a written explanation
  of why the target is wrong for this corpus.
- **A recorded decision on `top_k`**, now that the median chunk is a third of its
  former size and five chunks is a third of the former context. This is the most
  clearly-owed experiment in the repository.
- A recorded decision on the cross-encoder reranker, with the measured delta.
- ~~A recorded decision on query rewriting~~ — **done in Phase 6**: kept, on a
  measured `follow_up_lift` of +0.177 against a cold control.
- The `markdown` chunker re-measured against the FAQ suite, to establish whether its
  gain is corpus-specific (ADR 0012 assumes it is and says so).
- Every change carries a before/after number. Anything that did not move a metric
  has been reverted.

### Milestone D — Deployment and export
*Estimated 2–3 days.*

**Success criteria**
- A Dockerfile builds a service image; `docker compose up` runs service and
  database together.
- CI runs `make check` on every pull request and `make test-integration` on merge.
- An OTel exporter behind a configuration flag, with the local trace log retained
  as the default.

---

## 16. Alpha readiness

An honest assessment against the criteria this phase was held to. **Verdict: Alpha,
credibly.** Not Beta — three of the six areas below have a named gap that a user
would notice.

| Area | State | Evidence / gap |
|---|---|---|
| **Knowledge — authoritative corpus** | ✅ | `corpus.root` = `docs/company/schema`, named once, boundary asserted by test |
| **Knowledge — correct ingestion** | ✅ | 11 documents / 80 chunks; parse→chunk→embed→store verified end to end against live PostgreSQL |
| **Knowledge — reliable retrieval** | ✅ | `recall@5` 0.982, `ndcg@5` 0.918 |
| **Chatbot — single-turn** | ✅ | unchanged and asserted bit-identical after every Phase 6 change |
| **Chatbot — session memory** | ✅ | bounded, isolated, observable; 26 unit + 9 API + 6 E2E tests |
| **Chatbot — follow-ups** | ✅ | `follow_up_lift` **+0.177** against a cold control |
| **Chatbot — isolation & cleanup** | ✅ | `session_isolation` 1.000; close→404→clean new session verified over HTTP |
| **Quality — retrieval metrics** | ✅ | recall, precision, nDCG, MRR, hit-rate, all documented and baselined |
| **Quality — citation & groundedness** | ✅ | `groundedness` 1.000, `citation_coverage` 1.000 |
| **Quality — answer correctness** | ⚠️ | `fact_match` **0.782**. Retrieval succeeds and the fact fails to survive into the answer about one time in five |
| **Quality — abstention** | ❌ | `abstention_accuracy` **0.667**, on only six cases. The weakest measured behaviour, and the metric most in tension with the product's stated priority |
| **Quality — conversational evaluation** | ✅ | 18 sessions / 46 turns, every context-dependent turn control-run |
| **Engineering — one-command tests** | ✅ | `make verify`, 445 tests, one summary, stable across three runs |
| **Engineering — one-command evaluation** | ✅ | `make eval`, both suites, gated |
| **Engineering — E2E regression** | ✅ | full document path and full session lifecycle against live Ollama + PostgreSQL |
| **Engineering — regression gates** | ✅ | derived tolerances, trade-off guards, verified exit 1 on a real regression |
| **Operations — observability** | ✅ | one turn = one trace; `session_context` distinguishes a context failure from a quality one |
| **Operations — logs & diagnostics** | ✅ | rotating operational + audit streams, `./osc doctor` 9 ok / 0 fail |
| **Operations — deployment** | ❌ | no Dockerfile, no CI, no auth. `make verify` and `make eval-gate` both exit correctly; nothing runs them |
| **Documentation** | ✅ | 10 architecture pages, 14 ADRs, PROJECT_STATUS, current Graphify |

### What stops this being Beta

1. **No authentication.** Unchanged from Phase 5 and still the first hard blocker.
   Every endpoint is open, and the session id is the only thing separating two users'
   conversations.
2. **Abstention at 0.667.** A knowledge assistant that answers two of six questions it
   cannot answer is not one an employee should trust unsupervised.
3. **Memory does not survive a restart**, so the service cannot yet be run behind more
   than one replica without sticky sessions.

### What would be dishonest to claim

- That the citation guarantee is uniform across providers. It is not, and the gap has
  still never been measured (§10).
- That `fact_match` measures correctness. It is substring matching — a floor on
  correctness, not a measure of it.
- That the conversational numbers generalise beyond this corpus. 18 sessions over 11
  documents is a real measurement and a small one.
- That the LLM-judge faithfulness number means anything on the default profile, where
  judge and subject are the same model.

---

## Appendix — orientation for a new session

**Read in this order:** this file → `README.md` → `claude.md` →
`docs/engineering/architecture/overview.md` → `src/osc_assistant/protocols.py` →
`src/osc_assistant/container.py`.

**Before changing retrieval**, read `docs/engineering/architecture/evaluation.md` and
`evaluation-methodology.md`. The project's rule is that a retrieval change ships with
a measured improvement, and `make eval` is what makes that enforceable rather than
aspirational. **`--reindex` after a chunker change** — chunk ids derive from chunk
boundaries while document hashes do not, so an ordinary sync reports `skipped` and
silently measures the old index under the new label.

**The two canonical commands** are `make verify` ("does it work?" — every test tier
in one invocation) and `make eval` ("is it good?" — both suites, gated). Do not add a
third entry point for either question.

**First commands to run**

```bash
./osc doctor                 # is every component reachable and consistent?
./osc status                 # what is indexed?
./osc providers              # what can I switch to, and what am I running?
./osc config                 # what settings did the layers actually resolve to?
./osc search "<query>" --explain     # retrieval only, with the stage waterfall
./osc ask "<question>" --explain     # the whole pipeline, timed
./osc traces                 # what has run recently
./osc trace                  # expand the most recent
make verify                  # does it work?  every test, one summary
make eval-retrieval          # is retrieval any good? (fast, no model calls, ungated)
make help                    # every target
```

**When something is wrong**, in order: `./osc doctor` names the broken component;
`./osc traces --failed` finds the request; `./osc trace <id>` shows which stage
raised and what every earlier stage had done; `./osc search` separates "the model
misread the passage" from "the passage was never retrieved"; `./osc chunk <id>`
shows the exact text the model was given.

**The knowledge graph** in `graphify-out/` was updated incrementally on 2026-08-31
via the `/graphify` skill (AST + semantic extraction over the changed files).
Navigate by `wiki/index.md` (agent entry point), `GRAPH_REPORT.md`, or
`graph.html`; `graphify query "..."`, `graphify path "A" "B"` and
`graphify explain "X"` answer structural questions from the terminal.

**Rebuilding requires the extras**: `uv tool install "graphifyy[office,sql]"`.
Without `office` the four scenario documents are silently skipped; without `sql` the
migration contributes nothing.

Only committed artefacts are the ones a fresh clone needs to navigate without paying
for a rebuild — `graph.json`, `GRAPH_REPORT.md`, `wiki/`, `manifest.json`, the
labels and `converted/`. The AST cache, the dated backups, `graph.html` and the
per-run scratch files are gitignored; `.graphify_python` and `.graphify_root` are
too, because they hold absolute paths to whoever ran graphify last and were being
committed.

One caveat stands: the graph indexes the *whole repository*, including
`docs/company/` and `docs/engineering/`, so a graph query can return a schema
document or an ADR rather than code. That is the opposite of the assistant's own
corpus rule and is correct here — the graph is for navigating the repository, not
for answering employees.
