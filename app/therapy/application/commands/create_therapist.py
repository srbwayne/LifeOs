from dataclasses import dataclass

from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.ports.therapist_repository import ITherapistRepository


@dataclass(frozen=True)
class CreateTherapistCommand:
    owner_id: UserId
    name: str


class CreateTherapistCommandHandler:
    def __init__(self, repository: ITherapistRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: CreateTherapistCommand) -> TherapistDTO:
        with self._unit_of_work as uow:
            therapist = Therapist.create(owner_id=command.owner_id, name=command.name)
            self._repository.save(therapist)
            uow.commit()
        return TherapistDTO(therapist.id.value, therapist.name, therapist.active)
