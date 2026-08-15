from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from app.read.application.dtos.reading_history_dto import ReadingHistoryItemDTO
from app.read.application.queries.list_reading_history import (
    ListReadingHistoryQuery,
    ListReadingHistoryQueryHandler,
)
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.value_objects.book_id import BookId
from app.read.domain.value_objects.total_pages import TotalPages
from app.shared.domain.identifiers.user_id import UserId

START = datetime(2026, 8, 15, 12, 0, tzinfo=timezone.utc)
END = datetime(2026, 8, 15, 12, 30, tzinfo=timezone.utc)


def item(
    *,
    id: str = "session-1",
    book_id: str = "book-1",
    book_title: str = "Book",
    start_page: int = 10,
    end_page: int = 20,
    notes: str | None = None,
) -> ReadingHistoryItemDTO:
    return ReadingHistoryItemDTO.from_values(
        id=id,
        book_id=book_id,
        book_title=book_title,
        start_page=start_page,
        end_page=end_page,
        started_at=START,
        ended_at=END,
        notes=notes,
    )


class ReadingHistoryRepositoryStub:
    def __init__(self, total_items: int, items: tuple[ReadingHistoryItemDTO, ...]) -> None:
        self.total_items = total_items
        self.items = items
        self.calls: list[tuple[object, ...]] = []

    def count_by_owner(self, owner_id: UserId) -> int:
        self.calls.append(("count", owner_id))
        return self.total_items

    def list_page_by_owner(
        self,
        owner_id: UserId,
        offset: int,
        limit: int,
    ) -> tuple[ReadingHistoryItemDTO, ...]:
        self.calls.append(("list", owner_id, offset, limit))
        return self.items

    def save(self, *_args: object) -> None:
        raise AssertionError("History query must not save.")

    def commit(self) -> None:
        raise AssertionError("History query must not commit.")


def test_query_is_frozen() -> None:
    query = ListReadingHistoryQuery(UserId.new(), 1, 20)

    with pytest.raises(FrozenInstanceError):
        query.page = 2  # type: ignore[misc]


def test_empty_history_returns_requested_page_metadata() -> None:
    owner_id = UserId.new()
    repository = ReadingHistoryRepositoryStub(0, ())

    result = ListReadingHistoryQueryHandler(repository)(
        ListReadingHistoryQuery(owner_id=owner_id, page=1, size=20)
    )

    assert result.items == ()
    assert (result.page, result.size, result.total_items, result.total_pages) == (1, 20, 0, 0)
    assert repository.calls == [("count", owner_id), ("list", owner_id, 0, 20)]


def test_handler_returns_items_notes_timestamps_and_pagination() -> None:
    owner_id = UserId.new()
    items = (
        item(id="session-2", book_id="book-2", book_title="Second", notes="note"),
        item(id="session-1", notes=None),
    )
    repository = ReadingHistoryRepositoryStub(42, items)

    result = ListReadingHistoryQueryHandler(repository)(
        ListReadingHistoryQuery(owner_id=owner_id, page=2, size=20)
    )

    assert result.items == items
    assert result.items[0].book_title == "Second"
    assert result.items[0].notes == "note"
    assert result.items[1].notes is None
    assert result.items[0].started_at is START
    assert result.items[0].ended_at is END
    assert (result.page, result.size, result.total_items, result.total_pages) == (2, 20, 42, 3)
    assert repository.calls == [("count", owner_id), ("list", owner_id, 20, 20)]


def test_page_beyond_last_is_valid_and_returns_empty_items() -> None:
    owner_id = UserId.new()
    repository = ReadingHistoryRepositoryStub(42, ())

    result = ListReadingHistoryQueryHandler(repository)(
        ListReadingHistoryQuery(owner_id=owner_id, page=10, size=20)
    )

    assert result.items == ()
    assert (result.page, result.size, result.total_items, result.total_pages) == (10, 20, 42, 3)
    assert repository.calls[-1] == ("list", owner_id, 180, 20)


def test_pages_read_is_inclusive_and_matches_reading_session_semantics() -> None:
    owner_id = UserId.new()
    session = ReadingSession.create(
        owner_id=owner_id,
        book_id=BookId.new(),
        start_page=31,
        end_page=50,
        started_at=START,
        ended_at=END,
        book_total_pages=TotalPages(100),
    )
    history_item = item(start_page=31, end_page=50)

    assert history_item.pages_read == 20
    assert history_item.pages_read == session.pages_read


def test_handler_has_no_uow_event_bus_or_write_dependency() -> None:
    handler = ListReadingHistoryQueryHandler(ReadingHistoryRepositoryStub(0, ()))

    assert not hasattr(handler, "_unit_of_work")
    assert not hasattr(handler, "_event_bus")
