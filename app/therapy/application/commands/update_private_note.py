from dataclasses import dataclass, field

from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapy_session_dto import TherapySessionPrivateNoteDTO
from app.therapy.application.errors import TherapySessionNotFoundError
from app.therapy.domain.ports.therapy_session_repository import ITherapySessionRepository
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId


@dataclass(frozen=True)
class UpdatePrivateNoteCommand:
    owner_id: UserId
    session_id: TherapySessionId
    private_note: str | None = field(repr=False)


class UpdatePrivateNoteCommandHandler:
    def __init__(self, repository: ITherapySessionRepository, unit_of_work: IUnitOfWork) -> None:
        self._repository = repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: UpdatePrivateNoteCommand) -> TherapySessionPrivateNoteDTO:
        with self._unit_of_work as uow:
            session = self._repository.get_by_id_and_owner(command.session_id, command.owner_id)
            if session is None:
                raise TherapySessionNotFoundError()
            session.update_private_note(command.private_note)
            self._repository.save(session)
            uow.commit()
        return TherapySessionPrivateNoteDTO(session.id.value, session.private_note)
