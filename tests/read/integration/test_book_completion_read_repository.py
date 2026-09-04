from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from sqlalchemy import Connection, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.infrastructure.persistence.models.book_completion_model import (
    BookCompletionModel,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.repositories.book_completion_read_repository import (
    SqlAlchemyBookCompletionReadRepository,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base

COMPLETED_AT = datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc)


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
    now = datetime(2026, 8, 22)
    session.add(
        UserModel(
            id=owner_id.to_persistence(),
            email=f"{owner_id}@example.com",
            hashed_password="hash",
            created_at=now,
            updated_at=now,
        )
    )


def add_book(session: Session, owner_id: UserId, book_id: str, title: str) -> None:
    session.add(
        BookModel(
            id=book_id,
            user_id=owner_id.to_persistence(),
            title=title,
            author="Author",
            total_pages=100,
        )
    )


def add_completion(
    session: Session,
    book_id: str,
    completed_at: datetime,
    completion_id: str,
) -> None:
    session.add(
        BookCompletionModel(
            id=completion_id,
            book_id=book_id,
            completed_at=completed_at,
        )
    )


def seed_completions(session: Session) -> tuple[UserId, UserId]:
    owner = UserId.new()
    other = UserId.new()
    add_user(session, owner)
    add_user(session, other)
    add_book(session, owner, "0BOOK000000000000000000001", "First")
    add_book(session, owner, "0BOOK000000000000000000002", "Second")
    add_book(session, other, "0BOOK000000000000000000003", "Foreign")
    session.flush()
    add_completion(
        session,
        "0BOOK000000000000000000001",
        COMPLETED_AT,
        "0COMP00000000000000000001",
    )
    add_completion(
        session,
        "0BOOK000000000000000000002",
        datetime(2026, 8, 23, 12, 0, tzinfo=timezone.utc),
        "0COMP00000000000000000002",
    )
    add_completion(
        session,
        "0BOOK000000000000000000003",
        datetime(2026, 8, 24, 12, 0, tzinfo=timezone.utc),
        "0COMP00000000000000000003",
    )
    session.commit()
    return owner, other


def test_count_and_page_are_owner_scoped_with_current_book_title(session: Session) -> None:
    owner, other = seed_completions(session)
    book = session.get(BookModel, "0BOOK000000000000000000001")
    assert book is not None
    book.title = "Current First"
    session.commit()
    repository = SqlAlchemyBookCompletionReadRepository(session)

    assert repository.count_by_owner(owner) == 2
    assert repository.count_by_owner(other) == 1
    items = repository.list_page_by_owner(owner, offset=0, limit=20)

    assert [item.book_id for item in items] == [
        "0BOOK000000000000000000002",
        "0BOOK000000000000000000001",
    ]
    assert [item.book_title for item in items] == ["Second", "Current First"]
    assert all(item.completed_at.tzinfo == timezone.utc for item in items)


def test_order_tie_break_limit_offset_and_empty(session: Session) -> None:
    owner, _ = seed_completions(session)
    add_book(session, owner, "0BOOK000000000000000000004", "Tied")
    session.flush()
    add_completion(
        session,
        "0BOOK000000000000000000004",
        COMPLETED_AT,
        "0COMP00000000000000000004",
    )
    session.commit()
    repository = SqlAlchemyBookCompletionReadRepository(session)

    page = repository.list_page_by_owner(owner, offset=1, limit=1)

    assert [item.book_id for item in page] == ["0BOOK000000000000000000004"]
    assert repository.list_page_by_owner(owner, offset=20, limit=10) == ()
    assert repository.list_page_by_owner(UserId.new(), offset=0, limit=10) == ()


def test_count_and_page_execute_exactly_two_selects(session: Session) -> None:
    owner, _ = seed_completions(session)
    repository = SqlAlchemyBookCompletionReadRepository(session)
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


def test_page_projection_uses_join_without_per_item_select(session: Session) -> None:
    owner, _ = seed_completions(session)
    repository = SqlAlchemyBookCompletionReadRepository(session)
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
        items = repository.list_page_by_owner(owner, offset=0, limit=20)
    finally:
        event.remove(session.bind, "before_cursor_execute", record_select)

    assert len(items) == 2
    assert len(statements) == 1
    assert "JOIN BOOKS" in statements[0].upper()
