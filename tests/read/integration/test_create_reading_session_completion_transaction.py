from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Barrier, Lock

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker
from tsidpy import TSID

from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommand,
    CreateReadingSessionCommandHandler,
)
from app.read.domain.aggregates.book_completion import BookCompletion
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.read.infrastructure.persistence.models.book_completion_model import BookCompletionModel
from app.read.infrastructure.persistence.models.reading_session_model import ReadingSessionModel
from app.read.infrastructure.persistence.repositories.book_completion_repository import (
    SqlAlchemyBookCompletionRepository,
)
from app.read.infrastructure.persistence.repositories.book_repository import (
    SqlAlchemyBookRepository,
)
from app.read.infrastructure.persistence.repositories.reading_session_repository import (
    SqlAlchemyReadingSessionRepository,
)
from app.shared.application.event_bus import InMemoryEventBus
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def _config(path: Path) -> Config:
    config = Config(str(Path(__file__).resolve().parents[3] / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{path.as_posix()}")
    return config


def _id() -> str:
    return TSID.create().to_string()


def _seed(path: Path, owner: str, book: str, *, total_pages: int = 100, end_page: int = 99) -> None:
    import sqlite3

    database = sqlite3.connect(path)
    database.execute("PRAGMA foreign_keys = ON")
    now = "2026-01-01 00:00:00"
    database.execute(
        "INSERT INTO users (id, email, hashed_password, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (owner, f"{owner}@example.test", "hash", now, now),
    )
    database.execute(
        "INSERT INTO books (id, user_id, title, author, total_pages, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (book, owner, "Book", "Author", total_pages, now, now),
    )
    if end_page:
        database.execute(
            "INSERT INTO reading_sessions (id, user_id, book_id, start_page, end_page, "
            "started_at, ended_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (_id(), owner, book, 1, end_page, now, now, now, now),
        )
    database.commit()
    database.close()


@pytest.fixture
def database_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "slice4.db"
    monkeypatch.setenv("LIFEOS_DATABASE_URL", f"sqlite:///{path.as_posix()}")
    command.upgrade(_config(path), "0008")
    return path


class _CountingUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, session: Session) -> None:
        super().__init__(session, InMemoryEventBus())
        self.acquisition_count = 0
        self.flush_count = 0
        self.commit_count = 0

    def acquire_write_intent(self) -> None:
        self.acquisition_count += 1
        super().acquire_write_intent()

    def flush(self) -> None:
        self.flush_count += 1
        super().flush()

    def commit(self) -> None:
        self.commit_count += 1
        super().commit()


class _FailingFlushUnitOfWork(_CountingUnitOfWork):
    def flush(self) -> None:
        super().flush()
        raise RuntimeError("flush failure")


class _FailingCommitUnitOfWork(_CountingUnitOfWork):
    def commit(self) -> None:
        self.commit_count += 1
        raise RuntimeError("commit failure")


class _FailingReadingSessionRepository(SqlAlchemyReadingSessionRepository):
    def save(self, reading_session: ReadingSession) -> None:
        raise RuntimeError("reading session failure")


class _TrackingBookCompletionRepository(SqlAlchemyBookCompletionRepository):
    def __init__(
        self, session: Session, observer: list[str], observer_lock: Lock, label: str
    ) -> None:
        super().__init__(session)
        self._observer = observer
        self._observer_lock = observer_lock
        self._label = label
        self.save_entered = False

    def save(self, completion: BookCompletion) -> None:
        self.save_entered = True
        with self._observer_lock:
            self._observer.append(self._label)
        super().save(completion)


def _handler(
    session: Session,
    sleeper=lambda _: None,
    reading_session_repository: SqlAlchemyReadingSessionRepository | None = None,
    book_completion_repository: SqlAlchemyBookCompletionRepository | None = None,
    unit_of_work: SqlAlchemyUnitOfWork | None = None,
) -> CreateReadingSessionCommandHandler:
    return CreateReadingSessionCommandHandler(
        SqlAlchemyBookRepository(session),
        reading_session_repository or SqlAlchemyReadingSessionRepository(session),
        book_completion_repository or SqlAlchemyBookCompletionRepository(session),
        ReadingCoverageCalculator(),
        ReadingProgressCalculator(),
        unit_of_work or SqlAlchemyUnitOfWork(session, InMemoryEventBus()),
        sleeper,
    )


def _command(
    owner: UserId,
    book_id: BookId,
    start: int,
    end: int,
    ended_at: datetime | None = None,
) -> CreateReadingSessionCommand:
    timestamp = ended_at or datetime(2026, 1, 2, tzinfo=timezone.utc)
    return CreateReadingSessionCommand(owner, book_id, start, end, timestamp, timestamp)


def test_final_gap_is_atomic_and_creates_one_completion(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book)
    engine = create_engine(f"sqlite:///{database_path}")
    session = sessionmaker(bind=engine)()
    result = _handler(session)(
        _command(UserId.from_value(owner), BookId.from_value(book), 100, 100)
    )

    assert session.get(ReadingSessionModel, result.id) is not None
    completions = session.scalars(select(BookCompletionModel)).all()
    assert len(completions) == 1
    assert session.execute(text("PRAGMA foreign_key_check")).all() == []
    session.close()
    engine.dispose()


def test_reading_session_save_failure_rolls_back_without_completion(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book)
    engine = create_engine(f"sqlite:///{database_path}")
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    unit_of_work = _CountingUnitOfWork(session)

    with pytest.raises(RuntimeError, match="reading session failure"):
        _handler(
            session,
            reading_session_repository=_FailingReadingSessionRepository(session),
            unit_of_work=unit_of_work,
        )(_command(UserId.from_value(owner), BookId.from_value(book), 100, 100))

    assert unit_of_work.acquisition_count == 1
    assert unit_of_work.commit_count == 0
    session.close()

    verification_session = session_factory()
    try:
        assert verification_session.scalars(select(ReadingSessionModel)).all() != []
        assert (
            verification_session.scalars(
                select(ReadingSessionModel).where(ReadingSessionModel.start_page == 100)
            ).all()
            == []
        )
        assert verification_session.scalars(select(BookCompletionModel)).all() == []
        assert verification_session.execute(text("PRAGMA foreign_key_check")).all() == []
    finally:
        verification_session.close()
        engine.dispose()


def test_flush_failure_after_completion_save_rolls_back_both_rows(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book)
    engine = create_engine(f"sqlite:///{database_path}")
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    unit_of_work = _FailingFlushUnitOfWork(session)
    observers: list[str] = []
    completion_repository = _TrackingBookCompletionRepository(
        session, observers, Lock(), "completion"
    )

    with pytest.raises(RuntimeError, match="flush failure"):
        _handler(
            session,
            book_completion_repository=completion_repository,
            unit_of_work=unit_of_work,
        )(_command(UserId.from_value(owner), BookId.from_value(book), 100, 100))

    assert completion_repository.save_entered is True
    assert unit_of_work.acquisition_count == 1
    assert unit_of_work.flush_count == 1
    assert unit_of_work.commit_count == 0
    session.close()

    verification_session = session_factory()
    try:
        assert (
            verification_session.scalars(
                select(ReadingSessionModel).where(ReadingSessionModel.start_page == 100)
            ).all()
            == []
        )
        assert verification_session.scalars(select(BookCompletionModel)).all() == []
        assert verification_session.execute(text("PRAGMA foreign_key_check")).all() == []
    finally:
        verification_session.close()
        engine.dispose()


def test_commit_failure_is_not_retried_after_successful_acquisition(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book, end_page=0)
    engine = create_engine(f"sqlite:///{database_path}")
    session = sessionmaker(bind=engine)()
    unit_of_work = _FailingCommitUnitOfWork(session)
    sleeps: list[float] = []

    with pytest.raises(RuntimeError, match="commit failure"):
        _handler(session, sleeps.append, unit_of_work=unit_of_work)(
            _command(UserId.from_value(owner), BookId.from_value(book), 1, 1)
        )

    assert unit_of_work.acquisition_count == 1
    assert unit_of_work.commit_count == 1
    assert sleeps == []
    session.close()
    engine.dispose()


def test_real_sqlite_busy_retries_after_sleeper_releases_lock(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book, end_page=0)
    engine = create_engine(f"sqlite:///{database_path}", connect_args={"timeout": 0})
    lock = engine.connect()
    lock.execute(text("BEGIN IMMEDIATE"))
    session = sessionmaker(bind=engine)()
    sleeps: list[float] = []

    def release_lock(delay: float) -> None:
        sleeps.append(delay)
        lock.rollback()
        lock.close()

    _handler(session, release_lock)(
        _command(UserId.from_value(owner), BookId.from_value(book), 1, 1)
    )

    assert sleeps == [0.050]
    assert len(session.scalars(select(ReadingSessionModel)).all()) == 1
    session.close()
    engine.dispose()


def test_real_sqlite_busy_twice_propagates_without_persistence(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book, end_page=0)
    engine = create_engine(f"sqlite:///{database_path}", connect_args={"timeout": 0})
    lock = engine.connect()
    lock.execute(text("BEGIN IMMEDIATE"))
    session = sessionmaker(bind=engine)()
    sleeps: list[float] = []

    try:
        with pytest.raises(OperationalError):
            _handler(session, sleeps.append)(
                _command(UserId.from_value(owner), BookId.from_value(book), 1, 1)
            )

        assert sleeps == [0.050]
        assert session.scalars(select(ReadingSessionModel)).all() == []
        assert session.scalars(select(BookCompletionModel)).all() == []
    finally:
        lock.rollback()
        lock.close()
        session.close()
        engine.dispose()


def test_concurrent_final_gaps_are_serialized_with_one_completion(database_path: Path) -> None:
    owner = _id()
    book = _id()
    _seed(database_path, owner, book, end_page=98)
    engine = create_engine(f"sqlite:///{database_path}", connect_args={"timeout": 5})
    session_factory = sessionmaker(bind=engine)
    barrier = Barrier(2)
    observers: list[str] = []
    observer_lock = Lock()
    first_ended_at = datetime(2026, 1, 2, tzinfo=timezone.utc)
    second_ended_at = first_ended_at + timedelta(minutes=1)

    def create_final_page(page: int, label: str, ended_at: datetime) -> None:
        session = session_factory()
        try:
            barrier.wait()
            _handler(
                session,
                book_completion_repository=_TrackingBookCompletionRepository(
                    session,
                    observers,
                    observer_lock,
                    label,
                ),
            )(
                _command(
                    UserId.from_value(owner),
                    BookId.from_value(book),
                    page,
                    page,
                    ended_at,
                )
            )
        finally:
            session.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        first = executor.submit(create_final_page, 99, "first", first_ended_at)
        second = executor.submit(create_final_page, 100, "second", second_ended_at)
        first.result()
        second.result()

    session = session_factory()
    try:
        sessions = session.scalars(select(ReadingSessionModel)).all()
        completions = session.scalars(select(BookCompletionModel)).all()
        completion = SqlAlchemyBookCompletionRepository(session).get_by_book_and_owner(
            BookId.from_value(book),
            UserId.from_value(owner),
        )
        assert len(sessions) == 3
        assert len(completions) == 1
        assert len(observers) == 1
        assert completion is not None
        expected_completed_at = {
            "first": first_ended_at,
            "second": second_ended_at,
        }[observers[0]]
        assert completion.completed_at == expected_completed_at
        assert session.execute(text("PRAGMA foreign_key_check")).all() == []
    finally:
        session.close()
        engine.dispose()
