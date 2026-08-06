from sqlalchemy.orm import Session

from app.character.domain.aggregates.character import Character
from app.character.domain.ports.character_repository import ICharacterRepository
from app.character.domain.value_objects.player_id import PlayerId
from app.character.infrastructure.persistence.mappers.character_mapper import CharacterMapper
from app.character.infrastructure.persistence.models.character_model import CharacterModel


class SqlAlchemyCharacterRepository(ICharacterRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, character: Character) -> None:
        character_model = CharacterMapper.to_persistence(character)
        self._session.merge(character_model)

    def find_by_player_id(self, player_id: PlayerId) -> Character | None:
        model = (
            self._session.query(CharacterModel).filter_by(player_id=player_id.value).one_or_none()
        )
        return CharacterMapper.to_domain(model) if model else None
