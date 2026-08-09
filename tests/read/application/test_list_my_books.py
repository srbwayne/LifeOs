from dataclasses import FrozenInstanceError

import pytest

from app.read.application.queries.list_my_books import (
    ListMyBooksQuery,
    ListMyBooksQueryHandler,
)
from app.read.domain.aggregates.book import Book
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class BookRepositoryStub:
    def __init__(self, books: tuple[Book, ...]) -> None:
        self.books = books
        self.listed_owners: list[UserId] = []

    def save(self, book: Book) -> None:
        raise AssertionError("Query must not save books.")

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        self.listed_owners.append(owner_id)
        return self.books

    def get_by_id_and_owner(self, book_id: BookId, owner_id: UserId) -> Book | None:
        raise AssertionError("List query must not get an individual book.")


def test_list_my_books_query_is_immutable() -> None:
    query = ListMyBooksQuery(owner_id=UserId.new())

    with pytest.raises(FrozenInstanceError):
        query.owner_id = UserId.new()  # type: ignore[misc]


def test_list_my_books_passes_owner_and_converts_repository_books() -> None:
    owner_id = UserId.new()
    books = (
        Book.create(owner_id, "First", "Author One", 100),
        Book.create(owner_id, "Second", "Author Two", 200),
    )
    repository = BookRepositoryStub(books)
    handler = ListMyBooksQueryHandler(repository)

    result = handler(ListMyBooksQuery(owner_id=owner_id))

    assert repository.listed_owners == [owner_id]
    assert tuple(book.id for book in result) == tuple(book.id.to_persistence() for book in books)
    assert tuple(book.title for book in result) == ("First", "Second")
    assert all(not hasattr(book, "owner_id") for book in result)


def test_list_my_books_returns_empty_tuple_for_empty_library() -> None:
    owner_id = UserId.new()
    repository = BookRepositoryStub(())
    handler = ListMyBooksQueryHandler(repository)

    result = handler(ListMyBooksQuery(owner_id=owner_id))

    assert result == ()
    assert repository.listed_owners == [owner_id]


def test_list_my_books_preserves_all_optional_fields() -> None:
    owner_id = UserId.new()
    book = Book.create(
        owner_id=owner_id,
        title="Book",
        author="Author",
        total_pages=300,
        isbn="isbn",
        publisher="publisher",
        edition="edition",
        cover="cover",
        genre="genre",
        language="language",
    )
    handler = ListMyBooksQueryHandler(BookRepositoryStub((book,)))

    result = handler(ListMyBooksQuery(owner_id=owner_id))[0]

    assert result.isbn == "isbn"
    assert result.publisher == "publisher"
    assert result.edition == "edition"
    assert result.cover == "cover"
    assert result.genre == "genre"
    assert result.language == "language"
