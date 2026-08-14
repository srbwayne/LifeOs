from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.read.domain.value_objects.book_id import BookId
from app.shared.infrastructure.database import Base, get_db

INSIGHT_FIELDS = {
    "book_id",
    "remaining_pages",
    "gaps",
    "last_page_reached_with_gaps",
    "full_coverage_confirmed",
}


@pytest.fixture
def app() -> Iterator[FastAPI]:
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
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


def auth(client: TestClient, email: str) -> dict[str, str]:
    assert (
        client.post(
            "/auth/register", json={"email": email, "password": "a_strong_password"}
        ).status_code
        == 201
    )
    login = client.post("/auth/login", json={"email": email, "password": "a_strong_password"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def book(client: TestClient, headers: dict[str, str], total: int = 100) -> str:
    response = client.post(
        "/books", headers=headers, json={"title": "Book", "author": "Author", "total_pages": total}
    )
    assert response.status_code == 201
    return response.json()["id"]


def session(
    client: TestClient, headers: dict[str, str], book_id: str, start: int, end: int
) -> None:
    response = client.post(
        f"/books/{book_id}/reading-sessions",
        headers=headers,
        json={
            "start_page": start,
            "end_page": end,
            "started_at": "2026-08-14T00:00:00Z",
            "ended_at": "2026-08-14T00:00:00Z",
        },
    )
    assert response.status_code == 201


def get(client: TestClient, headers: dict[str, str], book_id: str):
    return client.get(f"/books/{book_id}/insights", headers=headers)


def test_requires_authentication(client: TestClient) -> None:
    assert client.get(f"/books/{BookId.new()}/insights").status_code == 401


def test_empty_book_returns_full_gap(client: TestClient) -> None:
    headers = auth(client, "insights-empty@example.com")
    book_id = book(client, headers)
    response = get(client, headers, book_id)
    assert response.status_code == 200
    assert response.json() == {
        "book_id": book_id,
        "remaining_pages": 100,
        "gaps": [{"start_page": 1, "end_page": 100}],
        "last_page_reached_with_gaps": False,
        "full_coverage_confirmed": False,
    }


@pytest.mark.parametrize(
    ("ranges", "remaining", "gaps", "last", "full"),
    [
        (((1, 20), (15, 30), (50, 60)), 59, [(31, 49), (61, 100)], False, False),
        (((1, 10), (1, 10)), 90, [(11, 100)], False, False),
        (((1, 50), (100, 100)), 49, [(51, 99)], True, False),
        (((1, 100),), 0, [], False, True),
    ],
)
def test_derives_exact_insights(
    client: TestClient,
    ranges: tuple[tuple[int, int], ...],
    remaining: int,
    gaps: list[tuple[int, int]],
    last: bool,
    full: bool,
) -> None:
    headers = auth(client, f"insights-{remaining}-{last}@example.com")
    book_id = book(client, headers)
    for start, end in ranges:
        session(client, headers, book_id, start, end)
    response = get(client, headers, book_id)
    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == INSIGHT_FIELDS
    assert payload["remaining_pages"] == remaining
    assert payload["gaps"] == [{"start_page": start, "end_page": end} for start, end in gaps]
    assert payload["last_page_reached_with_gaps"] is last
    assert payload["full_coverage_confirmed"] is full
    for forbidden in {
        "owner",
        "owner_id",
        "user_id",
        "total_pages",
        "percentage",
        "unique_pages_read",
        "highest_page_reached",
        "sessions",
        "notes",
        "message",
        "recommendation",
        "current_page",
        "next_page",
    }:
        assert forbidden not in payload


def test_missing_and_foreign_are_indistinguishable(client: TestClient) -> None:
    owner = auth(client, "insights-owner@example.com")
    other = auth(client, "insights-other@example.com")
    hidden = book(client, other)
    missing = get(client, owner, str(BookId.new()))
    foreign = get(client, owner, hidden)
    assert missing.status_code == foreign.status_code == 404
    assert missing.json() == foreign.json() == {"detail": "Book not found."}


def test_invalid_book_id_returns_422(client: TestClient) -> None:
    headers = auth(client, "insights-invalid@example.com")
    response = client.get("/books/not-a-tsid/insights", headers=headers)
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid book ID."}


def test_openapi_exposes_only_approved_insights_route(app: FastAPI) -> None:
    paths = app.openapi()["paths"]
    operation = paths["/books/{book_id}/insights"]
    assert set(operation) == {"get"}
    assert "requestBody" not in operation["get"]
    assert [
        item["name"] for item in operation["get"].get("parameters", []) if item["in"] == "query"
    ] == []
    assert "/books/{book_id}/reading-insights" not in paths
    assert "/insights/{book_id}" not in paths
    assert "/api/v1/books/{book_id}/insights" not in paths
