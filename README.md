# OSC Knowledge Assistant

A provider-agnostic retrieval-augmented **conversational** assistant over OSC's
internal documents. Answers are grounded in retrieved source material, carry
citations back to that material, and the assistant declines to answer rather than
guessing when the corpus does not support one. Sessions hold conversation history,
so follow-ups resolve against what was said before.

The chat model, embedding model, reranker, vector store and chunking strategy are
all selected by configuration. Switching any of them is a profile edit.

**The default configuration is fully local**: Qwen3 through Ollama for generation,
`nomic-embed-text` through Ollama for embeddings, and PostgreSQL with pgvector for
storage. No API credential is required and no corpus text leaves the host.

## Quick start

Requires PostgreSQL with the `pgvector` extension, and a running Ollama with
`qwen3:8b` and `nomic-embed-text` pulled.

```bash
make install                       # creates .venv and installs the project

# Point at your database if it is not the one in config/default.yaml.
export OSC_DATABASE__DSN=postgresql://USER@localhost:5432/osc

./osc doctor                       # is everything actually reachable?
./osc ingest                       # indexes `corpus.root`; migrations run on first use
./osc ask "Where is the add-on tier pricing payload stored?"
./osc serve                        # HTTP API + chat UI on http://localhost:8000

make verify                        # does it work?    every test, one report
make eval                          # is it any good?  every metric, gated
```

**The corpus is `docs/company/schema/`** — the authoritative knowledge source, set as
`corpus.root` in the profile and named in exactly one place. The sibling `faq/` and
`scenarios/` directories stay on disk and out of the index, and `docs/engineering/`
holds this repository's own knowledge base and is never indexed. An answer from the
wrong directory retrieves cleanly, grounds correctly and cites accurately, so nothing
downstream catches it — the boundary has to be the directory itself. See
[`knowledge-corpus.md`](docs/engineering/architecture/knowledge-corpus.md) and
[ADR 0011](docs/engineering/decisions/0011-schema-first-knowledge-corpus.md).

`./osc` runs the CLI without activating the virtualenv or typing a path into it;
`make help` lists a target for every command.

## The commands

| | |
|---|---|
| **Running things** | |
| `./osc serve` | HTTP API and chat UI |
| `./osc ingest [dir] [--reindex]` | Index `corpus.root`, or a directory you name |
| `./osc ask "…" [--explain] [--json]` | The whole pipeline, with citations |
| `./osc search "…" [--explain] [--json]` | Retrieval only — the debugging surface |
| **Understanding things** | |
| `./osc doctor` | Is every configured component reachable and consistent? |
| `./osc config` | The fully resolved configuration and where it came from |
| `./osc providers` | Every registered provider, marking the active ones |
| `./osc status` | What is indexed: counts, chunk sizes, formats |
| `./osc eval [--retrieval-only]` | **Every quality metric**, gated against the baseline |
| **Looking at data** | |
| `./osc documents [search]` | Indexed documents and their chunk counts |
| `./osc document <id\|path>` | One document's record and how it chunked |
| `./osc chunk <chunk-id>` | One chunk in full — the exact text the model saw |
| `./osc logs [--audit] [-f]` | Where the persistent logs are, their size ceiling, and the last lines |
| `./osc traces` | Recent traces — filter with `--failed`, `--name`, `--slower-than` |
| `./osc trace [id]` | Expand one trace, or the most recent, into a waterfall |
| `./osc version` | Installed version and the versions that shape behaviour |

Every inspection command takes `--json`, so they compose into scripts. `--help`
groups them by purpose rather than listing sixteen commands flat.

## How it fits together

```
files ─▶ parse ─▶ chunk ─▶ embed ─▶ vector store
                                         │
question ─▶ rewrite ─▶ search ─▶ rerank ─▶ generate ─▶ answer + citations
```

