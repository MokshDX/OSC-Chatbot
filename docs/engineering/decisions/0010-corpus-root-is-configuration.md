# ADR 0010 — The corpus root is configuration, defined once

**Status:** Accepted · **Date:** Phase 6

---

## Context

ADR 0007 established that `docs/company/` is the answer corpus and `docs/engineering/`
is not, because an answer sourced from an ADR would retrieve cleanly, ground correctly
and cite accurately while being from the wrong universe — and nothing downstream
catches it.

It established the *boundary* well and the *mechanism* badly. The root was written out
as a literal in three places:

| Place | Literal |
|---|---|
| `Makefile` | `DOCS ?= ./docs/company` |
| `cli/diagnose.py` | the `--corpus` default on `doctor` |
| `api/banner.py` | the empty-index startup note |

`PROJECT_STATUS.md` recorded the consequence as a rule for humans to remember: *"The
ingest root is named in exactly two places … and they must agree."* A regression test
asserted the first two agreed; the third was not covered by anything.

A rule that survives only as long as everyone remembers it is not a boundary, it is a
convention. And this particular convention protects the one corpus mistake that
produces no error, no warning and no failing metric.

Phase 6 then made the boundary move — the authoritative knowledge source became
`docs/company/schema/` (ADR 0011) — which is exactly the operation the three-literal
design handles worst.

## Decision

**The corpus root is `corpus.root` in the profile, and nothing else names it.**

`./osc ingest` with no argument reads it. `./osc doctor` checks it. The empty-index
startup note quotes it. A one-off root is still an explicit argument; there is simply
no second *default* anywhere.

The regression test changed with it. It used to assert that two hand-maintained
literals were equal — a property that is no longer expressible, because there is one
value. It now asserts the property those literals existed to protect: whatever the
configured root is, the engineering knowledge base is not inside it, and the root has
not drifted up to a bare `docs`.

## Alternatives considered

**Keep the literals, add a third assertion.** The obvious minimum: extend the existing
test to cover `banner.py` too. Rejected because it treats the symptom. Every new place
that needs to know the corpus root would need a new literal and a new assertion, and
the assertion would be written by whoever remembered — the same failure, one layer up.

**A module constant, imported by all three.** Better than three literals and worse than
configuration. It removes the drift but keeps the root un-overridable per deployment,
which was already wanted: the FAQ suite is now run against a different root in a
different workspace, and that must not require an edit to the source.

**An exclusion list — ingest `docs/` but skip `engineering/`.** Rejected in ADR 0007
and still rejected, for the reason given there: an exclusion list fails open. A new
directory of internal documentation is indexed by default and someone has to notice.
A directory boundary fails safe.

## Consequences

**The root is now deployment-specific**, which it should have been. A container sets
`OSC_CORPUS__ROOT` and ships.

**`make ingest` no longer states what it ingests.** Reading the `Makefile` used to
answer "what is the corpus?" and now answers "whatever is configured". This is a real
loss of local readability, accepted because the previous readability was of a value
that could be wrong. `./osc config` and `./osc doctor` both print the resolved root.

**One test got weaker and one got stronger.** The equality assertion is gone because
the thing it compared no longer exists in two copies. What replaced it tests the actual
invariant rather than a proxy for it, and it covers `banner.py`, which the old test
never did.

**Nothing stops a profile setting `corpus.root: docs`.** The test catches it in CI, not
at runtime. Making the settings model reject a root containing `engineering/` was
considered and left out: it would encode this repository's directory layout into a
generic configuration model, and the test already covers the case that matters.
