import hashlib
from dataclasses import dataclass

from app.auth.domain.errors.user_errors import (
    InvalidPasswordResetTokenError,
    UserNotFoundError,
)
from app.auth.domain.ports.password_hasher import IPasswordHasher
from app.auth.domain.ports.password_reset_repository import IPasswordResetTokenRepository
from app.auth.domain.ports.user_repository import IUserRepository
from app.shared.application.unit_of_work import IUnitOfWork


@dataclass(frozen=True)
class ResetPasswordCommand:
    token: str
    new_password: str


class ResetPasswordCommandHandler:
    def __init__(
        self,
        token_repository: IPasswordResetTokenRepository,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        unit_of_work: IUnitOfWork,
    ):
        self._token_repo = token_repository
        self._user_repo = user_repository
        self._password_hasher = password_hasher
        self._unit_of_work = unit_of_work

    def __call__(self, command: ResetPasswordCommand) -> None:
        with self._unit_of_work as uow:
            token_hash = hashlib.sha256(command.token.encode()).hexdigest()
            token_aggregate = self._token_repo.find_by_token_hash(token_hash)

            if not token_aggregate:
                raise InvalidPasswordResetTokenError()

            token_aggregate.use()

            user = self._user_repo.find_by_id(token_aggregate.user_id)
            if not user:
                raise UserNotFoundError()

            new_hashed_password = self._password_hasher.hash(command.new_password)
            user.change_password(new_hashed_password)

            self._user_repo.save(user)
            self._token_repo.save(token_aggregate)
            uow.commit()
