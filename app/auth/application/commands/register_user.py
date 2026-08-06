from dataclasses import dataclass

from app.auth.application.ports.character_factory import ICharacterFactory
from app.auth.domain.aggregates.user import User
from app.auth.domain.errors.user_errors import UserAlreadyExistsError
from app.auth.domain.ports.password_hasher import IPasswordHasher
from app.auth.domain.ports.user_repository import IUserRepository
from app.auth.domain.value_objects.email import Email
from app.shared.application.unit_of_work import IUnitOfWork


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str


class RegisterUserCommandHandler:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        character_factory: ICharacterFactory,
        unit_of_work: IUnitOfWork,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._character_factory = character_factory
        self._unit_of_work = unit_of_work

    def __call__(self, command: RegisterUserCommand) -> None:
        with self._unit_of_work as uow:
            email = Email(command.email)
            if self._user_repository.find_by_email(email):
                raise UserAlreadyExistsError()

            hashed_password = self._password_hasher.hash(command.password)
            user = User.register(email=email, hashed_password=hashed_password)

            self._user_repository.save(user)
            character_aggregates = self._character_factory.create_initial(
                user_id=user.id,
                email=user.email.value,
            )

            uow.track_aggregate(user)
            for aggregate in character_aggregates:
                uow.track_aggregate(aggregate)
            uow.commit()
