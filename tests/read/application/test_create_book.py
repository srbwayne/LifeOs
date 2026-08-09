from dataclasses import FrozenInstanceError

import pytest

from app.read.application.commands.create_book import (
    CreateBookCommand,
    CreateBookCommandHandler,
)
from app.read.application.dtos.book_dto import BookDTO
from app.read.domain.aggregates.book import Book
from app.read.domain.errors.book_errors import (
    InvalidBookAuthorError,
    InvalidBookTitleError,
    InvalidTotalPagesError,
)
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


class BookRepositoryFake:
    def __init__(self) -> None:
        self.saved: list[Book] = []

    def save(self, book: Book) -> None:
        self.saved.append(book)

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        return tuple(book for book in self.saved if book.owner_id == owner_id)


class UnitOfWorkFake:
    def __init__(self) -> None:
        self.enter_count = 0
        self.exit_count = 0
        self.commit_count = 0
        self.rollback_count = 0
        self.tracked_aggregates: list[AggregateRoot] = []

    def __enter__(self) -> "UnitOfWorkFake":
        self.enter_count += 1
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.exit_count += 1
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self.commit_count += 1

    def rollback(self) -> None:
        self.rollback_count += 1

    def track_aggregate(self, aggregate: AggregateRoot) -> None:
        self.tracked_aggregates.append(aggregate)


def build_handler() -> tuple[CreateBookCommandHandler, BookRepositoryFake, UnitOfWorkFake]:
    repository = BookRepositoryFake()
    unit_of_work = UnitOfWorkFake()
    return CreateBookCommandHandler(repository, unit_of_work), repository, unit_of_work


def valid_command(**overrides: object) -> CreateBookCommand:
    values: dict[str, object] = {
        "owner_id": UserId.new(),
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "total_pages": 560,
    }
    values.update(overrides)
    return CreateBookCommand(**values)  # type: ignore[arg-type]


def test_create_book_command_is_immutable() -> None:
    command = valid_command()

    with pytest.raises(FrozenInstanceError):
        command.title = "Changed"  # type: ignore[misc]


def test_create_book_persists_once_commits_once_and_returns_dto() -> None:
    handler, repository, unit_of_work = build_handler()
    owner_id = UserId.new()

    result = handler(valid_command(owner_id=owner_id))

    assert isinstance(result, BookDTO)
    assert len(repository.saved) == 1
    saved = repository.saved[0]
    assert saved.owner_id == owner_id
    assert result.id == saved.id.to_persistence()
    assert result.title == saved.title
    assert result.author == saved.author
    assert result.total_pages == saved.total_pages.value
    assert unit_of_work.enter_count == 1
    assert unit_of_work.exit_count == 1
    assert unit_of_work.commit_count == 1


def test_create_book_accepts_absent_optional_fields() -> None:
    handler, _, _ = build_handler()

    result = handler(valid_command())

    assert result.isbn is None
    assert result.publisher is None
    assert result.edition is None
    assert result.cover is None
    assert result.genre is None
    assert result.language is None


def test_create_book_preserves_all_optional_fields_in_dto() -> None:
    handler, _, _ = build_handler()

    result = handler(
        valid_command(
            isbn="978-0-321-12521-7",
            publisher="Addison-Wesley",
            edition="1st",
            cover="cover-reference",
            genre="Software",
            language="English",
        )
    )

    assert result.isbn == "978-0-321-12521-7"
    assert result.publisher == "Addison-Wesley"
    assert result.edition == "1st"
    assert result.cover == "cover-reference"
    assert result.genre == "Software"
    assert result.language == "English"


def test_create_book_dto_is_immutable_and_does_not_expose_owner() -> None:
    handler, _, _ = build_handler()

    result = handler(valid_command())

    assert not hasattr(result, "owner_id")
    assert not hasattr(result, "user_id")
    with pytest.raises(FrozenInstanceError):
        result.title = "Changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"title": " "}, InvalidBookTitleError),
        ({"author": " "}, InvalidBookAuthorError),
        ({"total_pages": 0}, InvalidTotalPagesError),
    ],
)
def test_domain_error_prevents_save_and_commit(
    overrides: dict[str, object], error: type[Exception]
) -> None:
    handler, repository, unit_of_work = build_handler()

    with pytest.raises(error):
        handler(valid_command(**overrides))

    assert repository.saved == []
    assert unit_of_work.commit_count == 0
    assert unit_of_work.rollback_count == 1


def test_create_book_does_not_check_duplicates_or_publish_events() -> None:
    handler, repository, unit_of_work = build_handler()
    owner_id = UserId.new()
    command = valid_command(owner_id=owner_id, isbn="same-isbn")

    first = handler(command)
    second = handler(command)

    assert first.id != second.id
    assert len(repository.saved) == 2
    assert unit_of_work.commit_count == 2
    assert unit_of_work.tracked_aggregates == []
    assert all(book.domain_events == [] for book in repository.saved)
