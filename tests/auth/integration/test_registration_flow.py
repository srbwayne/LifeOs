import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.app_factory import create_app
from app.auth.dependencies import get_db
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.character.infrastructure.persistence.models.character_model import CharacterModel
from app.character.infrastructure.persistence.models.player_model import PlayerModel
from app.shared.infrastructure.database import Base
from app.auth.dependencies import event_bus
from app.character.domain.events.character_created import CharacterCreated


@pytest.fixture
def test_database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    yield engine, session_factory
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def test_client(test_database):
    _, session_factory = test_database
    app = create_app()

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_register_user_successfully(test_client, test_database):
    _, session_factory = test_database
    published_events = []
    event_bus.subscribe(CharacterCreated, published_events.append)
    response = test_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "a_strong_password"},
    )

    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully."}

    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(UserModel)) == 1
        assert session.scalar(select(func.count()).select_from(PlayerModel)) == 1
        assert session.scalar(select(func.count()).select_from(CharacterModel)) == 1
    assert len(published_events) == 1
    assert isinstance(published_events[0], CharacterCreated)
