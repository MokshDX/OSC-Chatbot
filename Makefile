.PHONY: install test test-integration lint typecheck check ingest serve

# The default profile is fully local: Ollama for generation and embeddings,
# PostgreSQL with pgvector for storage. No API credential is required.
DSN ?= postgresql://mokshdutt@localhost:5432/osc

# `documents` adds PDF and Word extraction; `openai` supplies the SDK that the
# OpenAI-compatible adapter uses to reach Ollama.
install:
	python -m venv .venv && .venv/bin/pip install -e ".[dev,openai,documents]"

test:
	.venv/bin/pytest -q

# Adds the pgvector suite. OSC_TEST_DIMENSIONS must match the width the target
# database's chunks table was migrated with — 768 for nomic-embed-text. Against a
# throwaway database, drop it and the narrow stub width is used instead.
test-integration:
	OSC_TEST_DSN=$(DSN) OSC_TEST_DIMENSIONS=768 .venv/bin/pytest -q

lint:
	.venv/bin/ruff check .

typecheck:
	.venv/bin/mypy src

check: lint typecheck test

ingest:
	.venv/bin/osc-assistant ingest ./docs

serve:
	.venv/bin/osc-assistant serve
