from dataclasses import dataclass

from app.read.application.dtos.reading_progress_dto import ReadingProgressDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class GetReadingProgressQuery:
    owner_id: UserId
    book_id: BookId


class GetReadingProgressQueryHandler:
    def __init__(
        self,
        book_repository: IBookRepository,
        reading_session_repository: IReadingSessionRepository,
        calculator: ReadingProgressCalculator,
    ) -> None:
        self._book_repository = book_repository
        self._reading_session_repository = reading_session_repository
        self._calculator = calculator

    def __call__(self, query: GetReadingProgressQuery) -> ReadingProgressDTO:
        book = self._book_repository.get_by_id_and_owner(
            query.book_id,
            query.owner_id,
        )
        if book is None:
            raise BookNotFoundError()

        sessions = self._reading_session_repository.list_by_book_and_owner(
            query.book_id,
            query.owner_id,
        )
        progress = self._calculator.calculate(book, sessions)
        return ReadingProgressDTO.from_progress(progress)
