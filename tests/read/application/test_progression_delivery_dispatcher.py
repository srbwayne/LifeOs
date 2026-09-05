
from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.application.ports.progression_gateway import ProgressionDeliveryResult
from app.read.application.services.progression_delivery_dispatcher import (
    ProgressionDeliveryDispatcher,
)
from app.shared.domain.tsid import new_tsid


def _intent(subject: str, pages: int) -> ProgressionDeliveryIntent:
    delivery_id = new_tsid()
    return ProgressionDeliveryIntent(
        id=delivery_id,
        reading_session_id=new_tsid(),
        source="lifeos",
        idempotency_key=delivery_id,
        subject_namespace="lifeos",
        subject_external_id=subject,
        configuration_key="reading",
        configuration_revision=2,
        pages_read=pages,
    )


class FakeRepository:
    def __init__(self, intents: tuple[ProgressionDeliveryIntent, ...]) -> None:
        self.intents = {intent.id: intent for intent in intents}
        self.events: list[str] = []

    def get_by_id(self, delivery_id: str):
        return self.intents.get(delivery_id)

    def list_unresolved(self):
        return tuple(
            intent for intent in self.intents.values() if intent.status != "DELIVERED"
        )

    def mark_delivered(self, delivery_id, delivered_at):
        intent = self.intents[delivery_id]
        self.intents[delivery_id] = ProgressionDeliveryIntent(
            **{**intent.__dict__, "status": "DELIVERED", "attempt_count": intent.attempt_count + 1}
        )
        self.events.append(f"delivered:{delivery_id}")

    def mark_failed(self, delivery_id, attempt_at, error):
        intent = self.intents[delivery_id]
        self.intents[delivery_id] = ProgressionDeliveryIntent(
            **{
                **intent.__dict__,
                "status": "FAILED",
                "attempt_count": intent.attempt_count + 1,
                "last_error": error,
            }
        )
        self.events.append(f"failed:{delivery_id}")


class FakeGateway:
    def __init__(self, results):
        self.results = list(results)
        self.facts = []

    def evaluate_reading_session(self, fact):
        self.facts.append(fact)
        return self.results.pop(0)


class FakeCommitter:
    def __init__(self):
        self.count = 0

    def commit(self):
        self.count += 1


def test_success_marks_delivered_and_reuses_frozen_configuration_facts():
    intent = _intent(new_tsid(), 30)
    repository = FakeRepository((intent,))
    gateway = FakeGateway((ProgressionDeliveryResult(True, 200),))
    committer = FakeCommitter()

    ProgressionDeliveryDispatcher(repository, gateway, committer).dispatch(intent.id)

    assert gateway.facts[0].source_event_id == intent.idempotency_key
    assert gateway.facts[0].pages_read == 30
    assert repository.intents[intent.id].status == "DELIVERED"
    assert committer.count == 1


def test_failure_is_durable_and_earlier_subject_event_blocks_later_one():
    subject = new_tsid()
    first = _intent(subject, 5)
    second = _intent(subject, 10)
    repository = FakeRepository((first, second))
    gateway = FakeGateway((ProgressionDeliveryResult(False, 503, "http_error"),))
    committer = FakeCommitter()

    ProgressionDeliveryDispatcher(repository, gateway, committer).dispatch_unresolved()

    assert len(gateway.facts) == 1
    assert repository.intents[first.id].status == "FAILED"
    assert repository.intents[second.id].status == "PENDING"


def test_different_subjects_are_not_blocked_by_another_failure():
    first = _intent(new_tsid(), 5)
    second = _intent(new_tsid(), 10)
    repository = FakeRepository((first, second))
    gateway = FakeGateway(
        (
            ProgressionDeliveryResult(False, 503, "http_error"),
            ProgressionDeliveryResult(True, 200),
        )
    )
    committer = FakeCommitter()

    ProgressionDeliveryDispatcher(repository, gateway, committer).dispatch_unresolved()

    assert len(gateway.facts) == 2
    assert repository.intents[second.id].status == "DELIVERED"
