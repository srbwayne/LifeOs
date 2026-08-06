from sqlalchemy.orm import Session

from app.character.domain.aggregates.player import Player
from app.character.domain.ports.player_repository import IPlayerRepository
from app.character.infrastructure.persistence.mappers.player_mapper import PlayerMapper
from app.character.infrastructure.persistence.models.player_model import PlayerModel
from app.shared.domain.identifiers.user_id import UserId


class SqlAlchemyPlayerRepository(IPlayerRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, player: Player) -> None:
        player_model = PlayerMapper.to_persistence(player)
        self._session.merge(player_model)

    def find_by_user_id(self, user_id: UserId) -> Player | None:
        model = (
            self._session.query(PlayerModel)
            .filter_by(user_id=user_id.to_persistence())
            .one_or_none()
        )
        return PlayerMapper.to_domain(model) if model else None
