# Ollama

---

## What it is

A local runtime for open-weight language models. It pulls quantised models, serves them
over HTTP, and — critically for this project — exposes an **OpenAI-compatible API**
alongside its native one.

https://ollama.com/ · https://github.com/ollama/ollama

---

## Why OSC uses it

**No corpus text leaves the host.** The default profile is fully local: questions,
retrieved passages and answers never cross the network. For an internal knowledge
assistant over company documents, that eliminates an entire category of review before
the project can be demonstrated at all.

**No credential.** A new engineer runs `make install`, `make ingest`, `./osc ask "..."`
and has a working system. No key to request, no billing account, no rate limit. That
matters more than it sounds: the friction of obtaining a credential is where side
projects die.

**Zero marginal cost per run.** The evaluation harness makes 86 model calls per full
run. At a hosted provider's rates that is a real budget line, and a budget line is a
reason not to run it. Free evaluation is evaluation that actually happens.

**It is reached through the OpenAI-compatible adapter**, not a bespoke one. Ollama is
registered as `ollama` but shares the twelve-name `openai_compatible` family, so the
same adapter serves Groq, Together, Fireworks, vLLM and a local llama.cpp server.

---

## Where it is used

`config/default.yaml`, as three of the four model seams:

```yaml
llm:        {provider: ollama, model: qwen3:8b}
fast_llm:   {provider: ollama, model: qwen3:8b}   # rewriting, and the eval judge
embeddings: {provider: ollama, model: nomic-embed-text}
```

Reached via `providers/llm/openai_compatible.py` and
`providers/embeddings/openai_compatible.py`.

---

## The two models

### `qwen3:8b` — generation

A hybrid reasoning model: it thinks before answering by default.

**Reasoning is disabled** (`reasoning_effort: none`), for two measured reasons recorded
in `config/default.yaml`:

- Measured on this deployment: **138 completion tokens with thinking versus 3 without**,
  for the same reply.
- Ollama loads this model with a **4096-token context**. Thinking competes with the
  answer for that budget, and an exhausted budget returns *empty content* rather than a
  short answer.

Grounded question answering over retrieved passages is mostly extractive, so the
latency is not repaid. Setting it to `"low"` or `"medium"` requires raising
`generation.max_tokens` to match — the answerer reports a truncated answer rather than
hiding it.

`grounding.py` strips `<think>` blocks and ensures reasoning markers can never be
parsed as citations. `test_reasoning_models.py` holds those regressions.

### `nomic-embed-text` — embeddings

768 dimensions, purpose-built for retrieval rather than being a generative model's
hidden states. 768 sits comfortably inside pgvector's 2000-dimension HNSW limit.

Chosen independently of the chat model, which is a requirement rather than a
coincidence — see [chunking-and-embeddings.md](../architecture/chunking-and-embeddings.md).

---

## Trade-offs accepted

These are the honest costs, and they are the central caveat of the local stack.

**The model misreads figures.** Observed directly: asked for expense approval
thresholds, `qwen3:8b` rendered *"500 to 2,500 EUR"* as *"50,000 to 2,500 EUR"* while
citing the correct passage. Retrieval was right, the citation was right, the number was
wrong. This is exactly what the evaluation harness's `fact_match` metric exists to
quantify rather than anecdote.

**Citations are asserted, not verified.** Anthropic returns citations verified against
the source text. Every other provider — including this one — emits `[n]` markers that a
model can produce for an unsupported claim. Both paths produce the same `Citation`
object, so nothing downstream can tell the difference. A deliberate trade for vendor
agnosticism, and a gap that should be *measured*.

**4096-token context caps the corpus per answer.** Five chunks of ~900 characters. A
question needing six passages is answered incompletely rather than incorrectly — the
better of the two failure modes, but still a failure.

**Latency.** ~6 s for a short completion on the reference machine. Fine for a CLI, and
the reason a full evaluation run takes minutes rather than seconds.

---

## Alternatives considered

| Option | Why not the default |
|---|---|
| **Hosted Anthropic / OpenAI** | Better answers, verified citations (Anthropic), and corpus text leaving the host plus a credential and a bill. Available as `config/experiments/hosted-anthropic.yaml` |
| **llama.cpp directly** | Ollama *is* a wrapper around it, plus model management and an OpenAI-compatible server. The wrapper is the value |
| **vLLM** | Much better throughput under concurrency, much heavier to operate, GPU-oriented. The right answer for a production serving tier, wrong for a laptop |
| **A larger local model** | The obvious fix for the numeric-fidelity gap. Not adopted because it is a hypothesis, and the harness now exists to test it |

None of this is load-bearing. Switching is a profile change — that is the entire point
of the [provider architecture](../architecture/provider-architecture.md).

---

## Future evolution

- **Serve `qwen3:8b` with a larger context** and measure whether more sources improves
  answers. A `num_ctx` change and an eval run.
- **Quantify the numeric-fidelity gap** with `fact_match`, then test whether a larger
  model closes it. This is a Milestone A success criterion.
- **Run one hosted comparison end to end** — `--profile config/experiments/hosted-anthropic.yaml`
  — to put a number on the citation-strength difference.

---

## Reference environment

Ollama 0.32.5 serving `qwen3:8b` at a 4096-token context and `nomic-embed-text`.
`./osc doctor` makes a live call to both and reports round-trip latency; construction
alone would pass with Ollama stopped or the model unpulled, which are two of the three
most common causes of "it worked yesterday".
