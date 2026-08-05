from dataclasses import dataclass

from app.shared.domain.identifiers.user_id import UserId
from app.character.application.dtos.character_dtos import CharacterProfileDTO
from app.character.application.queries.get_character import (
    GetCharacterQuery,
    GetCharacterQueryHandler,
)


@dataclass(frozen=True)
class GetCharacterProfileQuery:
    user_id: UserId


class GetCharacterProfileQueryHandler:
    def __init__(self, character_handler: GetCharacterQueryHandler) -> None:
        self._character_handler = character_handler

    def __call__(self, query: GetCharacterProfileQuery) -> CharacterProfileDTO:
        character = self._character_handler(GetCharacterQuery(user_id=query.user_id))
        return CharacterProfileDTO(
            player_id=character.player_id,
            user_id=character.user_id,
            name=character.name,
            created_at=character.profile_created_at,
            updated_at=character.profile_updated_at,
        )
