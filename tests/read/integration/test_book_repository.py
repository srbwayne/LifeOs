from collections.abc import Iterator
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.domain.aggregates.book import Book
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    with session_factory() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId, email: str) -> None:
    now = datetime(2026, 8, 9, 0, 0, 0)
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=email,
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )
    session.commit()


def test_save_adds_book_without_committing(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id, "owner@example.com")
    repository = SqlAlchemyBookRepository(session)
    book = Book.create(owner_id, "Book", "Author", 100)

    repository.save(book)

    assert any(
        isinstance(model, BookModel) and model.id == book.id.to_persistence()
        for model in session.new
    )
    session.rollback()
    assert session.get(BookModel, book.id.to_persistence()) is None


def test_list_by_owner_is_isolated_and_returns_empty_tuple(session: Session) -> None:
    first_owner = UserId.new()
    second_owner = UserId.new()
    add_user(session, first_owner, "first@example.com")
    add_user(session, second_owner, "second@example.com")
    repository = SqlAlchemyBookRepository(session)
    first_book = Book.create(first_owner, "First", "Author", 100)
    second_book = Book.create(second_owner, "Second", "Author", 200)
    repository.save(first_book)
    repository.save(second_book)
    session.commit()

    assert repository.list_by_owner(first_owner) == (first_book,)
    assert repository.list_by_owner(second_owner) == (second_book,)
    assert repository.list_by_owner(UserId.new()) == ()


def test_list_by_owner_orders_by_book_id(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id, "ordered@example.com")
    repository = SqlAlchemyBookRepository(session)
    books = tuple(Book.create(owner_id, f"Book {index}", "Author", 100) for index in range(3))
    for book in reversed(books):
        repository.save(book)
    session.commit()

    result = repository.list_by_owner(owner_id)

    assert tuple(book.id.value for book in result) == tuple(sorted(book.id.value for book in books))


def test_repository_preserves_optionals_and_allows_duplicate_content(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id, "duplicates@example.com")
    repository = SqlAlchemyBookRepository(session)
    books = tuple(
        Book.create(
            owner_id,
            "Same Book",
            "Same Author",
            300,
            isbn="same-isbn",
            publisher="publisher",
            edition="edition",
            cover="cover",
            genre="genre",
            language="language",
        )
        for _ in range(2)
    )
    for book in books:
        repository.save(book)
    session.commit()

    result = repository.list_by_owner(owner_id)

    assert len(result) == 2
    assert result[0].id != result[1].id
    assert all(book.isbn == "same-isbn" for book in result)
    assert all(book.publisher == "publisher" for book in result)
    assert all(book.edition == "edition" for book in result)
    assert all(book.cover == "cover" for book in result)
    assert all(book.genre == "genre" for book in result)
    assert all(book.language == "language" for book in result)


def test_book_model_assigns_technical_timestamps_on_insert(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id, "timestamps@example.com")
    repository = SqlAlchemyBookRepository(session)
    book = Book.create(owner_id, "Book", "Author", 100)
    repository.save(book)
    session.commit()

    model = session.get(BookModel, book.id.to_persistence())

    assert model is not None
    assert model.created_at is not None
    assert model.updated_at is not None
