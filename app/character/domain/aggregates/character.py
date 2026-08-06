from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.character.domain.events.character_created import CharacterCreated
from app.character.domain.value_objects.character_id import CharacterId
from app.character.domain.value_objects.player_id import PlayerId
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.tsid import new_tsid


@dataclass
class Character(AggregateRoot):
    id: CharacterId
    player_id: PlayerId
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(player_id: PlayerId) -> Character:
        now = datetime.now()
        character = Character(
            id=CharacterId(new_tsid()), player_id=player_id, created_at=now, updated_at=now
        )
        character._add_domain_event(
            CharacterCreated(
                character_id=character.id,
                player_id=character.player_id,
            )
        )
        return character
