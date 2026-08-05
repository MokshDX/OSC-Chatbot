# PROJECT_STATUS.md

**Project:** OSC Internal Knowledge Assistant
**Status:** Phase 4 — a **measured**, observable, operable knowledge engine; not yet production-ready
**Last updated:** 2026-08-05
**Audience:** a senior engineer, or a future Claude session, joining with zero context

Read this file first, then `README.md` for how to run it, then `claude.md` for the
engineering standards this repository is held to. `docs/engineering/` is the
engineering knowledge base — architecture, technologies and decision records, written
to explain *why* rather than *what*. `graphify-out/` holds a generated, agent-crawlable
map of the codebase.

---

## 1. Executive summary

A provider-agnostic retrieval-augmented question answering service over OSC's
internal documents. Employees ask a question; the system retrieves supporting
passages from an indexed corpus, generates an answer grounded in them, attaches
citations back to the sources, and declines to answer rather than guessing when the
corpus does not support one.

Two constraints distinguish it.

**Vendor agnosticism.** The chat model, embedding model, reranker, vector store and
chunking strategy are each selected by configuration and swappable independently.
Business logic depends on five `Protocol` definitions and never imports a provider
module. 37 providers are registered today; adding one is a new file plus one import
line — and via the LangChain bridge, most of the remaining ecosystem is reachable
with no new file at all.

**Observability.** Every significant stage of ingestion and question answering is a
timed span, one request produces one trace, and that trace survives the process that
made it. A developer can ask what happened during any recent request — where the
time went, how the data changed between stages, which stage failed — without adding
a log line, attaching a debugger, or reproducing the request.

**Measurement.** As of this iteration every quality claim below is a number produced
by `make eval` against a curated golden set of 86 real questions, not an opinion.
Baselines are committed to `evaluation/baselines/` and a regression fails CI.

**Where it stands.** The full path runs against real infrastructure: drop PDFs, Word
documents, spreadsheets, HTML, Markdown and text into `./docs/company`, ingest them,
and they are parsed, chunked, embedded and stored in PostgreSQL with pgvector.
Questions retrieve by hybrid search and are answered by Qwen3 through Ollama, with
citations back to the source file. **277 tests**: all run with no network, database or
credential; 18 more against real PostgreSQL; 9 more end to end against live Ollama
*and* PostgreSQL. `ruff` and `mypy --strict` clean across 63 source files.

**Measured baseline** — default local profile, 86 golden cases, corpus of 21 documents
/ 193 chunks (`evaluation/baselines/full-default.json`):

| | | | |
|---|---|---|---|
| `recall@5` | **0.932** | `citation_coverage` | **1.00** |
| `hit_rate@5` | **0.938** | `groundedness` | **1.00** |
| `mrr` | **0.860** | `citation_precision` | **0.732** |
| `precision@5` | 0.190 | `fact_match` | **0.90** |
| `latency_p50` | 12.6 s | `abstention_accuracy` | 0.80 |
| `latency_p95` | 92.9 s | tokens in/out | 126k / 4.6k |

**What changed in the last three iterations.** Iteration 2 added the observability
layer, the operational CLI, `StoreInspector`, and a deliberately scoped LangChain
integration (§4). Iteration 3 completed the observability story for one-shot commands,
made the CLI coherent, and closed four architectural gaps. Iteration 4 — this one —
**built the evaluation framework**, restructured the knowledge corpus around the real
company documents, and wrote the engineering knowledge base (§5).

**Where it does not stand.** There is still no authentication, no per-document access
control, no rate limiting, and no conversation persistence. Answer quality is bounded
by an 8B local model, and `latency_p95` of 92.9 s under concurrency is the number that
would most surprise a user (§10).

**The honest one-line summary:** a working, verified, thoroughly observable and now
**measurable** knowledge engine on a local stack, one authentication story away from
being defensible in production.

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

**Status against those targets, as of Phase 4.** `recall@5` is 0.932, so the recall
target is met at a *stricter* k than it was set at. The latency targets are not met on
the local stack — `latency_p50` is 12.6s against a 10s p95 target — and that is a
statement about an 8B model on a laptop rather than about the architecture. Whether
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

**Default chunker is still `recursive`.** Switching it changes every chunk boundary
and therefore every chunk id in a live index, and the project's own rule is that a
retrieval change ships with a measured improvement. There is no golden set yet. The
LangChain strategies are registered, tested and one profile line away.

