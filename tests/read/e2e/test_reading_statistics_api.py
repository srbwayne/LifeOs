from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.shared.infrastructure.database import Base, get_db

FIELDS = {
    "total_books",
    "books_with_reading_sessions",
    "total_reading_sessions",
    "total_pages_read",
    "average_pages_per_session",
}
FORBIDDEN_FIELDS = {
    "unique_pages_read",
    "highest_page_reached",
    "percentage",
    "completed",
    "remaining_pages",
    "gaps",
    "full_coverage_confirmed",
    "duration",
    "frequency",
    "streak",
    "trend",
    "score",
}


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

    def override_get_db() -> Iterator[Session]:
        with factory() as database_session:
            yield database_session

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


def create_book(client: TestClient, headers: dict[str, str], title: str) -> str:
    response = client.post(
        "/books",
        headers=headers,
        json={"title": title, "author": "Author", "total_pages": 300},
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_session(
    client: TestClient,
    headers: dict[str, str],
    book_id: str,
    start_page: int,
    end_page: int,
) -> None:
    response = client.post(
        f"/books/{book_id}/reading-sessions",
        headers=headers,
        json={
            "start_page": start_page,
            "end_page": end_page,
            "started_at": "2026-08-14T12:00:00Z",
            "ended_at": "2026-08-14T12:30:00Z",
        },
    )
    assert response.status_code == 201


def test_statistics_requires_authentication(client: TestClient) -> None:
    assert client.get("/reading-statistics").status_code == 401


def test_empty_state_has_exactly_five_fields(client: TestClient) -> None:
    headers = auth(client, "statistics-empty@example.com")
    response = client.get("/reading-statistics", headers=headers)
    assert response.status_code == 200
    assert set(response.json()) == FIELDS
    assert response.json() == {
        "total_books": 0,
        "books_with_reading_sessions": 0,
        "total_reading_sessions": 0,
        "total_pages_read": 0,
        "average_pages_per_session": "0.00",
    }


def test_statistics_are_gross_distinct_and_owner_scoped(client: TestClient) -> None:
    owner = auth(client, "statistics-owner@example.com")
    other = auth(client, "statistics-other@example.com")
    owner_book_a = create_book(client, owner, "Owner book A")
    owner_book_b = create_book(client, owner, "Owner book B")
    other_book = create_book(client, other, "Other book")
    create_session(client, owner, owner_book_a, 1, 3)
    create_session(client, owner, owner_book_a, 1, 3)
    create_session(client, owner, owner_book_a, 2, 4)
    create_session(client, owner, owner_book_b, 10, 10)
    create_session(client, other, other_book, 1, 100)

    response = client.get("/reading-statistics", headers=owner)
    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == FIELDS
    assert not FORBIDDEN_FIELDS.intersection(payload)
    assert payload == {
        "total_books": 2,
        "books_with_reading_sessions": 2,
        "total_reading_sessions": 4,
        "total_pages_read": 10,
        "average_pages_per_session": "2.50",
    }

    other_payload = client.get("/reading-statistics", headers=other).json()
    assert other_payload["total_books"] == 1
    assert other_payload["total_reading_sessions"] == 1
    assert other_payload["total_pages_read"] == 100


def test_statistics_fractional_average_has_two_decimal_string(client: TestClient) -> None:
    headers = auth(client, "statistics-average@example.com")
    book_id = create_book(client, headers, "Average")
    create_session(client, headers, book_id, 1, 2)
    create_session(client, headers, book_id, 3, 3)

    payload = client.get("/reading-statistics", headers=headers).json()
    assert payload["total_pages_read"] == 3
    assert payload["total_reading_sessions"] == 2
    assert payload["average_pages_per_session"] == "1.50"
    assert isinstance(payload["average_pages_per_session"], str)
    assert len(payload["average_pages_per_session"].split(".")[1]) == 2


@pytest.mark.parametrize("path", ["/books", "/reading-sessions"])
def test_existing_read_collections_remain_available(client: TestClient, path: str) -> None:
    headers = auth(client, f"statistics-route-{path.strip('/').replace('/', '-')}@example.com")
    response = client.get(path, headers=headers)
    assert response.status_code == 200
