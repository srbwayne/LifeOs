from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from app.read.application.dtos.reading_statistics_dto import (
    ReadingStatisticsAggregateProjection,
    ReadingStatisticsDTO,
)
from app.read.application.queries.get_reading_statistics import (
    GetReadingStatisticsQuery,
    GetReadingStatisticsQueryHandler,
)
from app.shared.domain.identifiers.user_id import UserId


def projection(
    *,
    total_books: int = 0,
    books_with_reading_sessions: int = 0,
    total_reading_sessions: int = 0,
    total_pages_read: int = 0,
) -> ReadingStatisticsAggregateProjection:
    return ReadingStatisticsAggregateProjection(
        total_books=total_books,
        books_with_reading_sessions=books_with_reading_sessions,
        total_reading_sessions=total_reading_sessions,
        total_pages_read=total_pages_read,
    )


class RepositoryStub:
    def __init__(self, result: ReadingStatisticsAggregateProjection) -> None:
        self.result = result
        self.calls: list[UserId] = []

    def get_by_owner(self, owner_id: UserId) -> ReadingStatisticsAggregateProjection:
        self.calls.append(owner_id)
        return self.result


def test_query_projection_and_dto_are_immutable() -> None:
    query = GetReadingStatisticsQuery(UserId.new())
    with pytest.raises(FrozenInstanceError):
        query.owner_id = UserId.new()  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        projection().total_books = 1  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        ReadingStatisticsDTO(0, 0, 0, 0, Decimal("0.00")).total_books = 1  # type: ignore[misc]


def test_empty_aggregate_returns_zero_average() -> None:
    owner = UserId.new()
    repository = RepositoryStub(projection())
    result = GetReadingStatisticsQueryHandler(repository)(GetReadingStatisticsQuery(owner))
    assert result == ReadingStatisticsDTO(0, 0, 0, 0, Decimal("0.00"))
    assert repository.calls == [owner]


@pytest.mark.parametrize(
    ("pages", "sessions", "expected"),
    [
        (12, 1, Decimal("12.00")),
        (3, 2, Decimal("1.50")),
        (1, 8, Decimal("0.13")),
    ],
)
def test_average_uses_decimal_round_half_up(pages: int, sessions: int, expected: Decimal) -> None:
    owner = UserId.new()
    repository = RepositoryStub(
        projection(
            total_books=2,
            books_with_reading_sessions=1,
            total_reading_sessions=sessions,
            total_pages_read=pages,
        )
    )
    result = GetReadingStatisticsQueryHandler(repository)(GetReadingStatisticsQuery(owner))
    assert result.average_pages_per_session == expected
    assert result.total_books == 2
    assert result.books_with_reading_sessions == 1


def test_handler_preserves_gross_reread_and_overlap_aggregates() -> None:
    owner = UserId.new()
    repository = RepositoryStub(
        projection(
            total_books=2,
            books_with_reading_sessions=2,
            total_reading_sessions=3,
            total_pages_read=33,
        )
    )
    result = GetReadingStatisticsQueryHandler(repository)(GetReadingStatisticsQuery(owner))
    assert (
        result.total_books,
        result.books_with_reading_sessions,
        result.total_reading_sessions,
        result.total_pages_read,
    ) == (2, 2, 3, 33)
    assert result.average_pages_per_session == Decimal("11.00")
