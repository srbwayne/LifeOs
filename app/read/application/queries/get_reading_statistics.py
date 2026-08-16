from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from app.read.application.dtos.reading_statistics_dto import ReadingStatisticsDTO
from app.read.application.ports.reading_statistics_repository import (
    IReadingStatisticsReadRepository,
)
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetReadingStatisticsQuery:
    owner_id: UserId


class GetReadingStatisticsQueryHandler:
    def __init__(self, repository: IReadingStatisticsReadRepository) -> None:
        self._repository = repository

    def __call__(self, query: GetReadingStatisticsQuery) -> ReadingStatisticsDTO:
        projection = self._repository.get_by_owner(query.owner_id)
        if projection.total_reading_sessions == 0:
            average = Decimal("0.00")
        else:
            average = (
                Decimal(projection.total_pages_read) / Decimal(projection.total_reading_sessions)
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return ReadingStatisticsDTO(
            total_books=projection.total_books,
            books_with_reading_sessions=projection.books_with_reading_sessions,
            total_reading_sessions=projection.total_reading_sessions,
            total_pages_read=projection.total_pages_read,
            average_pages_per_session=average,
        )