| Module | Responsibility |
|---|---|
| `protocols.py` | The five seams: chat, embeddings, vector store, reranker, chunker — plus optional `StoreInspector` |
| `types.py` | Domain types. The only vocabulary shared between modules |
| `registries.py` | Name → implementation, so providers are additions rather than edits |
| `providers/` | Every provider adapter. Nothing else imports these |
| `integrations/` | The reverse direction: OSC exposed to other ecosystems |
| `observability/` | Execution tracing and its rendering |
| `ingestion/` | Connectors, text extraction, and the idempotent chunk/embed/store pipeline |
| `retrieval/` | Query rewriting, hybrid search, reranking |
| `generation/` | Prompts, citation policy, abstention |
| `container.py` | Composition root: the only module that wires providers together |
| `cli/` | The operator interface: running, diagnosing, inspecting |
| `api/` | HTTP, SSE, and the bundled chat client. Thin: validate, delegate, encode |

Business logic depends only on `protocols` and `types`. It never imports a
provider, which is what makes providers swappable.

## Observability

Every significant stage of ingestion and question answering is a timed span, and
one request produces one trace. Add `--explain` to any command:

```
$ ./osc ask "What is the expense approval threshold?" --explain

trace b189dd3b8cef4044  answer  9567ms  ok
──────────────────────────────────────────────────────────────
answer           ████████████████████████████   9566.9ms
                   mode=buffered  model=qwen3:8b  turns=0
  retrieve       █                               318.9ms
                   strategy=hybrid  candidates_requested=30  top_k=5
    embed_query  █                               290.8ms
                   model=nomic-embed-text  dimensions=768
    search       █                                27.9ms
                   strategy=hybrid  hits=20  top_score=0.03279
    threshold    █                                 0.0ms
                   min_score=0  kept=20  discarded=0
    rerank       █                                 0.0ms
                   reranker=noop  input=20  selected=5
  generate       ███████████████████████████    9247.7ms
                   model=qwen3:8b  sources=5  input_tokens=1354  output_tokens=66
  finalise                                  █      0.0ms
                   citations=1  sources_used=1  sources_offered=5
```

That output answers, without adding a log line or attaching a debugger: where the
time went (97% in generation), what each stage did to the data, how many of the
retrieved passages the model actually cited, and — when something raises — which
stage failed and with what.

A few things worth knowing:

- **Every answer carries its `trace_id`**, in the CLI footer, the JSON body and the
  SSE `complete` event. "This answer is wrong" becomes answerable hours later
  without reproducing the request.
- **An abstention is visible by shape.** A trace with a `retrieve` and no
  `generate` means the model was never called, which is different from a model
  that answered badly.
- **Streaming records time to first token separately** from total duration, because
  for a streaming client that is the number that describes the experience.
- **Traces outlive the process that made them.** They are appended to a bounded
  JSONL log under `.osc/`, so `./osc traces` and `./osc trace <id>` work after a
  one-shot command has exited. This matters because re-running with `--explain`
  does *not* get you the trace you want — a generation is not deterministic, so you
  get a different one, at the cost of another model call.
- **A failed command explains itself without being asked.** The trace prints before
  the error, and an `AssistantError` — an unknown provider, a missing credential, an
  unreachable database — is reported as a message rather than a traceback. Anything
  else keeps its traceback, because for a bug the frames are the point.
- **`/api/traces` and `/api/traces/{id}`** serve the same payload from a running
  service, and `./osc traces --url` renders it. They are registered only when
  `environment` is `development` — traces carry question text and chunk ids, and no
  endpoint is authenticated yet.
- **`observability.capture_text: false`** keeps every timing, count and stage while
  recording only the *length* of any text. For a corpus where a trace must not
  contain content.

```
$ ./osc traces --failed
9f31c0aa4e7b21d5  14:22:07  answer         2140.3ms   6 spans  FAILED

$ ./osc trace 9f31c0
trace 9f31c0aa4e7b21d5  answer  2140ms  FAILED
...
  generate       ███████████████████            2038.1ms ✗
                   error: ProviderError: ollama stream failed: connection reset
```

Structured JSON logging is unchanged, and each completed trace is additionally
emitted as one log record — a span tree is only meaningful whole.

### Running the server

`./osc serve` splits its output by audience. A human summary — URLs, active
components, and any warning worth knowing before the first request — goes to
**stderr**; the structured JSON log continues to **stdout**. So
`./osc serve > run.log` still produces a clean parseable log while the terminal
stays readable.

