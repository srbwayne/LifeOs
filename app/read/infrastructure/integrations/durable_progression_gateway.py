from app.read.application.ports.progression_gateway import ReadingProgressionOccurrence
from app.read.application.services.progression_delivery_dispatcher import (
    ProgressionDeliveryDispatcher,
)


class DurableProgressionGateway:
    def __init__(self, dispatcher: ProgressionDeliveryDispatcher) -> None:
        self._dispatcher = dispatcher

    def record(self, occurrence: ReadingProgressionOccurrence) -> None:
        self._dispatcher.dispatch_for_reading_session(occurrence.reading_session_id)
