# ADR 0012 — `markdown` becomes the default chunker, on a measurement

**Status:** Accepted · **Date:** Phase 6 · **Supersedes** [ADR 0006](0006-chunking-strategy.md)

---

## Context

ADR 0006 kept `recursive` as the default chunker with an explicit condition attached:
switching would change every chunk boundary and therefore every chunk id in a live
index, and the project's rule is that a retrieval change ships with a measured
improvement. There was no golden set at the time, so the decision was *defer until
measurable*, not *recursive is best*.

The harness has existed since Phase 4 and this comparison was the first open criterion
of Milestone A′ — built and never spent.

Phase 6 supplied the motive as well as the means. The schema corpus (ADR 0011) is
markdown tables, JSON payloads and field inventories rather than prose, and inspecting
the index showed `recursive` handling it badly. `schema.md` produced four chunks: one
of 147 characters holding only the heading, one starting mid-table at
`| \`json\` | Template catalogue…`, and one starting mid-word at `ormId\``. A chunk
beginning mid-identifier cannot be retrieved by the identifier it contains.

## Decision

**`markdown` is the default chunking strategy**, on the following measurement. All
four strategies were run against the schema suite with everything else held constant —
same corpus, same embedding model, same `top_k`, same retrieval strategy — each after
a full `--reindex`, because chunk ids derive from chunk boundaries and an ordinary
sync would have reported `skipped` and silently measured the old index under the new
label.

| strategy | chunks | recall@5 | mrr | ndcg@5 | precision@5 |
|---|---|---|---|---|---|
| `recursive` (previous default) | 52 | 0.909 | 0.855 | 0.868 | 0.186 |
| `langchain_recursive` | 71 | 0.927 | 0.874 | 0.888 | 0.189 |
| `fixed` | 45 | 0.946 | 0.872 | 0.890 | 0.193 |
| **`markdown`** | **80** | **0.982** | **0.897** | **0.918** | **0.200** |

`markdown` wins on every metric, and `precision@5` of 0.200 is the structural maximum
for this suite — most questions have one relevant document, so with `k=5` no ranking
can exceed 0.2.

The gain is concentrated exactly where the defect was. `addons-tier-pricing` and
`bulk-import-export` — the two most table-dense documents — were the weakest categories
under `recursive` at 0.60 recall.

## Alternatives considered

**Keep `recursive` and raise `chunk_size`.** A bigger window would swallow more of each
table, at the cost of diluting every chunk's embedding with unrelated fields. Not run,
because it treats a structural problem as a sizing problem: the boundary is in the
wrong *place*, not merely too close.

**`fixed`.** Second on recall and cheapest to reason about. Rejected on the numbers,
and its result is worth recording for a different reason — it beat `recursive` and
`langchain_recursive`, which suggests `recursive`'s separator ladder is actively
mis-firing on table syntax rather than merely being unaware of it.

**Preprocess tables into sentences before chunking.** Would likely beat all four. Not
attempted: parsers extract and never rewrite, because chunk text is quoted back as
citation evidence, and invented text would make that evidence a forgery.

## Consequences

**Every chunk id in the index changed.** Anything holding a chunk id across this change
— a bookmarked `./osc chunk <id>`, an audit record from before it — no longer resolves.
Audit records carry document ids too, so an old answer remains attributable at document
level. Upgrading requires `./osc ingest --reindex`; an ordinary sync reports `skipped`
because the content hash did not change.

**The index grew 54%**, from 52 chunks to 80, and the median chunk shrank from 826 to
278 characters. Heading-aware splitting produces many small chunks for a document that
is a list of short sections. More chunks is more embedding calls at ingest and a larger
table; at this corpus size both are irrelevant, and at a hundred times this size the
trade would need re-measuring rather than assuming.

**Small chunks make `top_k` a more open question than it was.** With a median of 278
characters, five chunks is now roughly 350 tokens of context where it used to be
roughly 1000. `top_k` was not re-tuned in this change — deliberately, because two
variables moved at once is how a measurement stops meaning anything — and it is the
obvious next experiment.

**This result is corpus-specific and must not be generalised.** `markdown` is worth
7 points of recall *on documents that are mostly tables*. The FAQ suite, which is prose,
is retained partly so that claim can be checked rather than assumed (ADR 0011). Running
this comparison against it is unfinished work.

**ADR 0006 was right and is now spent.** It deferred the decision until it could be
measured, and the deferral held for two phases. The record stays as written; this one
supersedes it.