```
  OSC Knowledge Assistant
  API   http://127.0.0.1:8000/api
  UI    http://127.0.0.1:8000/
  docs  http://127.0.0.1:8000/docs

  environment  development   workspace default
  llm          ollama/qwen3:8b
  embeddings   ollama/nomic-embed-text
  store        pgvector   retrieval hybrid   chunker recursive
  note         the index is empty — every question will abstain. Run `./osc ingest`.
```

That last line is the one that earns its place: a service which starts perfectly and
abstains from every question is indistinguishable from a broken model unless
somebody thinks to look.

## Ingestion

Drop files anywhere under the configured `corpus.root` and run `./osc ingest`.

| Format | Extensions | Extraction |
|---|---|---|
| Markdown / text | `.md` `.markdown` `.txt` `.rst` | Read directly, byte-for-byte |
| HTML | `.html` `.htm` | Standard library; `<script>` and `<style>` discarded, `<title>` used |
| PDF | `.pdf` | `pypdf`, page by page, page count retained |
| Word | `.docx` | `python-docx`, including table cells |
| Excel | `.xlsx` | `openpyxl`, one block per sheet, cells tab-joined so a row survives as one line |

PDF, Word and Excel need the `documents` extra. Adding a format is a function plus one
dict entry in `ingestion/parsers.py`; nothing else changes.

**Idempotent by content hash.** Re-running over an unchanged corpus makes zero
embedding calls. An edited file re-indexes alone; a deleted file is pruned along
with its chunks.

**`--reindex` when the chunker changes.** The content hash covers the document
text and nothing else, so changing `chunking.strategy`, `chunk_size` or the
embedding model leaves every stored chunk stale while every hash still matches. An
ordinary sync would report `skipped` for the whole corpus and quietly keep the old
chunks. `./osc ingest --reindex` forces the work.

**One bad file cannot break a sync.** A corrupt or password-protected document is
reported and skipped, the rest of the corpus still indexes, and the command exits
non-zero. Crucially it is *not* pruned — a file that failed to parse is still
present at the source, so its indexed copy is kept rather than destroyed.

```
processed=7 indexed=0 skipped=6 deleted=0 chunks=0 unreadable=1 in 0.1s
  failed: file:///.../corrupt-report.pdf: Could not read PDF: Stream has ended unexpectedly
```

Scanned PDFs are rejected with an explicit message rather than indexed as empty
documents — there is no OCR in the pipeline.

## Configuration

Layered, highest precedence first: environment variables, `.env`, then the YAML
profile at `config/default.yaml` (override with `OSC_PROFILE`).

```yaml
llm:
  provider: ollama
  model: qwen3:8b

embeddings:
  provider: ollama        # chosen independently of the chat model
  model: nomic-embed-text

vector_store:
  provider: pgvector
```

Any value is also addressable from the environment, nesting with a double
underscore:

```bash
OSC_LLM__PROVIDER=groq OSC_LLM__MODEL=llama-3.3-70b-versatile ./osc ask "..."
```

`./osc config` prints what was actually resolved, alongside the `OSC_*` variables
that participated — the fast answer to "production is using the wrong model".
Credentials and DSNs are redacted unless `--show-secrets` is passed.

### Running an experiment

Copy a profile, change one thing, point `OSC_PROFILE` at it:

```bash
OSC_PROFILE=config/experiments/hosted-anthropic.yaml ./osc ask "..."
```

`hosted-anthropic.yaml` moves every component to a hosted vendor and is the only
configuration with provider-verified citations; `local-only.yaml` swaps Ollama
embeddings for in-process sentence-transformers and enables the cross-encoder
reranker; `groq-voyage.yaml` shares no vendor with either; `langchain-bridge.yaml`
reaches a provider through LangChain and uses heading-aware chunking. None
requires a code change.

Changing the embedding model changes the vector width, which is fixed in the DDL
when the `chunks` table is created. A different model needs its own database and a
full re-index; the store refuses to start on a mismatch rather than silently
comparing incompatible vectors.

### Working with a reasoning model

