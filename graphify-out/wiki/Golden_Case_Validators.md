# Golden Case Validators

> 15 nodes

## Key Concepts

- **GateReport** (11 connections) — `src/osc_assistant/evaluation/gate.py`
- **Finding** (9 connections) — `src/osc_assistant/evaluation/gate.py`
- **Any** (6 connections)
- **_detect_trade_offs()** (4 connections) — `src/osc_assistant/evaluation/gate.py`
- **_configuration_differences()** (4 connections) — `src/osc_assistant/evaluation/gate.py`
- **.to_dict()** (2 connections) — `src/osc_assistant/evaluation/gate.py`
- **.regressions()** (2 connections) — `src/osc_assistant/evaluation/gate.py`
- **.improvements()** (2 connections) — `src/osc_assistant/evaluation/gate.py`
- **.to_dict()** (2 connections) — `src/osc_assistant/evaluation/gate.py`
- **.delta()** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **.failed()** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **One metric's verdict, with everything needed to act on it. Carries the numbers…** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **The gate's decision and the evidence for it.** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **Improvements that were bought with a regression elsewhere.** (1 connections) — `src/osc_assistant/evaluation/gate.py`
- **Configuration keys that differ, so a comparison cannot silently span two…** (1 connections) — `src/osc_assistant/evaluation/gate.py`

## Relationships

- [Session Memory Tests](Session_Memory_Tests.md) (7 shared connections)
- [Provider Registration & Embeddings](Provider_Registration_%26_Embeddings.md) (4 shared connections)
- [Reranker & Retrieval Settings](Reranker_%26_Retrieval_Settings.md) (4 shared connections)
- [Regression Gate Engine](Regression_Gate_Engine.md) (1 shared connections)

## Source Files

- `src/osc_assistant/evaluation/gate.py`

## Audit Trail

- EXTRACTED: 48 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*