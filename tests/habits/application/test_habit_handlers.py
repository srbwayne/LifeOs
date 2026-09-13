import pytest

from app.habits.application.commands.create_habit import (
    CreateHabitCommand,
    CreateHabitCommandHandler,
)
from app.habits.application.commands.deactivate_habit import (
    DeactivateHabitCommand,
    DeactivateHabitCommandHandler,
)
from app.habits.application.commands.reactivate_habit import (
    ReactivateHabitCommand,
    ReactivateHabitCommandHandler,
)
from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.errors.habit_errors import (
    HabitAlreadyExistsError,
    HabitNotFoundError,
)
from app.habits.application.queries.get_habit import GetHabitQuery, GetHabitQueryHandler
from app.habits.application.queries.list_habits import ListHabitsQuery, ListHabitsQueryHandler
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.errors.habit_errors import InvalidHabitNameError
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


class FakeHabitRepository:
    def __init__(self) -> None:
        self.items: dict[str, Habit] = {}
        self.saved: list[Habit] = []
        self.name_lookups: list[tuple[UserId, str]] = []

    def save(self, habit: Habit) -> None:
        self.saved.append(habit)
        self.items[habit.id.value] = habit

    def get_by_id_and_owner(self, habit_id: HabitId, owner_id: UserId) -> Habit | None:
        habit = self.items.get(habit_id.value)
        return habit if habit is not None and habit.owner_id == owner_id else None

    def get_by_owner_and_name(self, owner_id: UserId, name: str) -> Habit | None:
        self.name_lookups.append((owner_id, name))
        return next(
            (
                habit
                for habit in self.items.values()
                if habit.owner_id == owner_id and habit.name == name
            ),
            None,
        )


class FakeUnitOfWork:
    def __init__(self) -> None:
        self.commits = 0
        self.entered = 0
        self.exited = 0

    def __enter__(self) -> "FakeUnitOfWork":
        self.entered += 1
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.exited += 1

    def commit(self) -> None:
        self.commits += 1

    def flush(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def track_aggregate(self, aggregate: object) -> None:
        pass


class FakeReadRepository:
    def __init__(self, items: tuple[HabitDTO, ...]) -> None:
        self.items = items
        self.owner: UserId | None = None

    def list_by_owner(self, owner_id: UserId) -> tuple[HabitDTO, ...]:
        self.owner = owner_id
        return self.items


def test_create_normalizes_before_duplicate_lookup_and_commits() -> None:
    repository = FakeHabitRepository()
    unit_of_work = FakeUnitOfWork()
    handler = CreateHabitCommandHandler(repository, unit_of_work)
    owner_id = UserId.new()

    result = handler(CreateHabitCommand(owner_id, "  Read  ", "  Notes  "))

    assert result.name == "Read"
    assert result.description == "Notes"
    assert result.active is True
    assert repository.name_lookups == [(owner_id, "Read")]
    assert len(repository.saved) == 1
    assert unit_of_work.commits == 1


def test_create_accepts_long_name_and_blank_description() -> None:
    repository = FakeHabitRepository()
    handler = CreateHabitCommandHandler(repository, FakeUnitOfWork())

    result = handler(CreateHabitCommand(UserId.new(), "x" * 1000, "   "))

    assert len(result.name) == 1000
    assert result.description is None


def test_create_normalized_duplicate_does_not_save_or_commit() -> None:
    repository = FakeHabitRepository()
    owner_id = UserId.new()
    existing = Habit.create(owner_id, "Read")
    repository.save(existing)
    repository.saved.clear()
    unit_of_work = FakeUnitOfWork()

    with pytest.raises(HabitAlreadyExistsError):
        CreateHabitCommandHandler(repository, unit_of_work)(
            CreateHabitCommand(owner_id, "  Read  ")
        )

    assert repository.name_lookups == [(owner_id, "Read")]
    assert repository.saved == []
    assert unit_of_work.commits == 0


def test_create_same_name_different_owner_is_allowed() -> None:
    repository = FakeHabitRepository()
    first_owner = UserId.new()
    second_owner = UserId.new()
    repository.save(Habit.create(first_owner, "Read"))

    result = CreateHabitCommandHandler(repository, FakeUnitOfWork())(
        CreateHabitCommand(second_owner, "Read")
    )

    assert result.name == "Read"
    assert result.id in {habit.id.value for habit in repository.saved}


def test_create_blank_name_propagates_domain_error() -> None:
    repository = FakeHabitRepository()
    unit_of_work = FakeUnitOfWork()

    with pytest.raises(InvalidHabitNameError):
        CreateHabitCommandHandler(repository, unit_of_work)(CreateHabitCommand(UserId.new(), "   "))

    assert repository.name_lookups == []
    assert unit_of_work.commits == 0


@pytest.mark.parametrize(
    "handler_type", [DeactivateHabitCommandHandler, ReactivateHabitCommandHandler]
)
def test_lifecycle_handlers_are_idempotent_and_commit_successfully(handler_type: type) -> None:
    repository = FakeHabitRepository()
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Example")
    repository.save(habit)
    repository.saved.clear()
    unit_of_work = FakeUnitOfWork()
    handler = handler_type(repository, unit_of_work)

    command = (
        DeactivateHabitCommand(owner_id, habit.id)
        if handler_type is DeactivateHabitCommandHandler
        else ReactivateHabitCommand(owner_id, habit.id)
    )
    if handler_type is ReactivateHabitCommandHandler:
        habit.deactivate()

    first = handler(command)
    second = handler(command)

    assert first.active == second.active
    assert unit_of_work.commits == 2
    assert len(repository.saved) == 2


@pytest.mark.parametrize(
    "handler_type", [DeactivateHabitCommandHandler, ReactivateHabitCommandHandler]
)
def test_lifecycle_handlers_map_missing_and_foreign_to_not_found(handler_type: type) -> None:
    repository = FakeHabitRepository()
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Example")
    repository.save(habit)
    unit_of_work = FakeUnitOfWork()
    handler = handler_type(repository, unit_of_work)
    command_type = (
        DeactivateHabitCommand
        if handler_type is DeactivateHabitCommandHandler
        else ReactivateHabitCommand
    )

    for command in (
        command_type(owner_id, HabitId.new()),
        command_type(UserId.new(), habit.id),
    ):
        with pytest.raises(HabitNotFoundError):
            handler(command)

    assert unit_of_work.commits == 0


def test_get_returns_own_active_or_inactive_habit_and_rejects_other_owner() -> None:
    repository = FakeHabitRepository()
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Example")
    repository.save(habit)
    handler = GetHabitQueryHandler(repository)

    assert handler(GetHabitQuery(owner_id, habit.id)).active is True
    habit.deactivate()
    assert handler(GetHabitQuery(owner_id, habit.id)).active is False
    with pytest.raises(HabitNotFoundError):
        handler(GetHabitQuery(UserId.new(), habit.id))

    with pytest.raises(HabitNotFoundError):
        handler(GetHabitQuery(owner_id, HabitId.new()))


def test_list_delegates_owner_and_returns_active_and_inactive_dtos() -> None:
    owner_id = UserId.new()
    items = (
        HabitDTO("a", "Active", None, True),
        HabitDTO("b", "Inactive", "Details", False),
    )
    repository = FakeReadRepository(items)

    result = ListHabitsQueryHandler(repository)(ListHabitsQuery(owner_id))

    assert result == items
    assert repository.owner == owner_id