Qwen3 thinks before answering, spending completion tokens that never reach the
user. The default profile disables it (`extra_body.reasoning_effort: none`) because
Ollama loads the model with a 4096-token context, and reasoning competes with the
answer for that budget. `chunking.chunk_size`, `retrieval.top_k` and
`generation.max_tokens` are sized to fit the same window.

If you re-enable reasoning, raise `generation.max_tokens` with it. An exhausted
budget produces no answer text at all, and the adapter reports that explicitly
rather than letting it become a silent "I could not find anything".

## Providers

| Kind | Available |
|---|---|
| Chat | `ollama`, `anthropic`, `openai`, `gemini`, `gemini_openai`, `groq`, `openrouter`, `together`, `huggingface`, `vllm`, `lmstudio`, `local`, `langchain` |
| Embeddings | `ollama`, `openai`, `voyage`, `gemini`, `local` (sentence-transformers), `lmstudio`, `vllm`, `together`, `huggingface`, `langchain` |
| Reranker | `noop`, `cross_encoder` |
| Vector store | `pgvector`, `memory` |
| Chunker | `recursive`, `fixed`, `langchain_recursive`, `markdown` |

Anything speaking the OpenAI chat/embeddings wire format is covered by the
`openai_compatible` adapters; point `options.base_url` at it. Anything else that
LangChain has an integration for is covered by the `langchain` provider.

### Adding a provider

Create a module that registers a factory, and add it to its package `__init__`.
No existing file changes.

```python
# providers/llm/my_provider.py
@llm_registry.register("my_provider")
def _build(config: ComponentConfig) -> ChatModel:
    return MyChatModel(config.model, MyOptions.model_validate(config.options))
```

The class needs the shape of `protocols.ChatModel` — no base class to inherit,
nothing to register elsewhere.

## LangChain

LangChain is used where it earns its place and nowhere else. The rule applied
throughout: **adopt LangChain for undifferentiated work, keep OSC's own code where
OSC's design is better.**

**Adopted — text splitting.** `langchain-text-splitters` supplies the
`langchain_recursive` and `markdown` chunkers. Splitting text on the coarsest
boundary that fits is a genuinely generic problem, OSC's own implementation had
known rough edges (a chunk can exceed its budget by up to the overlap), and
heading-aware splitting would otherwise have to be written here. `markdown` splits
on structure first and packs to size second, recording the heading path on each
chunk's metadata.

**Adopted — provider reach.** The `langchain` chat and embedding providers wrap any
LangChain `BaseChatModel` or `Embeddings` behind OSC's protocols. This makes
Bedrock, Vertex, Azure, Cohere, Mistral, Fireworks and the rest reachable by
configuration rather than by writing an adapter each time:

```yaml
llm:
  provider: langchain
  model: mistral-large-latest
  options:
    class_path: langchain_mistralai.ChatMistralAI
    init: {timeout: 60}
```

The class is named by import path rather than resolved by `init_chat_model`, which
would pull the `langchain` meta-package and LangGraph in to save one line of
configuration.

**Adopted — outbound interoperability.** `integrations/langchain.py` presents OSC's
retrieval pipeline as a LangChain `BaseRetriever`, so a team building on LangChain
or LangGraph uses OSC's index, ranking and tuning rather than standing up a
parallel one that drifts.

**Not adopted — everything else.** Retrieval, the vector store, prompting, the
answer loop and tracing stay OSC's own, each for a specific reason:

- **Retrieval and the store.** The pgvector store fuses lexical and vector search
  with RRF *in SQL*, in one round trip. LangChain's PGVector does not, and
  replacing it would trade a measurable capability for a generic interface.
- **The answer loop.** Abstention, the citation policy and the streaming contract
  are the parts most specific to OSC's requirements and most in need of direct
  reading. LCEL would put an uncontrolled layer on exactly that path.
- **Prompts.** System prompts are frozen module constants precisely so the prefix
  stays byte-identical. A template engine has nothing to add to a constant.
- **Tracing.** LangChain callbacks observe LangChain runs, and most of this
  pipeline is not one. See below.

