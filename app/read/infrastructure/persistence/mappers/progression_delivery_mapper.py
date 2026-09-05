from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,
)


class ProgressionDeliveryMapper:
    @staticmethod
    def to_persistence(intent: ProgressionDeliveryIntent) -> ProgressionDeliveryModel:
        return ProgressionDeliveryModel(
            id=intent.id,
            reading_session_id=intent.reading_session_id,
            source=intent.source,
            idempotency_key=intent.idempotency_key,
            subject_namespace=intent.subject_namespace,
            subject_external_id=intent.subject_external_id,
            configuration_key=intent.configuration_key,
            configuration_revision=intent.configuration_revision,
            pages_read=intent.pages_read,
            status=intent.status,
            attempt_count=intent.attempt_count,
            created_at=intent.created_at,
            last_attempt_at=intent.last_attempt_at,
            delivered_at=intent.delivered_at,
            last_error=intent.last_error,
        )

    @staticmethod
    def to_domain(model: ProgressionDeliveryModel) -> ProgressionDeliveryIntent:
        return ProgressionDeliveryIntent(
            id=model.id,
            reading_session_id=model.reading_session_id,
            source=model.source,
            idempotency_key=model.idempotency_key,
            subject_namespace=model.subject_namespace,
            subject_external_id=model.subject_external_id,
            configuration_key=model.configuration_key,
            configuration_revision=model.configuration_revision,
            pages_read=model.pages_read,
            status=model.status,
            attempt_count=model.attempt_count,
            created_at=model.created_at,
            last_attempt_at=model.last_attempt_at,
            delivered_at=model.delivered_at,
            last_error=model.last_error,
        )
