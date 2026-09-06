import logging
import sqlite3
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from sqlalchemy.exc import OperationalError

from app.read.application.dtos.reading_session_dto import ReadingSessionDTO
from app.read.application.errors.book_errors import BookNotFoundError
from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
    ProgressionDeliveryRepository,
)
from app.read.application.ports.progression_gateway import (
    ProgressionGateway,
    ProgressionGatewayError,
    ReadingProgressionOccurrence,
)
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
from app.shared.domain.tsid import new_tsid

_SQLITE_BUSY_CODE: int = sqlite3.SQLITE_BUSY
logger = logging.getLogger(__name__)


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
        progression_gateway: ProgressionGateway | None = None,
        progression_delivery_repository: ProgressionDeliveryRepository | None = None,
    ) -> None:
        self._book_repository = book_repository
        self._reading_session_repository = reading_session_repository
        self._book_completion_repository = book_completion_repository
        self._coverage_calculator = coverage_calculator
        self._progress_calculator = progress_calculator
        self._unit_of_work = unit_of_work
        self._sleeper = sleeper
        self._event_bus = event_bus
        self._progression_gateway = progression_gateway
        self._progression_delivery_repository = progression_delivery_repository

    def __call__(self, command: CreateReadingSessionCommand) -> ReadingSessionDTO:
        committed_session: ReadingSession | None = None
        committed_completion: BookCompletion | None = None
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
                    if self._progression_delivery_repository is not None:
                        # The delivery record references the session.  Flush
                        # the parent rows first because these repositories add
                        # independent SQLAlchemy mappers without ORM
                        # relationships between them.
                        uow.flush()
                        self._progression_delivery_repository.save(
                            ProgressionDeliveryIntent(
                                id=new_tsid(),
                                reading_session_id=session.id,
                                owner_id=session.owner_id,
                                pages_read=session.pages_read,
                            )
                        )
                    uow.flush()
                    uow.commit()
                    committed_session = session
                    committed_completion = new_completion
                    break
            except OperationalError as error:
                if acquired or not _is_retryable_acquisition_busy(error) or attempt == 1:
                    raise
                self._sleeper(0.050)

        if committed_session is None:
            raise AssertionError("unreachable")

        if committed_completion is not None and self._event_bus is not None:
            self._event_bus.publish(
                [
                    BookCompleted(
                        completion_id=committed_completion.id,
                        book_id=committed_completion.book_id,
                        completed_at=committed_completion.completed_at,
                    )
                ]
            )

        if self._progression_gateway is not None:
            try:
                self._progression_gateway.record(
                    ReadingProgressionOccurrence(
                        owner_id=committed_session.owner_id,
                        reading_session_id=committed_session.id,
                        pages_read=committed_session.pages_read,
                    )
                )
            except ProgressionGatewayError:
                logger.warning(
                    "Progression occurrence delivery failed",
                    exc_info=True,
                    extra={
                        "reading_session_id": committed_session.id.to_persistence(),
                        "owner_id": committed_session.owner_id.to_persistence(),
                    },
                )

        return ReadingSessionDTO.from_session(committed_session)
