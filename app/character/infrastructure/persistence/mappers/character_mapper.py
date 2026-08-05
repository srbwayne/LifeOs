from app.character.domain.aggregates.character import Character
from app.character.infrastructure.persistence.models.character_model import CharacterModel
from app.character.domain.value_objects.character_id import CharacterId
from app.character.domain.value_objects.player_id import PlayerId

class CharacterMapper:
    @staticmethod
    def to_domain(model: CharacterModel) -> Character:
        return Character(
            id=CharacterId(model.id),
            player_id=PlayerId(model.player_id),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(entity: Character) -> CharacterModel:
        return CharacterModel(
            id=entity.id.value,
            player_id=entity.player_id.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
