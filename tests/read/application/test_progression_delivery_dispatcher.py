from contextlib import suppress
from datetime import datetime
from typing import cast

from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.application.ports.progression_gateway import (
    ProgressionGatewayError,
    ReadingProgressionOccurrence,
)
from app.read.application.services.progression_delivery_dispatcher import (
    DeliveryTransactionFactory,
    ProgressionDeliveryDispatcher,
    RetryableProgressionDeliveryError,
    TerminalProgressionDeliveryError,
)
from app.read.domain.value_objects.reading_session_id import ReadingSessionId
from app.shared.domain.identifiers.user_id import UserId
from app.shared.domain.tsid import new_tsid


class _Repository:
    def __init__(self, intent: ProgressionDeliveryIntent) -> None:
        self.intent = intent
        self.commits = 0
        self.blocked = False

    def get_by_id(self, delivery_id: str):
        return self.intent if delivery_id == self.intent.id else None

    def get_by_reading_session_id(self, reading_session_id):
        return self.intent if reading_session_id == self.intent.reading_session_id else None

    def list_unresolved(self):
        return (self.intent,)

    def has_older_blocking(self, delivery_id: str):
        return self.blocked

    def mark_delivered(self, delivery_id, delivered_at):
        self.intent = ProgressionDeliveryIntent(
            **{
                **self.intent.__dict__,
                "status": "DELIVERED",
                "attempt_count": self.intent.attempt_count + 1,
            }
        )

    def mark_failed(self, delivery_id, attempt_at, error):
        self.intent = ProgressionDeliveryIntent(
            **{
                **self.intent.__dict__,
                "status": "FAILED",
                "attempt_count": self.intent.attempt_count + 1,
                "last_error": error,
            }
        )


class _Transaction:
    def __init__(self, repository: _Repository) -> None:
        self.repository = repository

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def commit(self):
        self.repository.commits += 1


class _Gateway:
    def __init__(self, error: ProgressionGatewayError | None = None) -> None:
        self.error = error
        self.occurrences: list[ReadingProgressionOccurrence] = []

    def record(self, occurrence: ReadingProgressionOccurrence) -> None:
        self.occurrences.append(occurrence)
        if self.error:
            raise self.error


def _intent() -> ProgressionDeliveryIntent:
    owner = UserId.new()
    return ProgressionDeliveryIntent(
        id=new_tsid(),
        reading_session_id=ReadingSessionId.new(),
        owner_id=owner,
        pages_read=10,
        created_at=datetime(2026, 1, 1),
        updated_at=datetime(2026, 1, 1),
    )


def _dispatcher(repository, gateway):
    factory = cast(DeliveryTransactionFactory, lambda: _Transaction(repository))
    return ProgressionDeliveryDispatcher(factory, gateway)


def test_success_marks_delivered_once() -> None:
    repository = _Repository(_intent())
    gateway = _Gateway()
    _dispatcher(repository, gateway).dispatch(repository.intent.id)
    assert repository.intent.status == "DELIVERED"
    assert repository.intent.attempt_count == 1
    assert repository.commits == 1
    assert len(gateway.occurrences) == 1


def test_retryable_and_terminal_failures_are_persisted() -> None:
    for error, classification in (
        (RetryableProgressionDeliveryError("offline"), "delivery_failed"),
        (TerminalProgressionDeliveryError(400), "http_status_400"),
        (TerminalProgressionDeliveryError(409), "http_status_409"),
    ):
        repository = _Repository(_intent())
        with suppress(ProgressionGatewayError):
            _dispatcher(repository, _Gateway(error)).dispatch(repository.intent.id)
        assert repository.intent.status == "FAILED"
        assert repository.intent.last_error == classification
        assert repository.intent.attempt_count == 1
        assert repository.commits == 1


def test_blocked_delivery_does_not_attempt_or_increment() -> None:
    repository = _Repository(_intent())
    repository.blocked = True
    gateway = _Gateway()
    _dispatcher(repository, gateway).dispatch(repository.intent.id)
    assert gateway.occurrences == []
    assert repository.intent.status == "PENDING"
    assert repository.intent.attempt_count == 0
    assert repository.commits == 0
