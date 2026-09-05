from app.read.application.ports.progression_gateway import ReadingProgressionOccurrence


class NoOpProgressionGateway:
    def record(self, occurrence: ReadingProgressionOccurrence) -> None:
        return None
