.PHONY: install test lint typecheck check db ingest serve

install:
	python -m venv .venv && .venv/bin/pip install -e ".[dev,anthropic,openai]"

test:
	.venv/bin/pytest -q

# Integration tests need a live Postgres with pgvector; `make db` starts one.
test-integration:
	OSC_TEST_DSN=postgresql://postgres:postgres@localhost:5432/osc_assistant .venv/bin/pytest -q

lint:
	.venv/bin/ruff check .

typecheck:
	.venv/bin/mypy src

check: lint typecheck test

db:
	docker compose up -d

ingest:
	.venv/bin/osc-assistant ingest ./docs

serve:
	.venv/bin/osc-assistant serve
