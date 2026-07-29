# PROJECT_STATUS.md

**Project:** OSC Internal Knowledge Assistant
**Status:** Phase 2 — the knowledge engine runs end to end on a verified local stack; not yet production-ready
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

**Where it stands.** The full path has now been executed against real
infrastructure, not stubs: drop PDFs, Word documents, HTML, Markdown and text files
into `./docs`, ingest them, and they are parsed, chunked, embedded, and stored in
PostgreSQL with pgvector. Questions retrieve by hybrid search and are answered by
Qwen3 running locally through Ollama, with citations back to the source file. A
re-run over an unchanged corpus makes zero embedding calls. 119 tests, **0 skipped**;
`ruff` and `mypy --strict` clean across 45 source files.

The default configuration is now fully local and needs no credential: Ollama
(`qwen3:8b`) for generation, Ollama (`nomic-embed-text`, 768-d) for embeddings,
PostgreSQL 18 with pgvector 0.8.2 for storage.

**What changed this session.** The previously unverified PostgreSQL layer was run
for the first time and immediately produced a real defect: chunk and document
metadata was being **double-encoded**, so it read back as a `str` rather than a
`dict` for every consumer of `Chunk.metadata` (§12). That is exactly the class of
bug the untested-storage warning existed to flag. Ingestion also gained real
document parsing — it previously read only plain text — and a data-loss guard
around pruning.

**Where it does not stand.** There is still no authentication, no per-document
access control, no rate limiting, no conversation persistence, and **no evaluation
harness** — so no quality claim in this document is measured. Answer quality is
also bounded by an 8B local model: it is grounded and it cites correctly, but it
misreads figures (§9).

**The honest one-line summary:** a working, verified knowledge engine on a local
stack, one authentication story and one evaluation harness away from being
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
connectors ──▶ parse ──▶ chunk ──▶ embed ──▶ vector store
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

### Ingestion path

