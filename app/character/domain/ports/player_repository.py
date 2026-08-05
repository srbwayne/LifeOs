from typing import Protocol
from app.auth.domain.value_objects.user_id import UserId
from app.character.domain.aggregates.player import Player

class IPlayerRepository(Protocol):
    def save(self, player: Player) -> None:
        ...

    def find_by_user_id(self, user_id: UserId) -> Player | None:
        ...
