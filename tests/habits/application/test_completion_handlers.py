from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.habits.application.commands.mark_completion import (
    MarkCompletionCommand,
    MarkCompletionCommandHandler,
)
from app.habits.application.commands.unmark_completion import (
    UnmarkCompletionCommand,
    UnmarkCompletionCommandHandler,
)
from app.habits.application.errors.habit_errors import (
    HabitCompletionNotFoundError,
    HabitNotFoundError,
    InactiveHabitError,
)
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.aggregates.habit_completion import HabitCompletion
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId


class HabitRepositoryFake:
    def __init__(self, habits: list[Habit]) -> None:
        self.habits = {(habit.owner_id, habit.id): habit for habit in habits}

    def get_by_id_and_owner(self, habit_id: HabitId, owner_id: UserId) -> Habit | None:
        return self.habits.get((owner_id, habit_id))

    def save(self, habit: Habit) -> None:
        self.habits[(habit.owner_id, habit.id)] = habit

    def get_by_owner_and_name(self, owner_id: UserId, name: str) -> Habit | None:
        return next(
            (
                habit
                for habit in self.habits.values()
                if habit.owner_id == owner_id and habit.name == name
            ),
            None,
        )


class CompletionRepositoryFake:
    def __init__(self, completions: list[HabitCompletion] | None = None) -> None:
        self.completions = {
            (item.owner_id, item.habit_id, item.record_date): item for item in completions or []
        }
        self.saved: list[HabitCompletion] = []
        self.deleted: list[HabitCompletion] = []
        self.lookups = 0
        self.lookup_after_rollback = False
        self.unit_of_work: UnitOfWorkFake | None = None

    def save(self, completion: HabitCompletion) -> None:
        self.saved.append(completion)

    def get_by_owner_habit_date(
        self, owner_id: UserId, habit_id: HabitId, record_date: date
    ) -> HabitCompletion | None:
        self.lookups += 1
        if self.unit_of_work is not None and self.unit_of_work.rollbacks:
            self.lookup_after_rollback = True
        key = (owner_id, habit_id, record_date)
        if self.lookups == 2 and key not in self.completions:
            return self.winner
        return self.completions.get(key)

    def delete(self, completion: HabitCompletion) -> None:
        self.deleted.append(completion)

    winner: HabitCompletion | None = None


class UnitOfWorkFake:
    def __init__(self, flush_error: IntegrityError | None = None) -> None:
        self.flush_error = flush_error
        self.commits = 0
        self.rollbacks = 0
        self.flushes = 0

    def __enter__(self) -> IUnitOfWork:
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        pass

    def flush(self) -> None:
        self.flushes += 1
        if self.flush_error is not None:
            raise self.flush_error

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def track_aggregate(self, aggregate: AggregateRoot) -> None:
        pass


def make_habit(active: bool = True) -> tuple[UserId, Habit]:
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Read")
    if not active:
        habit.deactivate()
    return owner_id, habit


def test_mark_missing_or_foreign_habit_does_not_save_or_commit() -> None:
    owner_id, habit = make_habit()
    habits = HabitRepositoryFake([habit])
    completions = CompletionRepositoryFake()
    uow = UnitOfWorkFake()
    handler = MarkCompletionCommandHandler(habits, completions, uow)

    for command in (
        MarkCompletionCommand(owner_id, HabitId.new(), date(2026, 1, 1)),
        MarkCompletionCommand(UserId.new(), habit.id, date(2026, 1, 1)),
    ):
        with pytest.raises(HabitNotFoundError):
            handler(command)

    assert completions.saved == []
    assert uow.commits == 0


@pytest.mark.parametrize("active", [True, False])
def test_mark_existing_completion_is_idempotent_even_when_inactive(active: bool) -> None:
    owner_id, habit = make_habit(active)
    existing = HabitCompletion.create(owner_id, habit.id, date(2026, 1, 1))
    completions = CompletionRepositoryFake([existing])
    uow = UnitOfWorkFake()

    result = MarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
        MarkCompletionCommand(owner_id, habit.id, existing.record_date)
    )

    assert result.created is False
    assert result.completion.id == existing.id.value
    assert completions.saved == []
    assert uow.commits == 1


