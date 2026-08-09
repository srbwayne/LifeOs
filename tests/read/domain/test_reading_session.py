from collections.abc import Callable
from datetime import datetime, timedelta, timezone

import pytest

from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.errors.reading_session_errors import (
    InvalidPageNumberError,
    InvalidReadingRangeError,
    InvalidReadingSessionTimeError,
    ReadingBeyondBookError,
)
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.page_number import PageNumber
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.domain.value_objects.total_pages import TotalPages
from app.shared.domain.identifiers.user_id import UserId

UTC_START = datetime(2026, 8, 9, 14, 0, tzinfo=timezone.utc)
UTC_END = datetime(2026, 8, 9, 14, 30, tzinfo=timezone.utc)


def create_session(**overrides: object) -> ReadingSession:
    values: dict[str, object] = {
        "owner_id": UserId.new(),
        "book_id": BookId.new(),
        "start_page": 80,
        "end_page": 92,
        "started_at": UTC_START,
        "ended_at": UTC_END,
        "book_total_pages": TotalPages(300),
    }
    values.update(overrides)
    return ReadingSession.create(**values)  # type: ignore[arg-type]


def restore_session(**overrides: object) -> ReadingSession:
    values: dict[str, object] = {
        "id": ReadingSessionId.new(),
        "owner_id": UserId.new(),
        "book_id": BookId.new(),
        "start_page": PageNumber(80),
        "end_page": PageNumber(92),
        "started_at": UTC_START,
        "ended_at": UTC_END,
        "notes": None,
    }
    values.update(overrides)
    return ReadingSession.restore(**values)  # type: ignore[arg-type]


def test_create_reading_session_preserves_state_and_generates_id() -> None:
    owner_id = UserId.new()
    book_id = BookId.new()

    session = create_session(owner_id=owner_id, book_id=book_id)

    assert isinstance(session.id, ReadingSessionId)
    assert session.owner_id == owner_id
    assert session.book_id == book_id
    assert session.start_page == PageNumber(80)
    assert session.end_page == PageNumber(92)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("owner_id", None, "Reading session owner must be a UserId"),
        ("book_id", None, "Reading session book must be a BookId"),
    ],
)
def test_create_rejects_invalid_owner_or_book(field: str, value: object, message: str) -> None:
    with pytest.raises(TypeError, match=message):
        create_session(**{field: value})


def test_create_rejects_invalid_book_total_pages_type() -> None:
    with pytest.raises(TypeError, match="book total pages must be a TotalPages"):
        create_session(book_total_pages=300)


@pytest.mark.parametrize("field", ["start_page", "end_page"])
@pytest.mark.parametrize("value", [0, -1, True, "1"])
def test_create_rejects_invalid_page(field: str, value: object) -> None:
    with pytest.raises(InvalidPageNumberError):
        create_session(**{field: value})


def test_create_rejects_inverted_range() -> None:
    with pytest.raises(InvalidReadingRangeError):
        create_session(start_page=10, end_page=9)


def test_create_rejects_end_page_beyond_book() -> None:
    with pytest.raises(ReadingBeyondBookError):
        create_session(end_page=301)


@pytest.mark.parametrize(
    ("start_page", "end_page", "expected"),
    [(150, 150, 1), (80, 92, 13)],
)
def test_pages_read_is_calculated_from_inclusive_range(
    start_page: int, end_page: int, expected: int
) -> None:
    session = create_session(start_page=start_page, end_page=end_page)

    assert session.pages_read == expected


def test_pages_read_is_a_read_only_property() -> None:
    session = create_session()

    with pytest.raises(AttributeError):
        session.pages_read = 99  # type: ignore[misc]


@pytest.mark.parametrize("notes", [None, "", "   "])
def test_notes_absent_or_empty_normalizes_to_none(notes: str | None) -> None:
    assert create_session(notes=notes).notes is None


def test_notes_are_trimmed() -> None:
    assert create_session(notes="  Important reflection  ").notes == "Important reflection"


