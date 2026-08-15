from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from typing import cast

import pytest
from sqlalchemy import Connection, Table, create_engine, event, inspect
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.infrastructure.persistence.datetime import canonicalize_utc_datetime
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.read.infrastructure.persistence.repositories.reading_history_repository import (
    SqlAlchemyReadingHistoryReadRepository,
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


def add_book(session: Session, owner_id: UserId, id: str, title: str) -> None:
    session.add(
        BookModel(
            id=id,
            user_id=owner_id.to_persistence(),
            title=title,
            author="Author",
            total_pages=300,
        )
    )


def add_reading_session(
    session: Session,
    *,
    id: str,
    owner_id: UserId,
    book_id: str,
    started_at: datetime,
    notes: str | None = None,
) -> None:
    session.add(
        ReadingSessionModel(
            id=id,
            user_id=owner_id.to_persistence(),
            book_id=book_id,
            start_page=10,
            end_page=22,
            started_at=started_at,
            ended_at=started_at + timedelta(minutes=30),
            notes=notes,
        )
    )


def seed_history(session: Session) -> tuple[UserId, UserId]:
    owner = UserId.new()
    other = UserId.new()
    add_user(session, owner)
    add_user(session, other)
    add_book(session, owner, "0BOOK000000000000000000001", "Old title")
    add_book(session, owner, "0BOOK000000000000000000002", "Second book")
    add_book(session, other, "0BOOK000000000000000000003", "Foreign book")
    add_reading_session(
        session,
        id="0SESSION00000000000000001",
        owner_id=owner,
        book_id="0BOOK000000000000000000001",
        started_at=START,
        notes="note",
    )
    add_reading_session(
        session,
        id="0SESSION00000000000000002",
        owner_id=owner,
        book_id="0BOOK000000000000000000002",
        started_at=START + timedelta(hours=1),
    )
    add_reading_session(
        session,
        id="0SESSION00000000000000003",
        owner_id=other,
        book_id="0BOOK000000000000000000003",
        started_at=START + timedelta(hours=2),
    )
    session.commit()
    return owner, other


def test_count_and_projection_are_owner_scoped_with_current_book_title(
    session: Session,
) -> None:
    owner, other = seed_history(session)
    first_book = session.get(BookModel, "0BOOK000000000000000000001")
    assert first_book is not None
    first_book.title = "Current title"
    session.commit()
    repository = SqlAlchemyReadingHistoryReadRepository(session)

    assert repository.count_by_owner(owner) == 2
    assert repository.count_by_owner(other) == 1
    items = repository.list_page_by_owner(owner, offset=0, limit=20)

    assert tuple(item.id for item in items) == (
        "0SESSION00000000000000002",
        "0SESSION00000000000000001",
    )
    assert {item.book_title for item in items} == {"Current title", "Second book"}
    assert items[1].notes == "note"
    assert items[1].pages_read == 13
    assert all(item.started_at.tzinfo == timezone.utc for item in items)
    assert all(item.ended_at.tzinfo == timezone.utc for item in items)


def test_order_tie_break_limit_offset_and_empty(session: Session) -> None:
    owner, _ = seed_history(session)
    add_reading_session(
        session,
        id="0SESSION00000000000000004",
        owner_id=owner,
        book_id="0BOOK000000000000000000001",
        started_at=START + timedelta(hours=1),
    )
    session.commit()
    repository = SqlAlchemyReadingHistoryReadRepository(session)

    page = repository.list_page_by_owner(owner, offset=1, limit=1)

    assert tuple(item.id for item in page) == ("0SESSION00000000000000002",)
    assert repository.list_page_by_owner(owner, offset=20, limit=10) == ()
    assert repository.list_page_by_owner(UserId.new(), offset=0, limit=10) == ()


def test_join_rejects_book_from_a_different_owner(session: Session) -> None:
    owner, other = seed_history(session)
    add_reading_session(
        session,
        id="0SESSION00000000000000004",
        owner_id=owner,
        book_id="0BOOK000000000000000000003",
        started_at=START + timedelta(hours=3),
    )
    session.commit()
    repository = SqlAlchemyReadingHistoryReadRepository(session)

    assert repository.count_by_owner(owner) == 2
    assert repository.count_by_owner(other) == 1
    assert all(
        item.book_id != "0BOOK000000000000000000003"
        for item in repository.list_page_by_owner(owner, offset=0, limit=20)
    )


def test_count_and_page_execute_exactly_two_selects(session: Session) -> None:
    owner, _ = seed_history(session)
    repository = SqlAlchemyReadingHistoryReadRepository(session)
    assert session.bind is not None
    statements: list[str] = []

    def record_select(
        _connection: Connection,
        _cursor,
        statement: str,
        _parameters,
        _context,
        _executemany: bool,
    ) -> None:
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(session.bind, "before_cursor_execute", record_select)
    try:
        repository.count_by_owner(owner)
        repository.list_page_by_owner(owner, offset=0, limit=20)
    finally:
        event.remove(session.bind, "before_cursor_execute", record_select)

    assert len(statements) == 2


def test_datetime_helper_normalizes_naive_and_aware_values() -> None:
    naive = datetime(2026, 8, 14, 12, 0)
    offset = timezone(timedelta(hours=-3))
    aware = datetime(2026, 8, 14, 9, 0, tzinfo=offset)

    assert canonicalize_utc_datetime(naive) == START
    assert canonicalize_utc_datetime(aware) == START
    assert canonicalize_utc_datetime(aware).tzinfo == timezone.utc


def test_history_index_has_expected_name_and_column_order(session: Session) -> None:
    model_indexes = cast(Table, ReadingSessionModel.__table__).indexes
    index = next(
        item for item in model_indexes if item.name == "ix_reading_sessions_user_started_id"
    )
    assert tuple(column.name for column in index.columns) == (
        "user_id",
        "started_at",
        "id",
    )
    assert session.bind is not None
    database_indexes = inspect(session.bind).get_indexes("reading_sessions")
    database_index = next(
        item for item in database_indexes if item["name"] == "ix_reading_sessions_user_started_id"
    )
    assert tuple(database_index["column_names"]) == ("user_id", "started_at", "id")
