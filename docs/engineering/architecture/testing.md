# Testing

*Four tiers, each answering a different question. Confidence, not coverage.*

---

## The tiers

```bash
make test              # 279 tests · no network, no database, no credentials · ~2s
make test-integration  # + 18 pgvector tests against a real database
make test-e2e          # + 9 tests against live Ollama AND PostgreSQL
make eval              # not a test — measurement. See evaluation.md
```

| Tier | Answers | Runs where |
|---|---|---|
| Unit / component | Is the logic correct? | Anywhere, always |
| Integration | Does the SQL do what we think? | A machine with PostgreSQL |
| End-to-end | Does the whole thing work against real infrastructure? | A machine with Ollama and PostgreSQL |
| Evaluation | Is it any *good*? | After `make ingest` |

The last row is the distinction worth internalising: **`make test` asks whether the
system is correct, `make eval` asks whether it is good.** A system can pass every test
and answer every question badly.

---

## What makes the fast tier meaningful

279 tests run with no network, no database and no credential — and they still exercise
the *real* pipelines.

The trick is the protocol layer. `conftest.py` holds in-process implementations of the
protocols — not mocks. `StubEmbeddingModel` is a deterministic bag-of-words embedder
that hashes tokens into buckets, so texts sharing vocabulary land near each other under
cosine similarity; retrieval assertions are meaningful and identical on every machine,
with no model download. `StubChatModel` returns a scripted reply and goes through the
real marker-parsing citation path.

The API and CLI tests register these doubles **through the ordinary registry — the same
path a new provider takes.** So "the whole stack can be retargeted by configuration
alone" is asserted by the suite rather than assumed by the architecture document.

This is the payoff from [protocols rather than base
classes](provider-architecture.md#why-protocols-and-not-abstract-base-classes): a test
double is indistinguishable from a provider, so the tests are not testing a special
code path.

---

## Coverage by file

| File | Covers |
|---|---|
| `test_evaluation.py` | Metrics against worked examples; golden-set validation; failed cases excluded from means; retrieval-only omits generation metrics; judge verdict parsing and failure handling |
| `test_cli.py` | Every operational command; doctor's pass/warn/fail; trace commands across process boundaries; operator-error reporting; help grouping |
| `test_langchain_integration.py` | Both chunkers (id stability, content preservation, size budget, heading metadata); chat and embedding bridges; the outbound retriever |
| `test_pgvector_integration.py` | Migrations, tsvector, SQL fusion, cascade delete, JSONB, workspace isolation, transaction rollback, inspection SQL |
| `test_fusion_and_grounding.py` | RRF ordering and dedup; citation marker parsing; **prompt-injection containment** |
| `test_api.py` | Health, status, search, chat (both modes), SSE ordering, trace endpoints and their environment gate |
| `test_trace_store.py` | Cross-process readability, rotation, malformed lines, unwritable directories, round-trip fidelity |
| `test_observability.py` | Span tree shape, nested-trace merging, error capture, span cap, text redaction |
| `test_retrieval.py` | Store contract, all three strategies, top_k, reranking, rewriting, **min_score applied pre-rerank** |
| `test_parsers.py` | Every format, content preservation, corrupt and scanned files, empty workbooks, **failure isolation** |
| `test_ingestion.py` | Idempotency, change detection, pruning, **unreadable-file prune exemption**, `--reindex`, trace shape |
| `test_chunking.py` | Size budget, id stability, **content preservation** |
| `test_server_lifecycle.py` | Startup notes, **in-flight stream failure emits a terminal event**, shutdown releases only what was built |
| `test_inspection.py` | `StoreInspector` contract; empty-store edge cases |
| `test_answerer.py` | Abstention in both modes, citation policy, streaming reassembly |
| `test_settings.py` | Four-layer precedence, nested env merge, malformed profiles, trace exposure gate |
| `test_e2e.py` | Six formats indexed **from a corpus it generates itself**; idempotency; hybrid ranking; a cited answer; abstention; PDF text extraction proven; both modes agreeing; the run fully traced |
| `test_reasoning_models.py` | `<think>` stripping, exhausted-budget error, reasoning markers never becoming citations |
| `test_registry.py` | Registration, override, unknown-provider error |

**Bold entries are regressions for defects actually found and reproduced.** That is the
highest-value category of test in this suite, and the reason the list is worth keeping
visible.

---

## Rules

**Tests never touch the production corpus.** `docs/company/` is real company knowledge.
A test that asserted against it would start failing the day someone edited an FAQ
answer — a false alarm, and the fastest way to get a suite disabled. Every test builds
its own fixtures, `test_e2e.py` included: it generates a six-format corpus in
`tmp_path`, with a hand-assembled minimal PDF so extraction is still proven without a
rendering dependency.

This rule was violated and repaired. `test_e2e.py` ingested `Path("docs")` directly,
which was harmless while that directory held demonstration data and became two defects
the moment it held real content — the suite asserted against editable company
documents, *and* it swept `docs/engineering/` into its index, retrieving the knowledge
base. `test_ingestion.py` now asserts the Makefile and CLI corpus roots agree and that
the knowledge base is not reachable from the corpus root.

**Tests never write into the working directory.** Trace persistence defaults to on and
writes to `.osc/`. `conftest` redirects it per test via `tmp_path`, which also stops one
test's traces from being visible to the next and making CLI assertions
order-dependent.

**A test asserts a behaviour, not an implementation.** `test_store_contract` is
parametrised over store implementations; a new store is added to the parametrisation
and is then held to exactly the same behaviour as the existing ones.

**A found defect gets a regression test in the same commit.** The bold rows above are
that policy's output.

---

## Known gaps

Stated plainly, because a testing document that claims completeness is not useful.

1. **No hosted provider has ever been called.** Every hosted adapter is exercised only
   via stubs — including the Anthropic native-citation path, which is the *only*
   verified-citation implementation in the codebase. Its correctness is asserted by
   reading the SDK docs, not by a test.
2. **No load or concurrency test.** Behaviour under parallel requests, and the
   connection-pool bounds, are untested. `./osc eval --concurrency N` is now the
   closest thing to one and was not built for that purpose.
3. **The Gemini adapters hold an unreleasable HTTP client.** Six of eight adapters now
   implement `aclose()`; `genai.Client` exposes no async close in the installed surface
   and is an optional extra, so it is recorded rather than guessed at.
4. **The pgvector integration suite shares the application database.** Isolation is by
   `workspace_id` and it is honoured, but a run against a production DSN would write to
   production. The e2e suite takes a separate database, which is the right pattern; the
   pgvector suite should follow it.
5. **No CI.** `make check`, `make eval-gate` and the suites exist; nothing runs them
   automatically on a pull request.

---

## Related

- [evaluation.md](evaluation.md) — the fourth tier, and why it is not a test
- [provider-architecture.md](provider-architecture.md) — why the doubles are legitimate
