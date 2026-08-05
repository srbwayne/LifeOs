from dataclasses import dataclass
from datetime import datetime, timedelta
from app.shared.application.unit_of_work import IUnitOfWork
from app.auth.domain.aggregates.session import Session
from app.auth.domain.errors.user_errors import InvalidCredentialsError
from app.auth.domain.ports.password_hasher import IPasswordHasher
from app.auth.domain.ports.user_repository import IUserRepository
from app.auth.domain.ports.session_repository import ISessionRepository
from app.auth.domain.value_objects.email import Email
from app.auth.application.dtos.token_dtos import TokenDTO
from app.auth.application.services.token_service import TokenService
import hashlib

@dataclass(frozen=True)
class LoginCommand:
    email: str
    password: str
    user_agent: str | None
    ip_address: str | None

class LoginCommandHandler:
    def __init__(
        self,
        user_repository: IUserRepository,
        session_repository: ISessionRepository,
        password_hasher: IPasswordHasher,
        token_service: TokenService,
        unit_of_work: IUnitOfWork,
    ):
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._unit_of_work = unit_of_work

    def __call__(self, command: LoginCommand) -> TokenDTO:
        with self._unit_of_work as uow:
            email = Email(command.email)
            user = self._user_repository.find_by_email(email)

            if not user or not self._password_hasher.verify(command.password, user.hashed_password):
                raise InvalidCredentialsError()

            tokens = self._token_service.generate_tokens(user.id)
            
            refresh_token_hash = hashlib.sha256(tokens.refresh_token.encode()).hexdigest()
            expires_at = datetime.now() + timedelta(days=7)

            session = Session.start(
                user_id=user.id,
                refresh_token_hash=refresh_token_hash,
                expires_at=expires_at,
                user_agent=command.user_agent,
                ip_address=command.ip_address,
            )
            self._session_repository.save(session)
            uow.commit()

            return tokens
