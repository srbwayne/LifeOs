import sqlite3
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError, OperationalError

from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommand,
    CreateReadingSessionCommandHandler,
)
from app.read.application.dtos.reading_session_dto import ReadingSessionDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.errors.reading_session_errors import (
    InvalidPageNumberError,
    InvalidReadingRangeError,
    InvalidReadingSessionTimeError,
    ReadingBeyondBookError,
)
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId

UTC_START = datetime(2026, 8, 9, 14, 0, tzinfo=timezone.utc)
UTC_END = datetime(2026, 8, 9, 14, 30, tzinfo=timezone.utc)


class FakeBookRepository:
    def __init__(self, books: tuple[Book, ...] = ()) -> None:
        self.books = books
        self.lookups: list[tuple[BookId, UserId]] = []
        self.save_count = 0
        self.list_count = 0
        self.get_error: Exception | None = None

    def save(self, book: Book) -> None:
        self.save_count += 1

    def list_by_owner(self, owner_id: UserId) -> tuple[Book, ...]:
        self.list_count += 1
        raise AssertionError("Reading session creation must not list the library.")

    def get_by_id_and_owner(self, book_id: BookId, owner_id: UserId) -> Book | None:
        if self.get_error:
            raise self.get_error
        self.lookups.append((book_id, owner_id))
        return next(
            (book for book in self.books if book.id == book_id and book.owner_id == owner_id),
            None,
        )


class FakeReadingSessionRepository:
    def __init__(self, sessions: tuple[ReadingSession, ...] = ()) -> None:
        self.saved: list[ReadingSession] = []
        self.sessions = sessions
        self.lookups: list[tuple[BookId, UserId]] = []

    def save(self, session: ReadingSession) -> None:
        self.saved.append(session)

    def list_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> tuple[ReadingSession, ...]:
        self.lookups.append((book_id, owner_id))
        return self.sessions


class FakeBookCompletionRepository:
    def __init__(self, completion: BookCompletion | None = None) -> None:
        self.completion = completion
        self.saved: list[BookCompletion] = []
        self.lookups: list[tuple[BookId, UserId]] = []

    def save(self, completion: BookCompletion) -> None:
        self.saved.append(completion)

    def get_by_book_and_owner(self, book_id: BookId, owner_id: UserId) -> BookCompletion | None:
        self.lookups.append((book_id, owner_id))
        return self.completion


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.enter_count = 0
        self.exit_count = 0
        self.commit_count = 0
        self.rollback_count = 0
        self.flush_count = 0
        self.acquisition_count = 0
        self.acquisition_errors: list[Exception] = []
        self.flush_error: Exception | None = None
        self.commit_error: Exception | None = None
        self.tracked_aggregates: list[AggregateRoot] = []

    def __enter__(self) -> "FakeUnitOfWork":
        self.enter_count += 1
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.exit_count += 1
        if exc_type is not None:
            self.rollback()

    def flush(self) -> None:
        self.flush_count += 1
        if self.flush_error:
            raise self.flush_error

    def acquire_write_intent(self) -> None:
        self.acquisition_count += 1
        if self.acquisition_errors:
            raise self.acquisition_errors.pop(0)

    def commit(self) -> None:
        self.commit_count += 1
        if self.commit_error:
            raise self.commit_error

    def rollback(self) -> None:
        self.rollback_count += 1

    def track_aggregate(self, aggregate: AggregateRoot) -> None:
        self.tracked_aggregates.append(aggregate)


def valid_command(
    owner_id: UserId, book_id: BookId, **overrides: object
) -> CreateReadingSessionCommand:
    values: dict[str, object] = {
        "owner_id": owner_id,
        "book_id": book_id,
        "start_page": 80,
        "end_page": 92,
        "started_at": UTC_START,
        "ended_at": UTC_END,
        "notes": None,
    }
    values.update(overrides)
    return CreateReadingSessionCommand(**values)  # type: ignore[arg-type]


def build_handler(
    books: tuple[Book, ...],
    sessions: tuple[ReadingSession, ...] = (),
    completion: BookCompletion | None = None,
    sleeper=lambda _: None,
) -> tuple[
    CreateReadingSessionCommandHandler,
    FakeBookRepository,
    FakeReadingSessionRepository,
    FakeBookCompletionRepository,
    FakeUnitOfWork,
]:
    book_repository = FakeBookRepository(books)
    session_repository = FakeReadingSessionRepository(sessions)
    completion_repository = FakeBookCompletionRepository(completion)
    unit_of_work = FakeUnitOfWork()
    handler = CreateReadingSessionCommandHandler(
        book_repository,
        session_repository,
        completion_repository,
        ReadingCoverageCalculator(),
        ReadingProgressCalculator(),
        unit_of_work,
        sleeper,
    )
    return handler, book_repository, session_repository, completion_repository, unit_of_work


