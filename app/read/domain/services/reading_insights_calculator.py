from app.read.domain.models.page_interval import PageInterval
from app.read.domain.models.reading_coverage import ReadingCoverage
from app.read.domain.models.reading_insights import ReadingInsights
from app.read.domain.models.reading_progress import ReadingProgress


class ReadingInsightsCalculator:
    @staticmethod
    def calculate(
        progress: ReadingProgress,
        coverage: ReadingCoverage,
    ) -> ReadingInsights:
        ReadingInsightsCalculator._validate_consistency(progress, coverage)
        gaps: list[PageInterval] = []
        cursor = 1
        for interval in coverage.covered_intervals:
            if cursor < interval.start_page:
                gaps.append(PageInterval(cursor, interval.start_page - 1))
            cursor = interval.end_page + 1
        if cursor <= progress.total_pages:
            gaps.append(PageInterval(cursor, progress.total_pages))

        return ReadingInsights(
            book_id=progress.book_id,
            remaining_pages=progress.total_pages - progress.unique_pages_read,
            gaps=tuple(gaps),
            last_page_reached_with_gaps=(
                progress.highest_page_reached == progress.total_pages and not progress.completed
            ),
            full_coverage_confirmed=progress.completed,
        )

    @staticmethod
    def _validate_consistency(
        progress: ReadingProgress,
        coverage: ReadingCoverage,
    ) -> None:
        if progress.unique_pages_read != coverage.unique_pages_read:
            raise ValueError("Progress and coverage unique-page counts must match.")
        if progress.highest_page_reached != coverage.highest_page_reached:
            raise ValueError("Progress and coverage highest pages must match.")
        if coverage.covered_intervals and (
            coverage.covered_intervals[-1].end_page > progress.total_pages
        ):
            raise ValueError("Coverage must remain within the Book total pages.")
