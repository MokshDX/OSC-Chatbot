# OSC Knowledge Assistant

A provider-agnostic retrieval-augmented question answering service over OSC's
internal documents. Answers are grounded in retrieved source material, carry
citations back to that material, and the assistant declines to answer rather than
guessing when the corpus does not support one.

The chat model, embedding model, reranker, vector store and chunking strategy are
all selected by configuration. Switching any of them is a profile edit.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,anthropic,openai]"
cp .env.example .env            # then fill in the keys you actually use

createdb osc_assistant          # requires the pgvector extension to be available
osc-assistant ingest ./docs     # migrations run automatically on first use
osc-assistant ask "How many vacation days do employees get?"
osc-assistant serve
```

`osc-assistant providers` lists everything currently registered.

## How it fits together

```
connectors ─▶ chunk ─▶ embed ─▶ vector store
                                     │
question ─▶ rewrite ─▶ search ─▶ rerank ─▶ generate ─▶ answer + citations
```

| Module | Responsibility |
|---|---|
| `protocols.py` | The five seams: chat, embeddings, vector store, reranker, chunker |
| `types.py` | Domain types. The only vocabulary shared between modules |
| `registries.py` | Name → implementation, so providers are additions rather than edits |
| `providers/` | Every provider adapter. Nothing else imports these |
| `ingestion/` | Connectors and the idempotent chunk/embed/store pipeline |
| `retrieval/` | Query rewriting, hybrid search, reranking |
| `generation/` | Prompts, citation policy, abstention |
| `container.py` | Composition root: the only module that wires providers together |
| `api/` | HTTP and SSE. Thin: validate, delegate, encode |

Business logic depends only on `protocols` and `types`. It never imports a
provider, which is what makes providers swappable.

## Configuration

Layered, highest precedence first: environment variables, `.env`, then the YAML
profile at `config/default.yaml` (override with `OSC_PROFILE`).

```yaml
llm:
  provider: anthropic
  model: claude-opus-5

embeddings:
  provider: voyage        # chosen independently of the chat model
  model: voyage-3-large

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
OSC_PROFILE=config/experiments/local-only.yaml osc-assistant search "expense limit"
```

`config/experiments/local-only.yaml` runs generation, embeddings and reranking
entirely on the local machine; `groq-voyage.yaml` shares no vendor with the
default. Neither requires a code change.

## Providers

| Kind | Available |
|---|---|
| Chat | `anthropic`, `openai`, `gemini`, `gemini_openai`, `groq`, `openrouter`, `together`, `huggingface`, `ollama`, `vllm`, `lmstudio`, `local` |
| Embeddings | `openai`, `voyage`, `gemini`, `local` (sentence-transformers), `ollama`, `lmstudio`, `vllm`, `together`, `huggingface` |
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
marginal cost is one query and a fusion step.

**Native citations where available.** The Anthropic adapter passes sources as
structured documents and receives, per span of the answer, the source text that
supports it. Other providers fall back to `[n]` markers parsed out of the answer.
Both produce the same `Citation` shape, so nothing downstream branches on it — but
the first verifies a citation and the second only asserts one.

**Abstention is architectural.** With no retrieval hits the model is never called.
With no citations the answer is treated as ungrounded. In streaming mode the final
`complete` event is authoritative: if it reports an abstention, the client discards
the text it already rendered.

**Frozen prompts.** System prompts are module constants with no interpolation.
Anything dynamic would break prefix caching for every request and make evaluation
results unattributable.

## Testing

```bash
pytest          # no network, no database, no API credentials
ruff check .
mypy src
```

The suite runs the real pipelines against in-process implementations of the
provider protocols. The API tests register those doubles through the ordinary
registry, which is the same path a new provider takes.

## Not yet built

Authentication (OIDC), per-document access control, conversation persistence, the
evaluation harness and connectors beyond the filesystem. The service exposes no
write endpoint — ingestion is a CLI operation — and must sit behind the corporate
identity proxy until OIDC lands.
