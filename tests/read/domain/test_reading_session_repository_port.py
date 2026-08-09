from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.ports.reading_session_repository import IReadingSessionRepository


class ReadingSessionRepositoryStub:
    def __init__(self) -> None:
        self.saved: list[ReadingSession] = []

    def save(self, session: ReadingSession) -> None:
        self.saved.append(session)


def accepts_repository(repository: IReadingSessionRepository) -> IReadingSessionRepository:
    return repository


def test_repository_port_accepts_structural_implementation() -> None:
    repository = ReadingSessionRepositoryStub()

    assert accepts_repository(repository) is repository


def test_repository_port_defines_only_save_operation() -> None:
    public_operations = {
        name
        for name, value in IReadingSessionRepository.__dict__.items()
        if not name.startswith("_") and callable(value)
    }

    assert public_operations == {"save"}
