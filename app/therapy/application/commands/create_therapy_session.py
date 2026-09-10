from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime

from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.dtos.therapy_session_dto import TherapySessionDetailDTO
from app.therapy.application.errors import InactiveTherapistError, TherapistNotFoundError
from app.therapy.domain.aggregates.therapy_session import TherapySession
from app.therapy.domain.ports.therapist_repository import ITherapistRepository
from app.therapy.domain.ports.therapy_session_repository import ITherapySessionRepository
from app.therapy.domain.value_objects.therapist_id import TherapistId


@dataclass(frozen=True)
class CreateTherapySessionCommand:
    owner_id: UserId
    therapist_id: TherapistId
    occurred_at: datetime
    private_note: str | None = field(default=None, repr=False)


class CreateTherapySessionCommandHandler:
    def __init__(
        self,
        therapist_repository: ITherapistRepository,
        session_repository: ITherapySessionRepository,
        unit_of_work: IUnitOfWork,
        now_provider: Callable[[], datetime],
    ) -> None:
        self._therapists = therapist_repository
        self._sessions = session_repository
        self._uow = unit_of_work
        self._now = now_provider

    def __call__(self, command: CreateTherapySessionCommand) -> TherapySessionDetailDTO:
        with self._uow as uow:
            therapist = self._therapists.get_by_id_and_owner(command.therapist_id, command.owner_id)
            if therapist is None:
                raise TherapistNotFoundError()
            if not therapist.active:
                raise InactiveTherapistError()
            session = TherapySession.create(
                command.owner_id,
                command.therapist_id,
                command.occurred_at,
                self._now(),
                command.private_note,
            )
            self._sessions.save(session)
            uow.commit()
        return TherapySessionDetailDTO(
            session.id.value,
            therapist.id.value,
            therapist.name,
            session.occurred_at,
            session.private_note,
        )
