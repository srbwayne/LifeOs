from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_coverage import ReadingCoverage


class ReadingCoverageCalculator:
    @staticmethod
    def calculate(sessions: tuple[ReadingSession, ...]) -> ReadingCoverage:
        intervals = sorted(
            (
                PageInterval(session.start_page.value, session.end_page.value)
                for session in sessions
            ),
            key=lambda interval: (interval.start_page, interval.end_page),
        )
        if not intervals:
            return ReadingCoverage(())

        merged: list[PageInterval] = [intervals[0]]
        for interval in intervals[1:]:
            previous = merged[-1]
            if interval.start_page <= previous.end_page + 1:
                merged[-1] = PageInterval(
                    previous.start_page,
                    max(previous.end_page, interval.end_page),
                )
            else:
                merged.append(interval)
        return ReadingCoverage(tuple(merged))
