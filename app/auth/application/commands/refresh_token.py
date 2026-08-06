import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.auth.application.dtos.token_dtos import TokenDTO
from app.auth.application.services.token_service import TokenService
from app.auth.domain.errors.user_errors import InvalidSessionError
from app.auth.domain.ports.session_repository import ISessionRepository
from app.shared.application.unit_of_work import IUnitOfWork


@dataclass(frozen=True)
class RefreshTokenCommand:
    refresh_token: str


class RefreshTokenCommandHandler:
    def __init__(
        self,
        token_service: TokenService,
        session_repository: ISessionRepository,
        unit_of_work: IUnitOfWork,
    ):
        self._token_service = token_service
        self._session_repository = session_repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: RefreshTokenCommand) -> TokenDTO:
        with self._unit_of_work as uow:
            self._token_service.decode_token(
                command.refresh_token,
                expected_type="refresh",
            )
            refresh_token_hash = hashlib.sha256(command.refresh_token.encode()).hexdigest()

            session = self._session_repository.find_by_refresh_token_hash(refresh_token_hash)
            if not session:
                raise InvalidSessionError()

            new_tokens = self._token_service.generate_tokens(session.user_id)
            new_refresh_token_hash = hashlib.sha256(new_tokens.refresh_token.encode()).hexdigest()
            new_expires_at = datetime.now() + timedelta(days=7)

            session.refresh(new_refresh_token_hash, new_expires_at)
            self._session_repository.save(session)
            uow.commit()

            return new_tokens
