from sqlalchemy.orm import Session

from app.shared.application.event_bus import IEventBus
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.aggregate import AggregateRoot


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: Session, event_bus: IEventBus):
        self.session = session
        self._event_bus = event_bus
        self._tracked_aggregates: list[AggregateRoot] = []

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type:
            self.session.rollback()

    def track_aggregate(self, aggregate: AggregateRoot):
        if aggregate not in self._tracked_aggregates:
            self._tracked_aggregates.append(aggregate)

    def flush(self):
        self.session.flush()

    def _publish_domain_events(self):
        events = []
        for aggregate in self._tracked_aggregates:
            events.extend(aggregate.domain_events)
            aggregate.clear_domain_events()

        self._event_bus.publish(events)
        self._tracked_aggregates.clear()

    def commit(self):
        self.session.commit()
        self._publish_domain_events()

    def rollback(self):
        self.session.rollback()
