from datetime import datetime

from pydantic import BaseModel


class CharacterSchema(BaseModel):
    character_id: str
    player_id: str
    user_id: str
    name: str
    character_created_at: datetime
    character_updated_at: datetime
    profile_created_at: datetime
    profile_updated_at: datetime


class CharacterProfileSchema(BaseModel):
    player_id: str
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime
