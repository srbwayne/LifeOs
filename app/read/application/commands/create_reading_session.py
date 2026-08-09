from dataclasses import dataclass
from datetime import datetime

from app.read.application.dtos.reading_session_dto import ReadingSessionDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.value_objects.book_id import BookId
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.identifiers.user_id import UserId


@dataclass(frozen=True)
class CreateReadingSessionCommand:
    owner_id: UserId
    book_id: BookId
    start_page: int
    end_page: int
    started_at: datetime
    ended_at: datetime
    notes: str | None = None


class CreateReadingSessionCommandHandler:
    def __init__(
        self,
        book_repository: IBookRepository,
        reading_session_repository: IReadingSessionRepository,
        unit_of_work: IUnitOfWork,
    ) -> None:
        self._book_repository = book_repository
        self._reading_session_repository = reading_session_repository
        self._unit_of_work = unit_of_work

    def __call__(self, command: CreateReadingSessionCommand) -> ReadingSessionDTO:
        with self._unit_of_work as uow:
            book = self._book_repository.get_by_id_and_owner(
                command.book_id,
                command.owner_id,
            )
            if book is None:
                raise BookNotFoundError()

            session = ReadingSession.create(
                owner_id=command.owner_id,
                book_id=book.id,
                start_page=command.start_page,
                end_page=command.end_page,
                started_at=command.started_at,
                ended_at=command.ended_at,
                book_total_pages=book.total_pages,
                notes=command.notes,
            )
            self._reading_session_repository.save(session)
            uow.commit()

        return ReadingSessionDTO.from_session(session)
