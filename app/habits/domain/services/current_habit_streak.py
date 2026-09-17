from collections.abc import Collection
from datetime import date, timedelta


class CurrentHabitStreakCalculator:
    def calculate(
        self,
        evaluation_date: date,
        completion_dates: Collection[date],
    ) -> int:
        eligible_dates = {
            completion_date
            for completion_date in completion_dates
            if completion_date <= evaluation_date
        }
        cursor = evaluation_date
        if cursor not in eligible_dates:
            cursor -= timedelta(days=1)
            if cursor not in eligible_dates:
                return 0

        streak = 0
        while cursor in eligible_dates:
            streak += 1
            cursor -= timedelta(days=1)
        return streak
