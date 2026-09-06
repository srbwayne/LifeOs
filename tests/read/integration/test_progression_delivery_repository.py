from datetime import datetime

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.reading_session_model import ReadingSessionModel
from app.read.infrastructure.persistence.repositories.progression_delivery_repository import (
    SqlAlchemyProgressionDeliveryRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.domain.tsid import new_tsid
from app.shared.infrastructure.database import Base


def _database() -> tuple[Engine, str, str, str]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    owner = new_tsid()
    book = new_tsid()
    reading_session = new_tsid()
    now = datetime(2026, 1, 1)
    with Session(engine) as session:
        session.add(
            UserModel(
                id=owner,
                email=f"{owner}@example.test",
                hashed_password="hash",
                created_at=now,
                updated_at=now,
            )
        )
        session.add(
            BookModel(
                id=book,
                user_id=owner,
                title="Book",
                author="Author",
                total_pages=100,
                created_at=now,
                updated_at=now,
            )
        )
        session.add(
            ReadingSessionModel(
                id=reading_session,
                user_id=owner,
                book_id=book,
                start_page=1,
                end_page=10,
                started_at=now,
                ended_at=now,
                notes=None,
                created_at=now,
                updated_at=now,
            )
        )
        session.commit()
    return engine, owner, book, reading_session


def _intent(owner: str, reading_session: str, *, error: str | None = None, created_at=None):
    return ProgressionDeliveryIntent(
        id=new_tsid(),
        reading_session_id=ReadingSessionId.from_value(reading_session),
        owner_id=UserId.from_value(owner),
        pages_read=10,
        last_error=error,
        created_at=created_at,
        updated_at=created_at,
    )


def test_recovery_matrix_and_owner_ordering() -> None:
    engine, owner, book, first_session = _database()
    with Session(engine) as session:
        second_session = new_tsid()
        session.add(
            ReadingSessionModel(
                id=second_session,
                user_id=owner,
                book_id=book,
                start_page=11,
                end_page=20,
                started_at=datetime(2026, 1, 1),
                ended_at=datetime(2026, 1, 1),
                notes=None,
                created_at=datetime(2026, 1, 1),
                updated_at=datetime(2026, 1, 1),
            )
        )
        session.flush()
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        older = _intent(owner, first_session, created_at=datetime(2026, 1, 1))
        newer = _intent(
            owner,
            second_session,
            created_at=datetime(2026, 1, 2),
        )
        repository.save(older)
        repository.save(newer)
        session.commit()

        candidates = repository.list_unresolved()
        assert [item.id for item in candidates] == [older.id, newer.id]
        assert repository.has_older_blocking(newer.id) is True

        repository.mark_delivered(older.id, datetime(2026, 1, 3))
        session.commit()
        assert repository.has_older_blocking(newer.id) is False
    engine.dispose()


@pytest.mark.parametrize("error", ["http_status_400", "http_status_409"])
def test_terminal_failure_does_not_block_or_recover(error: str) -> None:
    engine, owner, book, first_session = _database()
    with Session(engine) as session:
        second_session = new_tsid()
        session.add(
            ReadingSessionModel(
                id=second_session,
                user_id=owner,
                book_id=book,
                start_page=11,
                end_page=20,
                started_at=datetime(2026, 1, 1),
                ended_at=datetime(2026, 1, 1),
                notes=None,
                created_at=datetime(2026, 1, 1),
                updated_at=datetime(2026, 1, 1),
            )
        )
        session.flush()
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        terminal = _intent(owner, first_session, error=error, created_at=datetime(2026, 1, 1))
        newer = _intent(owner, second_session, created_at=datetime(2026, 1, 2))
        repository.save(terminal)
        repository.save(newer)
        session.commit()

        assert [item.id for item in repository.list_unresolved()] == [newer.id]
        assert repository.has_older_blocking(newer.id) is False
    engine.dispose()


def test_unique_reading_session_and_transitions_are_persisted() -> None:
    engine, owner, book, reading_session = _database()
    with Session(engine) as session:
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        first = _intent(owner, reading_session, created_at=datetime(2026, 1, 1))
        repository.save(first)
        session.commit()
        duplicate = _intent(owner, reading_session, created_at=datetime(2026, 1, 2))
        repository.save(duplicate)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()

        repository.mark_failed(first.id, datetime(2026, 1, 2), "delivery_failed")
        session.commit()
        failed = repository.get_by_id(first.id)
        assert failed is not None
        assert failed.status == "FAILED"
        assert failed.attempt_count == 1
        assert failed.last_error == "delivery_failed"

        repository.mark_delivered(first.id, datetime(2026, 1, 3))
        session.commit()
        delivered = repository.get_by_id(first.id)
        assert delivered is not None
        assert delivered.status == "DELIVERED"
        assert delivered.attempt_count == 2
        assert delivered.last_error is None
    engine.dispose()
