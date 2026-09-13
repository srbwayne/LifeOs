from datetime import date

from app.habits.application.dtos.habit_checklist_dto import HabitChecklistItemDTO
from app.habits.application.dtos.habit_completion_dto import (
    HabitCompletionPageDTO,
)
from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.errors.habit_errors import HabitNotFoundError
from app.habits.application.queries.get_checklist import (
    GetChecklistQuery,
    GetChecklistQueryHandler,
)
from app.habits.application.queries.list_completions import (
    ListCompletionsQuery,
    ListCompletionsQueryHandler,
)
from app.habits.domain.aggregates.habit import Habit
from app.habits.domain.value_objects.habit_id import HabitId
from app.shared.domain.identifiers.user_id import UserId


class ChecklistReadRepositoryFake:
    def __init__(self, result: tuple[HabitChecklistItemDTO, ...]) -> None:
        self.result = result
        self.calls: list[tuple[UserId, date]] = []

    def get_checklist_by_owner_and_record_date(
        self, owner_id: UserId, record_date: date
    ) -> tuple[HabitChecklistItemDTO, ...]:
        self.calls.append((owner_id, record_date))
        return self.result

    def list_by_owner(self, owner_id: UserId) -> tuple[HabitDTO, ...]:
        return ()


class CompletionReadRepositoryFake:
    def __init__(self, result: HabitCompletionPageDTO) -> None:
        self.result = result
        self.calls: list[tuple[UserId, HabitId, int, int]] = []

    def list_by_owner_and_habit(
        self, owner_id: UserId, habit_id: HabitId, page: int, size: int
    ) -> HabitCompletionPageDTO:
        self.calls.append((owner_id, habit_id, page, size))
        return self.result


class HabitRepositoryFake:
    def __init__(self, habit: Habit | None) -> None:
        self.habit = habit
        self.calls = 0

    def get_by_id_and_owner(self, habit_id: HabitId, owner_id: UserId) -> Habit | None:
        self.calls += 1
        if self.habit is not None and self.habit.id == habit_id and self.habit.owner_id == owner_id:
            return self.habit
        return None

    def save(self, habit: Habit) -> None:
        self.habit = habit

    def get_by_owner_and_name(self, owner_id: UserId, name: str) -> Habit | None:
        return None


def test_checklist_query_forwards_owner_and_explicit_dates() -> None:
    owner_id = UserId.new()
    result = (HabitChecklistItemDTO("h", "Read", None, True),)
    repository = ChecklistReadRepositoryFake(result)
    record_date = date(2030, 1, 1)

    returned = GetChecklistQueryHandler(repository)(GetChecklistQuery(owner_id, record_date))

    assert returned == result
    assert repository.calls == [(owner_id, record_date)]


def test_list_completions_forwards_page_and_allows_inactive_habit() -> None:
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Read")
    habit.deactivate()
    page = HabitCompletionPageDTO((), 3, 10, 0, 0)
    repository = CompletionReadRepositoryFake(page)

    returned = ListCompletionsQueryHandler(HabitRepositoryFake(habit), repository)(
        ListCompletionsQuery(owner_id, habit.id, 3, 10)
    )

    assert returned == page
    assert repository.calls == [(owner_id, habit.id, 3, 10)]


def test_list_completions_missing_or_foreign_habit_is_not_found() -> None:
    stored_owner = UserId.new()
    stored_habit = Habit.create(stored_owner, "Read")
    read_repository = CompletionReadRepositoryFake(HabitCompletionPageDTO((), 1, 20, 0, 0))

    handler = ListCompletionsQueryHandler(HabitRepositoryFake(stored_habit), read_repository)
    for query in (
        ListCompletionsQuery(stored_owner, HabitId.new(), 1, 20),
        ListCompletionsQuery(UserId.new(), stored_habit.id, 1, 20),
    ):
        try:
            handler(query)
        except HabitNotFoundError:
            pass
        else:
            raise AssertionError("expected HabitNotFoundError")

    assert read_repository.calls == []


def test_empty_history_page_is_returned_without_not_found_error() -> None:
    owner_id = UserId.new()
    habit = Habit.create(owner_id, "Read")
    page = HabitCompletionPageDTO((), 1, 20, 0, 0)
    repository = CompletionReadRepositoryFake(page)

    returned = ListCompletionsQueryHandler(HabitRepositoryFake(habit), repository)(
        ListCompletionsQuery(owner_id, habit.id, 1, 20)
    )

    assert returned.items == ()
    assert returned.total_pages == 0
