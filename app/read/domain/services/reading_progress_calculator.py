from decimal import ROUND_HALF_UP, Decimal

from app.read.domain.aggregates.book import Book
from app.read.domain.aggregates.reading_session import ReadingSession
from app.read.domain.models.reading_coverage import ReadingCoverage
from app.read.domain.models.reading_progress import ReadingProgress
from app.read.domain.services.reading_coverage_calculator import ReadingCoverageCalculator

PERCENTAGE_PRECISION = Decimal("0.01")


class ReadingProgressCalculator:
    @staticmethod
    def calculate(
        book: Book,
        sessions: tuple[ReadingSession, ...],
    ) -> ReadingProgress:
        coverage = ReadingCoverageCalculator.calculate(sessions)
        return ReadingProgressCalculator.calculate_from_coverage(book, coverage)

    @staticmethod
    def calculate_from_coverage(
        book: Book,
        coverage: ReadingCoverage,
    ) -> ReadingProgress:
        unique_pages_read = coverage.unique_pages_read
        total_pages = book.total_pages.value
        percentage = (Decimal(unique_pages_read * 100) / Decimal(total_pages)).quantize(
            PERCENTAGE_PRECISION, rounding=ROUND_HALF_UP
        )

        return ReadingProgress(
            book_id=book.id,
            total_pages=total_pages,
            unique_pages_read=unique_pages_read,
            highest_page_reached=coverage.highest_page_reached,
            percentage=percentage,
            completed=unique_pages_read == total_pages,
        )
