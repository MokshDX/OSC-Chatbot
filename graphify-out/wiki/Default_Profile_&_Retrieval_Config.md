# Default Profile & Retrieval Config

> 12 nodes

## Key Concepts

- **Scoped LangChain Integration** (5 connections) — `PROJECT_STATUS.md`
- **Default profile — fully local stack** (5 connections) — `config/default.yaml`
- **LangChain bridge experiment profile** (4 connections) — `config/experiments/langchain-bridge.yaml`
- **Hybrid Retrieval** (3 connections) — `PROJECT_STATUS.md`
- **Reciprocal Rank Fusion (RRF)** (3 connections) — `PROJECT_STATUS.md`
- **Citation strength differs by provider, silently** (2 connections) — `PROJECT_STATUS.md`
- **Experiment profiles** (2 connections) — `README.md`
- **Retrieval settings — hybrid, 30 candidates, top_k 5, rrf_k 60** (2 connections) — `config/default.yaml`
- **hosted-anthropic Experiment Profile** (1 connections) — `config/experiments/hosted-anthropic.yaml`
- **workspace_id partition key from day one** (1 connections) — `PROJECT_STATUS.md`
- **Layered configuration (env > .env > YAML profile)** (1 connections) — `README.md`
- **One datastore (PostgreSQL)** (1 connections) — `README.md`

## Relationships

- [Chunking & Model Config Decisions](Chunking_%26_Model_Config_Decisions.md) (1 shared connections)
- [Evaluation Findings & Milestones](Evaluation_Findings_%26_Milestones.md) (1 shared connections)

## Source Files

- `PROJECT_STATUS.md`
- `README.md`
- `config/default.yaml`
- `config/experiments/hosted-anthropic.yaml`
- `config/experiments/langchain-bridge.yaml`

## Audit Trail

- EXTRACTED: 16 (53%)
- INFERRED: 14 (47%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*