from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.infrastructure.persistence.models.book_completion_model import BookCompletionModel
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.shared.infrastructure.database import Base, get_db

ITEM_FIELDS = {"book_id", "book_title", "completed_at"}
PAGE_FIELDS = {"items", "page", "size", "total_items", "total_pages"}


@pytest.fixture
def app() -> Iterator[FastAPI]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    application = create_app()
    application.state.test_session_factory = factory

    def override_get_db() -> Iterator[Session]:
        with factory() as session:
            yield session

    application.dependency_overrides[get_db] = override_get_db
    yield application
    application.dependency_overrides.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def auth(client: TestClient, email: str) -> dict[str, str]:
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
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def seed_completion(
    app: FastAPI,
    owner_id: str,
    book_id: str,
    title: str,
    completed_at: str,
    completion_id: str,
) -> None:
    factory = app.state.test_session_factory
    with factory() as session:
        session.add(
            BookModel(
                id=book_id,
                user_id=owner_id,
                title=title,
                author="Author",
                total_pages=100,
            )
        )
        session.flush()
        session.add(
            BookCompletionModel(
                id=completion_id,
                book_id=book_id,
                completed_at=datetime.fromisoformat(completed_at),
            )
        )
        session.commit()


def test_requires_authentication(client: TestClient) -> None:
    assert client.get("/book-completions").status_code == 401


def test_empty_response_has_exact_defaults_and_fields(client: TestClient) -> None:
    headers = auth(client, "completion-empty@example.com")

    response = client.get("/book-completions", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "page": 1,
        "size": 20,
        "total_items": 0,
        "total_pages": 0,
    }


def test_response_is_owner_scoped_and_has_exact_projection(
    client: TestClient, app: FastAPI
) -> None:
    owner = auth(client, "completion-owner@example.com")
    other = auth(client, "completion-other@example.com")
    with app.state.test_session_factory() as session:
        owner_user = session.query(UserModel).filter_by(email="completion-owner@example.com").one()
        other_user = session.query(UserModel).filter_by(email="completion-other@example.com").one()
        first_owner_id = owner_user.id
        second_owner_id = other_user.id
    seed_completion(
        app,
        first_owner_id,
        "0BOOK000000000000000000001",
        "Visible",
        "2026-08-22T12:00:00+00:00",
        "0COMP00000000000000000001",
    )
    seed_completion(
        app,
        second_owner_id,
        "0BOOK000000000000000000002",
        "Hidden",
        "2026-08-23T12:00:00+00:00",
        "0COMP00000000000000000002",
    )

    response = client.get("/book-completions", headers=owner)
    payload = response.json()

    assert response.status_code == 200
    assert set(payload) == PAGE_FIELDS
    assert len(payload["items"]) == 1
    assert set(payload["items"][0]) == ITEM_FIELDS
    assert payload["items"][0]["book_title"] == "Visible"
    assert all(
        key
        not in {"completion_id", "owner_id", "user_id", "player_id", "created_at", "total_pages"}
        for key in payload["items"][0]
    )
    assert (
        client.get("/book-completions", headers=other).json()["items"][0]["book_title"] == "Hidden"
    )


def test_ordering_tie_break_and_pagination(client: TestClient, app: FastAPI) -> None:
    headers = auth(client, "completion-order@example.com")
    with app.state.test_session_factory() as session:
        owner_id = session.query(UserModel).filter_by(email="completion-order@example.com").one().id
    for number, title, timestamp in (
        ("001", "Older", "2026-08-21T12:00:00+00:00"),
        ("002", "Tie low", "2026-08-22T12:00:00+00:00"),
        ("003", "Tie high", "2026-08-22T12:00:00+00:00"),
    ):
        seed_completion(
            app,
            owner_id,
            f"0BOOK000000000000000000{number}",
            title,
            timestamp,
            f"0COMP000000000000000000{number}",
        )

    first = client.get("/book-completions", headers=headers, params={"page": 1, "size": 2})
    second = client.get("/book-completions", headers=headers, params={"page": 2, "size": 2})

    assert [item["book_title"] for item in first.json()["items"]] == ["Tie high", "Tie low"]
    assert [item["book_title"] for item in second.json()["items"]] == ["Older"]
    assert first.json()["total_items"] == 3
    assert first.json()["total_pages"] == 2


@pytest.mark.parametrize(
    "params,email_suffix",
    [({"page": 0}, "page"), ({"size": 0}, "size-zero"), ({"size": 101}, "size-max")],
)
def test_invalid_pagination_returns_422(
    client: TestClient,
    params: dict[str, int],
    email_suffix: str,
) -> None:
    headers = auth(client, f"completion-invalid-{email_suffix}@example.com")

    assert client.get("/book-completions", headers=headers, params=params).status_code == 422


def test_page_beyond_end_and_size_100(client: TestClient) -> None:
    headers = auth(client, "completion-beyond@example.com")

    response = client.get(
        "/book-completions",
        headers=headers,
        params={"page": 10, "size": 100},
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "page": 10,
        "size": 100,
        "total_items": 0,
        "total_pages": 0,
    }


def test_openapi_exposes_completion_route_and_existing_read_routes(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]

    assert "/book-completions" in paths
    assert "/books" in paths
    assert "/reading-sessions" in paths
    assert "/reading-statistics" in paths
