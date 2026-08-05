import os

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.shared.infrastructure.database import get_db
from app.shared.application.event_bus import IEventBus, InMemoryEventBus
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

# Importações de Ports e Implementações
from app.auth.domain.ports.password_hasher import IPasswordHasher
from app.auth.infrastructure.services.argon2_password_hasher import Argon2PasswordHasher
from app.auth.domain.ports.user_repository import IUserRepository
from app.auth.infrastructure.persistence.repositories.user_repository import SqlAlchemyUserRepository
from app.auth.domain.ports.session_repository import ISessionRepository
from app.auth.infrastructure.persistence.repositories.session_repository import SqlAlchemySessionRepository
from app.auth.domain.ports.password_reset_repository import IPasswordResetTokenRepository
from app.auth.infrastructure.persistence.repositories.password_reset_repository import SqlAlchemyPasswordResetTokenRepository
from app.auth.application.services.token_service import TokenService
from app.auth.application.ports.character_factory import ICharacterFactory
from app.auth.application.ports.password_reset_notifier import IPasswordResetNotifier
from app.auth.infrastructure.services.smtp_password_reset_notifier import SmtpPasswordResetNotifier
from app.character.application.factories.character_factory import CharacterFactory
from app.character.domain.ports.player_repository import IPlayerRepository
from app.character.infrastructure.persistence.repositories.player_repository import SqlAlchemyPlayerRepository
from app.character.domain.ports.character_repository import ICharacterRepository
from app.character.infrastructure.persistence.repositories.character_repository import SqlAlchemyCharacterRepository

# Importações de Handlers
from app.auth.application.commands.register_user import RegisterUserCommandHandler
from app.auth.application.commands.login import LoginCommandHandler
from app.auth.application.commands.logout import LogoutCommandHandler
from app.auth.application.commands.refresh_token import RefreshTokenCommandHandler
from app.auth.application.commands.request_password_reset import RequestPasswordResetCommandHandler
from app.auth.application.commands.reset_password import ResetPasswordCommandHandler

# --- Configuração Global ---
SECRET_KEY = os.getenv(
    "LIFEOS_SECRET_KEY",
    "lifeos-development-secret-key-change-before-production",
)
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer(auto_error=False)

# --- Instâncias Singleton ---
password_hasher: IPasswordHasher = Argon2PasswordHasher()
token_service: TokenService = TokenService(SECRET_KEY, ALGORITHM)
password_reset_notifier: IPasswordResetNotifier = SmtpPasswordResetNotifier(
    host=os.getenv("LIFEOS_SMTP_HOST", "localhost"),
    port=int(os.getenv("LIFEOS_SMTP_PORT", "25")),
    sender=os.getenv("LIFEOS_SMTP_SENDER", "noreply@lifeos.local"),
)
event_bus: IEventBus = InMemoryEventBus() # Singleton para toda a aplicação

# --- Provedores de Dependência ---
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    from app.auth.domain.errors.user_errors import InvalidSessionError
    from app.auth.domain.value_objects.user_id import UserId

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise InvalidSessionError()
    payload = token_service.decode_token(credentials.credentials, expected_type="access")
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise InvalidSessionError()
    return UserId(subject)

def get_uow(db: Session = Depends(get_db)) -> SqlAlchemyUnitOfWork:
    # Note que o event_bus é um singleton injetado aqui
    return SqlAlchemyUnitOfWork(session=db, event_bus=event_bus)

# Repositórios
def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return SqlAlchemyUserRepository(db)

def get_session_repository(db: Session = Depends(get_db)) -> ISessionRepository:
    return SqlAlchemySessionRepository(db)

def get_password_reset_repository(db: Session = Depends(get_db)) -> IPasswordResetTokenRepository:
    return SqlAlchemyPasswordResetTokenRepository(db)

def get_player_repository(db: Session = Depends(get_db)) -> IPlayerRepository:
    return SqlAlchemyPlayerRepository(db)

def get_character_repository(db: Session = Depends(get_db)) -> ICharacterRepository:
    return SqlAlchemyCharacterRepository(db)

# Fábricas e Serviços
def get_character_factory(
    player_repo: IPlayerRepository = Depends(get_player_repository),
    character_repo: ICharacterRepository = Depends(get_character_repository),
) -> ICharacterFactory:
    return CharacterFactory(player_repo, character_repo)

def get_password_reset_notifier() -> IPasswordResetNotifier:
    return password_reset_notifier

# Handlers
def get_register_user_handler(
    user_repo: IUserRepository = Depends(get_user_repository),
    char_factory: ICharacterFactory = Depends(get_character_factory),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> RegisterUserCommandHandler:
    return RegisterUserCommandHandler(user_repository=user_repo, password_hasher=password_hasher, character_factory=char_factory, unit_of_work=uow)

def get_login_handler(
    user_repo: IUserRepository = Depends(get_user_repository),
    session_repo: ISessionRepository = Depends(get_session_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> LoginCommandHandler:
    return LoginCommandHandler(user_repository=user_repo, session_repository=session_repo, password_hasher=password_hasher, token_service=token_service, unit_of_work=uow)

def get_logout_handler(
    session_repo: ISessionRepository = Depends(get_session_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> LogoutCommandHandler:
    return LogoutCommandHandler(session_repository=session_repo, unit_of_work=uow)

def get_refresh_token_handler(
    session_repo: ISessionRepository = Depends(get_session_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> RefreshTokenCommandHandler:
    return RefreshTokenCommandHandler(token_service=token_service, session_repository=session_repo, unit_of_work=uow)

def get_request_password_reset_handler(
    user_repo: IUserRepository = Depends(get_user_repository),
    token_repo: IPasswordResetTokenRepository = Depends(get_password_reset_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    notifier: IPasswordResetNotifier = Depends(get_password_reset_notifier),
) -> RequestPasswordResetCommandHandler:
    return RequestPasswordResetCommandHandler(
        user_repository=user_repo,
        token_repository=token_repo,
        unit_of_work=uow,
        notifier=notifier,
    )

def get_reset_password_handler(
    token_repo: IPasswordResetTokenRepository = Depends(get_password_reset_repository),
    user_repo: IUserRepository = Depends(get_user_repository),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> ResetPasswordCommandHandler:
    return ResetPasswordCommandHandler(token_repository=token_repo, user_repository=user_repo, password_hasher=password_hasher, unit_of_work=uow)
