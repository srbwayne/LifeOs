import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
    ProgressionDeliveryRepository,
)
from app.read.infrastructure.persistence.mappers.progression_delivery_mapper import (
    ProgressionDeliveryMapper,
)
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,
)


class SqlAlchemyProgressionDeliveryRepository(ProgressionDeliveryRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, intent: ProgressionDeliveryIntent) -> None:
        self._session.add(ProgressionDeliveryMapper.to_persistence(intent))

    def get_by_id(self, delivery_id: str) -> ProgressionDeliveryIntent | None:
        model = self._session.get(ProgressionDeliveryModel, delivery_id)
        return ProgressionDeliveryMapper.to_domain(model) if model else None

    def list_unresolved(self) -> tuple[ProgressionDeliveryIntent, ...]:
        statement = (
            select(ProgressionDeliveryModel)
            .where(
                ProgressionDeliveryModel.status != "DELIVERED",
                ProgressionDeliveryModel.last_error.not_in(
                    ("http_status_400", "http_status_409")
                ),
            )
            .order_by(
                ProgressionDeliveryModel.subject_namespace.asc(),
                ProgressionDeliveryModel.subject_external_id.asc(),
                ProgressionDeliveryModel.created_at.asc(),
                ProgressionDeliveryModel.id.asc(),
            )
        )
        return tuple(
            ProgressionDeliveryMapper.to_domain(model)
            for model in self._session.scalars(statement).all()
        )

    def mark_delivered(self, delivery_id: str, delivered_at: datetime.datetime) -> None:
        model = self._session.get(ProgressionDeliveryModel, delivery_id)
        if model is None:
            raise LookupError(f"Progression delivery {delivery_id!r} not found.")
        model.status = "DELIVERED"
        model.attempt_count += 1
        model.last_attempt_at = delivered_at
        model.delivered_at = delivered_at
        model.last_error = None

    def mark_failed(self, delivery_id: str, attempt_at: datetime.datetime, error: str) -> None:
        model = self._session.get(ProgressionDeliveryModel, delivery_id)
        if model is None:
            raise LookupError(f"Progression delivery {delivery_id!r} not found.")
        model.status = "FAILED"
        model.attempt_count += 1
        model.last_attempt_at = attempt_at
        model.last_error = error[:500]
