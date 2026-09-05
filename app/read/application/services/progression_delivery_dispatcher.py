import datetime
import logging
from typing import Protocol

from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryRepository,
)
from app.read.application.ports.progression_gateway import (
    ProgressionGateway,
    ReadingProgressionFact,
)
from app.shared.domain.identifiers.user_id import UserId

logger = logging.getLogger(__name__)


class Committer(Protocol):
    def commit(self) -> None: ...


class ProgressionDeliveryDispatcher:
    def __init__(
        self,
        repository: ProgressionDeliveryRepository,
        gateway: ProgressionGateway,
        unit_of_work: Committer,
    ) -> None:
        self._repository = repository
        self._gateway = gateway
        self._unit_of_work = unit_of_work

    def dispatch(self, delivery_id: str) -> None:
        intent = self._repository.get_by_id(delivery_id)
        if intent is None or intent.status == "DELIVERED":
            return

        result = self._gateway.evaluate_reading_session(
            ReadingProgressionFact(
                source_event_id=intent.idempotency_key,
                user_id=UserId.from_value(intent.subject_external_id),
                pages_read=intent.pages_read,
                configuration_key=intent.configuration_key,
                configuration_revision=intent.configuration_revision,
            )
        )
        now = datetime.datetime.now(datetime.timezone.utc)
        if result.success:
            self._repository.mark_delivered(delivery_id, now)
            self._unit_of_work.commit()
            return

        error = (
            f"http_status_{result.status_code}"
            if result.status_code is not None
            else result.error or "delivery_failed"
        )
        self._repository.mark_failed(delivery_id, now, error)
        self._unit_of_work.commit()
        logger.warning(
            "LifeOS progression delivery unresolved",
            extra={
                "reading_session_id": intent.idempotency_key,
                "user_id": intent.subject_external_id,
                "status_code": result.status_code,
                "error": error,
            },
        )

    def dispatch_unresolved(self) -> None:
        intents = self._repository.list_unresolved()
        blocked_subjects: set[tuple[str, str]] = set()
        for intent in intents:
            if intent.last_error in {"http_status_400", "http_status_409"}:
                continue
            subject = (intent.subject_namespace, intent.subject_external_id)
            if subject in blocked_subjects:
                continue
            self.dispatch(intent.id)
            refreshed = self._repository.get_by_id(intent.id)
            if refreshed is None or refreshed.status != "DELIVERED":
                blocked_subjects.add(subject)
