from dataclasses import dataclass

from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.errors import TherapySessionNotFoundError
from app.therapy.domain.ports.therapy_session_repository import ITherapySessionRepository
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


@dataclass(frozen=True)
class DeleteTherapySessionCommand:
    owner_id: UserId
    session_id: TherapySessionId


class DeleteTherapySessionCommandHandler:
    def __init__(self, repository: ITherapySessionRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: DeleteTherapySessionCommand) -> None:
        with self._unit_of_work as uow:
            session = self._repository.get_by_id_and_owner(command.session_id, command.owner_id)
            if session is None:
                raise TherapySessionNotFoundError()
            self._repository.delete(session)
            uow.commit()
