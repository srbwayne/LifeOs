from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.shared.infrastructure.database import Base, get_db

ITEM_FIELDS = {
    "id",
    "book_id",
    "book_title",
    "start_page",
    "end_page",
    "pages_read",
    "started_at",
    "ended_at",
    "notes",
}
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


def create_book(
    client: TestClient,
    headers: dict[str, str],
    title: str,
) -> str:
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
    *,
    start_page: int = 1,
    end_page: int = 10,
    started_at: str = "2026-08-14T12:00:00Z",
    notes: str | None = None,
) -> dict:
    response = client.post(
        f"/books/{book_id}/reading-sessions",
        headers=headers,
        json={
            "start_page": start_page,
            "end_page": end_page,
            "started_at": started_at,
            "ended_at": started_at,
            "notes": notes,
        },
    )
    assert response.status_code == 201
    return response.json()


def history(
    client: TestClient,
    headers: dict[str, str],
    params: dict[str, int] | None = None,
):
    return client.get("/reading-sessions", headers=headers, params=params)


def test_requires_authentication(client: TestClient) -> None:
    assert client.get("/reading-sessions").status_code == 401


def test_empty_history_returns_exact_default_page(client: TestClient) -> None:
    headers = auth(client, "history-empty@example.com")

    response = history(client, headers)

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "page": 1,
        "size": 20,
        "total_items": 0,
        "total_pages": 0,
    }


def test_history_has_exact_item_fields_current_titles_notes_and_utc(
    client: TestClient,
) -> None:
    headers = auth(client, "history-fields@example.com")
    first_book = create_book(client, headers, "First")
    second_book = create_book(client, headers, "Second")
    create_session(
        client,
        headers,
        first_book,
        start_page=31,
        end_page=50,
        started_at="2026-08-14T09:00:00-03:00",
        notes="Original note",
    )
    create_session(
        client,
        headers,
        second_book,
        started_at="2026-08-14T13:00:00Z",
    )

    response = history(client, headers)
    payload = response.json()

    assert response.status_code == 200
    assert set(payload) == PAGE_FIELDS
    assert payload["total_items"] == 2
    assert payload["total_pages"] == 1
    assert [item["book_title"] for item in payload["items"]] == ["Second", "First"]
    assert all(set(item) == ITEM_FIELDS for item in payload["items"])
    assert payload["items"][0]["notes"] is None
    assert payload["items"][1]["notes"] == "Original note"
    assert payload["items"][1]["pages_read"] == 20
    assert payload["items"][1]["started_at"].endswith("Z")
    assert all(
        "owner" not in key and key not in {"user_id", "player_id"}
        for item in payload["items"]
        for key in item
    )


def test_ordering_uses_started_at_then_id_desc(client: TestClient) -> None:
    headers = auth(client, "history-order@example.com")
    book_id = create_book(client, headers, "Ordered")
    older = create_session(
        client,
        headers,
        book_id,
        started_at="2026-08-14T11:00:00Z",
    )
    tied_first = create_session(
        client,
        headers,
        book_id,
        started_at="2026-08-14T12:00:00Z",
    )
    tied_second = create_session(
        client,
        headers,
        book_id,
        started_at="2026-08-14T12:00:00Z",
    )

    items = history(client, headers).json()["items"]

    assert [item["id"] for item in items] == [
        tied_second["id"],
        tied_first["id"],
        older["id"],
    ]


def test_pagination_metadata_and_page_beyond_end(client: TestClient) -> None:
    headers = auth(client, "history-pages@example.com")
    book_id = create_book(client, headers, "Paged")
    for page in range(1, 6):
        create_session(
            client,
            headers,
            book_id,
            start_page=page,
            end_page=page,
            started_at=f"2026-08-14T{page:02d}:00:00Z",
        )

    second = history(client, headers, {"page": 2, "size": 2})
    beyond = history(client, headers, {"page": 10, "size": 2})

    assert second.status_code == 200
    assert len(second.json()["items"]) == 2
    assert second.json() | {"items": []} == {
        "items": [],
        "page": 2,
        "size": 2,
        "total_items": 5,
        "total_pages": 3,
    }
    assert beyond.status_code == 200
    assert beyond.json() == {
        "items": [],
        "page": 10,
        "size": 2,
        "total_items": 5,
        "total_pages": 3,
    }


def test_history_is_owner_scoped(client: TestClient) -> None:
    owner = auth(client, "history-owner@example.com")
    other = auth(client, "history-other@example.com")
    owner_book = create_book(client, owner, "Visible")
    other_book = create_book(client, other, "Hidden")
    create_session(client, owner, owner_book)
    create_session(client, other, other_book)

    payload = history(client, owner).json()

    assert payload["total_items"] == 1
    assert [item["book_title"] for item in payload["items"]] == ["Visible"]


@pytest.mark.parametrize(
    "params",
    [
        {"page": 0},
        {"size": 0},
        {"size": 101},
    ],
)
def test_invalid_pagination_returns_422(
    client: TestClient,
    params: dict[str, int],
) -> None:
    headers = auth(client, f"history-invalid-{tuple(params.values())[0]}@example.com")
    assert history(client, headers, params).status_code == 422


def test_openapi_exposes_history_without_changing_existing_routes(app: FastAPI) -> None:
    paths = app.openapi()["paths"]

    assert set(paths["/reading-sessions"]) == {"get"}
    assert "/api/v1/reading-sessions" not in paths
    assert "/books/reading-sessions" not in paths
    for path, method in (
        ("/books", "get"),
        ("/books", "post"),
        ("/books/{book_id}/reading-sessions", "post"),
        ("/books/{book_id}/progress", "get"),
        ("/books/{book_id}/insights", "get"),
    ):
        assert method in paths[path]
