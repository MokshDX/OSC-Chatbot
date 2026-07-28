# PROJECT_STATUS.md

**Project:** OSC Internal Knowledge Assistant
**Status:** Phase 1 vertical slice complete; not production-ready
**Last updated:** 2026-07-29
**Audience:** a senior engineer, or a future Claude session, joining with zero context

Read this file first, then `README.md` for how to run it, then `claude.md` for the
engineering standards this repository is held to. `graphify-out/wiki/index.md` is a
generated, agent-crawlable map of the codebase (812 nodes, 36 communities).

---

## 1. Executive summary

A provider-agnostic retrieval-augmented question answering service over OSC's
internal documents. Employees ask a question; the system retrieves supporting
passages from an indexed corpus, generates an answer grounded in them, attaches
citations back to the sources, and declines to answer rather than guessing when
the corpus does not support one.

The distinguishing constraint is **vendor agnosticism**: the chat model, embedding
model, reranker, vector store and chunking strategy are each selected by
configuration and swappable independently. Business logic depends on five
`Protocol` definitions and never imports a provider module. 13 chat providers,
11 embedding providers, 3 rerankers, 3 vector stores and 2 chunkers are registered
today; adding another is a new file plus one import line.

**Where it stands.** The end-to-end path works: ingest a directory, retrieve with
hybrid search, generate a cited answer, stream it over SSE. 93 tests, of which 82
run with no network, database or API credential. `ruff` and `mypy --strict` are
clean across 43 source files.

**Where it does not.** There is no authentication, no per-document access control,
no conversation persistence, and no evaluation harness. The service must sit behind
an identity proxy. Three P0 data-integrity defects were found and fixed during the
last session; three P1 issues remain open (§8). The PostgreSQL code path has tests
but they have **never been executed** — no Postgres was available on the build
machine. That is the single largest unknown in the project.

**The honest one-line summary:** a well-structured Phase 1 that is one authentication
story and one evaluation harness away from being defensible in production, with an
unverified database layer that should be run before anything else.

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
maintainability → readability → scalability → performance → development speed, in
that order.

**Architectural requirements** added after the initial design was approved:

1. Vendor-agnostic wherever practical; the chat model must support multiple
   providers through a common interface (Anthropic, OpenAI, Gemini, Hugging Face,
   Ollama, Groq, local models, future providers). Switching providers must require
   configuration changes only.
2. Embeddings provider-agnostic and independently swappable from the chat model.
3. The vector store must be replaceable. PostgreSQL + pgvector is the preferred
   default; migrating to Pinecone/Qdrant/Weaviate/Milvus must not require rewriting
   business logic.
4. Design for experimentation — LLMs, embedding models, rerankers, chunking
   strategies and vector stores will be swapped frequently, and that must be cheap.
5. Avoid unnecessary abstractions. Every abstraction must solve a real engineering
   problem.
6. New providers are plug-in additions: adding one creates a new implementation
   rather than modifying existing business logic.
7. Evaluate frameworks pragmatically — adopt LangChain/LlamaIndex if they genuinely
   improve the architecture, reject them if not, on evidence rather than ideology.

**Non-functional targets set during design** (none yet measured — see §10):
time-to-first-token < 2s p95, full answer < 10s p95, answer faithfulness ≥ 95% of
claims supported by their cited source, retrieval recall@10 ≥ 90%, full index
rebuildable unattended in < 4h.

---

## 3. Current architecture

