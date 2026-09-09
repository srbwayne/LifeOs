from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapy_session import TherapySession
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.therapy.infrastructure.persistence.models.therapy_session_model import (
    TherapySessionModel,
)


class TherapySessionMapper:
    @staticmethod
    def to_domain(model: TherapySessionModel) -> TherapySession:
        return TherapySession.restore(
            id=TherapySessionId.from_value(model.id),
            owner_id=UserId.from_value(model.user_id),
            therapist_id=TherapistId.from_value(model.therapist_id),
            occurred_at=canonicalize_utc_datetime(model.occurred_at),
            private_note=model.private_note,
        )

    @staticmethod
    def to_persistence(entity: TherapySession) -> TherapySessionModel:
        return TherapySessionModel(
            id=entity.id.to_persistence(),
            user_id=entity.owner_id.to_persistence(),
            therapist_id=entity.therapist_id.to_persistence(),
            occurred_at=entity.occurred_at,
            private_note=entity.private_note,
        )
