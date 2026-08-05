from dataclasses import dataclass

from app.character.domain.value_objects.character_id import CharacterId
from app.character.domain.value_objects.player_id import PlayerId
from app.shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class CharacterCreated(DomainEvent):
    character_id: CharacterId
    player_id: PlayerId
