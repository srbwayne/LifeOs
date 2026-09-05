import sqlite3
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from sqlalchemy.exc import OperationalError

from app.read.application.dtos.reading_session_dto import ReadingSessionDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.events.book_completed import BookCompleted
from app.read.domain.ports.book_completion_repository import IBookCompletionRepository
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.application.event_bus import IEventBus
from app.shared.domain.identifiers.user_id import UserId

_SQLITE_BUSY_CODE: int = sqlite3.SQLITE_BUSY


class ReadingSessionWriteUnitOfWork(Protocol):
    def __enter__(self) -> "ReadingSessionWriteUnitOfWork": ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...

    def acquire_write_intent(self) -> None: ...

    def flush(self) -> None: ...

    def commit(self) -> None: ...


def _is_retryable_acquisition_busy(error: OperationalError) -> bool:
    return (
        isinstance(error.orig, sqlite3.OperationalError)
        and getattr(error.orig, "sqlite_errorcode", None) == _SQLITE_BUSY_CODE
    )


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
        book_completion_repository: IBookCompletionRepository,
        coverage_calculator: ReadingCoverageCalculator,
        progress_calculator: ReadingProgressCalculator,
        unit_of_work: ReadingSessionWriteUnitOfWork,
        sleeper: Callable[[float], None] = time.sleep,
        event_bus: IEventBus | None = None,
    ) -> None:
        self._book_repository = book_repository
        self._reading_session_repository = reading_session_repository
        self._book_completion_repository = book_completion_repository
        self._coverage_calculator = coverage_calculator
        self._progress_calculator = progress_calculator
        self._unit_of_work = unit_of_work
        self._sleeper = sleeper
        self._event_bus = event_bus

    def __call__(self, command: CreateReadingSessionCommand) -> ReadingSessionDTO:
        for attempt in range(2):
            acquired = False
            try:
                with self._unit_of_work as uow:
                    new_completion: BookCompletion | None = None
                    uow.acquire_write_intent()
                    acquired = True

                    book = self._book_repository.get_by_id_and_owner(
                        command.book_id,
                        command.owner_id,
                    )
                    if book is None:
                        raise BookNotFoundError()

                    completion = self._book_completion_repository.get_by_book_and_owner(
                        book.id,
                        command.owner_id,
                    )
                    existing_sessions = self._reading_session_repository.list_by_book_and_owner(
                        book.id,
                        command.owner_id,
                    )
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
                    coverage = self._coverage_calculator.calculate(existing_sessions + (session,))
                    progress = self._progress_calculator.calculate_from_coverage(book, coverage)
                    self._reading_session_repository.save(session)
                    if progress.completed and completion is None:
                        new_completion = BookCompletion.create(book.id, session.ended_at)
                        self._book_completion_repository.save(new_completion)
                    uow.flush()
                    uow.commit()
                    if new_completion is not None and self._event_bus is not None:
                        self._event_bus.publish(
                            [
                                BookCompleted(
                                    completion_id=new_completion.id,
                                    book_id=new_completion.book_id,
                                    completed_at=new_completion.completed_at,
                                )
                            ]
                        )
                    return ReadingSessionDTO.from_session(session)
            except OperationalError as error:
                if acquired or not _is_retryable_acquisition_busy(error) or attempt == 1:
                    raise
                self._sleeper(0.050)

        raise AssertionError("unreachable")