def test_command_is_immutable() -> None:
    owner_id = UserId.new()
    command = valid_command(owner_id, BookId.new())

    with pytest.raises(FrozenInstanceError):
        command.start_page = 1  # type: ignore[misc]


def test_handler_creates_saves_commits_once_and_returns_dto() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    handler, book_repository, session_repository, _, unit_of_work = build_handler((book,))

    result = handler(valid_command(owner_id, book.id))

    assert isinstance(result, ReadingSessionDTO)
    assert book_repository.lookups == [(book.id, owner_id)]
    assert book_repository.list_count == 0
    assert book_repository.save_count == 0
    assert len(session_repository.saved) == 1
    saved = session_repository.saved[0]
    assert saved.book_id == book.id
    assert saved.owner_id == owner_id
    assert saved.end_page.value <= book.total_pages.value
    assert result == ReadingSessionDTO.from_session(saved)
    assert result.pages_read == 13
    assert unit_of_work.enter_count == 1
    assert unit_of_work.exit_count == 1
    assert unit_of_work.commit_count == 1
    assert unit_of_work.rollback_count == 0


def test_dto_does_not_expose_owner_and_is_immutable() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    handler, _, _, _, _ = build_handler((book,))

    result = handler(valid_command(owner_id, book.id))

    assert not hasattr(result, "owner_id")
    assert not hasattr(result, "user_id")
    with pytest.raises(FrozenInstanceError):
        result.notes = "Changed"  # type: ignore[misc]


@pytest.mark.parametrize("notes", [None, " Reflection "])
def test_handler_preserves_normalized_optional_notes(notes: str | None) -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    handler, _, _, _, _ = build_handler((book,))

    result = handler(valid_command(owner_id, book.id, notes=notes))

    assert result.notes == (notes.strip() if notes else None)


def test_handler_returns_utc_timestamps() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    handler, _, _, _, _ = build_handler((book,))
    offset = timezone(timedelta(hours=-3))

    result = handler(
        valid_command(
            owner_id,
            book.id,
            started_at=datetime(2026, 8, 9, 11, 0, tzinfo=offset),
            ended_at=datetime(2026, 8, 9, 11, 30, tzinfo=offset),
        )
    )

    assert result.started_at == UTC_START
    assert result.ended_at == UTC_END
    assert result.started_at.tzinfo is timezone.utc
    assert result.ended_at.tzinfo is timezone.utc


@pytest.mark.parametrize("include_other_owner", [False, True])
def test_missing_or_other_owner_book_has_same_error_without_save_or_commit(
    include_other_owner: bool,
) -> None:
    owner_id = UserId.new()
    book_id = BookId.new()
    books: tuple[Book, ...] = ()
    if include_other_owner:
        books = (
            Book.restore(
                id=book_id,
                owner_id=UserId.new(),
                title="Hidden",
                author="Author",
                total_pages=Book.create(UserId.new(), "Source", "Author", 100).total_pages,
            ),
        )
    handler, book_repository, session_repository, _, unit_of_work = build_handler(books)

    with pytest.raises(BookNotFoundError, match="Book not found"):
        handler(valid_command(owner_id, book_id))

    assert book_repository.lookups == [(book_id, owner_id)]
    assert session_repository.saved == []
    assert unit_of_work.commit_count == 0
    assert unit_of_work.rollback_count == 1


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"start_page": 0}, InvalidPageNumberError),
        ({"start_page": 10, "end_page": 9}, InvalidReadingRangeError),
        ({"end_page": 301}, ReadingBeyondBookError),
        ({"ended_at": UTC_START - timedelta(seconds=1)}, InvalidReadingSessionTimeError),
    ],
)
def test_domain_error_prevents_session_save_and_commit(
    overrides: dict[str, object], error: type[Exception]
) -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    handler, _, session_repository, _, unit_of_work = build_handler((book,))

    with pytest.raises(error):
        handler(valid_command(owner_id, book.id, **overrides))

    assert session_repository.saved == []
    assert unit_of_work.commit_count == 0
    assert unit_of_work.rollback_count == 1


