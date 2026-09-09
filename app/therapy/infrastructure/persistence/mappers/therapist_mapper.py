from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel


class TherapistMapper:
    @staticmethod
    def to_domain(model: TherapistModel) -> Therapist:
        return Therapist.restore(
            id=TherapistId.from_value(model.id),
            owner_id=UserId.from_value(model.user_id),
            name=model.name,
            active=model.active,
        )

    @staticmethod
    def to_persistence(entity: Therapist) -> TherapistModel:
        return TherapistModel(
            id=entity.id.to_persistence(),
            user_id=entity.owner_id.to_persistence(),
            name=entity.name,
            active=entity.active,
        )
