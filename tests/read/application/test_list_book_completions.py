from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from app.read.application.dtos.book_completion_dto import (
    BookCompletionItemDTO,
    BookCompletionPageDTO,
)
from app.read.application.queries.list_book_completions import (
    ListBookCompletionsQuery,
    ListBookCompletionsQueryHandler,
)
from app.shared.domain.identifiers.user_id import UserId

COMPLETED_AT = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


def item(book_id: str = "book-1") -> BookCompletionItemDTO:
    return BookCompletionItemDTO(book_id, "Book", COMPLETED_AT)


class ReadRepositoryStub:
    def __init__(self, total_items: int, items: tuple[BookCompletionItemDTO, ...]) -> None:
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
    ) -> tuple[BookCompletionItemDTO, ...]:
        self.calls.append(("page", owner_id, offset, limit))
        return self.items


def test_query_is_frozen() -> None:
    query = ListBookCompletionsQuery(UserId.new(), 1, 20)

    with pytest.raises(FrozenInstanceError):
        query.page = 2  # type: ignore[misc]


def test_handler_propagates_owner_pagination_and_calls_count_before_page() -> None:
    owner_id = UserId.new()
    repository = ReadRepositoryStub(42, (item(),))

    result = ListBookCompletionsQueryHandler(repository)(
        ListBookCompletionsQuery(owner_id=owner_id, page=3, size=10)
    )

    assert result.items == (item(),)
    assert (result.page, result.size, result.total_items, result.total_pages) == (3, 10, 42, 5)
    assert repository.calls == [
        ("count", owner_id),
        ("page", owner_id, 20, 10),
    ]


def test_empty_result_still_executes_page_query() -> None:
    owner_id = UserId.new()
    repository = ReadRepositoryStub(0, ())

    result = ListBookCompletionsQueryHandler(repository)(
        ListBookCompletionsQuery(owner_id=owner_id, page=1, size=20)
    )

    assert isinstance(result, BookCompletionPageDTO)
    assert result.items == ()
    assert (result.page, result.size, result.total_items, result.total_pages) == (1, 20, 0, 0)
    assert repository.calls == [("count", owner_id), ("page", owner_id, 0, 20)]


def test_page_beyond_final_returns_empty_items_with_actual_metadata() -> None:
    owner_id = UserId.new()
    repository = ReadRepositoryStub(42, ())

    result = ListBookCompletionsQueryHandler(repository)(
        ListBookCompletionsQuery(owner_id=owner_id, page=10, size=20)
    )

    assert result.items == ()
    assert (result.page, result.size, result.total_items, result.total_pages) == (10, 20, 42, 3)
    assert repository.calls[-1] == ("page", owner_id, 180, 20)


def test_page_dto_and_items_are_immutable() -> None:
    page = BookCompletionPageDTO((item(),), 1, 20, 1, 1)

    with pytest.raises(FrozenInstanceError):
        page.page = 2  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        page.items = ()  # type: ignore[misc]


def test_handler_has_no_write_or_event_dependencies() -> None:
    handler = ListBookCompletionsQueryHandler(ReadRepositoryStub(0, ()))

    assert not hasattr(handler, "_unit_of_work")
    assert not hasattr(handler, "_event_bus")
    assert not hasattr(handler, "_write_repository")