---

## 5. What changed in this iteration (Phase 4)

The brief was maturity and measurement. Three things were built.

### 5.1 The evaluation framework — the headline

`src/osc_assistant/evaluation/` (four modules), `evaluation/golden-set.yaml`
(86 curated cases), `./osc eval`, and three Makefile targets.

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

---

## 5b. What changed in the previous iteration (Phase 3)

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
├── logging.py              JSON formatter on stdlib logging
├── fusion.py               Reciprocal Rank Fusion (reference implementation)
├── grounding.py            source rendering, citation parsing, reasoning-model hygiene
├── container.py            composition root + lifecycle
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
├── evaluation/             dataset.py · metrics.py · judge.py · runner.py
├── integrations/           langchain.py — OSC exposed outward
└── api/                    app.py · schemas.py · sse.py · banner.py · static/index.html

tests/                      277 tests across 19 files
migrations/001_init.sql     schema, with a dimension-conditional HNSW index
docs/company/               THE CORPUS — company knowledge, 21 documents, 6 formats
docs/engineering/           the engineering knowledge base — NOT ingested
evaluation/golden-set.yaml  86 curated cases
evaluation/baselines/       committed reference runs (results/ is gitignored)
config/                     default.yaml + 4 experiment profiles
osc                         the CLI wrapper — no .venv paths anywhere
graphify-out/               generated knowledge graph
```

**A third rule, new in this phase:** `docs/company/` is the corpus and
`docs/engineering/` is not. The ingest root is named in exactly two places — `DOCS` in
the `Makefile` and the `--corpus` default in `cli/diagnose.py` — and they must agree.

**One rule to preserve:** business logic imports `protocols` and `types` only. If a
pipeline, route or CLI command ever imports a provider module, the vendor-agnosticism
this project is built around has been broken.

**A second, newer rule:** `integrations/` may import from the core, and the core may
never import from `integrations/`. That one-way dependency is what stops an outbound
adapter from becoming a dependency of the platform.

### What the knowledge graph says about this structure

Rebuilt in full on 2026-08-05 (not an incremental update): **1981 nodes, 4624
edges, 114 communities**, with 89% of edges EXTRACTED and 11% INFERRED at an average
confidence of 0.72. The evaluation subsystem is visible as its own cluster —
`runner.py`, `evaluate.py`, `test_evaluation.py` and `Evaluation` all appear as
community hubs, which is what a genuinely new subsystem should look like rather than
code smeared across existing ones.

**Node count went down and edge count went up**, which is the interesting part. The
previous build reported 2086/4572; this one reports 1981/4624 — density 2.19 → 2.33
edges per node. The earlier build derived its document nodes structurally (heading
stubs); this one extracted them semantically, so 429 stubs were replaced by 324
concepts that carry rationale attributes, external citations and hyperedges. A
smaller, denser, more meaningful graph. `to_json`'s shrink guard correctly refused
the write until the reduction was verified.

`MemoryVectorStore` (72 edges), `Document` (70), `StubEmbeddingModel` (69),
`ComponentConfig` (64) and `Container` (60) are the architectural hubs —
configuration, the corpus record and the composition root are what the system routes
through, which matches the intended design. An *earlier* build reported
`StubEmbeddingModel`, a **test double**, as the single most connected node in the
codebase, ahead of every real component: the graph's way of saying that the test
suite, not production wiring, was what exercised every seam. Real components lead
now. The doubles are still central and should be — they are how the protocol layer is
proven.

**Two gaps closed in this rebuild**, both previously invisible rather than known:

- `graphifyy[office]` — the four `.docx`/`.xlsx` scenario documents were being
  reported as `skipped_sensitive` and silently dropped. They are 82 of the production
  index's 193 chunks, so the graph had been blind to roughly 42% of the real corpus.
- `graphifyy[sql]` — `migrations/001_init.sql` now contributes nodes, so the storage
  schema no longer has to be read from raw SQL.

**On graph health.** The diagnostic reports 273 dangling-endpoint edges, and 245 of
them (90%) are `imports`/`imports_from` edges pointing at third-party packages and
stdlib modules — `pkg_pydantic`, `pathlib`, `typing`, `json`. Those are the graph
correctly declining to invent nodes for things outside the scanned corpus, not
information loss. Roughly 17 edges (0.3%) are genuine cross-chunk semantic references
that failed to resolve, which is the real and small cost of parallel extraction. The
202/232 "collapsed" edges are an undirected simple `Graph` merging multi-edges such
as `evaluate_eval → typer.Option ×8` at one source line — expected, not corruption.

**One caveat stands.** Community *labels* are hand-written for the 70 largest
communities and hub-derived for the remaining 44; `graphify label --backend=ollama`
requires the `openai` package, which is not installed. Hub names are arguably the
more honest label anyway.

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
| 25 | **Measured quality baseline** | recall@5 0.932 · mrr 0.860 · groundedness 1.00 · fact_match 0.90 |
| 26 | **Knowledge corpus restructure** | real company documents; corpus/engineering split; 17-file FAQ; `.xlsx` support |
| 27 | **Engineering knowledge base** | 8 architecture pages, 6 technology pages, 8 ADRs |

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
4. **Conversation persistence.** The API is stateless; history is client-supplied,
   and the bundled UI does not send it — so follow-up turns are independent questions.
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

### Closed in Phase 4 (this iteration)

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
- The UI does not send conversation history, so follow-up turns are independent
  questions (query rewriting is also off by default — §11).

---

## 10. Known limitations

**Citation strength differs by provider, silently.** Anthropic returns citations
verified against the source text. Every other provider — including the local default
and the LangChain bridge — asserts them via `[n]` markers that a model can emit for
an unsupported claim. Both produce the same `Citation` object, so nothing downstream
can tell the difference. A deliberate trade-off for vendor agnosticism, and the gap
is supposed to be *measured* by the evaluation harness that does not yet exist.

**Prompt injection is mitigated, not eliminated.** Source bodies can no longer close
the data delimiter (it carries a per-request nonce), but a document can still contain
persuasive text. Nothing prevents a corpus document from arguing with the system
prompt — only from impersonating it.

**Retrieval quality is now measured, and it is good but not uniform.** `recall@5`
0.932 over 81 scored cases. The six misses cluster where the corpus genuinely
overlaps: a question about collection-level bulk discounts is answered by both
`tiered-pricing-guide.md` and `combined-collection-quantity-discount-slabs.md`, and
the golden set names only one. Part measurement finding, part curation finding.

`precision@5` of 0.190 looks alarming and is not: most cases have exactly one relevant
document out of five slots, so the ceiling is 0.2. It is useful as a *relative*
measure across runs and misleading as an absolute one.

**Abstention has two mechanisms and only one is measured.** `abstention_accuracy` is
0.80 — four of five. The fifth (`abstain-woocommerce`) did not trip the architectural
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
4096-token window, capping the corpus sent to the model at five chunks of ~900
characters. A document needing six passages will be answered incompletely rather
than incorrectly.

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
`langchain_recursive` does not have this defect and is one config line away.

---

## 11. Testing status

```
279 tests collected
  279 pass with no network, no database, no credentials     make test    ✅ verified
  +18 pgvector integration tests against a real database    make test-integration  ✅
   +9 end-to-end tests against live Ollama and PostgreSQL   make test-e2e  ✅ 21.8s

  86 golden cases scored                                    make eval    ✅
  gate passes                                               make eval-gate  ✅

