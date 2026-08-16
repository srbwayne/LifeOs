from typing import Protocol

from app.read.application.dtos.reading_statistics_dto import (
    ReadingStatisticsAggregateProjection,
)
from app.shared.domain.identifiers.user_id import UserId


class IReadingStatisticsReadRepository(Protocol):
    def get_by_owner(self, owner_id: UserId) -> ReadingStatisticsAggregateProjection: ...
