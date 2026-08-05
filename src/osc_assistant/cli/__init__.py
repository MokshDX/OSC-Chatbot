"""Command line interface.

Split across three modules by what a command is *for*, not by what it touches:
`core` runs the pipelines, `diagnose` explains the system, `evaluate` measures it.
A flat command surface either way — `osc-assistant doctor` rather than
`osc-assistant diagnose doctor` — because sub-command nesting costs typing on every
invocation and buys grouping that a dozen commands do not need.

    Running things       serve · ingest · ask · search
    Understanding things doctor · config · providers · status · eval
    Looking at data      documents · document · chunk · trace
"""

from __future__ import annotations

import typer

from . import core, diagnose, evaluate

app = typer.Typer(
    name="osc-assistant",
    help="OSC internal knowledge assistant.",
    no_args_is_help=True,
    add_completion=False,
)

# Registered by merging the sub-apps rather than mounting them, which keeps the
# commands top-level while letting each module own its own group.
for _sub in (core.app, diagnose.app, evaluate.app):
    app.registered_commands.extend(_sub.registered_commands)

__all__ = ["app"]


if __name__ == "__main__":  # pragma: no cover
    app()
