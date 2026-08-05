from datetime import datetime

import pytest

from app.auth.domain.value_objects.user_id import UserId
from app.character.application.queries.get_character import (
    GetCharacterQuery,
    GetCharacterQueryHandler,
)
from app.character.application.queries.get_character_profile import (
    GetCharacterProfileQuery,
    GetCharacterProfileQueryHandler,
)
from app.character.domain.aggregates.character import Character
from app.character.domain.aggregates.player import Player
from app.character.domain.errors.character_errors import CharacterNotFoundError
from app.character.domain.value_objects.character_id import CharacterId
from app.character.domain.value_objects.player_id import PlayerId
from app.character.domain.value_objects.player_name import PlayerName


class PlayerRepositoryStub:
    def __init__(self, player: Player | None) -> None:
        self.player = player

    def save(self, player: Player) -> None:
        self.player = player

    def find_by_user_id(self, user_id: UserId) -> Player | None:
        if self.player and self.player.user_id == user_id:
            return self.player
        return None


class CharacterRepositoryStub:
    def __init__(self, character: Character | None) -> None:
        self.character = character

    def save(self, character: Character) -> None:
        self.character = character

    def find_by_player_id(self, player_id: PlayerId) -> Character | None:
        if self.character and self.character.player_id == player_id:
            return self.character
        return None


def build_handlers():
    now = datetime(2026, 8, 4, 12, 0, 0)
    user_id = UserId("user-1")
    player = Player(
        id=PlayerId("player-1"),
        user_id=user_id,
        name=PlayerName("player"),
        created_at=now,
        updated_at=now,
    )
    character = Character(
        id=CharacterId("character-1"),
        player_id=player.id,
        created_at=now,
        updated_at=now,
    )
    character_handler = GetCharacterQueryHandler(
        PlayerRepositoryStub(player),
        CharacterRepositoryStub(character),
    )
    return user_id, character_handler, GetCharacterProfileQueryHandler(character_handler)


def test_get_character_returns_persistent_identity_and_profile():
    user_id, handler, _ = build_handlers()

    result = handler(GetCharacterQuery(user_id=user_id))

    assert result.character_id == "character-1"
    assert result.player_id == "player-1"
    assert result.user_id == "user-1"
    assert result.name == "player"


def test_get_character_profile_returns_only_persistent_profile():
    user_id, _, handler = build_handlers()

    result = handler(GetCharacterProfileQuery(user_id=user_id))

    assert result.player_id == "player-1"
    assert result.user_id == "user-1"
    assert result.name == "player"
    assert not hasattr(result, "experience")
    assert not hasattr(result, "level")


def test_get_character_rejects_another_user_context():
    _, handler, _ = build_handlers()

    with pytest.raises(CharacterNotFoundError):
        handler(GetCharacterQuery(user_id=UserId("another-user")))
