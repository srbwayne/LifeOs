from collections.abc import Iterator
from datetime import datetime, timezone
from typing import cast

import pytest
from sqlalchemy import Table, create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.value_objects.total_pages import TotalPages
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.read.infrastructure.persistence.repositories.reading_session_repository import (
    SqlAlchemyReadingSessionRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base

START = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)
END = datetime(2026, 8, 9, 12, 30, tzinfo=timezone.utc)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    with session_factory() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId) -> None:
    now = datetime(2026, 8, 9)
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=f"{user_id}@example.com",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )
    session.commit()


def add_book(session: Session, owner_id: UserId) -> Book:
    book = Book.create(owner_id, "Book", "Author", 300)
    SqlAlchemyBookRepository(session).save(book)
    session.commit()
    return book


def make_reading_session(owner_id: UserId, book: Book, notes: str | None = None) -> ReadingSession:
    return ReadingSession.create(
        owner_id=owner_id,
        book_id=book.id,
        start_page=10,
        end_page=22,
        started_at=START,
        ended_at=END,
        book_total_pages=book.total_pages,
        notes=notes,
    )


def test_save_adds_session_without_committing(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    repository = SqlAlchemyReadingSessionRepository(session)
    reading_session = make_reading_session(owner_id, book)

    repository.save(reading_session)

    assert any(
        isinstance(model, ReadingSessionModel) and model.id == reading_session.id.to_persistence()
        for model in session.new
    )
    session.rollback()
    assert session.get(ReadingSessionModel, reading_session.id.to_persistence()) is None


def test_commit_persists_fields_timestamps_and_notes(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    reading_session = make_reading_session(owner_id, book, "reflection")
    SqlAlchemyReadingSessionRepository(session).save(reading_session)
    session.commit()

    model = session.get(ReadingSessionModel, reading_session.id.to_persistence())

    assert model is not None
    assert model.user_id == owner_id.to_persistence()
    assert model.book_id == book.id.to_persistence()
    assert model.start_page == 10
    assert model.end_page == 22
    assert model.notes == "reflection"
    assert model.created_at is not None
    assert model.updated_at is not None
    assert ReadingSessionModel.__table__.c.get("pages_read") is None


def test_repository_round_trip_restores_sqlite_datetimes_as_utc(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    reading_session = make_reading_session(owner_id, book)
    SqlAlchemyReadingSessionRepository(session).save(reading_session)
    session.commit()

    model = session.scalar(
        select(ReadingSessionModel).where(
            ReadingSessionModel.id == reading_session.id.to_persistence()
        )
    )
    assert model is not None

    from app.read.infrastructure.persistence.mappers.reading_session_mapper import (
        ReadingSessionMapper,
    )

    restored = ReadingSessionMapper.to_domain(model)
    assert restored.started_at == START
    assert restored.ended_at == END
    assert restored.pages_read == 13


@pytest.mark.parametrize(
    ("start_page", "end_page", "started_at", "ended_at"),
    [
        (0, 1, START, END),
        (2, 1, START, END),
        (1, 1, END, START),
    ],
)
def test_database_constraints_reject_invalid_intrinsic_state(
    session: Session,
    start_page: int,
    end_page: int,
    started_at: datetime,
    ended_at: datetime,
) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    book = add_book(session, owner_id)
    session.add(
        ReadingSessionModel(
            id="0HZZZZZZZZZZZZZZZZZZZZZZZZ",
            user_id=owner_id.to_persistence(),
            book_id=book.id.to_persistence(),
            start_page=start_page,
            end_page=end_page,
            started_at=started_at,
            ended_at=ended_at,
            notes=None,
        )
    )

    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_foreign_keys_reject_missing_owner_or_book(session: Session) -> None:
    session.add(
        ReadingSessionModel(
            id="0HZZZZZZZZZZZZZZZZZZZZZZZY",
            user_id=UserId.new().to_persistence(),
            book_id=Book.create(UserId.new(), "Book", "Author", 10).id.to_persistence(),
            start_page=1,
            end_page=1,
            started_at=START,
            ended_at=END,
            notes=None,
        )
    )

    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_model_has_no_secondary_indexes() -> None:
    indexes = cast(Table, ReadingSessionModel.__table__).indexes

    assert indexes == set()
    assert TotalPages(1).value == 1
