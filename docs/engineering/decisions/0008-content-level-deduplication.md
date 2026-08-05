# ADR 0008 — Ingestion deduplicates by source, not by content

**Status:** Accepted, with a known cost · **Date:** Phase 4

---

## Context

The knowledge graph surfaced something the ingestion pipeline could not:
`docs/company/scenarios/OSCP_B2B_Scenario_Document.docx` and
`OSCP_B2B_Scenario_Document-1.docx` extract to **byte-identical text** — 24,096
characters, content hash `54314756e14a2f4f` for both.

The two files differ at the byte level (different zip metadata, so different md5), so
nothing about them looks duplicated on disk. Only the *extracted* text matches.

The consequence is measurable. `./osc documents` shows both indexed at 34 chunks
each: **34 of the index's 193 chunks (17.6%) are exact duplicates.**

This is not merely wasted storage. Retrieval returns `top_k = 5` chunks, and
duplicate chunks compete for the same slots — a query matching that content can spend
two of its five slots on identical text, halving the diversity of what the model is
shown. It is a plausible contributor to a measured finding: four of the six recall
failures in `evaluation/baselines/full-default.json` retrieved a scenario chunk in
place of the FAQ document that answers the question.

**Why the existing machinery does not catch it.** `content_hash()` exists, is
computed on every document, and is used on every sync. But it answers *"has **this**
document changed since last time?"*, keyed on `document_id` — a SHA-256 digest of the
file's absolute URI. Nothing anywhere asks *"is this the same content as a **different**
document?"* Two paths with identical bytes are, by construction, two documents.

## Decision

**Keep source-keyed identity. Do not add content-level deduplication at ingest.**

The duplicate is a corpus problem, not a pipeline problem, and it is fixed by deleting
a file. Detection is worth having; automatic collapse is not.

Two things follow from that, and only the first is done:

1. **The condition is now visible.** It was found by the knowledge graph, which is a
   fragile way to find it. `./osc doctor` reporting duplicate content hashes across
   distinct document ids would make it an operational check rather than a lucky catch.
   *Not yet implemented — see Consequences.*
2. **The duplicate file itself is left in place.** `docs/company/` is authoritative
   company documentation and the project's rule is not to modify it without
   instruction. Which of the two copies is canonical is a question for whoever owns
   the corpus.

## Alternatives considered

**Deduplicate by content hash at ingest — index the first, skip the rest.** The
obvious fix, and it silently discards a document an operator explicitly placed in the
corpus. Worse, it makes the corpus's behaviour depend on filesystem iteration order:
which of two identical files "wins" would be whichever `rglob` reached first, and the
losing path would vanish from `./osc documents` with no explanation. A system that
quietly drops input is harder to trust than one that indexes it twice.

**Deduplicate at retrieval — collapse identical chunk text in the ranked list.** More
targeted, since the actual harm is slot competition, and it treats the symptom while
leaving 34 wasted chunks, wasted embedding calls and a misleading `./osc status`. It
also adds a text comparison to the hot path for a condition that should not exist.

**Make `document_id` a hash of content rather than of the source URI.** Solves it
completely and breaks something more important: a document's identity would then
change every time it is edited, so incremental re-indexing could no longer tell "this
document was updated" from "this document was deleted and a new one appeared". The
whole idempotency story depends on identity being stable across content changes.

**Warn at ingest and index both.** The closest to right, and the version worth
building. It is not in this ADR's decision only because ingest already prints a
summary line and adding a warning path deserves the same care as the pruning logic —
it is queued rather than rejected.

## Consequences

**What it costs, stated plainly.**

- The current index carries 34 duplicate chunks (17.6%), with the retrieval-slot
  competition described above. This is live, in the committed baseline, and every
  number in `evaluation/baselines/full-default.json` was measured against it.
- Nothing detects the condition today. It was found by a knowledge-graph rebuild that
  happened to have `graphifyy[office]` installed for the first time. That is not a
  control.
- Any corpus assembled by export-then-copy — which is how most real internal corpora
  arrive — is likely to contain this pattern more than once.

**What it buys.**

- Document identity stays stable across edits, which is what makes incremental
  ingestion, pruning and the unreadable-file prune exemption correct.
- No input is ever silently discarded.

**Open item, and it is cheap.** Add a `duplicates` check to `./osc doctor`: group
indexed documents by `content_hash`, report any hash held by more than one document
id. The store already exposes `list_document_hashes()`, so this is a dictionary
inversion and a warning line — roughly ten lines, and it turns a lucky catch into a
standing check. Until then the finding above is a snapshot, not a guarantee.

**A note on how this was found.** The graph did not find a duplicate *file*; it found
two document nodes whose extracted concepts were identical, and the subagent flagged
it rather than minting twenty ghost twins. That is the second time in this project
that the knowledge graph has reported something no architecture document would have —
the first being `StubEmbeddingModel` ranking as the most connected node in the
codebase. Both are arguments for treating the graph as a check on the system rather
than only as a map of it.
