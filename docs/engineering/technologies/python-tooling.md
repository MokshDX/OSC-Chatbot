# Python Tooling

*The libraries and checks that are not part of the retrieval story but shape every file
in it.*

Runtime: **Python 3.12+**. Required for `type` statement aliases, `StrEnum`, and PEP 695
generics (`def mean_of[T](...)`), all of which appear in the codebase.

---

## Pydantic and pydantic-settings

**What.** Runtime validation and settings management from type annotations.
https://docs.pydantic.dev/

**Why.** The project's rule is that **validation belongs at the trust boundary** — and
Pydantic is used at every one of them, and nowhere else:

| Boundary | Module |
|---|---|
| HTTP requests | `api/schemas.py` |
| Configuration files and environment | `settings.py` |
| Golden set YAML | `evaluation/dataset.py` |

Domain types (`types.py`) are **frozen dataclasses, not Pydantic models**, and that is
deliberate: they are constructed internally and never parsed from untrusted input, so
per-instantiation validation would be cost with no benefit. Frozen dataclasses with
`slots=True` are also cheaper and communicate immutability more directly.

**The settings layering** is the interesting part: process environment → `.env` → YAML
profile, implemented as a custom `PydanticBaseSettingsSource`. Any value is addressable
from the environment with `OSC_` and `__` for nesting
(`OSC_RETRIEVAL__TOP_K=8`). `./osc config` prints what actually resolved, with
credentials redacted. `test_settings.py` pins the precedence in ten tests, added after
the module was found to have none.

---

## Typer and Rich

**What.** A CLI framework built on Click that derives arguments from type annotations,
and a terminal rendering library. https://typer.tiangolo.com/ · https://rich.readthedocs.io/

**Why Typer.** The same property as FastAPI: the signature *is* the interface. A
command's options, types, defaults and help text live in one place, so they cannot
drift.

**Why Rich.** The tables, the trace waterfall and the colour in comparison deltas. The
waterfall in particular — bars positioned by offset and sized by duration — is the
difference between reading timings and *seeing* which stage dominated.

**How the CLI is organised.** Three modules by what a command is *for*, not by what it
touches:

| Module | Commands |
|---|---|
| `core` | `serve` `ingest` `ask` `search` |
| `diagnose` | `doctor` `status` `config` `providers` `documents` `document` `chunk` `traces` `trace` `version` |
| `evaluate` | `eval` |

They are merged into one flat surface — `./osc doctor`, not `./osc diagnose doctor` —
because sub-command nesting costs typing on every invocation and buys grouping that
fifteen commands do not need. `--help` groups them into three panels by purpose
instead, since `--help` is the discovery surface and a flat list makes the reader do the
sorting.

Shared plumbing lives in `_shared.py` so `core`, `diagnose` and `evaluate` depend on it
rather than on each other. `traced_command` — which prints the failed trace and reports
`AssistantError` as a message rather than a traceback — lives there for exactly that
reason.

---

## ruff

**What.** A linter and formatter, written in Rust. https://docs.astral.sh/ruff/

**Why.** It replaces flake8, isort, pyupgrade, pydocstyle and several plugins with one
tool and one config block, and it is fast enough to run on every save.

Rule set: `E`, `F`, `I`, `N`, `UP`, `B`, `C4`, `SIM`, `RUF`. Line length 100.
`make lint` / `make format`.

---

## mypy --strict

**What.** A static type checker, run in strict mode over 63 source files.
https://mypy.readthedocs.io/

**Why strict specifically.** The [provider
architecture](../architecture/provider-architecture.md) is built on `Protocol`, and a
protocol is **only enforced statically**. Nothing at runtime checks that a registered
provider actually satisfies `ChatModel` — the pipeline just calls `complete()` and finds
out. `mypy --strict` is what turns "satisfies the protocol" from a convention into a
check, and without it the central architectural claim of this project would be
unverified.

`ignore_missing_imports = true` because provider SDKs are optional extras and a missing
stub for `google-genai` must not fail the whole check.

`make typecheck`. `make check` runs lint, typecheck and tests together.

---

## pytest and pytest-asyncio

**What.** The test runner, with `asyncio_mode = "auto"` so `async def test_*` needs no
decorator. https://docs.pytest.org/

**Why the configuration matters.** Nearly every function in this codebase is a
coroutine; requiring `@pytest.mark.asyncio` on 300 tests would be noise.

`conftest.py` holds in-process implementations of the protocols — deliberately real
implementations rather than mocks, because the point of the protocol layer is that the
pipelines cannot tell a stub from a provider. See
[testing.md](../architecture/testing.md).

---

## hatchling

**What.** The build backend. https://hatch.pypa.io/

**Why.** PEP 517/621 compliant, no `setup.py`, and it force-includes `py.typed` so
consumers of the package see the annotations rather than treating it as untyped.

---

## The dependency posture

The core runtime is deliberately small. Everything vendor-specific is an extra, so a
deployment installs only the SDKs for the providers it actually configures:

```
core:      pydantic · pydantic-settings · fastapi · uvicorn · asyncpg · httpx
           pyyaml · typer · rich · langchain-core · langchain-text-splitters
extras:    anthropic · openai · gemini · local · documents · dev
```

`langchain-core` and `langchain-text-splitters` are core rather than extras because both
are pure Python with no vendor SDK behind them, and both must be importable for the
registries to be complete. The reasoning is in
[langchain.md](langchain.md#dependency-posture).

`documents` (`pypdf`, `python-docx`, `openpyxl`) is an extra because Markdown, text,
reStructuredText and HTML need nothing beyond the standard library — a deployment
ingesting only Markdown should not install three parsing libraries.

---

## The `./osc` wrapper

```bash
./osc doctor        # not .venv/bin/osc-assistant doctor
```

A three-line shell script that runs the CLI without activating the virtualenv. The rule
it enforces, from `CLAUDE.md`:

> **Never write `.venv/bin/...` in a command, a Makefile target or documentation.** If a
> workflow needs a path into the virtualenv, add a target instead.

The reason is that a path into a virtualenv in documentation is a path that is wrong on
someone else's machine, and it is wrong silently.
