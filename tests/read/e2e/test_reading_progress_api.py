from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.read.domain.value_objects.book_id import BookId
from app.shared.infrastructure.database import Base, get_db

PROGRESS_FIELDS = {
    "book_id",
    "total_pages",
    "unique_pages_read",
    "highest_page_reached",
    "percentage",
    "completed",
}


@pytest.fixture
def app() -> Iterator[FastAPI]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    application = create_app()

    def override_get_db() -> Iterator[Session]:
        with session_factory() as session:
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


def register_and_login(client: TestClient, email: str) -> dict[str, str]:
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


def create_book(
    client: TestClient,
    headers: dict[str, str],
    total_pages: int = 100,
) -> dict[str, object]:
    response = client.post(
        "/books",
        headers=headers,
        json={"title": "Book", "author": "Author", "total_pages": total_pages},
    )
    assert response.status_code == 201
    return response.json()


def create_session(
    client: TestClient,
    headers: dict[str, str],
    book_id: object,
    start_page: int,
    end_page: int,
) -> None:
    response = client.post(
        f"/books/{book_id}/reading-sessions",
        headers=headers,
        json={
            "start_page": start_page,
            "end_page": end_page,
            "started_at": "2026-08-12T12:00:00Z",
            "ended_at": "2026-08-12T12:00:00Z",
        },
    )
    assert response.status_code == 201


def test_reading_progress_requires_authentication(client: TestClient) -> None:
    response = client.get(f"/books/{BookId.new()}/progress")

    assert response.status_code == 401


def test_book_without_sessions_returns_zero_progress(client: TestClient) -> None:
    headers = register_and_login(client, "progress-empty@example.com")
    book = create_book(client, headers)

    response = client.get(f"/books/{book['id']}/progress", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "book_id": book["id"],
        "total_pages": 100,
        "unique_pages_read": 0,
        "highest_page_reached": None,
        "percentage": 0.0,
        "completed": False,
    }


@pytest.mark.parametrize(
    ("ranges", "unique_pages", "highest", "percentage", "completed"),
    [
        (((1, 20),), 20, 20, 20.0, False),
        (((1, 20), (15, 30)), 30, 30, 30.0, False),
        (((1, 10), (1, 10)), 10, 10, 10.0, False),
        (((1, 20), (15, 30), (50, 60)), 41, 60, 41.0, False),
        (((80, 90), (10, 20)), 22, 90, 22.0, False),
        (((90, 100),), 11, 100, 11.0, False),
        (((1, 30), (31, 60), (61, 100)), 100, 100, 100.0, True),
    ],
)
def test_progress_derives_approved_page_coverage(
    client: TestClient,
    ranges: tuple[tuple[int, int], ...],
    unique_pages: int,
    highest: int,
    percentage: float,
    completed: bool,
) -> None:
    suffix = "-".join(f"{start}-{end}" for start, end in ranges)
    headers = register_and_login(client, f"progress-{suffix}@example.com")
    book = create_book(client, headers)
    for start_page, end_page in ranges:
        create_session(client, headers, book["id"], start_page, end_page)

    response = client.get(f"/books/{book['id']}/progress", headers=headers)

    assert response.status_code == 200
    progress = response.json()
    assert set(progress) == PROGRESS_FIELDS
    assert progress["unique_pages_read"] == unique_pages
    assert progress["highest_page_reached"] == highest
    assert progress["percentage"] == percentage
    assert progress["completed"] is completed
    for forbidden in {
        "owner",
        "owner_id",
        "user",
        "user_id",
        "player",
        "player_id",
        "sessions",
        "session_count",
        "reading_sessions",
        "current_page",
        "next_page",
        "start_page",
        "end_page",
        "started_at",
        "ended_at",
        "notes",
    }:
        assert forbidden not in progress


def test_missing_and_other_owner_books_are_indistinguishable(client: TestClient) -> None:
    owner_headers = register_and_login(client, "progress-owner@example.com")
    other_headers = register_and_login(client, "progress-other@example.com")
    hidden_book = create_book(client, other_headers)
    create_session(client, other_headers, hidden_book["id"], 1, 50)

    missing = client.get(f"/books/{BookId.new()}/progress", headers=owner_headers)
    hidden = client.get(f"/books/{hidden_book['id']}/progress", headers=owner_headers)

    assert missing.status_code == hidden.status_code == 404
    assert missing.json() == hidden.json() == {"detail": "Book not found."}


def test_invalid_book_id_returns_existing_422_contract(client: TestClient) -> None:
    headers = register_and_login(client, "progress-invalid-id@example.com")

    response = client.get("/books/not-a-tsid/progress", headers=headers)

    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid book ID."}


def test_openapi_exposes_only_the_approved_progress_route(app: FastAPI) -> None:
    paths = app.openapi()["paths"]
    operation = paths["/books/{book_id}/progress"]

    assert set(operation) == {"get"}
    assert "requestBody" not in operation["get"]
    assert [
        parameter["name"]
        for parameter in operation["get"].get("parameters", [])
        if parameter["in"] == "query"
    ] == []
    assert "/books/{book_id}/reading-progress" not in paths
    assert "/reading-progress/{book_id}" not in paths
    assert "/progress/{book_id}" not in paths
