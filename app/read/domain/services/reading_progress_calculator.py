from decimal import ROUND_HALF_UP, Decimal

from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.models.reading_progress import ReadingProgress

PERCENTAGE_PRECISION = Decimal("0.01")


class ReadingProgressCalculator:
    @staticmethod
    def calculate(
        book: Book,
        sessions: tuple[ReadingSession, ...],
    ) -> ReadingProgress:
        intervals = tuple(
            sorted(
                ((session.start_page.value, session.end_page.value) for session in sessions),
                key=lambda interval: (interval[0], interval[1]),
            )
        )
        merged_intervals = ReadingProgressCalculator._merge_intervals(intervals)
        unique_pages_read = sum(
            end_page - start_page + 1 for start_page, end_page in merged_intervals
        )
        total_pages = book.total_pages.value
        percentage = (Decimal(unique_pages_read * 100) / Decimal(total_pages)).quantize(
            PERCENTAGE_PRECISION, rounding=ROUND_HALF_UP
        )

        return ReadingProgress(
            book_id=book.id,
            total_pages=total_pages,
            unique_pages_read=unique_pages_read,
            highest_page_reached=max(
                (session.end_page.value for session in sessions),
                default=None,
            ),
            percentage=percentage,
            completed=unique_pages_read == total_pages,
        )

    @staticmethod
    def _merge_intervals(
        intervals: tuple[tuple[int, int], ...],
    ) -> tuple[tuple[int, int], ...]:
        if not intervals:
            return ()

        merged: list[tuple[int, int]] = [intervals[0]]
        for start_page, end_page in intervals[1:]:
            previous_start, previous_end = merged[-1]
            if start_page <= previous_end + 1:
                merged[-1] = (previous_start, max(previous_end, end_page))
            else:
                merged.append((start_page, end_page))
        return tuple(merged)
