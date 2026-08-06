from dataclasses import dataclass

from app.auth.application.ports.password_reset_notifier import IPasswordResetNotifier
from app.auth.domain.aggregates.password_reset import PasswordResetToken
from app.auth.domain.ports.password_reset_repository import IPasswordResetTokenRepository
from app.auth.domain.ports.user_repository import IUserRepository
from app.auth.domain.value_objects.email import Email
from app.shared.application.unit_of_work import IUnitOfWork


@dataclass(frozen=True)
class RequestPasswordResetCommand:
    email: str


class RequestPasswordResetCommandHandler:
    def __init__(
        self,
        user_repository: IUserRepository,
        token_repository: IPasswordResetTokenRepository,
        unit_of_work: IUnitOfWork,
        notifier: IPasswordResetNotifier,
    ):
        self._user_repository = user_repository
        self._token_repository = token_repository
        self._unit_of_work = unit_of_work
        self._notifier = notifier

    def __call__(self, command: RequestPasswordResetCommand) -> None:
        with self._unit_of_work as uow:
            email = Email(command.email)
            user = self._user_repository.find_by_email(email)
            if not user:
                return

            token_aggregate, plain_token = PasswordResetToken.create(user_id=user.id)
            self._token_repository.save(token_aggregate)
            uow.commit()

        self._notifier.send(user.email.value, plain_token)
