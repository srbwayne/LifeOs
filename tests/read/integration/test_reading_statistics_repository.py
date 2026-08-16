from collections.abc import Iterator
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import Connection, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.dtos.reading_statistics_dto import ReadingStatisticsAggregateProjection
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.reading_session_model import ReadingSessionModel
from app.read.infrastructure.persistence.repositories.reading_statistics_repository import (
    SqlAlchemyReadingStatisticsReadRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base

START = datetime(2026, 8, 14, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    with factory() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, owner_id: UserId) -> None:
    now = datetime(2026, 8, 14)
    session.add(
        UserModel(
            id=owner_id.to_persistence(),
            email=f"{owner_id}@example.com",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )


def add_book(session: Session, owner_id: UserId, book_id: str) -> None:
    session.add(
        BookModel(
            id=book_id,
            user_id=owner_id.to_persistence(),
            title=book_id,
            author="Author",
            total_pages=300,
        )
    )


def add_session(
    session: Session,
    *,
    session_id: str,
    owner_id: UserId,
    book_id: str,
    start_page: int,
    end_page: int,
) -> None:
    session.add(
        ReadingSessionModel(
            id=session_id,
            user_id=owner_id.to_persistence(),
            book_id=book_id,
            start_page=start_page,
            end_page=end_page,
            started_at=START,
            ended_at=START + timedelta(minutes=30),
        )
    )


def test_empty_database_returns_zero_projection(session: Session) -> None:
    owner = UserId.new()
    add_user(session, owner)
    session.commit()
    result = SqlAlchemyReadingStatisticsReadRepository(session).get_by_owner(owner)
    assert result == ReadingStatisticsAggregateProjection(0, 0, 0, 0)


def test_statistics_are_owner_scoped_and_gross(session: Session) -> None:
    owner, other = UserId.new(), UserId.new()
    add_user(session, owner)
    add_user(session, other)
    add_book(session, owner, "0BOOK000000000000000000001")
    add_book(session, owner, "0BOOK000000000000000000002")
    add_book(session, other, "0BOOK000000000000000000003")
    add_session(
        session,
        session_id="0SESSION00000000000000001",
        owner_id=owner,
        book_id="0BOOK000000000000000000001",
        start_page=1,
        end_page=3,
    )
    add_session(
        session,
        session_id="0SESSION00000000000000002",
        owner_id=owner,
        book_id="0BOOK000000000000000000001",
        start_page=1,
        end_page=3,
    )
    add_session(
        session,
        session_id="0SESSION00000000000000003",
        owner_id=owner,
        book_id="0BOOK000000000000000000001",
        start_page=2,
        end_page=4,
    )
    add_session(
        session,
        session_id="0SESSION00000000000000004",
        owner_id=owner,
        book_id="0BOOK000000000000000000002",
        start_page=10,
        end_page=10,
    )
    add_session(
        session,
        session_id="0SESSION00000000000000005",
        owner_id=other,
        book_id="0BOOK000000000000000000003",
        start_page=1,
        end_page=100,
    )
    session.commit()
    repository = SqlAlchemyReadingStatisticsReadRepository(session)
    assert repository.get_by_owner(owner) == ReadingStatisticsAggregateProjection(2, 2, 4, 10)
    assert repository.get_by_owner(other) == ReadingStatisticsAggregateProjection(1, 1, 1, 100)


def test_books_without_sessions_are_counted(session: Session) -> None:
    owner = UserId.new()
    add_user(session, owner)
    add_book(session, owner, "0BOOK000000000000000000001")
    add_book(session, owner, "0BOOK000000000000000000002")
    add_session(
        session,
        session_id="0SESSION00000000000000001",
        owner_id=owner,
        book_id="0BOOK000000000000000000001",
        start_page=20,
        end_page=22,
    )
    session.commit()
    result = SqlAlchemyReadingStatisticsReadRepository(session).get_by_owner(owner)
    assert result == ReadingStatisticsAggregateProjection(2, 1, 1, 3)


def test_inconsistent_owner_relation_is_excluded(session: Session) -> None:
    owner, other = UserId.new(), UserId.new()
    add_user(session, owner)
    add_user(session, other)
    add_book(session, owner, "0BOOK000000000000000000001")
    add_book(session, other, "0BOOK000000000000000000002")
    add_session(
        session,
        session_id="0SESSION00000000000000001",
        owner_id=owner,
        book_id="0BOOK000000000000000000002",
        start_page=1,
        end_page=50,
    )
    session.commit()
    result = SqlAlchemyReadingStatisticsReadRepository(session).get_by_owner(owner)
    assert result == ReadingStatisticsAggregateProjection(1, 0, 0, 0)


def test_get_by_owner_executes_exactly_two_selects(session: Session) -> None:
    owner = UserId.new()
    add_user(session, owner)
    add_book(session, owner, "0BOOK000000000000000000001")
    session.commit()
    repository = SqlAlchemyReadingStatisticsReadRepository(session)
    assert session.bind is not None
    statements: list[str] = []

    def record_select(
        _connection: Connection, _cursor, statement: str, _parameters, _context, _executemany: bool
    ) -> None:
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(session.bind, "before_cursor_execute", record_select)
    try:
        repository.get_by_owner(owner)
    finally:
        event.remove(session.bind, "before_cursor_execute", record_select)
    assert len(statements) == 2