`langchain-core` and `langchain-text-splitters` are core dependencies: both are
pure Python with no vendor SDK behind them. Every LangChain *integration* package
stays an install-time choice, named by the operator in `options.class_path`.

## Design decisions worth knowing

**One datastore.** PostgreSQL holds chunk text, embeddings, the lexical index and
document metadata. A chunk and its vector cannot drift apart, there is one backup
to take, and hybrid retrieval is one round trip. A dedicated vector database earns
its place when vector search p95 degrades or the corpus passes a few million
chunks — the `VectorStore` protocol is where that swap happens.

**Hybrid retrieval by default.** Internal corpora are full of acronyms, product
names and error strings that semantic search alone handles badly, and paraphrase
that keyword search alone handles badly. Postgres provides both indexes, so the
marginal cost is one query and a fusion step. Ranking uses Reciprocal Rank Fusion,
implemented identically in SQL and in `fusion.py` so both stores agree.

**`min_score` applies before reranking.** First-stage scores are on a known scale;
a cross-encoder logit is unbounded and often negative for a relevant passage.
Thresholding reranker output would have emptied the result set the moment a
reranker was enabled.

**Native citations where available.** The Anthropic adapter passes sources as
structured documents and receives, per span of the answer, the source text that
supports it. Every other provider — including the local default and the LangChain
bridge — falls back to `[n]` markers parsed out of the answer. Both produce the
same `Citation` shape, so nothing downstream branches on it, but the first
verifies a citation and the second only asserts one.

**Abstention is architectural.** With no retrieval hits the model is never called.
With no citations the answer is treated as ungrounded. In streaming mode the final
`complete` event is authoritative: if it reports an abstention, the client discards
the text it already rendered.

**Frozen prompts.** System prompts are module constants with no interpolation.
Anything dynamic would break prefix caching for every request and make evaluation
results unattributable.

**Tracing is OSC's own, not OpenTelemetry and not LangChain callbacks.** OTel is
the right answer once traces leave the process, and `observability/trace.py` is
deliberately shaped like it — spans, parent ids, attributes — so that day is an
exporter rather than a rewrite. Today it would add a large dependency and a
collector to run for a capability that fits in one file. LangChain callbacks were
rejected for a stronger reason: they observe only LangChain runs, so a tracer built
on them would be blind to chunking, pgvector's SQL fusion and the abstention
decision — exactly the parts most in need of debugging.

**Inspection is a separate protocol.** `StoreInspector` is not part of
`VectorStore`, because every method on `VectorStore` is one a new store must
implement to be usable at all, and a hosted vector database exposing no aggregate
API should still be a perfectly good `VectorStore`. Tooling probes for the
inspection interface and reports its absence rather than failing. Both built-in
stores implement it.

## Interfaces

- **CLI** — the commands listed above. `make help` for the shortcuts.
- **HTTP** — `GET /api/health` (liveness plus the active component set),
  `GET /api/status` (what is indexed), `POST /api/search` (retrieval only),
  `POST /api/chat` (SSE by default), `POST /api/sessions` and
  `DELETE /api/sessions/{id}` (open and destroy a conversation). Both `POST`
  query endpoints accept `explain: true` to return the execution trace inline.
  `GET /api/traces` and `/api/traces/{id}` in development only.
- **UI** — a single static page at `/`. Deliberately one file with no build step;
  it consumes the same public API as any other client and is expected to be
  replaced by a richer one.
- **As a library** — `osc_assistant.integrations.langchain.OSCRetriever` makes the
  retrieval pipeline a LangChain retriever.

## Testing

**There are two canonical commands, and they answer two different questions.**

```bash
make verify   # Does OSC work?    every test, lint and types, in one report
make eval     # Is OSC any good?  every metric, gated against the baseline
```

A system can pass every test while answering every question badly, which is why
these are separate and why neither substitutes for the other.

`make verify` runs the **whole** suite — unit, pgvector integration and end-to-end —
in a *single* pytest invocation, so there is one summary line, one exit code and one
list of failures. Three invocations would mean a failure in the first can scroll off
the screen before the third finishes, which is the exact thing a canonical command
exists to prevent. `-ra` names every skip, so a suite silently skipping for a
missing database is visible rather than green.

