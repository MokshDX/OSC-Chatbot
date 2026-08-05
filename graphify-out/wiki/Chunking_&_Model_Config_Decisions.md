# Chunking & Model Config Decisions

> 12 nodes

## Key Concepts

- **--reindex escape hatch** (5 connections) — `README.md`
- **Two scenario workbooks are 42% of the index** (3 connections) — `PROJECT_STATUS.md`
- **Milestone A′ — Spend the Harness** (3 connections) — `PROJECT_STATUS.md`
- **Heading-aware markdown chunking** (3 connections) — `config/experiments/langchain-bridge.yaml`
- **Local answer model misreads figures** (2 connections) — `PROJECT_STATUS.md`
- **Idempotent ingestion by content hash** (2 connections) — `README.md`
- **Multi-format text extraction** (2 connections) — `README.md`
- **Working with a reasoning model (Qwen3)** (2 connections) — `README.md`
- **reasoning_effort: none for Qwen3** (2 connections) — `config/default.yaml`
- **Chunking settings — recursive, 900/120** (2 connections) — `config/default.yaml`
- **Embedding choice fixes the vector width** (2 connections) — `config/default.yaml`
- **Embeddings held local in the bridge experiment** (1 connections) — `config/experiments/langchain-bridge.yaml`

## Relationships

- [Evaluation Findings & Milestones](Evaluation_Findings_%26_Milestones.md) (3 shared connections)
- [Golden Set Curation & Corpus Rules](Golden_Set_Curation_%26_Corpus_Rules.md) (1 shared connections)
- [Default Profile & Retrieval Config](Default_Profile_%26_Retrieval_Config.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `README.md`
- `config/default.yaml`
- `config/experiments/langchain-bridge.yaml`

## Audit Trail

- EXTRACTED: 17 (59%)
- INFERRED: 12 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*