```
connectors ──▶ chunk ──▶ embed ──▶ vector store
                                        │
question ──▶ rewrite ──▶ search ──▶ rerank ──▶ generate ──▶ answer + citations
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

`types.py` holds the only vocabulary shared across modules (`Document`, `Chunk`,
`EmbeddedChunk`, `ScoredChunk`, `ChatRequest`, `Citation`, `Answer`, …), all frozen
dataclasses. **Business logic imports `protocols` and `types` only. It never
imports a provider.** That single rule is what makes the vendor-agnosticism
requirement real rather than aspirational.

### Wiring

`registries.py` holds five `Registry` instances mapping a provider name to a
factory. A provider module registers itself on import; `providers/__init__.py`
imports the sub-packages; `container.py` (the composition root) imports that
package once. Nothing in the call path imports every possible implementation.

`Container` builds components lazily via `cached_property`, so `osc-assistant
ingest` never constructs a chat model and therefore never needs an LLM credential.
It injects into the vector store the values the store cannot know itself — vector
width and the active embedding model id, both derived from the embedding model.

### Request path

1. **Authenticate** — *not implemented.* See §7.
2. **Rewrite** (`retrieval/rewrite.py`) — resolves conversational references into a
   standalone query using the configured *fast* model. Best-effort: any failure
   falls back to the original question.
3. **Retrieve** (`retrieval/pipeline.py`) — vector, keyword, or hybrid. Hybrid runs
   both and fuses with Reciprocal Rank Fusion (`fusion.py`); the pgvector store
   implements the same formula in SQL so both stores rank identically.
4. **Rerank** — `noop` by default; `cross_encoder` available.
5. **Generate** (`generation/answerer.py`) — builds a `ChatRequest` with the frozen
   system prompt and the retrieved chunks as `sources`.
6. **Cite** — Anthropic passes sources as structured documents and receives
   verified per-span citations. Every other provider renders sources into the
   prompt and parses `[n]` markers back out (`grounding.py`). Both paths produce
   the same `Citation` shape.
7. **Abstain** — no retrieval hits means the model is never called. No citations
   means the answer is treated as ungrounded.

### Storage

One PostgreSQL database holds chunk text, embeddings (`pgvector`), the lexical
index (a generated `tsvector` column) and document metadata. `migrations/001_init.sql`
is applied by a hand-rolled forward-only runner in `pgvector.py`; the embedding
dimension is substituted into the DDL at migration time. Every table carries a
`workspace_id` partition key — one workspace exists today.

---

## 4. Repository structure

```
src/osc_assistant/          4,475 lines
├── protocols.py            the five seams
├── types.py                domain vocabulary (224 lines — the largest shared surface)
├── registries.py           five Registry instances
├── registry.py             generic Registry[T] + ComponentConfig
├── settings.py             layered config: env > .env > YAML profile
├── errors.py               AssistantError hierarchy
├── logging.py              JSON formatter on stdlib logging
├── fusion.py               Reciprocal Rank Fusion (reference implementation)
├── grounding.py            nonce-delimited source rendering + marker citation parsing
├── container.py            composition root
├── cli.py                  serve / ingest / ask / search / providers
├── providers/
│   ├── llm/                anthropic (254) · openai_compatible (255) · gemini (185)
│   ├── embeddings/         openai_compatible · voyage · gemini · local
│   ├── reranking/          noop · cross_encoder
│   └── vectorstores/       pgvector (379 — largest file) · memory
├── chunking/recursive.py   RecursiveChunker + FixedSizeChunker
├── ingestion/              loaders.py · pipeline.py
├── retrieval/              pipeline.py · rewrite.py
├── generation/             answerer.py · prompts.py
└── api/                    app.py · schemas.py · sse.py