It needs a live Ollama and PostgreSQL. Without them the dependent suites skip and
say so.

Narrower slices, kept because a two-second hermetic loop is worth having:

```bash
make test              # fast hermetic subset: no network, no database, no credentials
make check             # lint + typecheck + the hermetic subset — the pre-commit loop
make test-integration  # + the pgvector suite against a real database
make test-e2e          # + the end-to-end suite against live Ollama and PostgreSQL
```

The end-to-end suite needs its **own** database (`OSC_E2E_DSN`): the `chunks` table
fixes its vector width at creation, and the suite clears its workspace when it
finishes. That separate variable is what lets `make verify` address both databases
in one process.

The suite runs the real pipelines against in-process implementations of the
provider protocols. The API and CLI tests register those doubles through the
ordinary registry, which is the same path a new provider takes — so "the whole
stack can be retargeted by configuration alone" is asserted, not assumed.

`make test-integration` needs `OSC_TEST_DIMENSIONS` to match the width the target
database was migrated with (768 for `nomic-embed-text`), because the `chunks` table
fixes its vector width at creation.

## Logging

Tracing explains one execution. Logging records everything that happened, survives
the process, and is what you grep next week. Both are on by default and joined by
`trace_id` — any log line expands into a full waterfall.

```
.osc/logs/
├── osc.log      operational — rotates at 10 MB, 5 kept (~60 MB ceiling)
└── audit.log    one record per answered question, 20 kept
```

```bash
./osc logs                                    # location, sizes, ceiling, last lines
tail -f .osc/logs/osc.log | jq .              # live
OSC_LOG_LEVEL=TRACE ./osc ask "..."           # one record per pipeline stage
jq 'select(.event == "cli.command")' .osc/logs/osc.log   # what has anyone run here
```

At `TRACE` every stage of the pipeline logs itself, because the logger subscribes to
the same spans the tracer collects — no pipeline contains a log statement for this:

```
TRACE embed_query     768.35ms  trace=505cd599
TRACE search           52.03ms  trace=505cd599
TRACE rerank            0.01ms  trace=505cd599
TRACE retrieve        821.06ms  trace=505cd599
```

**Credentials are redacted unconditionally**, and corpus text is reduced to a
character count unless `logging.capture_payloads` is enabled. Disk is bounded by
construction: the oldest rotated file is deleted, not archived.

Full detail: [`docs/engineering/architecture/logging.md`](docs/engineering/architecture/logging.md).

## Conversations

OSC is multi-turn. A session is opened by the client, the server holds the history,
and closing it destroys the memory.

```bash
SID=$(curl -sX POST localhost:8000/api/sessions | jq -r .session_id)
curl -sX POST localhost:8000/api/chat -H 'content-type: application/json' \
  -d "{\"question\":\"Where is the add-on tier pricing payload stored?\",
       \"session_id\":\"$SID\",\"stream\":false}" | jq -r .text
# "…the `oscp.adt` metafield on a ProductVariant… [1]"

curl -sX POST localhost:8000/api/chat -H 'content-type: application/json' \
  -d "{\"question\":\"What type is it?\",\"session_id\":\"$SID\",\"stream\":false}" | jq -r .text
# resolves "it" against the previous turn

curl -sX DELETE localhost:8000/api/sessions/$SID    # memory destroyed
```

Two ways to supply context, **mutually exclusive on one request**: `session_id`
(server-held, right for a chat UI) or `history` (client-held, right for a stateless
integration). Supplying both is a `422` rather than a silent choice about which to
believe.

Memory is **ephemeral by design** — process-local, bounded by message count, session
count and idle TTL, destroyed on close and on restart. The audit stream already holds
one durable record per answered question, which is what a compliance question actually
wants, without keeping user text in a second place with its own retention story.

