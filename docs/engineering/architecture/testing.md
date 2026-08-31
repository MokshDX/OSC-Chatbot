# Testing

*Four tiers, two commands. Confidence, not coverage.*

---

## Two canonical commands

```bash
make verify   # Does OSC work?    445 tests, lint and types, one report
make eval     # Is OSC any good?  every metric, gated. See evaluation.md
```

**`make verify` runs every tier in a single pytest invocation.** One summary line, one
exit code, one list of failures. Three invocations would mean a failure in the first
can scroll off the screen before the third finishes, which is the exact thing a
canonical command exists to prevent. `-ra` names every skip, so a tier silently
skipping for a missing database is visible rather than green.

The tiers need two different databases — the E2E suite fixes its `chunks` table at the
live embedding model's width and clears its workspace — which is why `OSC_E2E_DSN`
exists separately from `OSC_TEST_DSN`. With one variable between them, only one tier
could be pointed at the right place per run, and one invocation would be impossible.

### The tiers inside it

| Tier | Answers | Needs |
|---|---|---|
| Unit / component | Is the logic correct? | nothing |
| Integration | Does the SQL do what we think? | PostgreSQL |
| End-to-end | Does the whole thing work against real infrastructure? | Ollama and PostgreSQL |
| Evaluation | Is it any *good*? | `make ingest` first — and it is not a test |

Narrower slices, kept because a two-second hermetic loop is worth having and a
forty-second one is not:

```bash
make test              # the hermetic tier alone · ~2s
make check             # lint + types + hermetic — the pre-commit loop
make test-integration  # + the pgvector suite
make test-e2e          # + the end-to-end suite
```

The last row of the tier table is the distinction worth internalising: **`make verify`
asks whether the system is correct, `make eval` asks whether it is good.** A system can
pass every test and answer every question badly.

---

## What makes the fast tier meaningful

412 tests run with no network, no database and no credential — and they still exercise
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
| `test_logging.py` | Log creation, rotation, retention and the disk ceiling; level separation between console and file; **trace-id correlation**; the span bridge on/off; redaction of credentials and payloads; the invoked command and its flags, with the positional tail gated on `capture_payloads`; audit-stream isolation and its independent retention; unwritable directories; **tracebacks surviving the queue**; **token counts not read as credentials** |
| `test_evaluation.py` | Metrics against worked examples including **nDCG separating rankings recall and MRR cannot**; golden-set validation; failed cases excluded from means; retrieval-only omits generation metrics; judge verdict parsing; **the shipped suites load and declare their corpora** |
| `test_conversation.py` | Session creation, isolation, closure and cleanup; history trimmed from the oldest end; LRU eviction; idle expiry; **reading history postpones expiry so a turn cannot outlive itself**; follow-ups reaching generation in both modes; abstentions recorded as turns; a failed stream recording nothing; the `session_context` span |
| `test_conversational_evaluation.py` | Multi-turn dataset validation; per-turn scoring; **the cold control runs only for turns that need one**; lift computed from the pair and honest when negative; context pollution floored at zero; a failed turn costing one turn and still releasing its session |
| `test_gate.py` | Derived tolerances for deterministic and sampled metrics; smaller samples earning wider tolerances; latency reported but never blocking; **all three trade-off guards**; regression attribution down to the turn; counts excluded from gating |
| `test_cli.py` | Every operational command; doctor's pass/warn/fail; trace commands across process boundaries; operator-error reporting; help grouping |
| `test_langchain_integration.py` | Both chunkers (id stability, content preservation, size budget, heading metadata); chat and embedding bridges; the outbound retriever |
| `test_pgvector_integration.py` | Migrations, tsvector, SQL fusion, cascade delete, JSONB, workspace isolation, transaction rollback, inspection SQL |
| `test_fusion_and_grounding.py` | RRF ordering and dedup; citation marker parsing; **prompt-injection containment** |
| `test_api.py` | Health, status, search, chat (both modes), SSE ordering, trace endpoints and their environment gate; per-request correlation ids and the request/response log pair; **session open/close/404, isolation over HTTP, and `session_id` with `history` rejected** |
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
| `test_e2e.py` | Six formats indexed **from a corpus it generates itself**; idempotency; hybrid ranking; a cited answer; abstention; PDF text extraction proven; both modes agreeing; the run fully traced; **the whole session lifecycle against live Ollama and PostgreSQL** — follow-up carrying context, close destroying memory, a new session starting clean, two live sessions not sharing, one turn producing exactly one trace |
| `test_reasoning_models.py` | `<think>` stripping, exhausted-budget error, reasoning markers never becoming citations |
| `test_registry.py` | Registration, override, unknown-provider error |