`ingestion/parsers.py` maps a file extension to an extraction function:
Markdown/text read directly, HTML through the standard library's `html.parser`
(dropping `<script>` and `<style>`, preferring the document's own `<title>`), PDF
through `pypdf` (per page, retaining `page_count`), and `.docx` through
`python-docx` (including table cells, where policy documents keep the facts people
actually ask about). Parsers extract and never rewrite: chunk text is quoted back as
citation evidence, so invented text would make that evidence a forgery.

`FilesystemLoader` delegates to that registry and records any file it cannot read
in `failures`, which the pipeline treats as **present but unreadable** rather than
deleted (§12). Metadata — relative path, extension, size, page count, mtime — is
attached to the `Document` and denormalised onto every chunk.

### Storage

One PostgreSQL database holds chunk text, embeddings (`pgvector`), the lexical
index (a generated `tsvector` column) and document metadata. `migrations/001_init.sql`
is applied by a hand-rolled forward-only runner in `pgvector.py`; the embedding
dimension is substituted into the DDL at migration time. The HNSW index is created
only when that dimension is ≤ 2000, which is pgvector's hard limit; above it the
column is left unindexed and search degrades to an exact scan rather than the
migration failing outright. Every table carries a `workspace_id` partition key —
one workspace exists today.

---

## 4. Repository structure

```
src/osc_assistant/
├── protocols.py            the five seams
├── types.py                domain vocabulary — the largest shared surface
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
├── ingestion/              parsers.py · loaders.py · pipeline.py
├── retrieval/              pipeline.py · rewrite.py
├── generation/             answerer.py · prompts.py
└── api/                    app.py · schemas.py · sse.py · static/index.html

tests/                      119 tests, 0 skipped
migrations/001_init.sql     schema, with a dimension-conditional HNSW index
docs/                       the ingestion folder — seed corpus, 5 formats
config/                     default.yaml + experiments/{local-only,hosted-anthropic,groq-voyage}.yaml
graphify-out/               generated knowledge graph — graph.html, wiki/, GRAPH_REPORT.md
```

`graphify-out/` was regenerated after this session's changes: 1022 nodes, 2230
edges, 73 communities, and it now covers `ingestion/parsers.py`, the UI and the new
tests. **`graphify-out/wiki/` is the exception — it is still the previous build's
output and is stale.** Regenerate it with `/graphify . --wiki`, because
`CLAUDE.md` directs every new session to read it.

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
| 14 | **Test suite** | 119 tests, 0 skipped; 108 run with no network/DB/credentials; ruff + mypy --strict clean |
| 15 | **Three P0 defects found and fixed** | prompt injection, ingestion data loss, chunker content corruption — see §12 |
| 16 | **Multi-format document parsing** | `.md` `.markdown` `.txt` `.rst` `.html` `.htm` `.pdf` `.docx`, one function per format; verified against a real corpus of all five families |
| 17 | **PostgreSQL layer verified against a real database** | 11 integration tests executed for the first time, all green; found and fixed the metadata double-encoding defect (§12) |
| 18 | **Fully local default stack** | Ollama `qwen3:8b` + `nomic-embed-text` + pgvector; no credential, no corpus text off-host |
| 19 | **Reasoning-model handling** | thinking disabled by default and budgeted for; leaked `<think>` blocks stripped before citation parsing; exhausted budget reported instead of silently abstaining |
| 20 | **Prune data-loss guard** | an unreadable file is exempt from pruning, so a transient parse failure cannot delete a healthy indexed document |
| 21 | **Chat UI** | one static page at `/`, streaming over SSE, honouring the authoritative-`complete` contract |

---

## 6. Partially completed milestones

**Prompt caching — implemented, currently inert.** The `cache_system_prompt` option
marks the Anthropic system block as cacheable, and prompts are frozen module
constants specifically so the prefix stays byte-identical. But `ANSWER_SYSTEM_PROMPT`
is roughly 250 tokens, below the minimum cacheable prefix on current models, so
`cache_read_input_tokens` will be zero on every request. The discipline is correct;
the saving does not currently occur.

**Reranking — built, now safe to enable, still unmeasured.** The `min_score` scale
defect is fixed: the threshold is applied to first-stage scores before reranking,
so a cross-encoder's negative logits no longer empty the result set. A regression
test asserts it. What remains is the reason it is still off by default — there is
no golden set to demonstrate that it improves anything.

**pgvector store — complete and now verified.** All eleven integration tests have
been executed against PostgreSQL 18.4 with pgvector 0.8.2 and pass: the migration
runner, the generated `tsvector` column, the SQL rank-fusion query, the
`replace_document` transaction, cascade deletion and workspace isolation. Running
them also surfaced the metadata double-encoding defect (§12).

One caveat: the suite shares a database with the application, so
`OSC_TEST_DIMENSIONS` must match the width the `chunks` table was migrated with
(768). A dedicated test database would be better and is a small change.

**Workspace partitioning — schema-complete, single-tenant in practice.** Every table
carries `workspace_id` and every query is scoped by it, but only one workspace ever
exists and nothing resolves a workspace from a request.

**Query rewriting — implemented, now disabled by default.** It works and degrades
safely, but it was never justified by measurement, and on the local stack it costs a
second Qwen3 call on the critical path. It is off in `config/default.yaml`; the
architecture, the `fast_llm` seam and the tests remain. The UI correspondingly does
not send conversation history, so follow-up turns are currently independent
questions. Turning both on together is the right move once there is a golden set to
show it helps.

**Prompt caching — implemented, inert, and now doubly so.** `cache_system_prompt`
marks the Anthropic system block cacheable, but the prompt is below the minimum
cacheable prefix, and the default stack is Ollama, which has no such feature. The
discipline (frozen prompts, stable prefix) is still correct and costs nothing.

**Documentation — thorough in code, thin operationally.** Module docstrings explain
intent and trade-offs throughout, and README now covers ingestion, formats and the
reasoning-model budget. There is still no deployment guide and no on-call runbook.

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

### Fixed this session

- **`min_score` compared against an undefined scale** — now applied to first-stage
  scores before reranking, with a regression test using a negative-scoring reranker.
- **Metadata double-encoding in the pgvector store** — see §12.
- **Pruning could delete an unreadable-but-present document** — see §12.
- **Migration failed for embedding models wider than 2000 dimensions** — the HNSW
  index is now conditional. This would have broken the *previous* default profile
  (`text-embedding-3-large`, 3072-d) on its first real migration.

### P1 — fix before real traffic

**Endpoints are unauthenticated, unbounded and unthrottled.**
Documented as deferred in the README, which is fine as a plan and not fine as a
release state — the constraint lives in prose, not in the code path. Now slightly
more pressing, because a UI at `/` makes the service look ready to use. *Smallest
fix:* refuse to start when `environment != "development"` and no auth is configured.
Ten lines, and the constraint becomes enforced.

**No evaluation harness, and now more surface to evaluate.** Chunk size, `top_k`
and the reasoning budget were all tuned this session against a 4096-token context by
reasoning, not measurement. They are plausible; they are not verified. Every
retrieval and generation setting in `config/default.yaml` is currently an educated
guess.

**The integration suite shares the application database.** Isolation is by
`workspace_id` and it is honoured, but a test run against a production DSN would
write to production. *Smallest fix:* a dedicated test database, and refuse to run
when the DSN matches the configured application DSN.

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

**No OCR path for scanned PDFs.** They are detected and rejected with a clear
message rather than silently indexed as empty, which is the right failure. But a
real internal corpus contains scans, and today they simply cannot be ingested.

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

**The local answer model misreads figures.** Observed directly: asked for the
expense approval thresholds, `qwen3:8b` rendered the source's "500 to 2,500 EUR" as
"50,000 to 2,500 EUR" while citing the correct passage. The retrieval was right, the
citation was right, and the number was wrong. This is the central honest caveat of
the local stack: citations tell a user *where to check*, and on an 8B model they
genuinely have to. `hosted-anthropic.yaml` exists partly as the comparison point,
and quantifying this gap is the first job of the evaluation harness.

**Answers are limited by a 4096-token context.** Ollama loads `qwen3:8b` with a
4096-token window, which is what caps the corpus sent to the model at five chunks of
~900 characters. A longer document needing six passages to answer will be answered
incompletely rather than incorrectly, but it will still be answered. Serving the
model with a larger context and raising `top_k`, `chunk_size` and `max_tokens` is a
configuration change.

**Follow-up questions are not conversational.** Query rewriting is off by default
(§6) and the UI sends no history, so "what about the second one?" retrieves against
those literal words.

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

**Graph health — now clean.** The previous build reported 135 dangling-endpoint
edges, 5 self-loops and 100 collapsed undirected edges. After the rebuild the
diagnostic reports **zero** of each across all 2230 edges, so the edge count no
longer understates the raw extraction.

**The graph now contains the seed corpus as well as the code.** `docs/` is test
data for the RAG system, but to graphify it is just more documents, so six
communities (leave policy, expense limits, incident severity, deployment runbook,
data retention, access control) describe OSC's fictional internal policies rather
than this codebase. Harmless, and it does mean a graph query can return a policy
node. Exclude `docs/` from the scan if that becomes noise.

---

## 10. Testing status

```
119 tests collected · 119 passing · 0 skipped
ruff check .   clean
mypy --strict  clean, 45 source files
```

| File | Tests | Covers |
|---|---|---|
| `test_fusion_and_grounding.py` | 16 | RRF ordering/dedup; citation marker parsing; **prompt-injection containment** |
| `test_retrieval.py` | 15 | store contract, all three strategies, top_k, reranking, query rewriting, **min_score applied pre-rerank** |
| `test_parsers.py` | 13 | every format, content preservation, script/style stripping, corrupt and scanned files, **failure isolation**, provenance metadata |
| `test_chunking.py` | 12 | size budget, id stability, **content preservation** |
| `test_pgvector_integration.py` | 11 | migrations, tsvector, SQL fusion, cascade delete, JSONB, workspace isolation, **transaction rollback** — *all executing* |
| `test_ingestion.py` | 11 | idempotency, change detection, pruning, **unreadable-file prune exemption**, failure isolation |
| `test_answerer.py` | 11 | abstention in both modes, citation policy, streaming reassembly |
| `test_api.py` | 11 | health, search, chat (both modes), SSE event ordering, input validation, UI route |
| `test_registry.py` | 10 | registration, override, unknown-provider error, built-in inventory |
| `test_reasoning_models.py` | 9 | `<think>` stripping, anchoring, exhausted-budget error, **reasoning markers never becoming citations** |

**What the suite is good at.** It runs the *real* pipelines — real container, real
retrieval, real answerer — against in-process implementations of the protocols. The
API tests register those doubles through the ordinary registry, which is the same
path a new provider takes. Three of the tests are regressions for defects that were
actually found and reproduced, not speculative.

**Manual end-to-end verification performed this session** (not automated — see
gap 1 below):

| Check | Result |
|---|---|
| Ingest 7 documents across 5 formats | 7 indexed, 20 chunks, 1.8s |
| Schema in PostgreSQL | 3 tables, 5 indexes, `vector(768)`, `tsv` populated on all chunks |
| Re-ingest unchanged corpus | `indexed=0 skipped=7`, zero embedding calls, 0.07s |
| Edit one file and re-ingest | `indexed=1 skipped=6` |
| Delete a file and re-ingest | `deleted=1`, chunks 20 → 18 via cascade |
| Corrupt PDF dropped into corpus | `unreadable=1`, exit 1, **0 documents pruned** |
| Retrieval (hybrid) | correct document ranked first, RRF scores ~0.016 |
| Answer from `.pdf` / `.docx` table / `.html` | correct, each citing the right source |
| Unanswerable question | abstained; general knowledge not used |
| SSE stream | 88 deltas, sources → citation → complete, usage reported |
| UI stream parsing | replayed a real stream at adversarial chunk boundaries; frames reassembled, no parse errors |

**Four material gaps:**

1. **The end-to-end path is not automated.** Everything in the table above was run
   by hand. It needs a smoke test that a CI job can run against a live Ollama and
   Postgres, or it will rot.
2. **No hosted provider has ever been called.** Every hosted adapter is exercised
   only via stubs. Request-shape errors against real Anthropic/OpenAI/Gemini APIs
   would not be caught by this suite — including the Anthropic native-citation path,
   which is the only verified-citation implementation in the codebase.
3. **`settings.py` is untested** (§8), despite carrying custom precedence logic.
4. **Answer quality is unmeasured.** No coverage measurement, no performance test,
   no golden set.

**How to run:**
```bash
make test              # 119 tests, no network, no database, no credentials
make test-integration  # the same suite plus the pgvector tests against a real DB
make check             # lint + typecheck + test
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

**Defaults (all local):** Ollama `qwen3:8b` for answers with reasoning disabled,
Ollama `nomic-embed-text` (768-d) for embeddings, pgvector store, `noop` reranker,
recursive chunking (900/120), hybrid retrieval (30 candidates → top 5), 1500 max
completion tokens, query rewriting off.

**Reference environment as verified:** PostgreSQL 18.4 with pgvector 0.8.2, database
`osc`; Ollama 0.32.5 serving `qwen3:8b` at a 4096-token context and
`nomic-embed-text`. `docker-compose.yml` remains as an alternative for machines
without a local PostgreSQL.

**Three constraints that will bite:**
- Changing the embedding model changes the vector width, which is fixed in the DDL
  at migration time. It requires a new database (or a dropped `chunks` table) and a
  full re-index. The store asserts the dimensions match at startup and refuses to
  run otherwise. This is why each experiment profile names its own database.
- pgvector cannot build an HNSW index above 2000 dimensions. The migration handles
  this by skipping the index, so vector search silently becomes an exact scan.
  Correct, but O(n): check this before choosing a wide embedding model.
- The prompt budget is sized for a 4096-token context. Raising `top_k` or
  `chunk_size` without also serving the model with a larger context will push the
  answer out of the window.

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

**Text extraction is a plain dict of functions, not a registry.** The five component
seams use the `Registry[T]` machinery because they are selected by a name from
configuration and need per-provider options. A parser is selected by file extension
and takes none, so `PARSERS: dict[str, Parser]` is the whole mechanism. Reaching for
the heavier abstraction here would have added indirection without removing a line.

**Reasoning control is configuration, not code.** Qwen3's thinking is disabled with
`extra_body.reasoning_effort: none` through the adapter's existing pass-through for
vendor-specific parameters. No new code path, and it works for any reasoning model
behind an OpenAI-compatible endpoint. Only the *consequences* of reasoning —
stripping a leaked block, reporting an exhausted budget — needed code, because those
are correctness concerns rather than tuning.

### Three defects found and fixed in this session

1. **Metadata was double-encoded in PostgreSQL.** The connection registers a `jsonb`
   codec whose encoder is `json.dumps`, and `replace_document` *also* called
   `json.dumps` before passing the value. Postgres therefore stored a JSON string
   containing JSON, and every read produced `str` where the domain type promises a
   `Mapping`. Nothing crashed — `Chunk.metadata` is typed as a `Mapping` and a `str`
   is not one, but nothing at runtime checks that — so any future filtering on
   metadata would have failed inexplicably. Fixed by passing the dict and letting the
   codec do its job. `test_metadata_round_trips_as_json` covers it and would have
   caught it the day it was written, had it ever been run.

2. **Pruning could permanently delete a document that still exists.** `_prune`
   deletes anything indexed but absent from the current sync. A file that failed to
   parse is absent from the sync but present at the source, so a corrupt byte — or
   simply deploying without the `documents` extra installed — would have deleted
   every PDF from the index on the next run, reporting `deleted=N` as if it were
   routine. Loaders now record failures as `LoadFailure`, and the pipeline exempts
   those document ids from pruning. Two regression tests pin both halves: the
   exemption, and that genuinely removed documents are still pruned.

3. **The migration would have failed on the previous default embedding model.**
   `CREATE INDEX ... USING hnsw` is capped at 2000 dimensions by pgvector, and the
   default profile specified `text-embedding-3-large` at 3072. The first real
   migration on the previous default configuration would have aborted. The index is
   now created conditionally, with a warning when it is skipped.

### Three defects found and fixed in the previous session

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

The ordering principle is unchanged — **make the system verifiable before making it
bigger** — but the binding constraint has moved. The storage layer is no longer an
unknown; measurement is. Every tuning decision in `config/default.yaml` is currently
an educated guess, and the local model's figure-misreading (§9) is unquantified.

1. **Build the evaluation harness.** Now the single highest-leverage item by a wide
   margin. Nothing after this can be judged without it — not reranking, not chunk
   size, not the local-versus-hosted question, not whether the 4096-token budget is
   actually costing answers. It is the gate for items 5–7.
2. **Automate the end-to-end smoke test.** The table in §10 was produced by hand.
   One test that ingests a fixture corpus, asks a question and asserts a citation,
   run against live Ollama and Postgres, keeps all of it honest.
3. **Add authentication (OIDC).** The first hard blocker to exposing the service,
   and more pressing now that there is a UI. Group membership from the IdP is also
   the input to item 4.
4. **Add per-document ACLs.** Only after auth exists and only with explicit sign-off
   on which corpora are ingested. Until then, keep the restriction to
   company-wide-readable content.
5. **Tune retrieval against the golden set** — reranking, chunk size, query
   rewriting, top_k, and a serious look at whether a larger-context model changes the
   answer. Every change gated by a measured improvement; anything that does not move
   a metric gets reverted.
6. **Conversation persistence and feedback capture.** Feedback is the raw material
   for future evaluation sets, so it compounds. Re-enabling query rewriting belongs
   here, together with sending history from the UI.
7. **Second connector.** The loader shape is established and now has a parser layer
   behind it; this proves both.
8. **Deployment artefacts and admin visibility.** Dockerfile, CI, ingestion status
   view. `IngestionReport` already carries the data.

**Deliberately late:** the web client (the API and CLI are sufficient for a pilot),
multi-tenancy beyond the partition key, and any additional provider. **Deliberately
absent:** fine-tuning, agentic tool use, a knowledge-graph layer.

---

## 14. Next 3–5 milestones with success criteria

### ~~Milestone A — Verify the storage layer~~ ✅ complete

Run the integration suite against a real PostgreSQL and fix whatever it reveals.

**Outcome:** `make test-integration` → 119 passed, 0 skipped. The metadata
double-encoding defect and the >2000-dimension migration failure were found and
fixed (§12). An end-to-end run against real Postgres ingests `./docs`, searches, and
re-runs as `indexed=0 skipped=7`. The dimension-mismatch guard produces a clear,
actionable error. The pgvector image digest is *not* pinned — the reference
environment uses a native PostgreSQL, so the compose file is now a secondary path.

### Milestone B — Close the remaining P1 debt
*Estimated 1 day. Partially complete.*

`min_score` is fixed and has a regression test. What remains is the production auth
guard and the `settings.py` tests.

**Success criteria**
- ~~Enabling `reranker: cross_encoder` does not reduce the number of retrieved
  chunks; a test asserts the threshold is applied to first-stage scores.~~ ✅
- Starting with `OSC_ENVIRONMENT=production` and no auth configured exits non-zero
  with an explanatory message; a test asserts it.
- Four settings-precedence tests pass: env over YAML, nested env merge, missing
  profile tolerated, unknown key rejected.
- The integration suite refuses to run against the configured application DSN.

### Milestone B2 — Automate the end-to-end check
*Estimated 0.5 day.*

The verification table in §10 was produced by hand and will rot. One test, marked so
it is skipped without a live Ollama and Postgres, that ingests a fixture corpus,
asserts idempotency on a second run, asks a question and asserts a citation back to
the expected file.

**Success criteria**
- `make test-e2e` passes against the reference environment and skips cleanly without it.
- It covers at least one binary format (PDF or DOCX), so a parser regression is caught.
- It asserts abstention on a question the fixture corpus cannot answer.

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
- At least one provider comparison is run end-to-end (default vs
  `hosted-anthropic.yaml`) and the result recorded — this is also the first real
  exercise of the vendor-agnosticism the architecture was built for.
- The local model's numeric-fidelity gap (§9) is quantified rather than anecdotal:
  a faithfulness figure for `qwen3:8b` against one for a hosted model, so the
  decision to run locally is made on a number and not on a preference.

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
osc-assistant ingest ./docs      # index the corpus; safe and cheap to re-run
osc-assistant search "<query>"   # retrieval only — the debugging surface
osc-assistant ask "<question>"   # the whole pipeline, with citations
curl localhost:8000/api/health   # the active component set of a running deployment
open graphify-out/graph.html     # interactive knowledge graph
```

**Checking the environment before debugging the code.** Most of a session's
surprises here come from outside the process:

```bash
curl -s localhost:11434/api/tags                    # models Ollama actually has
psql "$DSN" -c "select count(*) from chunks"        # is anything indexed?
psql "$DSN" -c "select format_type(atttypid, atttypmod) from pg_attribute \
  where attrelid='chunks'::regclass and attname='embedding'"   # the fixed vector width
```

A model's `capabilities` in `/api/tags` is worth checking specifically: `qwen3:8b`
reports `completion, tools, thinking` and **cannot embed**, which is why a separate
embedding model is required.

**The knowledge graph** in `graphify-out/` was rebuilt on 2026-07-29 and is current:
1022 nodes, 2230 edges, 73 communities, health diagnostic clean. `wiki/index.md` is
the agent entry point but **was not regenerated and is stale** — run
`/graphify . --wiki` to refresh it. One caveat from §9 still stands: the SQL schema
is absent because `tree_sitter_sql` is not installed (`pip install "graphifyy[sql]"`),
so `migrations/001_init.sql` contributes no nodes and storage must be read from the
SQL directly. `docs/handbook/onboarding-checklist.docx` is likewise absent —
`.docx` extraction needs `pip install "graphifyy[office]"`.

**The one rule to preserve:** business logic imports `protocols` and `types` only.
If a pipeline, route or CLI command ever imports a provider module, the
vendor-agnosticism this project is built around has been broken. It is checkable
with a grep, and it is worth checking.
