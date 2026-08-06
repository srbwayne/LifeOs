from typing import Protocol

from app.character.domain.aggregates.character import Character
from app.character.domain.value_objects.player_id import PlayerId


class ICharacterRepository(Protocol):
    def save(self, character: Character) -> None: ...

    def find_by_player_id(self, player_id: PlayerId) -> Character | None: ...