tests/                      1,612 lines, 93 tests
migrations/001_init.sql     60 lines
config/                     default.yaml + experiments/{local-only,groq-voyage}.yaml
graphify-out/               generated knowledge graph — graph.html, wiki/, GRAPH_REPORT.md
```

**What the knowledge graph says about this structure.** Betweenness centrality
identifies `ComponentConfig` (bridging 15 communities) and `Document` (bridging 15)
as the true architectural hubs — configuration and the corpus record are what the
whole system routes through. That matches the intended design.

One finding is worth acting on: **`StubEmbeddingModel`, a test double, is the most
connected node in the entire codebase (57 edges) — ahead of `VectorStore`,
`Document` and every real provider.** The graph is reporting that the test suite,
not production wiring, is what actually exercises every seam. That is expected for
a system whose providers are all optional extras, but it also means the seams are
proven against stubs far more thoroughly than against real providers (§10).

---

## 5. Completed milestones

| # | Milestone | Evidence |
|---|---|---|
| 1 | **Five-protocol seam layer** | `protocols.py`; no provider import in any pipeline (verifiable by grep) |
| 2 | **Registry + composition root** | 32 registered providers across 5 registries; `osc-assistant providers` lists them from the registries themselves |
| 3 | **13 chat providers** | `anthropic` (native citations), `gemini` (native SDK), and one OpenAI-compatible adapter serving 11 names: openai, groq, ollama, vllm, lmstudio, huggingface, openrouter, together, gemini_openai, local |
| 4 | **11 embedding providers** | openai-compatible family, `voyage` (REST, asymmetric input types), `gemini`, `local` (sentence-transformers) |
| 5 | **2 vector stores** | `pgvector` (production) and `memory` (tests + experiments); identical RRF ranking |
| 6 | **Layered configuration** | env > `.env` > YAML profile; two working experiment profiles that share no vendor with the default |
| 7 | **Idempotent ingestion** | content-hash skip, incremental re-index, pruning, per-document failure isolation; re-running an unchanged corpus makes zero embedding calls (asserted) |
| 8 | **Hybrid retrieval** | BM25-equivalent `tsvector` + pgvector cosine, fused by RRF in SQL; same formula in `fusion.py` for the memory store |
| 9 | **Grounded generation with citations** | Anthropic native path + marker-parsing fallback, converging on one `Citation` shape |
| 10 | **Abstention policy** | no hits → no model call; no citations → ungrounded. Identical in streaming and buffered modes; the `complete` event is authoritative |
| 11 | **HTTP API + SSE streaming** | `/api/health` (reports active components), `/api/search`, `/api/chat` |
| 12 | **CLI** | `serve`, `ingest`, `ask`, `search`, `providers` |
| 13 | **Structured logging** | one trace per query with retrieved chunk ids, latency, token counts |
| 14 | **Test suite** | 93 tests; 82 run with no network/DB/credentials; ruff + mypy --strict clean |
| 15 | **Three P0 defects found and fixed** | prompt injection, ingestion data loss, chunker content corruption — see §12 |

---

## 6. Partially completed milestones

**Prompt caching — implemented, currently inert.** The `cache_system_prompt` option
marks the Anthropic system block as cacheable, and prompts are frozen module
constants specifically so the prefix stays byte-identical. But `ANSWER_SYSTEM_PROMPT`
is roughly 250 tokens, below the minimum cacheable prefix on current models, so
`cache_read_input_tokens` will be zero on every request. The discipline is correct;
the saving does not currently occur.

**Reranking — built, not enabled, and unsafe to enable as configured.** The
`cross_encoder` reranker works, but `retrieval.min_score` is applied *after*
reranking and defaults to `0.0`, while cross-encoder logits are routinely negative
for relevant passages. Switching the reranker on today would silently destroy
recall. See §8.

**pgvector store — complete, entirely unverified.** All eleven integration tests
are written and skip unless `OSC_TEST_DSN` is set. No Postgres was available during
development, so the migration runner, the generated `tsvector` column, the SQL
rank-fusion query and the `replace_document` transaction have **never run**.

**Workspace partitioning — schema-complete, single-tenant in practice.** Every table
carries `workspace_id` and every query is scoped by it, but only one workspace ever
exists and nothing resolves a workspace from a request.

**Query rewriting — implemented, enabled by default, unjustified.** It works and
degrades safely, but it was defaulted on before anyone confirmed follow-up turns are
actually a problem. It costs a second model, a second credential and an extra call
on the critical path.

**Documentation — thorough in code, thin operationally.** Module docstrings explain
intent and trade-offs throughout. There is no runbook, no deployment guide, and no
description of what to do when ingestion fails.

---

## 7. Not yet implemented features

Ordered by how much they block a production release.

1. **Authentication (OIDC).** No identity anywhere. `/api/chat` and `/api/search`
   accept arbitrary unauthenticated input. Intended design: OIDC against OSC's
   existing IdP, with group membership feeding access control.
2. **Per-document access control.** The design calls for ACLs resolved at index time
   and enforced as a SQL predicate at query time, so an unauthorised chunk is never
   retrieved and never reaches the model. No ACL column, no principal resolution,
   no filtering exists. Phase 1 was scoped to company-wide-readable content
   specifically to avoid needing this yet.
3. **Rate limiting and concurrency bounds.** A request can hold a connection for the
   full 120s provider timeout. Nothing caps requests per user.
4. **Evaluation harness.** The design treats this as a first-class subsystem: a
   golden set of 50–100 real questions, retrieval metrics (recall@k, MRR) and
   generation metrics (citation coverage, faithfulness) gating pull requests. None
   of it exists. Every quality claim in this document is currently unmeasurable.
5. **Conversation persistence.** The API is stateless; history is client-supplied.
   No storage, no retrieval, no deletion.
6. **Feedback capture.** No thumbs, no comments, no storage — so no raw material for
   future evaluation sets.
7. **Connectors beyond the filesystem.** Confluence, Google Drive, SharePoint. The
   loader shape (`load() -> AsyncIterator[Document]`) is established and used.
8. **Admin visibility.** No view of what is indexed, when it last synced, what
   failed. `IngestionReport` carries the data; nothing surfaces it.
9. **Web client.** No frontend at all; the API is the only interface besides the CLI.
10. **Deployment artefacts.** No Dockerfile for the service, no IaC, no CI pipeline.
    `docker-compose.yml` covers only the development database.

---

## 8. Technical debt

Ordered by impact. P0 items from the last audit are fixed; these are what remains.

### P1 — fix before real traffic

**`min_score` is compared against an undefined scale.**
`retrieval/pipeline.py` filters on score *after* reranking. RRF yields ~0.016,
pgvector cosine yields [-1, 1], a cross-encoder yields an unbounded and frequently
negative logit. `min_score: 0.0` is harmless with the `noop` reranker and destroys
recall the moment someone follows the README and enables `cross_encoder`. The
failure presents as "the reranker is bad", so investigation goes to the model
rather than the threshold. *Smallest fix:* apply the threshold before reranking and
rename it `min_retrieval_score` — or delete it, since it earns nothing today.

**Endpoints are unauthenticated, unbounded and unthrottled.**
Documented as deferred in the README, which is fine as a plan and not fine as a
release state — the constraint lives in prose, not in the code path. *Smallest fix:*
refuse to start when `environment != "development"` and no auth is configured. Ten
lines, and the constraint becomes enforced.

**`cache_system_prompt` is inert.** See §6. *Smallest fix:* log once at startup when
the system prompt is below the cacheable threshold, so nobody builds cost
projections on a saving that is not happening.

### P2 — maintainability

**`provider: local` means two different things.** In `llm_registry` it is an
OpenAI-compatible server on `:8000`; in `embedding_registry` it is
sentence-transformers. Same token, two unrelated behaviours, in the same profile
file. *Fix:* rename the LLM one to `openai_local`.

**Provider resources are never released.** `Container.shutdown()` closes only the
vector store. `VoyageEmbeddingModel` opens an `httpx.AsyncClient` and defines an
`aclose()` that nothing calls; the OpenAI and Gemini clients are never closed.
Harmless at process exit, a leak in tests and any future in-process reload.

**`settings.py` has zero tests.** It carries the only hand-written logic an operator
will touch: a custom YAML settings source and four-layer precedence. Nothing
verifies that env overrides YAML, that nested `OSC_LLM__PROVIDER` merges rather than
replacing the whole block, or that a missing profile is tolerated. A precedence
regression is invisible in tests and surfaces as "production is running the wrong
model".

**Speculative code with no consumer.**
- `providers/{llm,embeddings}/gemini.py` — ~330 lines and a `google-genai`
  dependency reaching a service the `gemini_openai` preset already reaches through
  an adapter that is already shipped and already tested.
- `FixedSizeChunker` — an evaluation baseline for an evaluation harness that does
  not exist.
- `rewrite_queries: true` — see §6.

### Minor

- `api/app.py` uses `response_model=None` on `/chat`, dropping the JSON branch from
  the OpenAPI schema. Split into `/chat` and `/chat/stream`.
- The SSE generator catches `AssistantError` only; a plain `Exception` kills the
  stream with no terminal event.
- `RetrievalResult` is the only unfrozen dataclass in the domain.
- No `py.typed` marker — the package ships annotations consumers cannot see.
- `pgvector/pgvector:pg16` is a moving tag; pin the digest.
- `container.py` imports `RecursiveChunker` purely for a registration side effect.

---

## 9. Known limitations

**Citation strength differs by provider, silently.** Anthropic returns citations
verified against the source text. Every other provider asserts them via `[n]`
markers that a model can emit for a claim the source does not support. Both produce
the same `Citation` object, so nothing downstream — including the UI — can tell the
difference. This is a deliberate trade-off for vendor agnosticism, and the gap is
supposed to be *measured* by the evaluation harness that does not yet exist.

**Prompt injection is mitigated, not eliminated.** Source bodies can no longer close
the data delimiter (it carries a per-request nonce), but a document can still
contain persuasive text. Nothing prevents a corpus document from arguing with the
system prompt — only from impersonating it.

**Retrieval quality is unmeasured.** No recall figure, no faithfulness figure. Every
number in §2's non-functional targets is a target, not an observation.

**Chunk overlap can exceed the size budget.** `_merge` prepends the overlap after
packing, so a chunk may exceed `chunk_size` by up to `chunk_overlap`, and the
overlap slice can cut mid-word.

**Ingestion assumes a single writer.** `_prune` reads the document-hash map once at
the start of a sync and deletes anything absent at the end. A concurrent writer's
documents would be deleted.

**ACLs, when built, will be a point-in-time snapshot.** A permission revoked between
syncs will not be reflected until the next one.

**The knowledge graph is missing the database schema.** `migrations/001_init.sql`
is absent from `graphify-out/` because `tree_sitter_sql` was not installable in the
tool environment. The tables, indexes and the foreign key that forced the
`replace_document` design are invisible to the graph. Anyone using the wiki to
understand storage must read the SQL directly.

**Graph health caveats.** The generated graph reports 135 dangling-endpoint edges
(mostly AST references to external library symbols such as `pydantic` and typer's
`Option`), 5 self-loops, and 100 collapsed undirected edges (node pairs joined by
both `calls` and `references`). The graph is usable; its edge count understates the
raw extraction.

---

## 10. Testing status

```
93 tests collected · 82 passing · 11 skipped (integration)
ruff check .   clean
mypy --strict  clean, 43 source files
```

| File | Tests | Covers |
|---|---|---|
| `test_fusion_and_grounding.py` | 16 | RRF ordering/dedup; citation marker parsing; **prompt-injection containment** |
| `test_retrieval.py` | 14 | store contract, all three strategies, top_k, min_score, reranking, query rewriting |
| `test_chunking.py` | 12 | size budget, id stability, **content preservation** |
| `test_pgvector_integration.py` | 11 | migrations, tsvector, SQL fusion, cascade delete, JSONB, workspace isolation, **transaction rollback** — *all skipped* |
| `test_answerer.py` | 11 | abstention in both modes, citation policy, streaming reassembly |
| `test_registry.py` | 10 | registration, override, unknown-provider error, built-in inventory |
| `test_api.py` | 10 | health, search, chat (both modes), SSE event ordering, input validation |
| `test_ingestion.py` | 9 | idempotency, change detection, pruning, failure isolation, filesystem loader |

**What the suite is good at.** It runs the *real* pipelines — real container, real
retrieval, real answerer — against in-process implementations of the protocols. The
API tests register those doubles through the ordinary registry, which is the same
path a new provider takes. Three of the tests are regressions for defects that were
actually found and reproduced, not speculative.

**Three material gaps:**

1. **The PostgreSQL path has never executed.** Eleven tests exist and skip. Until
   `OSC_TEST_DSN` is set and they run green, the production storage layer is
   unverified — including a transaction whose correctness the ingestion pipeline
   now depends on.
2. **No remote provider has ever been called.** Every adapter is exercised only via
   stubs. Request-shape errors against real Anthropic/OpenAI/Gemini APIs would not
   be caught by this suite.
3. **`settings.py` is untested** (§8), despite carrying custom precedence logic.

There is no coverage measurement, no performance test, and no evaluation of answer
quality.

**How to run:**
```bash
pytest                                     # 82 tests, no dependencies
docker compose up -d && make test-integration   # adds the 11 pgvector tests
ruff check . && mypy src
```

---

## 11. Configuration and environment requirements

**Runtime:** Python 3.12+. PostgreSQL 16 with the `pgvector` extension
(`docker compose up -d` provides one).

**Install:** core dependencies are deliberately small; every provider SDK is an
optional extra, so a deployment installs only what it configures.

```bash
pip install -e ".[dev,anthropic,openai]"     # typical
pip install -e ".[gemini]"                   # native Gemini adapter
pip install -e ".[local]"                    # sentence-transformers (local embeddings + cross-encoder)
```

**Configuration layers**, highest precedence first: process environment → `.env` →
YAML profile (`config/default.yaml`, overridable with `OSC_PROFILE`). Any value is
addressable from the environment with `OSC_` and `__` for nesting:

```bash
OSC_LLM__PROVIDER=groq OSC_LLM__MODEL=llama-3.3-70b-versatile osc-assistant ask "..."
```

**Credentials** — only for providers actually configured. `ANTHROPIC_API_KEY`,
`OPENAI_API_KEY`, `GEMINI_API_KEY`/`GOOGLE_API_KEY`, `GROQ_API_KEY`,
`VOYAGE_API_KEY`, `HF_TOKEN`. Local providers (ollama, vllm, lmstudio,
sentence-transformers) need none. `config/experiments/local-only.yaml` runs the
entire system with zero credentials and no corpus text leaving the host.

**Defaults:** Anthropic `claude-opus-5` for answers, `claude-haiku-4-5` for query
rewriting, OpenAI `text-embedding-3-large` for embeddings, pgvector store, `noop`
reranker, recursive chunking (1200/150), hybrid retrieval (40 candidates → top 8).

**Two constraints that will bite:**
- Changing the embedding model changes the vector width, which is fixed in the DDL
  at migration time. It requires a new database (or a dropped `chunks` table) and a
  full re-index. The store asserts the dimensions match at startup and refuses to
  run otherwise.
- `min_score` interacts with the reranker as described in §8. Do not enable
  `cross_encoder` without addressing it.

---

## 12. Important design decisions and why they were made

**No LLM framework.** LangChain and LlamaIndex were evaluated and rejected — on
evidence, per requirement 7. The seams this system needs are five protocols totalling
about 120 lines. A framework would impose its own document and retriever
abstractions on top of ours, add a large transitive dependency tree, and place an
uncontrolled layer on the exact code path that most needs tracing and tuning.
Provider SDKs are used directly, each as an optional extra.

**One adapter for eight services.** OpenAI, Groq, Ollama, vLLM, LM Studio, Hugging
Face, OpenRouter and Together all speak `/v1/chat/completions`. They are registered
under separate provider names with base URL and credential environment variable
pre-filled. Eight adapters would have been eight places to fix the same bug.

**Protocols, not base classes.** Structural typing means a provider is compatible by
virtue of its shape. No inheritance, nothing to register beyond the factory, and a
test double is indistinguishable from a provider — which is what makes the API tests
meaningful.

**One datastore.** PostgreSQL holds chunk text, embeddings, lexical index and
document metadata. A chunk and its vector cannot drift apart, there is one backup to
take, and hybrid retrieval is one round trip instead of a fan-out. A dedicated vector
database earns its place when vector search p95 degrades or the corpus passes a few
million chunks; the `VectorStore` protocol is where that swap happens.

**Hybrid retrieval by default.** Internal corpora are dense with acronyms, product
codenames and error strings that semantic search handles badly, and paraphrase that
keyword search handles badly. Postgres provides both indexes, so the marginal cost is
one query and a fusion step. This is avoiding a known failure mode, not premature
optimisation.

**Native citations where available, markers elsewhere.** Discussed in §9. The
capability flag lives in the adapter so no business logic branches on it.

**Abstention is architectural, not a prompt.** No hits → no model call, because
generating from nothing is guessing. In streaming mode the final `complete` event is
authoritative and the client discards what it rendered — a policy that only held when
not streaming would be worse than none.

**Frozen prompts.** System prompts are module constants with no interpolation. Any
dynamic value would break prefix caching for every request and make evaluation
results unattributable to a reviewable string.

**`workspace_id` from day one.** The only speculative design in the codebase, and
defended: adding a partition key to a populated corpus is a data migration; carrying
it now costs one column and one index prefix.

### Three defects found and fixed in the last session

These are recorded because each one changed the design, and each has a regression
test.

1. **Prompt injection via source bodies.** Titles were escaped; bodies were not. A
   document containing `</source></sources>` closed the data block and landed its own
   text where the model reads it as instruction — reproduced, two closing tags in the
   output. Fixed with a per-request nonce in the delimiter. Escaping bodies was
   rejected because it would corrupt the technical content this corpus is full of,
   turning `<div>` into `&lt;div&gt;` for the model to read and quote back.

2. **Ingestion could permanently lose a document.** The pipeline wrote the content
   hash before the chunks, in three separate un-transacted calls. A crash in between
   left a current hash with zero chunks; every later sync read the hash as "already
   indexed" and skipped it — silently invisible forever, with the report counting it
   as success. A plain reorder was impossible (chunks reference the document row via
   a foreign key), so `upsert` + `record_document` were replaced with a single
   `replace_document(document, chunks)` in one transaction. **The protocol got
   smaller** — two methods out, one in.

3. **The chunker silently corrupted document text.** Separators were re-attached with
   `part + separator`, appending one to the final fragment that was never there — 287
   characters in, 286 out, with a doubled `.`. In a system whose trust model is "click
   the citation and verify", the indexed text was not the source text, and the
   Anthropic path was quoting it back as verbatim evidence. Fixed with a split that
   guarantees `"".join(parts) == text`.

---

## 13. Recommended implementation order for the remaining work

The ordering principle: **make the system verifiable before making it bigger.** Two
things currently block honest judgement of everything else — the database layer has
never run, and there is no way to tell whether a retrieval change helps or hurts.
Both are cheap relative to the confidence they buy.

1. **Run the pgvector integration tests.** Everything about the storage layer is
   currently taken on trust. Zero new code.
2. **Close the P1 debt** (`min_score`, the auth start-up guard, the inert cache
   flag). Small, and one of them is a live footgun.
3. **Build the evaluation harness.** Nothing after this point can be judged without
   it — not reranking, not chunking, not a model swap. It is the gate for items 6–8.
4. **Add authentication (OIDC).** The first hard blocker to exposing the service.
   Group membership from the IdP is also the input to item 5.
5. **Add per-document ACLs.** Only after auth exists and only with explicit sign-off
   on which corpora are ingested. Until then, keep Phase 1's restriction to
   company-wide-readable content.
6. **Tune retrieval against the golden set** — reranking, chunking strategy, query
   rewriting. Every change gated by a measured improvement; anything that does not
   move a metric gets reverted.
7. **Conversation persistence and feedback capture.** Feedback is the raw material
   for future evaluation sets, so it compounds.
8. **Second connector.** The loader shape is established; this proves it.
9. **Deployment artefacts and admin visibility.** Dockerfile, CI, ingestion status
   view.

**Deliberately late:** the web client (the API and CLI are sufficient for a pilot),
multi-tenancy beyond the partition key, and any additional provider. **Deliberately
absent:** fine-tuning, agentic tool use, a knowledge-graph layer.

---

## 14. Next 3–5 milestones with success criteria

### Milestone A — Verify the storage layer
*Estimated 0.5 day. No new features.*

Run the integration suite against a real PostgreSQL, fix whatever it reveals, and
pin the pgvector image digest.

**Success criteria**
- `docker compose up -d && make test-integration` → 93 passed, 0 skipped.
- A `CREATE EXTENSION vector` failure and a dimension mismatch each produce a clear,
  actionable error rather than a stack trace.
- An end-to-end run against real Postgres: `osc-assistant ingest ./docs` then
  `osc-assistant search "<term>"` returns hits; re-running ingest reports
  `indexed=0 skipped=N`.

### Milestone B — Close the P1 debt
*Estimated 1 day.*

Fix the `min_score` scale problem, add the production auth guard, resolve the inert
cache flag, and add the missing `settings.py` tests.

**Success criteria**
- Enabling `reranker: cross_encoder` in a profile does not reduce the number of
  retrieved chunks; a test asserts the threshold is applied to first-stage scores.
- Starting with `OSC_ENVIRONMENT=production` and no auth configured exits non-zero
  with an explanatory message; a test asserts it.
- Four settings-precedence tests pass: env over YAML, nested env merge, missing
  profile tolerated, unknown key rejected.
- Either `cache_read_input_tokens > 0` is observed on a repeated request, or a
  startup log line states that the prompt is below the cacheable threshold.

### Milestone C — Evaluation harness
*Estimated 3–4 days. The highest-leverage item in the project.*

50–100 real questions curated with OSC employees, each with known-correct source
documents. Offline retrieval metrics and generation metrics, runnable as
`make eval`, wired into CI as a gate on changes to retrieval or generation.

**Success criteria**
- `make eval` prints recall@10, MRR, citation coverage and faithfulness against the
  golden set, and writes a JSON result for comparison across runs.
- A pull request that drops recall@10 below a configured threshold fails CI.
- Baseline numbers for the current default profile are committed, so future changes
  are measured against a real starting point rather than an assumption.
- At least one provider comparison is run end-to-end (e.g. default vs
  `groq-voyage.yaml`) and the result recorded — this is also the first real
  exercise of the vendor-agnosticism the architecture was built for.

### Milestone D — Authentication
*Estimated 2–3 days.*

OIDC against OSC's IdP. Tokens validated server-side; the resolved principal set
(user id + group ids) attached to every request and carried into the retrieval call
so ACL filtering has somewhere to plug in.

**Success criteria**
- An unauthenticated request to `/api/chat` or `/api/search` returns 401.
- A valid token yields an answer, and the user id and group ids appear in the
  structured log for that request.
- The production start-up guard from Milestone B is satisfied by real auth rather
  than bypassed.
- Rate limiting per authenticated principal, with a test that a bounded burst is
  rejected.

### Milestone E — Retrieval quality pass
*Estimated 3–5 days. Requires Milestone C.*

With measurement in place, tune what was deferred: enable and measure reranking,
try structure-aware chunking, decide on query rewriting with evidence, and remove
whatever does not earn its place.

**Success criteria**
- Faithfulness ≥ 95% and recall@10 ≥ 90% on the golden set, or a written explanation
  of why the target is wrong for this corpus.
- A recorded decision on the cross-encoder reranker, with the measured delta.
- A recorded decision on query rewriting: kept with a measured improvement, or
  defaulted off and the `fast_llm` dependency removed.
- Every change in this milestone has a before/after number attached. Any change that
  did not move a metric has been reverted.

---

## Appendix — orientation for a new session

**Read in this order:** this file → `README.md` → `claude.md` →
`src/osc_assistant/protocols.py` (the five seams) → `src/osc_assistant/container.py`
(how everything is wired).

**Useful commands**
```bash
osc-assistant providers          # every registered provider, read from the registries
osc-assistant search "<query>"   # retrieval only — the debugging surface
curl localhost:8000/api/health   # the active component set of a running deployment
open graphify-out/graph.html     # interactive knowledge graph
```

**The knowledge graph** in `graphify-out/` was generated on 2026-07-29 from 62 files:
812 nodes, 1973 edges, 36 communities. `wiki/index.md` is the agent entry point.
Regenerate with `/graphify . --wiki` after significant changes. Note the two caveats
in §9: the SQL schema is missing from it, and its edge count understates the raw
extraction.

**The one rule to preserve:** business logic imports `protocols` and `types` only.
If a pipeline, route or CLI command ever imports a provider module, the
vendor-agnosticism this project is built around has been broken. It is checkable
with a grep, and it is worth checking.
