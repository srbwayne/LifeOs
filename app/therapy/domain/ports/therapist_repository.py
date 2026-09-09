from typing import Protocol

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.value_objects.therapist_id import TherapistId


class ITherapistRepository(Protocol):
    def save(self, therapist: Therapist) -> None: ...

    def get_by_id_and_owner(
        self,
        therapist_id: TherapistId,
        owner_id: UserId,
    ) -> Therapist | None: ...
