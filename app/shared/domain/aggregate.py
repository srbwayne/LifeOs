from typing import TypeVar

from app.shared.domain.domain_event import DomainEvent

T = TypeVar("T", bound="AggregateRoot")


class AggregateRoot:
    """Classe base para Aggregate Roots."""

    def __init__(self) -> None:
        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> list[DomainEvent]:
        if not hasattr(self, "_domain_events"):
            self._domain_events = []
        return self._domain_events

    def _add_domain_event(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)

    def clear_domain_events(self) -> None:
        self.domain_events.clear()