def test_mark_inactive_without_completion_fails_without_save_or_commit() -> None:
    owner_id, habit = make_habit(active=False)
    completions = CompletionRepositoryFake()
    uow = UnitOfWorkFake()

    with pytest.raises(InactiveHabitError):
        MarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
            MarkCompletionCommand(owner_id, habit.id, date(2030, 1, 1))
        )

    assert completions.saved == []
    assert uow.commits == 0


@pytest.mark.parametrize("record_date", [date(2020, 1, 1), date(2030, 1, 1)])
def test_mark_active_creates_historical_or_future_completion(record_date: date) -> None:
    owner_id, habit = make_habit()
    completions = CompletionRepositoryFake()
    uow = UnitOfWorkFake()

    result = MarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
        MarkCompletionCommand(owner_id, habit.id, record_date)
    )

    assert result.created is True
    assert result.completion.habit_id == habit.id.value
    assert result.completion.record_date == record_date
    assert len(completions.saved) == 1
    assert uow.flushes == 1
    assert uow.commits == 1


def test_mark_integrity_recovery_rolls_back_before_reloading_winner() -> None:
    owner_id, habit = make_habit()
    winner = HabitCompletion.restore(
        HabitCompletion.create(owner_id, habit.id, date(2026, 2, 2)).id,
        owner_id,
        habit.id,
        date(2026, 2, 2),
    )
    completions = CompletionRepositoryFake()
    completions.winner = winner
    uow = UnitOfWorkFake(IntegrityError("flush", {}, RuntimeError("unique")))
    completions.unit_of_work = uow

    result = MarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
        MarkCompletionCommand(owner_id, habit.id, winner.record_date)
    )

    assert result.created is False
    assert result.completion.id == winner.id.value
    assert uow.rollbacks == 1
    assert completions.lookup_after_rollback is True
    assert uow.commits == 1
    assert completions.saved[0].id != winner.id


def test_mark_integrity_recovery_reraises_when_no_winner_exists() -> None:
    owner_id, habit = make_habit()
    completions = CompletionRepositoryFake()
    error = IntegrityError("flush", {}, RuntimeError("unrelated"))
    uow = UnitOfWorkFake(error)

    with pytest.raises(IntegrityError) as raised:
        MarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
            MarkCompletionCommand(owner_id, habit.id, date(2026, 3, 3))
        )

    assert raised.value is error
    assert uow.rollbacks == 1


def test_unmark_deletes_own_completion_and_allows_inactive_habit() -> None:
    owner_id, habit = make_habit(active=False)
    completion = HabitCompletion.create(owner_id, habit.id, date(2026, 4, 4))
    completions = CompletionRepositoryFake([completion])
    uow = UnitOfWorkFake()

    UnmarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
        UnmarkCompletionCommand(owner_id, habit.id, completion.record_date)
    )

    assert completions.deleted == [completion]
    assert uow.commits == 1


def test_unmark_missing_or_foreign_habit_does_not_delete_or_commit() -> None:
    owner_id, habit = make_habit()
    completion = HabitCompletion.create(owner_id, habit.id, date(2026, 5, 5))
    completions = CompletionRepositoryFake([completion])
    uow = UnitOfWorkFake()
    handler = UnmarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)

    for command in (
        UnmarkCompletionCommand(owner_id, HabitId.new(), completion.record_date),
        UnmarkCompletionCommand(UserId.new(), habit.id, completion.record_date),
    ):
        with pytest.raises(HabitNotFoundError):
            handler(command)

    assert completions.deleted == []
    assert uow.commits == 0


def test_unmark_absent_completion_raises_without_delete_or_commit() -> None:
    owner_id, habit = make_habit()
    completions = CompletionRepositoryFake()
    uow = UnitOfWorkFake()

    with pytest.raises(HabitCompletionNotFoundError):
        UnmarkCompletionCommandHandler(HabitRepositoryFake([habit]), completions, uow)(
            UnmarkCompletionCommand(owner_id, habit.id, date(2026, 6, 6))
        )

    assert completions.deleted == []
    assert uow.commits == 0
