from dataclasses import dataclass

from app.character.application.dtos.character_dtos import CharacterDTO
from app.character.domain.errors.character_errors import CharacterNotFoundError
from app.character.domain.ports.character_repository import ICharacterRepository
from app.character.domain.ports.player_repository import IPlayerRepository
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetCharacterQuery:
    user_id: UserId


class GetCharacterQueryHandler:
    def __init__(
        self,
        player_repository: IPlayerRepository,
        character_repository: ICharacterRepository,
    ) -> None:
        self._player_repository = player_repository
        self._character_repository = character_repository

    def __call__(self, query: GetCharacterQuery) -> CharacterDTO:
        player = self._player_repository.find_by_user_id(query.user_id)
        if player is None:
            raise CharacterNotFoundError()

        character = self._character_repository.find_by_player_id(player.id)
        if character is None:
            raise CharacterNotFoundError()

        return CharacterDTO(
            character_id=character.id.value,
            player_id=player.id.value,
            user_id=player.user_id.value,
            name=player.name.value,
            character_created_at=character.created_at,
            character_updated_at=character.updated_at,
            profile_created_at=player.created_at,
            profile_updated_at=player.updated_at,
        )
