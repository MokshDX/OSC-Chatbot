# OSC Knowledge Assistant

A provider-agnostic retrieval-augmented question answering service over OSC's
internal documents. Answers are grounded in retrieved source material, carry
citations back to that material, and the assistant declines to answer rather than
guessing when the corpus does not support one.

The chat model, embedding model, reranker, vector store and chunking strategy are
all selected by configuration. Switching any of them is a profile edit.

**The default configuration is fully local**: Qwen3 through Ollama for generation,
`nomic-embed-text` through Ollama for embeddings, and PostgreSQL with pgvector for
storage. No API credential is required and no corpus text leaves the host.

## Quick start

Requires PostgreSQL with the `pgvector` extension, and a running Ollama with
`qwen3:8b` and `nomic-embed-text` pulled.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,openai,documents]"

# Point at your database if it is not the one in config/default.yaml.
export OSC_DATABASE__DSN=postgresql://USER@localhost:5432/osc

osc-assistant ingest ./docs        # migrations run automatically on first use
osc-assistant ask "How many days of annual leave do employees get?"
osc-assistant serve                # HTTP API + chat UI on http://localhost:8000
```

`osc-assistant providers` lists everything currently registered.

## How it fits together

```
files ─▶ parse ─▶ chunk ─▶ embed ─▶ vector store
                                         │
question ─▶ rewrite ─▶ search ─▶ rerank ─▶ generate ─▶ answer + citations
```

| Module | Responsibility |
|---|---|
| `protocols.py` | The five seams: chat, embeddings, vector store, reranker, chunker |
| `types.py` | Domain types. The only vocabulary shared between modules |
| `registries.py` | Name → implementation, so providers are additions rather than edits |
| `providers/` | Every provider adapter. Nothing else imports these |
| `ingestion/` | Connectors, text extraction, and the idempotent chunk/embed/store pipeline |
| `retrieval/` | Query rewriting, hybrid search, reranking |
| `generation/` | Prompts, citation policy, abstention |
| `container.py` | Composition root: the only module that wires providers together |
| `api/` | HTTP, SSE, and the bundled chat client. Thin: validate, delegate, encode |

Business logic depends only on `protocols` and `types`. It never imports a
provider, which is what makes providers swappable.

## Ingestion

Drop files anywhere under `./docs` and run `osc-assistant ingest ./docs`.

| Format | Extensions | Extraction |
|---|---|---|
| Markdown / text | `.md` `.markdown` `.txt` `.rst` | Read directly, byte-for-byte |
| HTML | `.html` `.htm` | Standard library; `<script>` and `<style>` discarded, `<title>` used |
| PDF | `.pdf` | `pypdf`, page by page, page count retained |
| Word | `.docx` | `python-docx`, including table cells |

PDF and Word need the `documents` extra. Adding a format is a function plus one
dict entry in `ingestion/parsers.py`; nothing else changes.

**Idempotent by content hash.** Re-running over an unchanged corpus makes zero
embedding calls. An edited file re-indexes alone; a deleted file is pruned along
with its chunks.

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
OSC_LLM__PROVIDER=groq OSC_LLM__MODEL=llama-3.3-70b-versatile osc-assistant ask "..."
```

### Running an experiment

Copy a profile, change one thing, point `OSC_PROFILE` at it:

```bash
OSC_PROFILE=config/experiments/hosted-anthropic.yaml osc-assistant ask "..."
```

`hosted-anthropic.yaml` moves every component to a hosted vendor and is the only
configuration with provider-verified citations; `local-only.yaml` swaps Ollama
embeddings for in-process sentence-transformers and enables the cross-encoder
reranker; `groq-voyage.yaml` shares no vendor with either. None requires a code
change.

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
| Chat | `ollama`, `anthropic`, `openai`, `gemini`, `gemini_openai`, `groq`, `openrouter`, `together`, `huggingface`, `vllm`, `lmstudio`, `local` |
| Embeddings | `ollama`, `openai`, `voyage`, `gemini`, `local` (sentence-transformers), `lmstudio`, `vllm`, `together`, `huggingface` |
| Reranker | `noop`, `cross_encoder` |
| Vector store | `pgvector`, `memory` |
| Chunker | `recursive`, `fixed` |

Anything speaking the OpenAI chat/embeddings wire format is covered by the
`openai_compatible` adapters; point `options.base_url` at it.

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

## Design decisions worth knowing

**No LLM framework.** LangChain and LlamaIndex were evaluated and not adopted. The
seams this system needs are five protocols totalling about 120 lines; a framework
would add its own document and retriever abstractions on top of ours, a large
transitive dependency tree, and an uncontrolled layer on the exact path we most
need to trace. Provider SDKs are used directly, each as an optional extra.

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
supports it. Every other provider — including the local default — falls back to
`[n]` markers parsed out of the answer. Both produce the same `Citation` shape, so
nothing downstream branches on it, but the first verifies a citation and the second
only asserts one.

**Abstention is architectural.** With no retrieval hits the model is never called.
With no citations the answer is treated as ungrounded. In streaming mode the final
`complete` event is authoritative: if it reports an abstention, the client discards
the text it already rendered.

**Frozen prompts.** System prompts are module constants with no interpolation.
Anything dynamic would break prefix caching for every request and make evaluation
results unattributable.

## Interfaces

- **CLI** — `serve`, `ingest`, `ask`, `search`, `providers`.
- **HTTP** — `GET /api/health` (reports the active component set), `POST /api/search`
  (retrieval only, the debugging surface), `POST /api/chat` (SSE by default).
- **UI** — a single static page at `/`. Deliberately one file with no build step;
  it consumes the same public API as any other client and is expected to be
  replaced by a richer one.

## Testing

```bash
make test              # 119 tests, no network, no database, no credentials
make test-integration  # adds the pgvector suite against a real PostgreSQL
make check             # lint + typecheck + test
```

The suite runs the real pipelines against in-process implementations of the
provider protocols. The API tests register those doubles through the ordinary
registry, which is the same path a new provider takes.

`make test-integration` needs `OSC_TEST_DIMENSIONS` to match the width the target
database was migrated with (768 for `nomic-embed-text`), because the `chunks` table
fixes its vector width at creation.

## Not yet built

Authentication (OIDC), per-document access control, rate limiting, conversation
persistence, the evaluation harness, and connectors beyond the filesystem. The
service exposes no write endpoint — ingestion is a CLI operation — and must sit
behind the corporate identity proxy until OIDC lands. See `PROJECT_STATUS.md` for
the full picture and the recommended order of work.
