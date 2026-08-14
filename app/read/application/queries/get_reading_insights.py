from dataclasses import dataclass

from app.read.application.dtos.reading_insights_dto import ReadingInsightsDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_insights_calculator import ReadingInsightsCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetReadingInsightsQuery:
    owner_id: UserId
    book_id: BookId


class GetReadingInsightsQueryHandler:
    def __init__(
        self,
        book_repository: IBookRepository,
        reading_session_repository: IReadingSessionRepository,
        coverage_calculator: ReadingCoverageCalculator,
        progress_calculator: ReadingProgressCalculator,
        insights_calculator: ReadingInsightsCalculator,
    ) -> None:
        self._book_repository = book_repository
        self._reading_session_repository = reading_session_repository
        self._coverage_calculator = coverage_calculator
        self._progress_calculator = progress_calculator
        self._insights_calculator = insights_calculator

    def __call__(self, query: GetReadingInsightsQuery) -> ReadingInsightsDTO:
        book = self._book_repository.get_by_id_and_owner(query.book_id, query.owner_id)
        if book is None:
            raise BookNotFoundError()

        sessions = self._reading_session_repository.list_by_book_and_owner(
            query.book_id,
            query.owner_id,
        )
        coverage = self._coverage_calculator.calculate(sessions)
        progress = self._progress_calculator.calculate_from_coverage(book, coverage)
        insights = self._insights_calculator.calculate(progress, coverage)
        return ReadingInsightsDTO.from_insights(insights)
