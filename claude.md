# CLAUDE.md

# OSC Engineering Handbook

## Purpose

This repository belongs to **OSC**, a company that delivers enterprise AI solutions to businesses.

Our goal is to build reliable, maintainable, scalable software that can be confidently deployed in production. Every technical decision should favour long-term quality over short-term convenience.

You are not simply writing code—you are contributing to a production system that should remain understandable and maintainable for years.

---

# Current Project

Build an enterprise-grade AI chatbot for OSC that serves as an internal knowledge assistant.

The chatbot should prioritise:

* Accuracy
* Minimal hallucinations
* Maintainability
* Scalability
* Modular architecture
* Excellent developer experience

The system should be designed to evolve into a broader enterprise AI knowledge platform capable of supporting multiple knowledge sources, document formats, and future capabilities.

Design today's decisions so they remain valuable as the project grows.

---

# Engineering Philosophy

Our mission is to build software that is:

* Correct
* Reliable
* Understandable
* Maintainable
* Extensible
* Well documented

Code quality is more important than implementation speed.

Always optimise for long-term maintainability.

Prefer simple, well-designed systems over clever solutions.

Every module should have a clear purpose.

Every architectural decision should have a reason.

If a simpler solution achieves the same goal without sacrificing future extensibility, prefer the simpler solution.

---

# How To Think

Before writing code:

1. Understand the problem completely.
2. Question assumptions.
3. Consider multiple approaches.
4. Recommend the best solution with reasoning.
5. Implement only after the approach is clear.

If requirements are unclear:

* Ask questions.
* Explain trade-offs.
* Avoid making hidden assumptions.

Think like a senior software architect, not a code generator.

When making engineering decisions, optimise in this order:

1. Correctness
2. Reliability
3. Maintainability
4. Readability
5. Scalability
6. Performance
7. Development speed

Never sacrifice correctness for convenience.

Avoid premature optimisation.

---

# Architecture & Code Standards

Design systems that are:

* Modular
* Loosely coupled
* Highly cohesive
* Easy to test
* Easy to extend
* Easy to replace

Prefer composition over unnecessary inheritance.

Keep responsibilities clearly separated.

Avoid tightly coupling unrelated modules.

Design features so they can evolve without large-scale rewrites.

Follow established engineering principles where appropriate:

* DRY
* KISS
* SOLID
* Separation of Concerns
* Single Responsibility Principle
* Explicit over implicit behaviour

Avoid:

* Duplicated logic
* Dead code
* Unnecessary abstractions
* Overengineering
* Magic numbers
* Hidden side effects

Prefer readable code over clever code.

Code should explain itself whenever possible.

Write efficient code, but prioritise correctness and maintainability over micro-optimisations.

Optimise only after identifying real bottlenecks.

Handle errors explicitly.

Fail clearly.

Provide meaningful error messages.

Validate inputs where appropriate.

---

# Comments, Documentation & Testing

Comments are important, but they should explain:

* Why something exists
* Architectural intent
* Business rules
* Assumptions
* Edge cases
* Complex algorithms
* Important implementation decisions

Avoid comments that merely describe what the code already says.

Documentation is a first-class deliverable.

Whenever significant changes are made:

* Update relevant documentation
* Explain architectural decisions
* Document new dependencies
* Explain important trade-offs
* Keep documentation accurate

Documentation should explain:

* What was built
* Why it was built
* How it works

Assume future developers know nothing about today's decisions.

Testing is encouraged whenever practical.

Prefer:

* Unit tests
* Edge-case testing
* Failure-path testing
* Deterministic tests

Testing should increase confidence rather than simply improve coverage.

---

# Dependencies & Repository Rules

New libraries may be introduced when they provide meaningful value.

If I have already specified a preferred library or technology, use it unless there is a compelling reason not to. Otherwise, recommend the most suitable, well-supported solution for the project.

Before adding significant dependencies:

* Consider existing project dependencies first.
* Evaluate long-term maintenance and community support.
* Explain why the dependency is beneficial.

Respect existing code.

Avoid unnecessary rewrites.

Do not remove comments, documentation, or functionality without a clear reason.

Large architectural or repository changes should be proposed before implementation.

Small improvements that clearly improve maintainability may be implemented directly.

---

# Communication

Explain important technical decisions.

Present trade-offs when multiple good solutions exist.

If recommending a different approach than requested, explain why.

Be concise but complete.

Avoid unnecessary verbosity.

---

# Definition of Success

A successful contribution:

* Improves the project.
* Leaves the codebase cleaner than before.
* Is understandable by another engineer.
* Is properly documented.
* Can be confidently maintained in the future.

Always leave the project in a better state than you found it.


---

# Operational Tooling

Before debugging by reading source, use the tooling. It exists so that the common
questions have answers that cannot go stale.

```bash
./osc doctor                 # is every configured component reachable and consistent?
./osc status                 # what is indexed: counts, chunk sizes, formats
./osc config                 # what did the configuration layers actually resolve to?
./osc providers              # what can I switch to, and what am I running?
./osc traces                 # what has run recently  (--failed, --name, --slower-than)
./osc trace [id]             # expand one trace, or the most recent, into a waterfall
./osc documents / document / chunk    # what is in the index, down to the exact text
make help                    # every target
```

`./osc` runs the CLI without activating the virtualenv. **Never write `.venv/bin/...`
in a command, a Makefile target or documentation** — if a workflow needs a path into
the virtualenv, add a target instead.

## Diagnosing a failure

In this order, because each step narrows the next:

1. `./osc doctor` — names the broken component on one line.
2. `./osc traces --failed` — finds the request.
3. `./osc trace <id>` — shows which stage raised, and what every earlier stage had
   already done.
4. `./osc search "<query>"` — separates "the model misread the passage" from "the
   passage was never retrieved". Different bugs, different fixes.
5. `./osc chunk <id>` — the exact text the model was given.

A failing command prints its trace automatically; `--explain` is for when it
succeeded and you still want to know how.

## Observability rules for new code

* **A new pipeline stage gets a span.** `with span("name", **attributes)`, with
  attributes describing how the data changed — counts, ids, scores — not prose.
* **Instrument the pipeline, not the adapter.** Provider adapters stay pure
  translation; wrapping the call site covers every provider at once.
* **Anything derived from a document or a user goes through `set_text`**, never
  `set`. That is the seam `observability.capture_text: false` switches off.
* **Never let instrumentation raise.** A tracer that can break the thing it observes
  is a liability, because it is trusted.

## Output rules

* **Machine-readable output goes to stdout; human-readable output goes to stderr.**
  `./osc serve > run.log` must still produce a clean parseable log.
* **Operator problems are messages; bugs are tracebacks.** Raise an `AssistantError`
  subclass with an actionable message for anything an operator must fix. Everything
  else keeps its frames.
* **Never let a vendor exception escape a provider adapter.** Translate it into the
  error hierarchy at the adapter boundary, or the layers above cannot handle it.

---

## Session Startup

Before implementing any feature:

1. Read PROJECT_STATUS.md — the engineering report and handover document.
2. Read README.md — how to run it and what the commands are.
3. Read graphify-out/ — the generated architectural map. Use it to navigate to the
   files a change touches rather than reading the repository recursively.
4. Run `./osc doctor` — confirm the environment before suspecting the code. Most
   surprises here come from outside the process.
5. Understand the current milestone (PROJECT_STATUS.md §15).
6. Confirm the implementation plan before modifying code.
