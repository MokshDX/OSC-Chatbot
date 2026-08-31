.PHONY: help install verify test test-integration test-e2e lint typecheck check format \
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

# The corpus root is NOT defined here. It is `corpus.root` in the active profile,
# and `./osc ingest` with no argument reads it. This file used to carry its own
# copy, which meant the ingest root and the root `doctor` checked were two facts
# that had to be kept equal by hand. Override for a one-off with:
#   make ingest DOCS=docs/company/faq
DOCS ?=

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

# ============================================================================
# The two canonical commands.
#
#   make verify   Does OSC work?     every automated test, one summary
#   make eval     Is OSC any good?   every metric, gated against the baseline
#
# Everything below them is a narrower slice of one of the two, kept because a
# two-second hermetic loop is worth having and a thirty-second one is not.
# ============================================================================

# The smoke test needs its OWN database: the chunks table fixes its vector width at
# creation, and the suite clears its workspace when it finishes.
E2E_DSN ?= postgresql://mokshdutt@localhost:5432/osc_e2e

verify:  ## EVERY test — unit, integration, E2E — plus lint and types, in one report
	@$(VENV)/bin/ruff check . && $(VENV)/bin/mypy src
	@createdb $(notdir $(E2E_DSN)) 2>/dev/null || true
	@OSC_TEST_DSN=$(DSN) OSC_TEST_DIMENSIONS=768 \
	 OSC_E2E=1 OSC_E2E_DSN=$(E2E_DSN) \
	 $(VENV)/bin/pytest -q -ra
# One pytest invocation rather than three, so there is one summary line, one exit
# code and one list of failures. Three invocations mean a failure in the first can
# scroll off the screen before the third finishes, which is the exact thing a
# canonical command exists to prevent. `-ra` names every skip and failure, so a
# suite silently skipping for a missing database is visible rather than green.
#
# Integration and E2E need two different databases; `OSC_E2E_DSN` is what lets them
# both be addressed in one process. OSC_TEST_DIMENSIONS must match the width the
# target database's chunks table was migrated with — 768 for nomic-embed-text.

test:  ## Fast hermetic subset: no network, no database, no credentials
	$(VENV)/bin/pytest -q

test-integration:  ## Unit tests plus the pgvector suite against a real database
	OSC_TEST_DSN=$(DSN) OSC_TEST_DIMENSIONS=768 $(VENV)/bin/pytest -q

test-e2e:  ## End-to-end smoke test against a live Ollama and PostgreSQL
	@createdb $(notdir $(E2E_DSN)) 2>/dev/null || true
	OSC_E2E=1 OSC_E2E_DSN=$(E2E_DSN) $(VENV)/bin/pytest tests/test_e2e.py -q

# Measurement, not testing: `make verify` asks "is it correct?", `make eval` asks
# "is it any good?". Needs the corpus indexed first (`make ingest`).

eval:  ## EVERY metric — single-turn and conversational — gated against the baseline
	$(OSC) eval

# Ungated on purpose: this is the experimentation loop. Comparing four chunkers
# means three of the runs are *expected* to be worse than the baseline, and a
# non-zero exit on each of them would train the reflex of passing --no-gate.
eval-retrieval:  ## Retrieval only, ungated — fast, free, and enough to compare chunkers
	$(OSC) eval --retrieval-only --no-gate

# What CI runs. No thresholds are typed here any more: the gate derives each
# metric's tolerance from the run itself (one case for deterministic retrieval
# metrics, two standard errors for sampled generation metrics) and compares against
# the committed baselines. See src/osc_assistant/evaluation/gate.py.
#
# Retrieval-only because a gate must be deterministic: generation samples, so a
# gate including it could change its mind between two runs of the same commit.
eval-gate:  ## Fail if retrieval quality has regressed beyond tolerance
	$(OSC) eval --retrieval-only

lint:  ## ruff
	$(VENV)/bin/ruff check .

format:  ## ruff --fix
	$(VENV)/bin/ruff check --fix .

typecheck:  ## mypy --strict
	$(VENV)/bin/mypy src

check: lint typecheck test  ## Fast pre-commit loop: lint + types + hermetic tests

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
