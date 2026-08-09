from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.read.domain.value_objects.book_id import BookId
from app.shared.infrastructure.database import Base, get_db

SESSION_FIELDS = {
    "id",
    "book_id",
    "start_page",
    "end_page",
    "pages_read",
    "started_at",
    "ended_at",
    "notes",
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
    *,
    total_pages: int = 300,
) -> dict[str, object]:
    response = client.post(
        "/books",
        headers=headers,
        json={"title": "Book", "author": "Author", "total_pages": total_pages},
    )
    assert response.status_code == 201
    return response.json()


def valid_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "start_page": 80,
        "end_page": 92,
        "started_at": "2026-08-09T14:00:00-03:00",
        "ended_at": "2026-08-09T14:30:00-03:00",
        "notes": None,
    }
    payload.update(overrides)
    return payload


@pytest.mark.parametrize(
    "headers",
    [None, {"Authorization": "Bearer invalid-token"}],
)
def test_create_reading_session_requires_valid_authentication(
    client: TestClient,
    headers: dict[str, str] | None,
) -> None:
    response = client.post(
        f"/books/{BookId.new()}/reading-sessions",
        headers=headers,
        json=valid_payload(),
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    ("start_page", "end_page", "pages_read"),
    [(150, 150, 1), (80, 92, 13)],
)
def test_create_reading_session_returns_201_and_calculated_pages(
    client: TestClient,
    start_page: int,
    end_page: int,
    pages_read: int,
) -> None:
    headers = register_and_login(client, f"pages-{start_page}-{end_page}@example.com")
    book = create_book(client, headers, total_pages=200)

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=valid_payload(start_page=start_page, end_page=end_page),
    )

    assert response.status_code == 201
    session = response.json()
    assert set(session) == SESSION_FIELDS
    assert session["id"]
    assert session["book_id"] == book["id"]
    assert session["start_page"] == start_page
    assert session["end_page"] == end_page
    assert session["pages_read"] == pages_read
    assert session["notes"] is None
    assert "owner_id" not in session
    assert "user_id" not in session
    assert "created_at" not in session
    assert "updated_at" not in session


def test_notes_are_normalized_and_offset_timestamps_return_as_utc(client: TestClient) -> None:
    headers = register_and_login(client, "timezone@example.com")
    book = create_book(client, headers)

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=valid_payload(notes="  reflection  "),
    )

    assert response.status_code == 201
    session = response.json()
    assert session["notes"] == "reflection"
    started_at = datetime.fromisoformat(session["started_at"].replace("Z", "+00:00"))
    ended_at = datetime.fromisoformat(session["ended_at"].replace("Z", "+00:00"))
    assert started_at == datetime(2026, 8, 9, 17, 0, tzinfo=timezone.utc)
    assert ended_at == datetime(2026, 8, 9, 17, 30, tzinfo=timezone.utc)


def test_equal_start_and_end_time_is_accepted(client: TestClient) -> None:
    headers = register_and_login(client, "zero-duration@example.com")
    book = create_book(client, headers)

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=valid_payload(
            started_at="2026-08-09T17:00:00Z",
            ended_at="2026-08-09T17:00:00Z",
        ),
    )

    assert response.status_code == 201


def test_reading_session_creation_is_isolated_by_authenticated_owner(
    client: TestClient,
) -> None:
    first_headers = register_and_login(client, "session-owner-a@example.com")
    second_headers = register_and_login(client, "session-owner-b@example.com")
    first_book = create_book(client, first_headers)
    second_book = create_book(client, second_headers)

    own_response = client.post(
        f"/books/{first_book['id']}/reading-sessions",
        headers=first_headers,
        json=valid_payload(),
    )
    hidden_response = client.post(
        f"/books/{second_book['id']}/reading-sessions",
        headers=first_headers,
        json=valid_payload(),
    )
    second_response = client.post(
        f"/books/{second_book['id']}/reading-sessions",
        headers=second_headers,
        json=valid_payload(),
    )

    assert own_response.status_code == 201
    assert hidden_response.status_code == 404
    assert hidden_response.json() == {"detail": "Book not found."}
    assert second_response.status_code == 201