Conversation history reaches retrieval only through query rewriting, which is why
`retrieval.rewrite_queries` is on by default — with it off, the measured contribution
of memory to retrieval was exactly zero. See [Evaluation](#evaluation).

Full detail: [`docs/engineering/architecture/conversation.md`](docs/engineering/architecture/conversation.md).

## Evaluation

Quality is measured, not asserted. Two suites, both scored against
`docs/company/schema/`:

| Suite | Cases | What it measures |
|---|---|---|
| `evaluation/suites/schema.yaml` | 55 + 6 abstention | Single-turn retrieval, answer, citation, abstention |
| `evaluation/suites/conversational.yaml` | 18 sessions, 46 turns | Follow-ups, context switching, isolation |

```bash
make eval              # BOTH suites, gated against the committed baselines
make eval-retrieval    # retrieval only, ungated: fast, free, no model calls
make eval-gate         # what CI runs: retrieval only, exits non-zero on a regression
```

### Measured baseline

Default local profile — Qwen3-8B via Ollama, `nomic-embed-text`, pgvector,
`markdown` chunking, `top_k=5`. Corpus of 11 documents / 80 chunks.

| Retrieval | | Answer & citations | | Conversation | |
|---|---|---|---|---|---|
| `recall@5` | **0.982** | `groundedness` | **1.000** | `follow_up_resolution` | **0.941** |
| `hit_rate@5` | **0.982** | `citation_coverage` | **1.000** | ↳ cold control | 0.765 |
| `ndcg@5` | **0.918** | `citation_precision` | 0.875 | ↳ **lift** | **+0.177** |
| `mrr` | **0.897** | `fact_match` | 0.782 | `context_pollution` | **0.000** |
| `precision@5` | 0.200 ᵃ | `abstention_accuracy` | 0.667 ᵇ | `session_isolation` | **1.000** |

ᵃ At the structural maximum — most questions have one relevant document, so with
`k=5` no ranking can exceed 0.2. ᵇ The weakest number here: two of six unanswerable
questions still got an answer.

**Every conversational number is reported with its control.** Each
context-dependent turn is run twice — once in the session, once cold — because a
follow-up that gets answered proves nothing on its own; it may have retrieved the
right document by keyword luck. The *lift* is the evidence. It measured exactly
**0.000** before query rewriting was enabled, which is what turned "does memory
work?" from a suspicion into a number.

### Comparing two configurations

```bash
./osc eval --suite schema --retrieval-only --no-gate -o before.json
OSC_CHUNKING__STRATEGY=markdown ./osc ingest --reindex
./osc eval --suite schema --retrieval-only --baseline before.json
```

The gate derives each metric's tolerance from the run itself — one case for
deterministic retrieval metrics, two standard errors for sampled generation metrics
— rather than comparing against a threshold someone typed. It reports the previous
and current value, the tolerance and where it came from, the cases that changed from
passing to failing, and the categories they span. It also blocks **trade-offs**: a
precision win bought with a recall loss is not a win.

`--reindex` after a chunker change. Chunk ids derive from chunk boundaries while
document hashes do not, so an ordinary sync reports `skipped` and silently measures
the old index under the new label.

Add `--judge` for LLM-as-judge faithfulness. It is opt-in and never gates, because a
gate that can change its mind between two runs of the same commit is not a gate.

Full detail: [`docs/engineering/architecture/evaluation.md`](docs/engineering/architecture/evaluation.md)
and [`evaluation-methodology.md`](docs/engineering/architecture/evaluation-methodology.md),
which documents every metric's definition, limitations, baseline and regression
criteria.

## Engineering knowledge base

[`docs/engineering/`](docs/engineering/README.md) explains **why** the system is built
the way it is — architecture, technologies and Architecture Decision Records, with
diagrams and references. Start with
[`architecture/overview.md`](docs/engineering/architecture/overview.md).

## Not yet built

Authentication (OIDC), per-document access control, rate limiting, **durable**
conversation persistence, and connectors beyond the filesystem. The service exposes
no write endpoint — ingestion is a CLI operation — and must sit behind the corporate
identity proxy until OIDC lands. See `PROJECT_STATUS.md` for the full picture and the
recommended order of work.

Conversation memory exists and works, but it lives in the answering process
(see [Conversations](#conversations)): it does not survive a restart, and behind more
than one replica a client's next turn may reach a process that never heard of its
session. Sticky sessions or a shared store is a prerequisite for horizontal scaling.
