from datetime import date, timedelta

from app.habits.domain.services.current_habit_streak import CurrentHabitStreakCalculator


def test_calculates_chain_ending_at_evaluation_date() -> None:
    evaluation_date = date(2026, 9, 14)

    assert (
        CurrentHabitStreakCalculator().calculate(
            evaluation_date,
            (
                evaluation_date,
                evaluation_date - timedelta(days=1),
                evaluation_date - timedelta(days=2),
            ),
        )
        == 3
    )


def test_falls_back_to_previous_date_when_evaluation_date_is_missing() -> None:
    evaluation_date = date(2026, 9, 14)

    assert (
        CurrentHabitStreakCalculator().calculate(
            evaluation_date,
            (evaluation_date - timedelta(days=1), evaluation_date - timedelta(days=2)),
        )
        == 2
    )


def test_returns_zero_when_evaluation_date_and_previous_date_are_missing() -> None:
    evaluation_date = date(2026, 9, 14)

    assert (
        CurrentHabitStreakCalculator().calculate(
            evaluation_date,
            (evaluation_date - timedelta(days=3), evaluation_date - timedelta(days=4)),
        )
        == 0
    )


def test_supports_empty_unordered_duplicate_and_future_dates() -> None:
    evaluation_date = date(2026, 9, 14)

    assert CurrentHabitStreakCalculator().calculate(evaluation_date, ()) == 0
    assert (
        CurrentHabitStreakCalculator().calculate(
            evaluation_date,
            (
                evaluation_date + timedelta(days=2),
                evaluation_date - timedelta(days=1),
                evaluation_date,
                evaluation_date - timedelta(days=1),
            ),
        )
        == 2
    )


def test_only_evaluation_date_is_one_and_past_dates_are_supported() -> None:
    evaluation_date = date(2026, 9, 14)

    assert CurrentHabitStreakCalculator().calculate(evaluation_date, (evaluation_date,)) == 1
    assert CurrentHabitStreakCalculator().calculate(date(2026, 9, 10), (date(2026, 9, 10),)) == 1