**Bold entries are regressions for defects actually found and reproduced.** That is the
highest-value category of test in this suite, and the reason the list is worth keeping
visible.

---

## Rules

**Tests never assert against the production corpus.** `docs/company/` is real company
knowledge. A test that asserted against its *content* would start failing the day
someone edited a document — a false alarm, and the fastest way to get a suite disabled.
Every test builds its own fixtures, `test_e2e.py` included: it generates a six-format
corpus in `tmp_path`, with a hand-assembled minimal PDF so extraction is still proven
without a rendering dependency.

**The line is content, not filenames.** Three tests do read repository files, and the
distinction is worth stating because it looks like an exception and is not:

* `test_evaluation.py` and `test_conversational_evaluation.py` load
  `evaluation/suites/*.yaml` and assert they *parse and declare their corpus*. Those
  are engineering artefacts under this repository's control, not company prose, and a
  broken suite file means a broken `make eval` — cheap to catch here rather than forty
  minutes into an evaluation run.
* `test_ingestion.py` reads the configured `corpus.root` and asserts the engineering
  knowledge base is not inside it. It reads a path, never a document.

None of them would break because someone edited a schema document, which is the
property the rule is actually protecting.

This rule was violated and repaired. `test_e2e.py` ingested `Path("docs")` directly,
which was harmless while that directory held demonstration data and became two defects
the moment it held real content — the suite asserted against editable company
documents, *and* it swept `docs/engineering/` into its index, retrieving the knowledge
base. `test_ingestion.py` now asserts that the engineering knowledge base is not
reachable from whatever `corpus.root` resolves to, and that the root has not drifted
up to a bare `docs`.

**Tests never write into the working directory.** Trace *and log* persistence both
default to on and write under `.osc/`. `conftest` redirects both per test via
`tmp_path`, which also stops one test's records from being visible to the next and
making CLI assertions order-dependent. It additionally calls `shutdown_logging()` on
teardown, because the log listener is a background thread and a leaked one writes a
later test's records into a deleted `tmp_path`.

The redirection has to be re-applied wherever a suite purges the environment.
`test_cli.py` deletes every `OSC_*` variable to prove the commands can be retargeted
through configuration alone — which also deletes the isolation `conftest` installed.
It had re-applied `OSC_OBSERVABILITY__TRACE_DIR` and not `OSC_LOGGING__DIRECTORY`, so
every CLI test wrote into the developer's real `.osc/logs`. Caught by watching the
file grow during a run, and the reason the two overrides now sit adjacent with a
comment naming both.

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
5. **No CI.** `make verify`, `make eval-gate` and the suites exist and both exit
   non-zero correctly; nothing runs them automatically on a pull request.
6. **Session memory is tested single-process only.** Isolation, expiry and cleanup are
   asserted within one `InMemorySessionStore`. The failure that matters at scale —
   a client's next turn reaching a replica that never heard of its session — is a
   property of a deployment this suite cannot construct.
7. **One end-to-end assertion is deliberately tolerant.** Whether a live 8B model
   abstains is not deterministic, so the abstention E2E tests assert
   `abstained or not citations` rather than `abstained`. Asserting it strictly made a
   test that passed in isolation and failed in a full run; the strict form of the
   property is covered against stubs in `test_answerer.py`.

---

## Related

- [evaluation.md](evaluation.md) — the fourth tier, and why it is not a test
- [conversation.md](conversation.md) — what the session tests are asserting about
- [provider-architecture.md](provider-architecture.md) — why the doubles are legitimate
