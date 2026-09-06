from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,
)
from app.shared.domain.identifiers.user_id import UserId


class ProgressionDeliveryMapper:
    @staticmethod
    def to_persistence(intent: ProgressionDeliveryIntent) -> ProgressionDeliveryModel:
        return ProgressionDeliveryModel(
            id=intent.id,
            reading_session_id=intent.reading_session_id.to_persistence(),
            owner_id=intent.owner_id.to_persistence(),
            pages_read=intent.pages_read,
            status=intent.status,
            attempt_count=intent.attempt_count,
            last_error=intent.last_error,
            created_at=intent.created_at,
            updated_at=intent.updated_at,
            last_attempt_at=intent.last_attempt_at,
            delivered_at=intent.delivered_at,
        )

    @staticmethod
    def to_domain(model: ProgressionDeliveryModel) -> ProgressionDeliveryIntent:
        return ProgressionDeliveryIntent(
            id=model.id,
            reading_session_id=ReadingSessionId.from_value(model.reading_session_id),
            owner_id=UserId.from_value(model.owner_id),
            pages_read=model.pages_read,
            status=model.status,
            attempt_count=model.attempt_count,
            last_error=model.last_error,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_attempt_at=model.last_attempt_at,
            delivered_at=model.delivered_at,
        )
