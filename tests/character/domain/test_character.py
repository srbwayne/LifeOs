from app.character.domain.aggregates.character import Character
from app.character.domain.events.character_created import CharacterCreated
from app.character.domain.value_objects.player_id import PlayerId


def test_character_creation_uses_identity_and_raises_event():
    player_id = PlayerId("player-1")

    character = Character.create(player_id)

    assert character.player_id == player_id
    assert character.id.value
    assert len(character.domain_events) == 1
    event = character.domain_events[0]
    assert isinstance(event, CharacterCreated)
    assert event.character_id == character.id
    assert event.player_id == player_id