def test_handler_does_not_track_or_publish_domain_events() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    handler, _, session_repository, _, unit_of_work = build_handler((book,))

    handler(valid_command(owner_id, book.id))

    assert unit_of_work.tracked_aggregates == []
    assert session_repository.saved[0].domain_events == []


def test_handler_creates_completion_when_new_session_reaches_full_coverage() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 100)
    existing = ReadingSession.create(owner_id, book.id, 1, 79, UTC_START, UTC_END, book.total_pages)
    handler, _, sessions, completions, uow = build_handler((book,), (existing,))

    result = handler(valid_command(owner_id, book.id, start_page=80, end_page=100))

    assert result.id == sessions.saved[0].id.to_persistence()
    assert len(completions.saved) == 1
    assert completions.saved[0].completed_at == sessions.saved[0].ended_at
    assert uow.flush_count == 1
    assert uow.commit_count == 1


def test_existing_completion_is_not_rewritten() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 100)
    existing_completion = BookCompletion.create(book.id, UTC_START)
    handler, _, sessions, completions, _ = build_handler((book,), completion=existing_completion)

    handler(valid_command(owner_id, book.id))

    assert len(sessions.saved) == 1
    assert completions.saved == []
    assert existing_completion.completed_at == UTC_START


class _Busy(sqlite3.OperationalError):
    sqlite_errorcode = sqlite3.SQLITE_BUSY


class _Locked(sqlite3.OperationalError):
    sqlite_errorcode = sqlite3.SQLITE_LOCKED


def _operational_error(original: Exception) -> OperationalError:
    return OperationalError("BEGIN IMMEDIATE", {}, original)


def test_busy_retries_once_after_context_rollback() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    slept: list[float] = []
    handler, _, _, _, uow = build_handler((book,), sleeper=slept.append)
    uow.acquisition_errors = [_operational_error(_Busy())]

    handler(valid_command(owner_id, book.id))

    assert uow.acquisition_count == 2
    assert uow.rollback_count == 1
    assert uow.commit_count == 1
    assert slept == [0.050]


def test_busy_twice_propagates_after_two_rollbacks() -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    slept: list[float] = []
    handler, _, sessions, completions, uow = build_handler((book,), sleeper=slept.append)
    uow.acquisition_errors = [_operational_error(_Busy()), _operational_error(_Busy())]

    with pytest.raises(OperationalError):
        handler(valid_command(owner_id, book.id))

    assert uow.acquisition_count == 2
    assert uow.rollback_count == 2
    assert uow.commit_count == 0
    assert slept == [0.050]
    assert sessions.saved == []
    assert completions.saved == []


@pytest.mark.parametrize(
    "error",
    [
        _operational_error(_Locked()),
        OperationalError("BEGIN IMMEDIATE", {}, Exception("generic")),
    ],
)
def test_non_busy_acquisition_errors_do_not_retry(error: OperationalError) -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    slept: list[float] = []
    handler, _, _, _, uow = build_handler((book,), sleeper=slept.append)
    uow.acquisition_errors = [error]
    with pytest.raises(OperationalError):
        handler(valid_command(owner_id, book.id))
    assert (uow.acquisition_count, uow.rollback_count, slept) == (1, 1, [])


@pytest.mark.parametrize(
    "failure_stage",
    ["post_acquisition", "flush", "commit", "integrity", "unknown"],
)
def test_failures_after_acquisition_do_not_retry(failure_stage: str) -> None:
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 300)
    slept: list[float] = []
    handler, book_repository, _, _, uow = build_handler((book,), sleeper=slept.append)

    if failure_stage == "post_acquisition":
        book_repository.get_error = OperationalError("SELECT", {}, Exception("failure"))
    elif failure_stage == "flush":
        uow.flush_error = OperationalError("FLUSH", {}, Exception("failure"))
    elif failure_stage == "commit":
        uow.commit_error = OperationalError("COMMIT", {}, Exception("failure"))
    elif failure_stage == "integrity":
        book_repository.get_error = IntegrityError("SELECT", {}, Exception("failure"))
    else:
        book_repository.get_error = RuntimeError("failure")

    with pytest.raises(Exception, match="failure"):
        handler(valid_command(owner_id, book.id))

    assert uow.acquisition_count == 1
    assert uow.rollback_count == 1
    assert slept == []
