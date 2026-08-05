from typing import Protocol, List, Type, Dict, Callable
from app.shared.domain.domain_event import DomainEvent

class EventHandler(Protocol):
    def __call__(self, event: DomainEvent) -> None:
        ...

class IEventBus(Protocol):
    def publish(self, events: List[DomainEvent]) -> None:
        ...

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        ...

# Implementação simples em memória
class InMemoryEventBus(IEventBus):
    def __init__(self) -> None:
        self._handlers: Dict[Type[DomainEvent], List[EventHandler]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            event_type = type(event)
            if event_type in self._handlers:
                for handler in self._handlers[event_type]:
                    try:
                        handler(event)
                    except Exception as e:
                        # Em um sistema real, aqui haveria um log robusto
                        print(f"Error handling event {event_type.__name__}: {e}")
