# Structured Logging

> 12 nodes · cohesion 0.20

## Key Concepts

- **container.py** (25 connections) — `src/osc_assistant/container.py`
- **logging.py** (13 connections) — `src/osc_assistant/logging.py`
- **get_logger()** (10 connections) — `src/osc_assistant/logging.py`
- **configure_logging()** (7 connections) — `src/osc_assistant/logging.py`
- **JsonFormatter** (4 connections) — `src/osc_assistant/logging.py`
- **.format()** (3 connections) — `src/osc_assistant/logging.py`
- **Logger** (1 connections)
- **LogRecord** (1 connections)
- **Composition root. The only module that knows both which providers exist and how…** (1 connections) — `src/osc_assistant/container.py`
- **Structured logging. Answers must be auditable: which chunks were retrieved,…** (1 connections) — `src/osc_assistant/logging.py`
- **Renders records as single-line JSON.** (1 connections) — `src/osc_assistant/logging.py`
- **Install the root handler. Safe to call more than once.** (1 connections) — `src/osc_assistant/logging.py`

## Relationships

- [Answer Generation & Abstention](Answer_Generation_%26_Abstention.md) (6 shared connections)
- [HTTP API Layer](HTTP_API_Layer.md) (5 shared connections)
- [Corpus Loaders & Ingestion](Corpus_Loaders_%26_Ingestion.md) (5 shared connections)
- [Command Line Interface](Command_Line_Interface.md) (4 shared connections)
- [Error Hierarchy](Error_Hierarchy.md) (4 shared connections)
- [Reranker Interface & Registries](Reranker_Interface_%26_Registries.md) (3 shared connections)
- [Settings Loading & YAML Profiles](Settings_Loading_%26_YAML_Profiles.md) (2 shared connections)
- [pgvector Setup & Codecs](pgvector_Setup_%26_Codecs.md) (2 shared connections)
- [Chunking Strategies](Chunking_Strategies.md) (1 shared connections)
- [Composition Root](Composition_Root.md) (1 shared connections)
- [Chat Model Interface](Chat_Model_Interface.md) (1 shared connections)
- [Chunker Registration](Chunker_Registration.md) (1 shared connections)

## Source Files

- `src/osc_assistant/container.py`
- `src/osc_assistant/logging.py`

## Audit Trail

- EXTRACTED: 68 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*