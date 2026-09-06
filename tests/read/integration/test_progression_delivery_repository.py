from datetime import datetime
from pathlib import Path
from typing import cast

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.application.ports.progression_gateway import (
    ReadingProgressionOccurrence,
)
from app.read.application.services.progression_delivery_dispatcher import (
    DeliveryTransactionFactory,
    ProgressionDeliveryDispatcher,
    RetryableProgressionDeliveryError,
)
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.read.infrastructure.integrations.durable_progression_gateway import (
    DurableProgressionGateway,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,
)
from app.read.infrastructure.persistence.models.reading_session_model import ReadingSessionModel
from app.read.infrastructure.persistence.repositories.progression_delivery_repository import (
    SqlAlchemyProgressionDeliveryRepository,
    SqlAlchemyProgressionDeliveryTransaction,
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


def _intent(
    owner: str,
    reading_session: str,
    *,
    error: str | None = None,
    status: str = "PENDING",
    created_at=None,
):
    return ProgressionDeliveryIntent(
        id=new_tsid(),
        reading_session_id=ReadingSessionId.from_value(reading_session),
        owner_id=UserId.from_value(owner),
        pages_read=10,
        status=status,
        last_error=error,
        created_at=created_at,
        updated_at=created_at,
    )


class _RecordingGateway:
    def __init__(self, failing_session: str | None = None) -> None:
        self.failing_session = failing_session
        self.calls: list[str] = []

    def record(self, occurrence: ReadingProgressionOccurrence) -> None:
        session_id = occurrence.reading_session_id.to_persistence()
        self.calls.append(session_id)
        if session_id == self.failing_session:
            raise RetryableProgressionDeliveryError("offline")


def _file_database(tmp_path: Path) -> tuple[Engine, str, str, str]:
    engine = create_engine(f"sqlite:///{(tmp_path / 'delivery.db').as_posix()}")
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


def test_retryable_failed_record_is_a_recovery_candidate() -> None:
    engine, owner, _, reading_session = _database()
    with Session(engine) as session:
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        intent = _intent(
            owner,
            reading_session,
            status="FAILED",
            error="delivery_failed",
            created_at=datetime(2026, 1, 1),
        )
        repository.save(intent)
        session.commit()

        candidates = repository.list_unresolved()

        assert [candidate.id for candidate in candidates] == [intent.id]
    engine.dispose()


def test_dispatch_for_reading_session_uses_concrete_persistence_path(tmp_path: Path) -> None:
    engine, owner, _, reading_session = _file_database(tmp_path)
    factory = sessionmaker(bind=engine)
    with factory() as creation_session:
        repository = SqlAlchemyProgressionDeliveryRepository(creation_session)
        intent = _intent(owner, reading_session, created_at=datetime(2026, 1, 1))
        repository.save(intent)
        creation_session.commit()

    delivery_sessions: list[Session] = []

    def tracked_session_factory() -> Session:
        session = factory()
        delivery_sessions.append(session)
        return session

    downstream = _RecordingGateway()
    dispatcher = ProgressionDeliveryDispatcher(
        cast(
            DeliveryTransactionFactory,
            lambda: SqlAlchemyProgressionDeliveryTransaction(tracked_session_factory),
        ),
        downstream,
    )
    dispatcher.dispatch_for_reading_session(ReadingSessionId.from_value(reading_session))

    with factory() as verification:
        persisted = verification.get(ProgressionDeliveryModel, intent.id)
        assert persisted is not None
        assert persisted.status == "DELIVERED"
        assert persisted.attempt_count == 1
        assert persisted.last_attempt_at is not None
        assert persisted.delivered_at is not None
        assert persisted.last_error is None
    assert downstream.calls == [reading_session]
    assert delivery_sessions
    assert all(session is not creation_session for session in delivery_sessions)
    engine.dispose()


def test_recovery_entry_orders_and_isolates_subjects(tmp_path: Path) -> None:
    engine, owner_a, book_a, session_a = _file_database(tmp_path)
    owner_b = new_tsid()
    book_b = new_tsid()
    session_b = new_tsid()
    session_a_newer = new_tsid()
    now = datetime(2026, 1, 1)
    with Session(engine) as session:
        session.add(
            UserModel(
                id=owner_b,
                email=f"{owner_b}@example.test",
                hashed_password="hash",
                created_at=now,
                updated_at=now,
            )
        )
        session.add(
            BookModel(
                id=book_b,
                user_id=owner_b,
                title="Book B",
                author="Author",
                total_pages=100,
                created_at=now,
                updated_at=now,
            )
        )
        session.add_all(
            [
                ReadingSessionModel(
                    id=session_a_newer,
                    user_id=owner_a,
                    book_id=book_a,
                    start_page=11,
                    end_page=20,
                    started_at=now,
                    ended_at=now,
                    notes=None,
                    created_at=datetime(2026, 1, 2),
                    updated_at=datetime(2026, 1, 2),
                ),
                ReadingSessionModel(
                    id=session_b,
                    user_id=owner_b,
                    book_id=book_b,
                    start_page=1,
                    end_page=10,
                    started_at=now,
                    ended_at=now,
                    notes=None,
                    created_at=now,
                    updated_at=now,
                ),
            ]
        )
        session.commit()
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        intent_a = _intent(
            owner_a,
            session_a,
            status="FAILED",
            error="delivery_failed",
            created_at=datetime(2026, 1, 1),
        )
        intent_b = _intent(owner_a, session_a_newer, created_at=datetime(2026, 1, 2))
        intent_c = _intent(owner_b, session_b, created_at=datetime(2026, 1, 1))
        repository.save(intent_a)
        repository.save(intent_b)
        repository.save(intent_c)
        session.commit()

    downstream = _RecordingGateway(failing_session=session_a)
    from sqlalchemy.orm import sessionmaker

    factory = sessionmaker(bind=engine)
    dispatcher = ProgressionDeliveryDispatcher(
        cast(
            DeliveryTransactionFactory,
            lambda: SqlAlchemyProgressionDeliveryTransaction(factory),
        ),
        downstream,
    )
    first_pass_start = len(downstream.calls)
    dispatcher.dispatch_unresolved()
    first_pass_calls = downstream.calls[first_pass_start:]

    with factory() as verification:
        repo = SqlAlchemyProgressionDeliveryRepository(verification)
        recovered_a = repo.get_by_id(intent_a.id)
        recovered_b = repo.get_by_id(intent_b.id)
        recovered_c = repo.get_by_id(intent_c.id)
        assert recovered_a is not None and recovered_a.status == "FAILED"
        assert recovered_b is not None and recovered_b.status == "PENDING"
        assert recovered_c is not None and recovered_c.status == "DELIVERED"

    downstream.failing_session = None
    second_pass_start = len(downstream.calls)
    dispatcher.dispatch_unresolved()
    second_pass_calls = downstream.calls[second_pass_start:]
    with factory() as verification:
        repo = SqlAlchemyProgressionDeliveryRepository(verification)
        recovered_a = repo.get_by_id(intent_a.id)
        recovered_b = repo.get_by_id(intent_b.id)
        assert recovered_a is not None and recovered_a.status == "DELIVERED"
        assert recovered_b is not None and recovered_b.status == "DELIVERED"
    assert session_a_newer not in first_pass_calls
    assert session_a in first_pass_calls
    assert session_b in first_pass_calls
    assert second_pass_calls == [session_a, session_a_newer]
    assert downstream.calls.count(session_a) == 2
    engine.dispose()


def test_durable_gateway_record_uses_dispatcher_and_fresh_transaction(tmp_path: Path) -> None:
    engine, owner, _, reading_session = _file_database(tmp_path)
    factory = sessionmaker(bind=engine)
    with factory() as session:
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        intent = _intent(owner, reading_session, created_at=datetime(2026, 1, 1))
        repository.save(intent)
        session.commit()

    downstream = _RecordingGateway()
    delivery_sessions: list[Session] = []

    def tracked_factory() -> Session:
        session = factory()
        delivery_sessions.append(session)
        return session

    dispatcher = ProgressionDeliveryDispatcher(
        cast(
            DeliveryTransactionFactory,
            lambda: SqlAlchemyProgressionDeliveryTransaction(tracked_factory),
        ),
        downstream,
    )
    gateway = DurableProgressionGateway(dispatcher)
    gateway.record(
        ReadingProgressionOccurrence(
            owner_id=UserId.from_value(owner),
            reading_session_id=ReadingSessionId.from_value(reading_session),
            pages_read=10,
        )
    )

    with factory() as verification:
        model = verification.get(ProgressionDeliveryModel, intent.id)
        assert model is not None
        assert model.status == "DELIVERED"
        assert model.attempt_count == 1
    assert downstream.calls == [reading_session]
    assert len(delivery_sessions) == 2
    engine.dispose()
