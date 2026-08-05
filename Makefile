.PHONY: help install test test-integration test-e2e lint typecheck check format \
        serve ingest reindex doctor status config providers documents document \
        chunk ask search traces trace version clean eval eval-retrieval eval-gate

# Every target below goes through ./osc or $(VENV), so no command in this file —
# and none in the documentation — asks anyone to type a path into .venv.
VENV := .venv
PY   := $(VENV)/bin/python
OSC  := ./osc

# The default profile is fully local: Ollama for generation and embeddings,
# PostgreSQL with pgvector for storage. No API credential is required.
DSN ?= postgresql://mokshdutt@localhost:5432/osc

# Corpus directory for `make ingest`. This is `docs/company`, not `docs`: the
# company knowledge corpus and this repository's own engineering documentation both
# live under docs/, and only the first of them belongs in the answer index. See
# docs/engineering/architecture/knowledge-corpus.md.
DOCS ?= ./docs/company

# Free-form argument for the commands that take one:
#   make ask Q="how many leave days?"
#   make document ID=leave-policy
Q  ?=
ID ?=

help:  ## Show every target with its description
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ------------------------------------------------------------------ environment

install:  ## Create the virtualenv and install the project with dev extras
	python -m venv $(VENV) && $(VENV)/bin/pip install -e ".[dev,openai,documents]"

clean:  ## Remove caches and build artefacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache **/__pycache__

# ------------------------------------------------------------------------ checks

test:  ## Unit tests: no network, no database, no credentials
	$(VENV)/bin/pytest -q

# Adds the pgvector suite. OSC_TEST_DIMENSIONS must match the width the target
# database's chunks table was migrated with — 768 for nomic-embed-text. Against a
# throwaway database, drop it and the narrow stub width is used instead.
test-integration:  ## Unit tests plus the pgvector suite against a real database
	OSC_TEST_DSN=$(DSN) OSC_TEST_DIMENSIONS=768 $(VENV)/bin/pytest -q

# The smoke test drives the whole path against live Ollama and PostgreSQL. It needs
# its OWN database: the chunks table fixes its vector width at creation, and this
# suite deletes every document in its workspace when it finishes.
E2E_DSN ?= postgresql://mokshdutt@localhost:5432/osc_e2e

test-e2e:  ## End-to-end smoke test against a live Ollama and PostgreSQL
	@createdb $(notdir $(E2E_DSN)) 2>/dev/null || true
	OSC_E2E=1 OSC_TEST_DSN=$(E2E_DSN) $(VENV)/bin/pytest tests/test_e2e.py -q

# Measurement, not testing: `make test` asks "is it correct?", `make eval` asks
# "is it any good?". The golden set needs the corpus indexed first (`make ingest`).
GOLDEN ?= evaluation/golden-set.yaml

eval:  ## Score the golden set with generation — the full quality picture
	$(OSC) eval --golden-set $(GOLDEN)

eval-retrieval:  ## Score retrieval only — fast and free, enough to compare chunkers
	$(OSC) eval --golden-set $(GOLDEN) --retrieval-only

# The CI gate. Thresholds are the committed baseline rounded down, so an ordinary
# run passes and a regression does not. Raise them when a change earns it.
eval-gate:  ## Fail if retrieval quality has regressed below the committed baseline
	$(OSC) eval --golden-set $(GOLDEN) --retrieval-only \
	  --baseline evaluation/baselines/retrieval-default.json \
	  --fail-under recall@5=0.90 --fail-under mrr=0.82

lint:  ## ruff
	$(VENV)/bin/ruff check .

format:  ## ruff --fix
	$(VENV)/bin/ruff check --fix .

typecheck:  ## mypy --strict
	$(VENV)/bin/mypy src

check: lint typecheck test  ## lint + typecheck + test

# ----------------------------------------------------------------- running things

serve:  ## Run the HTTP API and chat UI
	$(OSC) serve

ingest:  ## Index $(DOCS) — safe and cheap to re-run
	$(OSC) ingest $(DOCS)

reindex:  ## Re-chunk and re-embed everything (needed after a chunker change)
	$(OSC) ingest $(DOCS) --reindex

ask:  ## Ask a question: make ask Q="..."
	@test -n '$(Q)' || (echo 'usage: make ask Q="your question"' && exit 1)
	$(OSC) ask '$(Q)' --explain

search:  ## Retrieval only: make search Q="..."
	@test -n '$(Q)' || (echo 'usage: make search Q="your query"' && exit 1)
	$(OSC) search '$(Q)' --explain

# ------------------------------------------------------------------ understanding

doctor:  ## Check every configured component is reachable and consistent
	$(OSC) doctor

status:  ## Summarise what is indexed
	$(OSC) status

config:  ## Print the fully resolved configuration
	$(OSC) config

providers:  ## List registered providers, marking the active ones
	$(OSC) providers

documents:  ## List indexed documents
	$(OSC) documents

document:  ## Inspect one document: make document ID=leave-policy
	@test -n '$(ID)' || (echo 'usage: make document ID=<id or path fragment>' && exit 1)
	$(OSC) document '$(ID)'

chunk:  ## Print one chunk in full: make chunk ID=<chunk id>
	@test -n '$(ID)' || (echo 'usage: make chunk ID=<chunk id>' && exit 1)
	$(OSC) chunk '$(ID)'

traces:  ## List recent execution traces from the persisted log
	$(OSC) traces

trace:  ## Expand one trace, or the most recent: make trace [ID=<trace id>]
	$(OSC) trace $(ID)

version:  ## Print the installed version and the versions that shape behaviour
	$(OSC) version
