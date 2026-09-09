from dataclasses import dataclass

from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.application.ports.therapist_read_repository import ITherapistReadRepository


@dataclass(frozen=True)
class ListTherapistsQuery:
    owner_id: UserId


class ListTherapistsQueryHandler:
    def __init__(self, repository: ITherapistReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: ListTherapistsQuery) -> tuple[TherapistDTO, ...]:
        return self._repository.list_by_owner(query.owner_id)
