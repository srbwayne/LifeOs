from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.shared.infrastructure.database import Base, get_db

BOOK_FIELDS = {
    "id",
    "title",
    "author",
    "total_pages",
    "isbn",
    "publisher",
    "edition",
    "cover",
    "genre",
    "language",
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


def test_book_endpoints_require_authentication(client: TestClient) -> None:
    assert (
        client.post(
            "/books",
            json={"title": "Domain-Driven Design", "author": "Eric Evans", "total_pages": 560},
        ).status_code
        == 401
    )
    assert client.get("/books").status_code == 401


def test_create_book_with_required_fields_returns_201(client: TestClient) -> None:
    headers = register_and_login(client, "required@example.com")
    response = client.post(
        "/books",
        headers=headers,
        json={"title": "Domain-Driven Design", "author": "Eric Evans", "total_pages": 560},
    )

    assert response.status_code == 201
    book = response.json()
    assert set(book) == BOOK_FIELDS
    assert book["id"]
    assert book["title"] == "Domain-Driven Design"
    assert book["author"] == "Eric Evans"
    assert book["total_pages"] == 560
    for optional in {"isbn", "publisher", "edition", "cover", "genre", "language"}:
        assert book[optional] is None
    assert "owner_id" not in book
    assert "user_id" not in book


def test_create_book_preserves_optionals_and_domain_normalization(client: TestClient) -> None:
    headers = register_and_login(client, "optionals@example.com")
    response = client.post(
        "/books",
        headers=headers,
        json={
            "title": "  Clean Architecture  ",
            "author": "  Robert C. Martin  ",
            "total_pages": 432,
            "isbn": "  9780134494166  ",
            "publisher": "  Pearson  ",
            "edition": "  First  ",
            "cover": "  https://example.test/cover  ",
            "genre": "  Software  ",
            "language": "  en  ",
        },
    )

    assert response.status_code == 201
    book = response.json()
    assert book == {
        "id": book["id"],
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "total_pages": 432,
        "isbn": "9780134494166",
        "publisher": "Pearson",
        "edition": "First",
        "cover": "https://example.test/cover",
        "genre": "Software",
        "language": "en",
    }

    empty_optionals = client.post(
        "/books",
        headers=headers,
        json={
            "title": "Refactoring",
            "author": "Martin Fowler",
            "total_pages": 448,
            "isbn": " ",
            "publisher": "",
        },
    )
    assert empty_optionals.status_code == 201
    assert empty_optionals.json()["isbn"] is None
    assert empty_optionals.json()["publisher"] is None


@pytest.mark.parametrize("owner_field", ["owner_id", "user_id", "player_id"])
def test_create_book_rejects_owner_from_client(client: TestClient, owner_field: str) -> None:
    headers = register_and_login(client, f"{owner_field}@example.com")
    payload = {
        "title": "Book",
        "author": "Author",
        "total_pages": 100,
        owner_field: "0HZXJ2NQZ89Y0",
    }

    assert client.post("/books", headers=headers, json=payload).status_code == 422


@pytest.mark.parametrize("missing_field", ["title", "author", "total_pages"])
def test_create_book_rejects_missing_required_field(
    client: TestClient,
    missing_field: str,
) -> None:
    headers = register_and_login(client, f"missing-{missing_field}@example.com")
    payload = {"title": "Book", "author": "Author", "total_pages": 100}
    del payload[missing_field]

    assert client.post("/books", headers=headers, json=payload).status_code == 422


@pytest.mark.parametrize(
    ("payload", "detail"),
    [
        ({"title": " ", "author": "Author", "total_pages": 100}, "Book title cannot be empty."),
        ({"title": "Book", "author": " ", "total_pages": 100}, "Book author cannot be empty."),
        (
            {"title": "Book", "author": "Author", "total_pages": 0},
            "Book total pages must be a positive integer.",
        ),
        (
            {"title": "Book", "author": "Author", "total_pages": -1},
            "Book total pages must be a positive integer.",
        ),
    ],
)
def test_create_book_translates_domain_errors(
    client: TestClient,
    payload: dict[str, str | int],
    detail: str,
) -> None:
    if "title" in detail:
        email_suffix = "title"
    elif "author" in detail:
        email_suffix = "author"
    else:
        email_suffix = str(payload["total_pages"])
    headers = register_and_login(client, f"invalid-{email_suffix}@example.com")
    response = client.post("/books", headers=headers, json=payload)

    assert response.status_code == 422
    assert response.json() == {"detail": detail}


def test_empty_library_returns_200_and_empty_list(client: TestClient) -> None:
    headers = register_and_login(client, "empty@example.com")

    response = client.get("/books", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


def test_library_is_isolated_by_authenticated_user_and_ordered(client: TestClient) -> None:
    first_headers = register_and_login(client, "first-reader@example.com")
    second_headers = register_and_login(client, "second-reader@example.com")

    first_book = client.post(
        "/books",
        headers=first_headers,
        json={"title": "First", "author": "Author A", "total_pages": 100},
    ).json()
    second_first_book = client.post(
        "/books",
        headers=first_headers,
        json={"title": "Second", "author": "Author A", "total_pages": 200},
    ).json()
    other_book = client.post(
        "/books",
        headers=second_headers,
        json={"title": "Other", "author": "Author B", "total_pages": 300},
    ).json()

    first_library = client.get("/books", headers=first_headers)
    second_library = client.get("/books", headers=second_headers)

    assert first_library.status_code == 200
    assert [book["id"] for book in first_library.json()] == sorted(
        [first_book["id"], second_first_book["id"]]
    )
    assert {book["title"] for book in first_library.json()} == {"First", "Second"}
    assert other_book["id"] not in {book["id"] for book in first_library.json()}
    assert second_library.status_code == 200
    assert second_library.json() == [other_book]
    assert first_book["id"] not in {book["id"] for book in second_library.json()}


def test_owner_query_and_header_cannot_override_authenticated_identity(
    client: TestClient,
) -> None:
    first_headers = register_and_login(client, "owner-source@example.com")
    second_headers = register_and_login(client, "owner-target@example.com")
    first_user_id = client.get("/character", headers=first_headers).json()["user_id"]

    response = client.post(
        f"/books?owner_id={first_user_id}&user_id={first_user_id}&player_id={first_user_id}",
        headers={**second_headers, "X-Owner-Id": first_user_id},
        json={"title": "Protected", "author": "Owner", "total_pages": 120},
    )

    assert response.status_code == 201
    assert client.get("/books", headers=first_headers).json() == []
    assert client.get("/books", headers=second_headers).json() == [response.json()]


def test_get_books_declares_no_filtering_parameters(app: FastAPI) -> None:
    operation = app.openapi()["paths"]["/books"]["get"]

    assert operation.get("parameters", []) == []
