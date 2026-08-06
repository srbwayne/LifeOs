from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.character.domain.value_objects.player_id import PlayerId
from app.character.domain.value_objects.player_name import PlayerName
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId
from app.shared.domain.tsid import new_tsid


@dataclass
class Player(AggregateRoot):
    id: PlayerId
    user_id: UserId
    name: PlayerName
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(user_id: UserId, name: PlayerName) -> Player:
        now = datetime.now()
        return Player(
            id=PlayerId(new_tsid()), user_id=user_id, name=name, created_at=now, updated_at=now
        )
