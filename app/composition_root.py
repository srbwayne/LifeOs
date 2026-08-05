from fastapi import Depends

from app.auth.application.commands.register_user import RegisterUserCommandHandler
from app.auth.application.ports.character_factory import ICharacterFactory
from app.auth.dependencies import (
    get_current_user_id,
    get_uow,
    get_user_repository,
    password_hasher,
)
from app.auth.domain.ports.user_repository import IUserRepository
from app.character.application.factories.character_factory import CharacterFactory
from app.character.dependencies import (
    get_character_repository,
    get_player_repository,
)
from app.character.domain.ports.character_repository import ICharacterRepository
from app.character.domain.ports.player_repository import IPlayerRepository
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def get_character_factory(
    player_repo: IPlayerRepository = Depends(get_player_repository),
    character_repo: ICharacterRepository = Depends(get_character_repository),
) -> ICharacterFactory:
    return CharacterFactory(player_repo, character_repo)


def get_register_user_handler(
    user_repo: IUserRepository = Depends(get_user_repository),
    character_factory: ICharacterFactory = Depends(get_character_factory),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> RegisterUserCommandHandler:
    return RegisterUserCommandHandler(
        user_repository=user_repo,
        password_hasher=password_hasher,
        character_factory=character_factory,
        unit_of_work=unit_of_work,
    )


__all__ = [
    'get_current_user_id',
    'get_register_user_handler',
]
