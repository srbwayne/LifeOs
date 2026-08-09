from fastapi import Depends
from sqlalchemy.orm import Session

from app.read.application.commands.create_book import CreateBookCommandHandler
from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommandHandler,
)
from app.read.application.queries.list_my_books import ListMyBooksQueryHandler
from app.read.domain.ports.book_repository import IBookRepository
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
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
