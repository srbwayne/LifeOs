from dataclasses import dataclass

from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.application.errors import TherapistNotFoundError
from app.therapy.domain.ports.therapist_repository import ITherapistRepository
from app.therapy.domain.value_objects.therapist_id import TherapistId


@dataclass(frozen=True)
class ReactivateTherapistCommand:
    owner_id: UserId
    therapist_id: TherapistId


class ReactivateTherapistCommandHandler:
    def __init__(self, repository: ITherapistRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: ReactivateTherapistCommand) -> TherapistDTO:
        with self._unit_of_work as uow:
            therapist = self._repository.get_by_id_and_owner(command.therapist_id, command.owner_id)
            if therapist is None:
                raise TherapistNotFoundError()
            therapist.activate()
            self._repository.save(therapist)
            uow.commit()
        return TherapistDTO(therapist.id.value, therapist.name, therapist.active)
