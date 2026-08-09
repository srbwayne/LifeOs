from collections.abc import Callable

import pytest

from app.read.domain.aggregates.book import Book
from app.read.domain.errors.book_errors import (
    InvalidBookAuthorError,
    InvalidBookTitleError,
    InvalidTotalPagesError,
)
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.total_pages import TotalPages
from app.shared.domain.identifiers.user_id import UserId


def create_book(**overrides: object) -> Book:
    values: dict[str, object] = {
        "owner_id": UserId.new(),
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "total_pages": 560,
    }
    values.update(overrides)
    return Book.create(**values)  # type: ignore[arg-type]


def restore_book(**overrides: object) -> Book:
    values: dict[str, object] = {
        "id": BookId.new(),
        "owner_id": UserId.new(),
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "total_pages": TotalPages(560),
    }
    values.update(overrides)
    return Book.restore(**values)  # type: ignore[arg-type]


def test_create_book_preserves_valid_state_and_generates_id() -> None:
    owner_id = UserId.new()

    book = create_book(owner_id=owner_id)

    assert isinstance(book.id, BookId)
    assert book.owner_id == owner_id
    assert book.title == "Domain-Driven Design"
    assert book.author == "Eric Evans"
    assert book.total_pages == TotalPages(560)


@pytest.mark.parametrize("owner_id", [None, "owner-id"])
def test_create_book_rejects_invalid_owner(owner_id: object) -> None:
    with pytest.raises(TypeError, match="Book owner must be a UserId"):
        create_book(owner_id=owner_id)


def test_create_book_trims_title_and_author() -> None:
    book = create_book(title="  Clean Architecture  ", author="  Robert C. Martin  ")

    assert book.title == "Clean Architecture"
    assert book.author == "Robert C. Martin"


@pytest.mark.parametrize("title", ["", "   ", None, 123])
def test_create_book_rejects_invalid_title(title: object) -> None:
    with pytest.raises(InvalidBookTitleError):
        create_book(title=title)


@pytest.mark.parametrize("author", ["", "   ", None, 123])
def test_create_book_rejects_invalid_author(author: object) -> None:
    with pytest.raises(InvalidBookAuthorError):
        create_book(author=author)


@pytest.mark.parametrize("total_pages", [0, -10, True, "100"])
def test_create_book_rejects_invalid_total_pages(total_pages: object) -> None:
    with pytest.raises(InvalidTotalPagesError):
        create_book(total_pages=total_pages)


def test_create_book_accepts_absent_optional_fields() -> None:
    book = create_book()

    assert book.isbn is None
    assert book.publisher is None
    assert book.edition is None
    assert book.cover is None
    assert book.genre is None
    assert book.language is None


def test_create_book_preserves_and_trims_present_optional_fields() -> None:
    book = create_book(
        isbn=" 978-0-321-12521-7 ",
        publisher=" Addison-Wesley ",
        edition=" 1st ",
        cover=" cover-reference ",
        genre=" Software ",
        language=" English ",
    )

    assert book.isbn == "978-0-321-12521-7"
    assert book.publisher == "Addison-Wesley"
    assert book.edition == "1st"
    assert book.cover == "cover-reference"
    assert book.genre == "Software"
    assert book.language == "English"


@pytest.mark.parametrize("value", ["", "   "])
def test_create_book_normalizes_empty_optional_fields_to_none(value: str) -> None:
    book = create_book(
        isbn=value,
        publisher=value,
        edition=value,
        cover=value,
        genre=value,
        language=value,
    )

    assert book.isbn is None
    assert book.publisher is None
    assert book.edition is None
    assert book.cover is None
    assert book.genre is None
    assert book.language is None


@pytest.mark.parametrize(
    ("field", "factory"),
    [
        ("isbn", lambda: 123),
        ("publisher", list),
        ("edition", dict),
        ("cover", object),
        ("genre", lambda: True),
        ("language", tuple),
    ],
)
def test_create_book_rejects_non_string_optional_field(
    field: str, factory: Callable[[], object]
) -> None:
    with pytest.raises(TypeError, match=rf"Book {field} must be a string or None"):
        create_book(**{field: factory()})


def test_restore_book_preserves_identity_owner_and_normalized_state() -> None:
    book_id = BookId.new()
    owner_id = UserId.new()

    book = restore_book(
        id=book_id,
        owner_id=owner_id,
        title="  Refactoring  ",
        author="  Martin Fowler  ",
        isbn="  ",
    )

    assert book.id == book_id
    assert book.owner_id == owner_id
    assert book.title == "Refactoring"
    assert book.author == "Martin Fowler"
    assert book.isbn is None


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("id", "book-id", TypeError),
        ("owner_id", None, TypeError),
        ("title", " ", InvalidBookTitleError),
        ("author", " ", InvalidBookAuthorError),
        ("total_pages", 0, TypeError),
    ],
)
def test_restore_book_rejects_invalid_state(
    field: str, value: object, error: type[Exception]
) -> None:
    with pytest.raises(error):
        restore_book(**{field: value})


def test_book_equality_uses_only_book_id() -> None:
    book_id = BookId.new()
    first = restore_book(id=book_id, title="First title")
    second = restore_book(id=book_id, title="Different title")

    assert first == second


def test_books_with_same_content_and_different_ids_are_different() -> None:
    owner_id = UserId.new()
    first = create_book(owner_id=owner_id)
    second = create_book(owner_id=owner_id)

    assert first != second
    assert first.title == second.title
    assert first.author == second.author


def test_book_is_equal_only_to_another_book() -> None:
    book = create_book()

    assert book != book.id


def test_book_is_not_hashable() -> None:
    with pytest.raises(TypeError, match="unhashable type"):
        hash(create_book())


def test_duplicate_book_data_is_allowed() -> None:
    owner_id = UserId.new()

    first = create_book(owner_id=owner_id, isbn="same-isbn")
    second = create_book(owner_id=owner_id, isbn="same-isbn")

    assert first.id != second.id
    assert first.isbn == second.isbn


def test_create_book_does_not_produce_domain_events() -> None:
    assert create_book().domain_events == []


def test_restore_book_does_not_produce_domain_events() -> None:
    assert restore_book().domain_events == []
