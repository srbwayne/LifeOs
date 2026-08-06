from typing import Protocol

from app.character.domain.aggregates.player import Player
from app.shared.domain.identifiers.user_id import UserId


class IPlayerRepository(Protocol):
    def save(self, player: Player) -> None: ...

    def find_by_user_id(self, user_id: UserId) -> Player | None: ...
