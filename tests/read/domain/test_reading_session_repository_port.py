from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository
from app.read.domain.value_objects.book_id import BookId
from app.shared.domain.identifiers.user_id import UserId


class ReadingSessionRepositoryStub:
    def __init__(self) -> None:
        self.saved: list[ReadingSession] = []

    def save(self, session: ReadingSession) -> None:
        self.saved.append(session)

    def list_by_book_and_owner(
        self,
        book_id: BookId,
        owner_id: UserId,
    ) -> tuple[ReadingSession, ...]:
        return ()


def accepts_repository(repository: IReadingSessionRepository) -> IReadingSessionRepository:
    return repository


def test_repository_port_accepts_structural_implementation() -> None:
    repository = ReadingSessionRepositoryStub()

    assert accepts_repository(repository) is repository


def test_repository_port_defines_only_approved_operations() -> None:
    public_operations = {
        name
        for name, value in IReadingSessionRepository.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert public_operations == {"save", "list_by_book_and_owner"}