@pytest.mark.parametrize("factory", [lambda: 123, list, dict, object])
def test_notes_reject_invalid_type(factory: Callable[[], object]) -> None:
    with pytest.raises(TypeError, match="notes must be a string or None"):
        create_session(notes=factory())


def test_timezone_offset_is_normalized_to_utc() -> None:
    offset = timezone(timedelta(hours=-3))
    started_at = datetime(2026, 8, 9, 11, 0, tzinfo=offset)
    ended_at = datetime(2026, 8, 9, 11, 30, tzinfo=offset)

    session = create_session(started_at=started_at, ended_at=ended_at)

    assert session.started_at == UTC_START
    assert session.ended_at == UTC_END
    assert session.started_at.tzinfo is timezone.utc
    assert session.ended_at.tzinfo is timezone.utc


@pytest.mark.parametrize("field", ["started_at", "ended_at"])
def test_create_rejects_naive_datetime(field: str) -> None:
    with pytest.raises(InvalidReadingSessionTimeError):
        create_session(**{field: datetime(2026, 8, 9, 14, 0)})


@pytest.mark.parametrize("field", ["started_at", "ended_at"])
def test_create_rejects_non_datetime_value(field: str) -> None:
    with pytest.raises(InvalidReadingSessionTimeError):
        create_session(**{field: "2026-08-09T14:00:00Z"})


def test_create_rejects_end_before_start() -> None:
    with pytest.raises(InvalidReadingSessionTimeError):
        create_session(ended_at=UTC_START - timedelta(seconds=1))


def test_create_allows_equal_start_and_end_time() -> None:
    session = create_session(ended_at=UTC_START)

    assert session.started_at == session.ended_at


def test_restore_preserves_identity_owner_book_and_intrinsic_state() -> None:
    session_id = ReadingSessionId.new()
    owner_id = UserId.new()
    book_id = BookId.new()

    session = restore_session(
        id=session_id,
        owner_id=owner_id,
        book_id=book_id,
        notes="  Restored  ",
    )

    assert session.id == session_id
    assert session.owner_id == owner_id
    assert session.book_id == book_id
    assert session.notes == "Restored"


def test_restore_does_not_require_or_validate_book_total_pages() -> None:
    session = restore_session(start_page=PageNumber(500), end_page=PageNumber(600))

    assert session.end_page == PageNumber(600)
    assert session.pages_read == 101


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("id", "session-id", TypeError),
        ("owner_id", None, TypeError),
        ("book_id", None, TypeError),
        ("start_page", 1, TypeError),
        ("end_page", 2, TypeError),
        ("started_at", datetime(2026, 8, 9, 14, 0), InvalidReadingSessionTimeError),
    ],
)
def test_restore_rejects_invalid_intrinsic_state(
    field: str, value: object, error: type[Exception]
) -> None:
    with pytest.raises(error):
        restore_session(**{field: value})


def test_restore_rejects_inverted_range() -> None:
    with pytest.raises(InvalidReadingRangeError):
        restore_session(start_page=PageNumber(10), end_page=PageNumber(9))


def test_reading_session_equality_uses_only_identity() -> None:
    session_id = ReadingSessionId.new()

    first = restore_session(id=session_id, notes="First")
    second = restore_session(id=session_id, notes="Second")

    assert first == second


def test_reading_sessions_with_different_ids_are_different() -> None:
    owner_id = UserId.new()
    book_id = BookId.new()

    first = create_session(owner_id=owner_id, book_id=book_id)
    second = create_session(owner_id=owner_id, book_id=book_id)

    assert first != second


def test_reading_session_is_equal_only_to_another_session() -> None:
    session = create_session()

    assert session != session.id


def test_reading_session_is_not_hashable() -> None:
    with pytest.raises(TypeError, match="unhashable type"):
        hash(create_session())


def test_create_and_restore_do_not_produce_domain_events() -> None:
    assert create_session().domain_events == []
    assert restore_session().domain_events == []


def test_reading_session_has_no_public_edit_operations() -> None:
    forbidden = {"change_pages", "update_notes", "change_time", "update"}

    assert forbidden.isdisjoint(dir(ReadingSession))
