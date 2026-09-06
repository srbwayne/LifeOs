from __future__ import annotations

import datetime
from typing import Protocol

from sqlalchemy.exc import SQLAlchemyError

from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryRepository,
)
from app.read.application.ports.progression_gateway import (
    ProgressionGateway,
    ProgressionGatewayError,
    ReadingProgressionOccurrence,
)
from app.read.domain.value_objects.reading_session_id import ReadingSessionId


class DeliveryTransaction(Protocol):
    repository: ProgressionDeliveryRepository

    def __enter__(self) -> DeliveryTransaction: ...

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...

    def commit(self) -> None: ...


class DeliveryTransactionFactory(Protocol):
    def __call__(self) -> DeliveryTransaction: ...


class RetryableProgressionDeliveryError(ProgressionGatewayError):
    classification = "delivery_failed"


class TerminalProgressionDeliveryError(ProgressionGatewayError):
    def __init__(self, status_code: int) -> None:
        if status_code not in (400, 409):
            raise ValueError("Only status 400 and 409 are terminal delivery errors.")
        self.classification = f"http_status_{status_code}"
        super().__init__(self.classification)


class ProgressionDeliveryDispatcher:
    def __init__(
        self,
        transaction_factory: DeliveryTransactionFactory,
        downstream: ProgressionGateway,
    ) -> None:
        self._transaction_factory = transaction_factory
        self._downstream = downstream

    def dispatch_for_reading_session(self, reading_session_id: ReadingSessionId) -> None:
        with self._transaction_factory() as transaction:
            intent = transaction.repository.get_by_reading_session_id(reading_session_id)
        if intent is not None:
            self.dispatch(intent.id)

    def dispatch_unresolved(self) -> None:
        with self._transaction_factory() as transaction:
            delivery_ids = tuple(intent.id for intent in transaction.repository.list_unresolved())
        for delivery_id in delivery_ids:
            try:
                self.dispatch(delivery_id)
            except ProgressionGatewayError:
                continue

    def dispatch(self, delivery_id: str) -> None:
        try:
            with self._transaction_factory() as transaction:
                repository = transaction.repository
                intent = repository.get_by_id(delivery_id)
                if intent is None or intent.status == "DELIVERED":
                    return
                if repository.has_older_blocking(delivery_id):
                    return

                try:
                    self._downstream.record(
                        ReadingProgressionOccurrence(
                            owner_id=intent.owner_id,
                            reading_session_id=intent.reading_session_id,
                            pages_read=intent.pages_read,
                        )
                    )
                except ProgressionGatewayError as error:
                    repository.mark_failed(
                        delivery_id,
                        _utc_now(),
                        _classification(error),
                    )
                    transaction.commit()
                    raise

                repository.mark_delivered(delivery_id, _utc_now())
                transaction.commit()
        except SQLAlchemyError as error:
            raise ProgressionGatewayError("delivery_persistence_failed") from error


def _classification(error: ProgressionGatewayError) -> str:
    classification = getattr(error, "classification", None)
    return classification if isinstance(classification, str) else "delivery_failed"


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
