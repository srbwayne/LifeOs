from dataclasses import dataclass

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.application.errors import TherapistNotFoundError
from app.therapy.domain.ports.therapist_repository import ITherapistRepository
from app.therapy.domain.value_objects.therapist_id import TherapistId


@dataclass(frozen=True)
class GetTherapistQuery:
    owner_id: UserId
    therapist_id: TherapistId


class GetTherapistQueryHandler:
    def __init__(self, repository: ITherapistRepository) -> None:
        self._repository = repository

    def __call__(self, query: GetTherapistQuery) -> TherapistDTO:
        therapist = self._repository.get_by_id_and_owner(query.therapist_id, query.owner_id)
        if therapist is None:
            raise TherapistNotFoundError()
        return TherapistDTO(therapist.id.value, therapist.name, therapist.active)
