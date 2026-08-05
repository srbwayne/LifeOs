import pytest

from app.auth.domain.value_objects.user_id import UserId
from app.character.domain.aggregates.player import Player
from app.character.domain.value_objects.player_name import PlayerName


def test_player_creation_preserves_user_identity_and_profile():
    user_id = UserId("user-1")

    player = Player.create(user_id=user_id, name=PlayerName(" Player "))

    assert player.user_id == user_id
    assert player.name.value == "Player"
    assert player.id.value


def test_player_name_cannot_be_empty():
    with pytest.raises(ValueError, match="Player name cannot be empty"):
        PlayerName("   ")
