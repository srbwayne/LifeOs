from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.domain.value_objects.user_id import UserId
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.character.domain.aggregates.character import Character
from app.character.domain.aggregates.player import Player
from app.character.domain.value_objects.player_name import PlayerName
from app.character.infrastructure.persistence.repositories.character_repository import (
    SqlAlchemyCharacterRepository,
)
from app.character.infrastructure.persistence.repositories.player_repository import (
    SqlAlchemyPlayerRepository,
)
from app.shared.infrastructure.database import Base


def test_repositories_restore_one_to_one_character_identity():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    now = datetime(2026, 8, 4, 12, 0, 0)

    with session_factory() as session:
        user_id = UserId("user-1")
        session.add(
            UserModel(
                id=user_id.value,
                email="character@example.com",
                hashed_password="hash",
                created_at=now,
                updated_at=now,
            )
        )
        player = Player.create(user_id, PlayerName("character"))
        character = Character.create(player.id)
        player_repository = SqlAlchemyPlayerRepository(session)
        character_repository = SqlAlchemyCharacterRepository(session)
        player_repository.save(player)
        character_repository.save(character)
        session.commit()

        restored_player = player_repository.find_by_user_id(user_id)
        restored_character = character_repository.find_by_player_id(player.id)

        assert restored_player == player
        assert restored_character == character

    Base.metadata.drop_all(engine)
    engine.dispose()
