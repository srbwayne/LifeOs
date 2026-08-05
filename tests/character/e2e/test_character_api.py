import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.app_factory import create_app
from app.shared.infrastructure.database import Base, get_db


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    app = create_app()

    def override_get_db():
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def register_and_login(client: TestClient, email: str) -> str:
    register = client.post(
        "/auth/register",
        json={"email": email, "password": "a_strong_password"},
    )
    assert register.status_code == 201
    login = client.post(
        "/auth/login",
        json={"email": email, "password": "a_strong_password"},
    )
    assert login.status_code == 200
    return login.json()["access_token"]


def test_character_endpoints_return_authenticated_persistent_data(client: TestClient):
    token = register_and_login(client, "character@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    character_response = client.get("/character", headers=headers)
    profile_response = client.get("/character/profile", headers=headers)

    assert character_response.status_code == 200
    character = character_response.json()
    assert character["name"] == "character"
    assert character["character_id"]
    assert character["player_id"]
    assert character["user_id"]
    assert set(character) == {
        "character_id",
        "player_id",
        "user_id",
        "name",
        "character_created_at",
        "character_updated_at",
        "profile_created_at",
        "profile_updated_at",
    }

    assert profile_response.status_code == 200
    profile = profile_response.json()
    assert profile["player_id"] == character["player_id"]
    assert profile["user_id"] == character["user_id"]
    assert profile["name"] == "character"
    assert "experience" not in profile
    assert "level" not in profile


def test_character_endpoints_require_access_token(client: TestClient):
    assert client.get("/character").status_code == 401
    assert client.get("/character/profile").status_code == 401


def test_character_query_is_isolated_by_authenticated_user(client: TestClient):
    first_token = register_and_login(client, "first@example.com")
    second_token = register_and_login(client, "second@example.com")

    first = client.get(
        "/character",
        headers={"Authorization": f"Bearer {first_token}"},
    ).json()
    second = client.get(
        "/character",
        headers={"Authorization": f"Bearer {second_token}"},
    ).json()

    assert first["character_id"] != second["character_id"]
    assert first["player_id"] != second["player_id"]
    assert first["user_id"] != second["user_id"]


def test_character_api_has_no_profile_write_endpoints(client: TestClient):
    token = register_and_login(client, "readonly@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    assert client.put("/character", headers=headers, json={}).status_code == 405
    assert client.patch("/character", headers=headers, json={}).status_code == 405
    assert client.patch("/character/name", headers=headers, json={}).status_code == 404
    assert client.patch("/character/avatar", headers=headers, json={}).status_code == 404