def test_missing_and_other_owner_books_are_indistinguishable(client: TestClient) -> None:
    first_headers = register_and_login(client, "not-found-a@example.com")
    second_headers = register_and_login(client, "not-found-b@example.com")
    hidden_book = create_book(client, second_headers)

    missing = client.post(
        f"/books/{BookId.new()}/reading-sessions",
        headers=first_headers,
        json=valid_payload(),
    )
    hidden = client.post(
        f"/books/{hidden_book['id']}/reading-sessions",
        headers=first_headers,
        json=valid_payload(),
    )

    assert missing.status_code == hidden.status_code == 404
    assert missing.json() == hidden.json() == {"detail": "Book not found."}


def test_invalid_book_id_returns_422(client: TestClient) -> None:
    headers = register_and_login(client, "invalid-book-id@example.com")

    response = client.post(
        "/books/not-a-tsid/reading-sessions",
        headers=headers,
        json=valid_payload(),
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid book ID."}


@pytest.mark.parametrize(
    ("overrides", "detail"),
    [
        (
            {"start_page": 0},
            "Reading session page number must be a positive integer.",
        ),
        (
            {"start_page": -1},
            "Reading session page number must be a positive integer.",
        ),
        (
            {"start_page": 20, "end_page": 10},
            "Reading session end page cannot precede the start page.",
        ),
        (
            {"end_page": 301},
            "Reading session end page cannot exceed the book total pages.",
        ),
        (
            {"started_at": "2026-08-09T14:00:00"},
            "Reading session times must be timezone-aware and end at or after the start.",
        ),
        (
            {"ended_at": "2026-08-09T14:30:00"},
            "Reading session times must be timezone-aware and end at or after the start.",
        ),
        (
            {
                "started_at": "2026-08-09T15:00:00Z",
                "ended_at": "2026-08-09T14:00:00Z",
            },
            "Reading session times must be timezone-aware and end at or after the start.",
        ),
    ],
)
def test_domain_validation_returns_422(
    client: TestClient,
    overrides: dict[str, object],
    detail: str,
) -> None:
    headers = register_and_login(client, f"domain-{abs(hash(detail + str(overrides)))}@example.com")
    book = create_book(client, headers)

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=valid_payload(**overrides),
    )

    assert response.status_code == 422
    assert response.json() == {"detail": detail}


@pytest.mark.parametrize(
    "missing_field",
    ["start_page", "end_page", "started_at", "ended_at"],
)
def test_request_rejects_missing_required_fields(
    client: TestClient,
    missing_field: str,
) -> None:
    headers = register_and_login(client, f"missing-{missing_field}@example.com")
    book = create_book(client, headers)
    payload = valid_payload()
    del payload[missing_field]

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("start_page", []),
        ("end_page", {}),
        ("started_at", "not-a-datetime"),
        ("ended_at", 123),
        ("notes", []),
    ],
)
def test_request_rejects_incompatible_types(
    client: TestClient,
    field: str,
    value: object,
) -> None:
    headers = register_and_login(client, f"type-{field}@example.com")
    book = create_book(client, headers)

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=valid_payload(**{field: value}),
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "extra_field",
    ["owner_id", "user_id", "player_id", "pages_read", "book_id", "id"],
)
def test_request_forbids_client_controlled_or_derived_fields(
    client: TestClient,
    extra_field: str,
) -> None:
    headers = register_and_login(client, f"extra-{extra_field}@example.com")
    book = create_book(client, headers)

    response = client.post(
        f"/books/{book['id']}/reading-sessions",
        headers=headers,
        json=valid_payload(**{extra_field: "forbidden"}),
    )

    assert response.status_code == 422


def test_no_reading_session_query_or_mutation_routes_are_exposed(app: FastAPI) -> None:
    paths = app.openapi()["paths"]
    session_path = "/books/{book_id}/reading-sessions"

    assert set(paths[session_path]) == {"post"}
    assert "/reading-sessions" not in paths
    assert "/reading-sessions/{id}" not in paths
