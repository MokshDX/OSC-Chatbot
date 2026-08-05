"""Plumbing shared by the CLI command modules.

Kept separate so `core` and `diagnose` depend on this rather than on each other,
and so the one piece of behaviour every command shares — how settings, logging and
tracing are initialised — has a single definition.
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import Coroutine, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from ..errors import AssistantError
from ..logging import configure_logging
from ..observability import RECORDER, configure_observability, render_waterfall
from ..settings import Settings, load_settings

console = Console()
error_console = Console(stderr=True)

# Help panels. Commands are grouped by what a developer is trying to do, not by
# which module implements them: `--help` is the discovery surface, and a flat list
# of thirteen commands makes the reader do the sorting.
RUNNING = "Running things"
UNDERSTANDING = "Understanding the system"
LOOKING = "Looking at data"

ProfileOption = Annotated[
    Path | None,
    typer.Option("--profile", "-p", help="YAML profile to load instead of config/default.yaml."),
]
VerboseOption = Annotated[
    bool,
    typer.Option("--verbose", "-v", help="Show the structured logs the service emits."),
]
JsonOption = Annotated[
    bool, typer.Option("--json", help="Emit machine-readable JSON instead of a table.")
]
ExplainOption = Annotated[
    bool,
    typer.Option("--explain", help="Print the execution trace: every stage, timed."),
]


def load(profile: Path | None, *, verbose: bool = False, quiet_logs: bool = True) -> Settings:
    """Resolve settings and initialise logging and tracing for one command.

    Interactive commands suppress the service's own INFO logs by default. The
    structured JSON stream is the right output for a running service and the wrong
    output for a terminal, where it buries the answer the operator asked for.
    `--verbose` restores it, and `--explain` shows the same information in the form
    a human can actually read.
    """
    if profile is not None:
        os.environ["OSC_PROFILE"] = str(profile)
    settings = load_settings()

    if verbose or not quiet_logs:
        configure_logging(settings.log_level, settings.log_format)
    else:
        configure_logging("WARNING", "text")

    configure_observability(
        enabled=settings.observability.enabled,
        capacity=settings.observability.trace_buffer_size,
        max_spans=settings.observability.max_spans_per_trace,
        # Already rendered by --explain or shown by --verbose; logging it as well
        # would print the same trace twice.
        log_traces=verbose and settings.observability.log_traces,
        capture_text=settings.observability.capture_text,
        persist=settings.observability.persist_traces,
        trace_dir=settings.observability.trace_dir,
        max_trace_bytes=settings.observability.max_trace_file_bytes,
    )
    return settings


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


def table(*columns: str, title: str | None = None) -> Table:
    """A table styled consistently across every command."""
    built = Table(title=title, title_justify="left", header_style="bold", box=None, pad_edge=False)
    for column in columns:
        built.add_column(column)
    return built


def fail(message: str) -> None:
    """Report an operator-facing error and exit non-zero."""
    error_console.print(f"[red]error:[/red] {message}")
    raise typer.Exit(code=1)


def print_trace(explain: bool) -> None:
    """Render the trace the command just produced, if one was asked for."""
    if not explain:
        return
    recent = RECORDER.recent(limit=1)
    if not recent:
        console.print(
            "[yellow]no trace recorded — is observability.enabled set to false?[/yellow]"
        )
        return
    console.print()
    console.print(render_waterfall(recent[0]), highlight=False)


@contextmanager
def traced_command() -> Iterator[None]:
    """Report a failed command usefully instead of as a stack trace.

    Two things happen on the way out of an exception.

    **The trace is printed, if there is a failed one.** `--explain` is only useful
    to someone who anticipated needing it, and nobody anticipates a failure. The
    trace names the stage that raised and shows what every stage before it had
    already done, which is strictly more than the exception says on its own.

    **`AssistantError` is reported as a message, not a traceback.** That hierarchy
    is the project's vocabulary for problems an operator must fix — an unknown
    provider, a missing credential, an unreachable database — and each one already
    carries an actionable message. A traceback buries it under frames that describe
    our call stack rather than their problem. Anything *else* is a bug in this
    codebase and keeps its traceback, because for a bug the frames are the point.
    """
    try:
        yield
    except typer.Exit:
        raise
    except Exception as exc:
        recent = RECORDER.recent(limit=1)
        if recent and recent[0].failed:
            error_console.print()
            error_console.print(render_waterfall(recent[0]), highlight=False)
        if isinstance(exc, AssistantError):
            error_console.print(f"\n[red]{type(exc).__name__}:[/red] {exc}\n")
            raise typer.Exit(code=1) from exc
        raise
