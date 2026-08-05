from fastapi import Depends

from app.character.application.queries.get_character import GetCharacterQueryHandler
from app.character.application.queries.get_character_profile import (
    GetCharacterProfileQueryHandler,
)
from app.character.domain.ports.character_repository import ICharacterRepository
from app.character.domain.ports.player_repository import IPlayerRepository
from app.character.infrastructure.persistence.repositories.character_repository import (
    SqlAlchemyCharacterRepository,
)
from app.character.infrastructure.persistence.repositories.player_repository import (
    SqlAlchemyPlayerRepository,
)
from app.shared.infrastructure.database import get_db


def get_player_repository(db=Depends(get_db)) -> IPlayerRepository:
    return SqlAlchemyPlayerRepository(db)


def get_character_repository(db=Depends(get_db)) -> ICharacterRepository:
    return SqlAlchemyCharacterRepository(db)


def get_character_query_handler(
    player_repository: IPlayerRepository = Depends(get_player_repository),
    character_repository: ICharacterRepository = Depends(get_character_repository),
) -> GetCharacterQueryHandler:
    return GetCharacterQueryHandler(player_repository, character_repository)


def get_character_profile_query_handler(
    character_handler: GetCharacterQueryHandler = Depends(get_character_query_handler),
) -> GetCharacterProfileQueryHandler:
    return GetCharacterProfileQueryHandler(character_handler)
