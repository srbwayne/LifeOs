import hashlib
from dataclasses import dataclass

from app.auth.domain.ports.session_repository import ISessionRepository
from app.shared.application.unit_of_work import IUnitOfWork


@dataclass(frozen=True)
class LogoutCommand:
    refresh_token: str


class LogoutCommandHandler:
    def __init__(self, session_repository: ISessionRepository, unit_of_work: IUnitOfWork):
        self._session_repository = session_repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: LogoutCommand) -> None:
        with self._unit_of_work as uow:
            refresh_token_hash = hashlib.sha256(command.refresh_token.encode()).hexdigest()
            session = self._session_repository.find_by_refresh_token_hash(refresh_token_hash)

            if session:
                session.revoke()
                self._session_repository.save(session)
                uow.commit()
