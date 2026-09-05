from datetime import datetime, timezone

from app.read.application.commands.create_reading_session import (
    CreateReadingSessionCommand,
    CreateReadingSessionCommandHandler,
)
from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.domain.aggregates.book import Book
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator
from app.read.domain.services.reading_progress_calculator import ReadingProgressCalculator
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class Repository:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.saved: list[ProgressionDeliveryIntent] = []

    def get_by_id_and_owner(self, book_id, owner_id):
        return self.book if book_id == self.book.id and owner_id == self.book.owner_id else None

    def list_by_book_and_owner(self, book_id, owner_id):
        return ()

    def get_by_book_and_owner(self, book_id, owner_id):
        return None

    def save(self, value):
        if isinstance(value, ProgressionDeliveryIntent):
            self.saved.append(value)


class Uow:
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def acquire_write_intent(self):
        return None

    def flush(self):
        return None

    def commit(self):
        return None


def test_disabled_delivery_preserves_reading_session_without_intent():
    owner_id = UserId.new()
    book = Book.create(owner_id, "Book", "Author", 100)
    repositories = Repository(book)
    handler = CreateReadingSessionCommandHandler(
        repositories,
        repositories,
        repositories,
        ReadingCoverageCalculator(),
        ReadingProgressCalculator(),
        Uow(),
        progression_delivery_repository=repositories,
        progression_delivery_enabled=False,
    )

    result = handler(
        CreateReadingSessionCommand(
            owner_id=owner_id,
            book_id=BookId.from_value(book.id.to_persistence()),
            start_page=1,
            end_page=1,
            started_at=datetime(2026, 9, 5, tzinfo=timezone.utc),
            ended_at=datetime(2026, 9, 5, tzinfo=timezone.utc),
        )
    )

    assert result.pages_read == 1
    assert repositories.saved == []
