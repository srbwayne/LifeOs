import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, func, select, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.app_factory import create_app
from app.auth.dependencies import event_bus, get_db
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.character.domain.events.character_created import CharacterCreated
from app.character.infrastructure.persistence.models.character_model import CharacterModel
from app.character.infrastructure.persistence.models.player_model import PlayerModel
from app.shared.domain.domain_event import DomainEvent
from app.shared.infrastructure.database import Base
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


@pytest.fixture
def test_database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys = ON")

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
    published_events: list[DomainEvent] = []
    commit_count = 0

    def capture_event(event: DomainEvent) -> None:
        published_events.append(event)

    def assert_events_are_post_commit(session: Session) -> None:
        nonlocal commit_count
        assert published_events == []
        commit_count += 1

    event_bus.subscribe(CharacterCreated, capture_event)
    event.listen(Session, "after_commit", assert_events_are_post_commit)
    try:
        response = test_client.post(
            "/auth/register",
            json={"email": "test@example.com", "password": "a_strong_password"},
        )
    finally:
        event.remove(Session, "after_commit", assert_events_are_post_commit)

    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully."}
    assert commit_count == 1

    with session_factory() as session:
        assert session.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
        assert session.scalar(select(func.count()).select_from(UserModel)) == 1
        assert session.scalar(select(func.count()).select_from(PlayerModel)) == 1
        assert session.scalar(select(func.count()).select_from(CharacterModel)) == 1
        user = session.scalars(select(UserModel)).one()
        player = session.scalars(select(PlayerModel)).one()
        character = session.scalars(select(CharacterModel)).one()
        assert player.user_id == user.id
        assert character.player_id == player.id
        assert session.execute(text("PRAGMA foreign_key_check")).all() == []
    assert len(published_events) == 1
    assert isinstance(published_events[0], CharacterCreated)


def test_register_user_rolls_back_when_player_flush_fails(test_client, test_database, monkeypatch):
    _, session_factory = test_database
    published_events: list[DomainEvent] = []
    flush_count = 0
    original_flush = SqlAlchemyUnitOfWork.flush

    def fail_after_player_flush(unit_of_work):
        nonlocal flush_count
        flush_count += 1
        original_flush(unit_of_work)
        if flush_count == 2:
            raise RuntimeError("player flush failed")

    def capture_event(event: DomainEvent) -> None:
        published_events.append(event)

    event_bus.subscribe(CharacterCreated, capture_event)
    monkeypatch.setattr(SqlAlchemyUnitOfWork, "flush", fail_after_player_flush)

    with pytest.raises(RuntimeError, match="player flush failed"):
        test_client.post(
            "/auth/register",
            json={"email": "player-failure@example.com", "password": "a_strong_password"},
        )

    assert flush_count == 2
    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(UserModel)) == 0
        assert session.scalar(select(func.count()).select_from(PlayerModel)) == 0
        assert session.scalar(select(func.count()).select_from(CharacterModel)) == 0
    assert published_events == []


def test_register_user_rolls_back_when_final_persistence_fails(
    test_client, test_database, monkeypatch
):
    _, session_factory = test_database
    published_events: list[DomainEvent] = []
    flush_count = 0
    original_flush = SqlAlchemyUnitOfWork.flush

    def observe_flush(unit_of_work):
        nonlocal flush_count
        flush_count += 1
        original_flush(unit_of_work)

    def fail_final_commit(unit_of_work):
        unit_of_work.session.flush()
        raise RuntimeError("final persistence failed")

    def capture_event(event: DomainEvent) -> None:
        published_events.append(event)

    event_bus.subscribe(CharacterCreated, capture_event)
    monkeypatch.setattr(SqlAlchemyUnitOfWork, "flush", observe_flush)
    monkeypatch.setattr(SqlAlchemyUnitOfWork, "commit", fail_final_commit)

    with pytest.raises(RuntimeError, match="final persistence failed"):
        test_client.post(
            "/auth/register",
            json={"email": "character-failure@example.com", "password": "a_strong_password"},
        )

    assert flush_count == 2
    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(UserModel)) == 0
        assert session.scalar(select(func.count()).select_from(PlayerModel)) == 0
        assert session.scalar(select(func.count()).select_from(CharacterModel)) == 0
    assert published_events == []


def test_register_user_duplicate_email_remains_conflict(test_client, test_database):
    _, session_factory = test_database
    payload = {"email": "duplicate@example.com", "password": "a_strong_password"}

    assert test_client.post("/auth/register", json=payload).status_code == 201
    duplicate_response = test_client.post("/auth/register", json=payload)

    assert duplicate_response.status_code == 409
    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(UserModel)) == 1
        assert session.scalar(select(func.count()).select_from(PlayerModel)) == 1
        assert session.scalar(select(func.count()).select_from(CharacterModel)) == 1