ruff check .   clean
mypy --strict  clean, 63 source files
```

**`make test` asks whether the system is correct. `make eval` asks whether it is
good.** They are different questions and a system can pass every test while answering
every question badly, which is why evaluation is a separate command and not a test
file.

| File | Covers |
|---|---|
| `test_evaluation.py` | **New.** Metrics against worked examples; golden-set validation and its five rejection cases; failed cases excluded from quality means; retrieval-only omits generation metrics; concurrency does not change results; judge verdict parsing and failure handling |
| `test_cli.py` | Every operational command; doctor's pass/warn/fail behaviour; trace commands across process boundaries; operator-error reporting; help grouping |
| `test_langchain_integration.py` | Both chunkers (id stability, content preservation, size budget, heading metadata); the chat and embedding bridges; the outbound retriever |
| `test_pgvector_integration.py` | Migrations, tsvector, SQL fusion, cascade delete, JSONB, workspace isolation, transaction rollback, inspection SQL |
| `test_fusion_and_grounding.py` | RRF ordering/dedup; citation marker parsing; **prompt-injection containment** |
| `test_api.py` | Health, status, search, chat (both modes), SSE ordering, trace endpoints and their environment gate |
| `test_trace_store.py` | Cross-process readability, rotation, malformed lines, unwritable directories, round-trip fidelity |
| `test_observability.py` | Span tree shape, nested-trace merging, error capture, span cap, text redaction |
| `test_retrieval.py` | Store contract, all three strategies, top_k, reranking, rewriting, **min_score applied pre-rerank** |
| `test_parsers.py` | Every format, content preservation, corrupt and scanned files, **failure isolation** |
| `test_ingestion.py` | Idempotency, change detection, pruning, **unreadable-file prune exemption**, `--reindex`, trace shape |
| `test_chunking.py` | Size budget, id stability, **content preservation** |
| `test_server_lifecycle.py` | Startup notes, **in-flight stream failure emits a terminal event**, shutdown releases components without constructing unused ones |
| `test_inspection.py` | `StoreInspector` contract on the memory store; empty-store edge cases |
| `test_answerer.py` | Abstention in both modes, citation policy, streaming reassembly |
| `test_settings.py` | Four-layer precedence, nested env merge, malformed profiles, trace exposure gate |
| `test_e2e.py` | Five formats indexed; idempotency; hybrid ranking; a cited answer; abstention; a binary format answerable; both modes agreeing; the run fully traced |
| `test_reasoning_models.py` | `<think>` stripping, exhausted-budget error, reasoning markers never becoming citations |
| `test_registry.py` | Registration, override, unknown-provider error |

**What the suite is good at.** It runs the *real* pipelines against in-process
implementations of the protocols. The API and CLI tests register those doubles
through the ordinary registry — the same path a new provider takes — so "the whole
stack can be retargeted by configuration alone" is asserted, not assumed. Several
tests are regressions for defects actually found and reproduced.

**Remaining gaps:**

1. **No hosted provider has ever been called.** Every hosted adapter is exercised
   only via stubs — including the Anthropic native-citation path, the only verified
   citation implementation in the codebase. Running
   `./osc eval --profile config/experiments/hosted-anthropic.yaml` is one command and
   needs one credential; it would put a number on the citation-strength gap.
2. **No load or concurrency test.** Behaviour under parallel requests, and the
   connection-pool bounds, are untested. `./osc eval --concurrency N` is now the
   closest thing to one and was not built for that purpose — though it is what
   produced the p95 figure in §9.
3. **The Gemini adapters still hold an unreleasable client.** `genai.Client` exposes
   no async close in the installed surface and the package is an optional extra, so
   guessing at a method name on an untestable path would be worse than recording it.
   The other six adapters are covered.
4. **The golden set contains no question written by a real user.** It was curated from
   the corpus, so it inherits the corpus's blind spots. Feedback capture is the natural
   next source.

---

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
`nomic-embed-text` (768-d), pgvector, `noop` reranker, recursive chunking (900/120),
hybrid retrieval (30 candidates → top 5), 1500 max completion tokens, query
rewriting off, tracing on and persisted to `.osc/`.

**Reference environment as verified:** PostgreSQL 18.4 with pgvector 0.8.2; Ollama
0.32.5 serving `qwen3:8b` at a 4096-token context and `nomic-embed-text`.

**Four constraints that will bite:**
- Changing the embedding model changes the vector width, fixed in the DDL at
  migration time. It requires a new database and a full re-index.
- pgvector cannot build an HNSW index above 2000 dimensions; above it search
  degrades to an exact scan.
- The prompt budget is sized for a 4096-token context.
- Changing the chunker invalidates every stored chunk while every content hash
  still matches. Use `./osc ingest ./docs/company --reindex`.

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
bigger** — but **the binding constraint has moved.** Measurement was item 1 for three
phases; it now exists, and everything it was gating is unblocked at once.

1. **Spend the harness.** The highest-value work in the project, and now the cheapest:
   a chunker comparison (`recursive` vs `langchain_recursive` vs `markdown`), a
   reranker decision, a `top_k`/`rrf_k` sweep, and one hosted-provider run. Each is two
   commands and a recorded number. Several of these decisions have been *waiting on a
   measurement for two phases*; leaving them unmeasured now would be the worst outcome
   of this iteration.
2. **Add authentication (OIDC).** The first hard blocker to exposing the service.
   Group membership from the IdP is also the input to item 3.
3. **Production start-up guard.** Refuse to start when `environment != development`
   and no auth is configured. Ten lines, and the constraint becomes enforced rather
   than announced. Cheap enough to land alongside item 2.
4. **Add per-document ACLs.** Only after auth exists.
5. **Investigate the spreadsheet chunks.** 42% of the index, implicated in four of six
   recall failures. Either tabular data needs a different chunking strategy, or the
   golden set under-specifies. Answerable now, unanswerable a week ago.
6. **Conversation persistence and feedback capture.** Feedback is the raw material for
   growing the golden set past curated questions, so it compounds. Re-enabling query
   rewriting belongs here, together with sending history from the UI.
7. **Second connector.** The loader shape is established and has a parser layer
   behind it; this proves both.
8. **Deployment artefacts and trace export.** Dockerfile, CI (running `make check` and
   `make eval-gate`), and an OTel exporter once traces need to leave the host.

**Deliberately late:** a richer web client, multi-tenancy beyond the partition key,
additional providers (the bridge covers the long tail). **Deliberately absent:**
fine-tuning, agentic tool use, a knowledge-graph layer.

---

## 15. Next milestones with success criteria

### Milestone A — Evaluation harness — **DONE, except two criteria**
*Delivered in Phase 4.*

| Criterion | Status |
|---|---|
| `make eval` prints retrieval and generation metrics and writes a comparable JSON | ✅ 11 metrics |
| A pull request that drops recall below a threshold fails CI | ✅ `make eval-gate` — but no CI runs it yet |
| Baseline numbers for the default profile are committed | ✅ `evaluation/baselines/` |
| The local model's numeric-fidelity gap is quantified | ✅ `fact_match` 0.90 |
| At least one provider comparison run end to end | ❌ needs a credential |
| **A chunker comparison is recorded** with a decision and a number | ❌ **not run** |

The two open criteria are the first item in §14. The harness was built and *not yet
spent*, which is the honest state and the obvious next move.

### Milestone A′ — Spend the harness
*Estimated 1 day. No new code.*

**Success criteria**
- A recorded chunker decision: `recursive` vs `langchain_recursive` vs `markdown`,
  with a before/after number. Whichever wins becomes the default and supersedes
  ADR 0006.
- A recorded reranker decision, with the measured delta.
- A recorded decision on `top_k` and `rrf_k` — the latter is currently the SIGIR
  paper's value, adopted on authority and never tuned for this corpus.
- One hosted-provider run (`config/experiments/hosted-anthropic.yaml`), putting a
  number on the verified-vs-parsed citation gap.
- The spreadsheet-chunk question (§9) answered either way.

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

### Milestone C — Retrieval quality pass
*Estimated 3–5 days. Requires Milestone A.*

**Success criteria**
- Faithfulness ≥ 95% and recall@5 ≥ 95% on the golden set (recall@5 is already
  0.932), or a written
  explanation of why the target is wrong for this corpus.
- A recorded decision on the cross-encoder reranker, with the measured delta.
- A recorded decision on query rewriting: kept with a measured improvement, or
  defaulted off and the `fast_llm` dependency removed.
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

## Appendix — orientation for a new session

**Read in this order:** this file → `README.md` → `claude.md` →
`docs/engineering/architecture/overview.md` → `src/osc_assistant/protocols.py` →
`src/osc_assistant/container.py`.

**Before changing retrieval**, read `docs/engineering/architecture/evaluation.md`. The
project's rule is that a retrieval change ships with a measured improvement, and
`make eval` is what makes that enforceable rather than aspirational.

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
make eval-retrieval          # is retrieval any good? (fast, no model calls)
make help                    # every target
```

**When something is wrong**, in order: `./osc doctor` names the broken component;
`./osc traces --failed` finds the request; `./osc trace <id>` shows which stage
raised and what every earlier stage had done; `./osc search` separates "the model
misread the passage" from "the passage was never retrieved"; `./osc chunk <id>`
shows the exact text the model was given.

**The knowledge graph** in `graphify-out/` was rebuilt in full on 2026-08-05 via
the `/graphify` skill (AST + semantic extraction over docs). Navigate by
`wiki/index.md` (agent entry point, 124 articles, current), `GRAPH_REPORT.md`, or
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

One caveat stands: `docs/company/` is the live corpus while `docs/engineering/` is
the knowledge base, so a graph query can return an OSCP FAQ answer or an ADR rather
than code.
