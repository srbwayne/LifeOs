from fastapi import Depends
from sqlalchemy.orm import Session

from app.read.application.commands.create_book import CreateBookCommandHandler
from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommandHandler,
)
from app.read.application.ports.reading_history_repository import (
    IReadingHistoryReadRepository,
)
from app.read.application.queries.get_reading_insights import GetReadingInsightsQueryHandler
from app.read.application.queries.get_reading_progress import GetReadingProgressQueryHandler
from app.read.application.queries.list_my_books import ListMyBooksQueryHandler
from app.read.application.queries.list_reading_history import (
    ListReadingHistoryQueryHandler,
)
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_insights_calculator import ReadingInsightsCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.read.infrastructure.persistence.repositories.reading_history_repository import (
    SqlAlchemyReadingHistoryReadRepository,
)
from app.read.infrastructure.persistence.repositories.reading_session_repository import (
    SqlAlchemyReadingSessionRepository,
)
from app.shared.application.event_bus import InMemoryEventBus
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def get_book_repository(db: Session = Depends(get_db)) -> IBookRepository:
    return SqlAlchemyBookRepository(db)


def get_reading_session_repository(
    db: Session = Depends(get_db),
) -> IReadingSessionRepository:
    return SqlAlchemyReadingSessionRepository(db)


def get_reading_history_repository(
    db: Session = Depends(get_db),
) -> IReadingHistoryReadRepository:
    return SqlAlchemyReadingHistoryReadRepository(db)


def get_book_uow(db: Session = Depends(get_db)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(db, InMemoryEventBus())


def get_create_book_handler(
    repository: IBookRepository = Depends(get_book_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_book_uow),
) -> CreateBookCommandHandler:
    return CreateBookCommandHandler(repository, unit_of_work)


def get_list_my_books_handler(
    repository: IBookRepository = Depends(get_book_repository),
) -> ListMyBooksQueryHandler:
    return ListMyBooksQueryHandler(repository)


def get_create_reading_session_handler(
    book_repository: IBookRepository = Depends(get_book_repository),
    reading_session_repository: IReadingSessionRepository = Depends(get_reading_session_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_book_uow),
) -> CreateReadingSessionCommandHandler:
    return CreateReadingSessionCommandHandler(
        book_repository,
        reading_session_repository,
        unit_of_work,
    )


def get_reading_progress_handler(
    book_repository: IBookRepository = Depends(get_book_repository),
    reading_session_repository: IReadingSessionRepository = Depends(get_reading_session_repository),
) -> GetReadingProgressQueryHandler:
    return GetReadingProgressQueryHandler(
        book_repository,
        reading_session_repository,
        ReadingProgressCalculator(),
    )


def get_reading_insights_handler(
    book_repository: IBookRepository = Depends(get_book_repository),
    reading_session_repository: IReadingSessionRepository = Depends(get_reading_session_repository),
) -> GetReadingInsightsQueryHandler:
    return GetReadingInsightsQueryHandler(
        book_repository,
        reading_session_repository,
        ReadingCoverageCalculator(),
        ReadingProgressCalculator(),
        ReadingInsightsCalculator(),
    )


def get_list_reading_history_handler(
    repository: IReadingHistoryReadRepository = Depends(get_reading_history_repository),
) -> ListReadingHistoryQueryHandler:
    return ListReadingHistoryQueryHandler(repository)
