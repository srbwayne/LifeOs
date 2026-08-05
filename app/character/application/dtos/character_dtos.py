from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CharacterDTO:
    character_id: str
    player_id: str
    user_id: str
    name: str
    character_created_at: datetime
    character_updated_at: datetime
    profile_created_at: datetime
    profile_updated_at: datetime


@dataclass(frozen=True)
class CharacterProfileDTO:
    player_id: str
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime
