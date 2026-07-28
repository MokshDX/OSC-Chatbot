"""A minimal registry so new providers are additions, never edits.

This exists to solve one concrete problem: selecting an implementation by a name
that comes from configuration, without any module in the call path importing every
possible implementation. A provider module registers itself on import; the
composition root imports the provider package once; business logic never sees a
provider class at all.

Deliberately not entry-point based. Entry points would let providers ship as
separate distributions, which we do not need — every provider here lives in this
repository, and a plain dict is far easier to reason about and test.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .errors import UnknownComponentError


class ComponentConfig(BaseModel):
    """Selects and configures one swappable component.

    `options` is intentionally untyped here: each factory validates it into its own
    typed settings model. That keeps provider-specific fields out of the global
    settings schema, so adding a provider never touches shared configuration code.
    """

    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str = ""
    options: dict[str, Any] = Field(default_factory=dict)


type Factory[T] = Callable[[ComponentConfig], T]


class Registry[T]:
    """Maps a provider name to a factory for one kind of component."""

    def __init__(self, kind: str) -> None:
        self._kind = kind
        self._factories: dict[str, Factory[T]] = {}

    def register(self, name: str) -> Callable[[Factory[T]], Factory[T]]:
        """Decorator registering a factory under `name`.

        Re-registering a name replaces the previous factory, which lets a test or a
        downstream deployment override a built-in provider without patching it.
        """

        def decorator(factory: Factory[T]) -> Factory[T]:
            self._factories[name] = factory
            return factory

        return decorator

    def create(self, config: ComponentConfig) -> T:
        try:
            factory = self._factories[config.provider]
        except KeyError:
            raise UnknownComponentError(self._kind, config.provider, self.names()) from None
        return factory(config)

    def names(self) -> list[str]:
        return sorted(self._factories)

    def __contains__(self, name: object) -> bool:
        return name in self._factories
