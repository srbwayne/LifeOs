from dataclasses import FrozenInstanceError

import pytest

from app.shared.domain.aggregate import AggregateRoot
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.commands.create_therapist import (
    CreateTherapistCommand,
    CreateTherapistCommandHandler,
)
from app.therapy.application.commands.deactivate_therapist import (
    DeactivateTherapistCommand,
    DeactivateTherapistCommandHandler,
)
from app.therapy.application.commands.reactivate_therapist import (
    ReactivateTherapistCommand,
    ReactivateTherapistCommandHandler,
)
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.application.errors import TherapistNotFoundError
from app.therapy.application.queries.get_therapist import (
    GetTherapistQuery,
    GetTherapistQueryHandler,
)
from app.therapy.application.queries.list_therapists import (
    ListTherapistsQuery,
    ListTherapistsQueryHandler,
)
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.errors.therapy_errors import InvalidTherapistNameError
from app.therapy.domain.value_objects.therapist_id import TherapistId


class FakeUow:
    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0

    def __enter__(self) -> "FakeUow":
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if exc_type is not None:
            self.rollbacks += 1

    def flush(self) -> None:
        pass

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def track_aggregate(self, aggregate: AggregateRoot) -> None:
        pass


class FakeRepository:
    def __init__(self) -> None:
        self.items: dict[str, Therapist] = {}
        self.saved: list[Therapist] = []

    def save(self, therapist: Therapist) -> None:
        self.items[therapist.id.value] = therapist
        self.saved.append(therapist)

    def get_by_id_and_owner(self, therapist_id: TherapistId, owner_id: UserId) -> Therapist | None:
        item = self.items.get(therapist_id.value)
        return item if item is not None and item.owner_id == owner_id else None


class FakeReadRepository:
    def __init__(self, items=()) -> None:
        self.items = tuple(items)
        self.owner: UserId | None = None

    def list_by_owner(self, owner_id: UserId):
        self.owner = owner_id
        return self.items


def test_create_normalizes_name_and_commits() -> None:
    repository, uow = FakeRepository(), FakeUow()
    owner = UserId.new()
    result = CreateTherapistCommandHandler(repository, uow)(
        CreateTherapistCommand(owner, "  Dr. Example  ")
    )

    assert result.name == "Dr. Example"
    assert result.active is True
    assert repository.saved[0].owner_id == owner
    assert len(repository.saved) == 1
    assert uow.commits == 1


def test_create_domain_error_prevents_save_and_commit() -> None:
    repository, uow = FakeRepository(), FakeUow()
    with pytest.raises(InvalidTherapistNameError):
        CreateTherapistCommandHandler(repository, uow)(CreateTherapistCommand(UserId.new(), " "))
    assert repository.saved == []
    assert uow.commits == 0
    assert uow.rollbacks == 1


def test_commands_and_queries_are_owner_safe_and_idempotent() -> None:
    owner, foreign = UserId.new(), UserId.new()
    repository, uow = FakeRepository(), FakeUow()
    therapist = Therapist.create(owner, "A")
    repository.save(therapist)
    deactivate = DeactivateTherapistCommandHandler(repository, uow)
    reactivate = ReactivateTherapistCommandHandler(repository, uow)

    assert deactivate(DeactivateTherapistCommand(owner, therapist.id)).active is False
    assert deactivate(DeactivateTherapistCommand(owner, therapist.id)).active is False
    assert reactivate(ReactivateTherapistCommand(owner, therapist.id)).active is True
    assert reactivate(ReactivateTherapistCommand(owner, therapist.id)).active is True
    with pytest.raises(TherapistNotFoundError):
        deactivate(DeactivateTherapistCommand(foreign, therapist.id))
    with pytest.raises(TherapistNotFoundError):
        deactivate(DeactivateTherapistCommand(owner, TherapistId.new()))
    with pytest.raises(TherapistNotFoundError):
        reactivate(ReactivateTherapistCommand(foreign, therapist.id))
    with pytest.raises(TherapistNotFoundError):
        reactivate(ReactivateTherapistCommand(owner, TherapistId.new()))
    assert uow.commits == 4


def test_get_own_returns_dto_and_list_preserves_inactive_order() -> None:
    owner = UserId.new()
    therapist = Therapist.create(owner, "A")
    repository = FakeRepository()
    repository.save(therapist)
    result = GetTherapistQueryHandler(repository)(GetTherapistQuery(owner, therapist.id))
    assert result == TherapistDTO(therapist.id.value, "A", True)

    inactive = Therapist.create(owner, "Inactive")
    inactive.deactivate()
    ordered = (
        TherapistDTO(inactive.id.value, "Inactive", False),
        TherapistDTO(therapist.id.value, "A", True),
    )
    read = FakeReadRepository(ordered)
    assert ListTherapistsQueryHandler(read)(ListTherapistsQuery(owner)) == ordered
    assert read.owner == owner


def test_get_missing_and_foreign_are_same_error_and_list_delegates() -> None:
    owner, foreign = UserId.new(), UserId.new()
    therapist = Therapist.create(owner, "A")
    repository = FakeRepository()
    repository.save(therapist)
    handler = GetTherapistQueryHandler(repository)
    with pytest.raises(TherapistNotFoundError, match="Therapist not found"):
        handler(GetTherapistQuery(foreign, therapist.id))
    with pytest.raises(TherapistNotFoundError, match="Therapist not found"):
        handler(GetTherapistQuery(owner, TherapistId.new()))

    read = FakeReadRepository((TherapistDTO(therapist.id.value, therapist.name, therapist.active),))
    result = ListTherapistsQueryHandler(read)(ListTherapistsQuery(owner))
    assert result == read.items
    assert read.owner == owner


def test_command_is_immutable() -> None:
    command = CreateTherapistCommand(UserId.new(), "A")
    with pytest.raises(FrozenInstanceError):
        command.name = "B"  # type: ignore[misc]
