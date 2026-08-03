"""Outbound adapters: OSC presented to other ecosystems.

The inverse of `providers/`. A provider brings an external system *into* OSC behind
one of the five protocols; an integration exposes OSC *to* an external system.

Nothing here is imported by the rest of the package, and nothing here may be
imported by it — that one-way rule is what stops an outbound adapter from becoming
a dependency of the core. Modules are imported directly by their consumer:

    from osc_assistant.integrations.langchain import OSCRetriever
"""

from __future__ import annotations
