# Committed baselines

The reference runs `./osc eval` gates against. `evaluation/results/` is gitignored and
holds every run; this directory holds the few that are *trusted*, and they are
committed so a regression is a diff rather than a memory.

## Naming

`<suite>-<variant>.json`, which is what `_default_baseline()` in `cli/evaluate.py`
computes. A suite is gated against its own baseline automatically:

| File | Suite | Variant | Gates |
|---|---|---|---|
| `schema-retrieval.json` | `suites/schema.yaml` | retrieval only | `make eval-gate`, and what CI should run |
| `schema-full.json` | `suites/schema.yaml` | with generation | `make eval` |
| `conversational-full.json` | `suites/conversational.yaml` | with generation | `make eval` |
| `faq-retrieval.json` | `suites/faq.yaml` | retrieval only | the preserved FAQ suite |
| `faq-full.json` | `suites/faq.yaml` | with generation | the preserved FAQ suite |

Retrieval-only and full runs have **separate baselines on purpose**. A retrieval-only
run reports no generation metrics at all, and comparing one against a full run would
silently diff the intersection of two different measurements.

## The FAQ baselines are historical

`faq-*.json` were `full-default.json` and `retrieval-default.json` through Phase 5,
when `docs/company/faq/` was the production corpus. Phase 6 moved the authoritative
knowledge source to `docs/company/schema/` ([ADR 0011](../../docs/engineering/decisions/0011-schema-first-knowledge-corpus.md))
and they were renamed into the scheme above.

They are kept, not deleted. They are the measurement record behind ADR 0003 and
ADR 0008, and deleting evidence because the system moved on is how a benchmark becomes
a story. **Their numbers are not comparable to the schema suite's** — different corpus,
different questions — and `PROJECT_STATUS.md` reports both labelled rather than
overwriting one with the other.

To reproduce one:

```bash
OSC_WORKSPACE_ID=faq ./osc ingest docs/company/faq
OSC_WORKSPACE_ID=faq ./osc eval --golden-set evaluation/suites/faq.yaml
```

## Committing a new baseline

Only when the improvement is understood and intended:

```bash
./osc eval --suite schema --retrieval-only --no-gate -o evaluation/baselines/schema-retrieval.json
```

The result file carries a `configuration` snapshot, so a comparison cannot silently
span two different systems — the gate prints every configuration key that differs.
Re-baselining to make a red build green, without a reason recorded in the commit
message, is the one thing this directory exists to make visible.
