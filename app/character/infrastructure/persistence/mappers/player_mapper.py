from app.character.domain.aggregates.player import Player
from app.character.domain.value_objects.player_id import PlayerId
from app.character.domain.value_objects.player_name import PlayerName
from app.character.infrastructure.persistence.models.player_model import PlayerModel
from app.shared.domain.identifiers.user_id import UserId


class PlayerMapper:
    @staticmethod
    def to_domain(model: PlayerModel) -> Player:
        return Player(
            id=PlayerId(model.id),
            user_id=UserId.from_value(model.user_id),
            name=PlayerName(model.name),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_persistence(entity: Player) -> PlayerModel:
        return PlayerModel(
            id=entity.id.value,
            user_id=entity.user_id.to_persistence(),
            name=entity.name.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
