from __future__ import annotations

import datetime

from sqlalchemy import and_, exists, or_, select
from sqlalchemy.orm import Session

from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
    ProgressionDeliveryRepository,
)
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.infrastructure.persistence.mappers.progression_delivery_mapper import (
    ProgressionDeliveryMapper,
)
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,
)
from app.shared.application.event_bus import InMemoryEventBus
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

_TERMINAL_ERRORS = ("http_status_400", "http_status_409")


class SqlAlchemyProgressionDeliveryRepository(ProgressionDeliveryRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, intent: ProgressionDeliveryIntent) -> None:
        self._session.add(ProgressionDeliveryMapper.to_persistence(intent))

    def get_by_id(self, delivery_id: str) -> ProgressionDeliveryIntent | None:
        model = self._session.get(ProgressionDeliveryModel, delivery_id)
        return ProgressionDeliveryMapper.to_domain(model) if model else None

    def get_by_reading_session_id(
        self, reading_session_id: ReadingSessionId
    ) -> ProgressionDeliveryIntent | None:
        model = self._session.scalar(
            select(ProgressionDeliveryModel).where(
                ProgressionDeliveryModel.reading_session_id == reading_session_id.to_persistence()
            )
        )
        return ProgressionDeliveryMapper.to_domain(model) if model else None

    def list_unresolved(self) -> tuple[ProgressionDeliveryIntent, ...]:
        statement = (
            select(ProgressionDeliveryModel)
            .where(
                ProgressionDeliveryModel.status != "DELIVERED",
                or_(
                    ProgressionDeliveryModel.last_error.is_(None),
                    ProgressionDeliveryModel.last_error.not_in(_TERMINAL_ERRORS),
                ),
            )
            .order_by(
                ProgressionDeliveryModel.owner_id.asc(),
                ProgressionDeliveryModel.created_at.asc(),
                ProgressionDeliveryModel.id.asc(),
            )
        )
        return tuple(
            ProgressionDeliveryMapper.to_domain(model)
            for model in self._session.scalars(statement).all()
        )

    def has_older_blocking(self, delivery_id: str) -> bool:
        candidate = self._session.get(ProgressionDeliveryModel, delivery_id)
        if candidate is None:
            return False

        older = (
            select(ProgressionDeliveryModel.id)
            .where(
                ProgressionDeliveryModel.owner_id == candidate.owner_id,
                ProgressionDeliveryModel.status != "DELIVERED",
                or_(
                    ProgressionDeliveryModel.last_error.is_(None),
                    ProgressionDeliveryModel.last_error.not_in(_TERMINAL_ERRORS),
                ),
                or_(
                    ProgressionDeliveryModel.created_at < candidate.created_at,
                    and_(
                        ProgressionDeliveryModel.created_at == candidate.created_at,
                        ProgressionDeliveryModel.id < candidate.id,
                    ),
                ),
            )
            .limit(1)
        )
        return self._session.scalar(exists(older).select()) is True

    def mark_delivered(self, delivery_id: str, delivered_at: datetime.datetime) -> None:
        model = self._required(delivery_id)
        model.status = "DELIVERED"
        model.attempt_count += 1
        model.last_error = None
        model.last_attempt_at = delivered_at
        model.delivered_at = delivered_at
        model.updated_at = delivered_at

    def mark_failed(self, delivery_id: str, attempt_at: datetime.datetime, error: str) -> None:
        model = self._required(delivery_id)
        model.status = "FAILED"
        model.attempt_count += 1
        model.last_error = error[:500]
        model.last_attempt_at = attempt_at
        model.updated_at = attempt_at

    def _required(self, delivery_id: str) -> ProgressionDeliveryModel:
        model = self._session.get(ProgressionDeliveryModel, delivery_id)
        if model is None:
            raise LookupError(f"Progression delivery {delivery_id!r} not found.")
        return model


class SqlAlchemyProgressionDeliveryTransaction:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None
        self._unit_of_work: SqlAlchemyUnitOfWork | None = None
        self.repository: SqlAlchemyProgressionDeliveryRepository

    def __enter__(self) -> SqlAlchemyProgressionDeliveryTransaction:
        self._session = self._session_factory()
        self._unit_of_work = SqlAlchemyUnitOfWork(self._session, InMemoryEventBus())
        self._unit_of_work.__enter__()
        self.repository = SqlAlchemyProgressionDeliveryRepository(self._session)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._unit_of_work is not None:
            self._unit_of_work.__exit__(exc_type, exc_value, traceback)
        if self._session is not None:
            self._session.close()

    def commit(self) -> None:
        if self._unit_of_work is None:
            raise RuntimeError("Delivery transaction is not active.")
        self._unit_of_work.commit()
