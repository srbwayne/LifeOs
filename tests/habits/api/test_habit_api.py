from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.composition_root import get_current_user_id
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.infrastructure.persistence.models.habit_completion_model import (
    HabitCompletionModel,
)
from app.habits.infrastructure.persistence.models.habit_model import HabitModel
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base, get_db


@pytest.fixture
def api() -> Iterator[
    tuple[TestClient, list[UserId], UserId, UserId, sessionmaker[Session], FastAPI]
]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    app = create_app()
    owner = UserId.new()
    other_owner = UserId.new()
    with factory() as session:
        now = datetime.now()
        session.add_all(
            [
                UserModel(
                    id=owner.value,
                    email=f"{owner.value}@test",
                    hashed_password="x",
                    created_at=now,
                    updated_at=now,
                ),
                UserModel(
                    id=other_owner.value,
                    email=f"{other_owner.value}@test",
                    hashed_password="x",
                    created_at=now,
                    updated_at=now,
                ),
            ]
        )
        session.commit()

    def override_db() -> Iterator[Session]:
        with factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    current_owner = [owner]
    app.dependency_overrides[get_current_user_id] = lambda: current_owner[0]
    with TestClient(app) as client:
        yield client, current_owner, owner, other_owner, factory, app
    app.dependency_overrides.clear()
    engine.dispose()


def test_habits_authentication_is_required(api) -> None:
    client, _, _, _, _, app = api
    app.dependency_overrides.pop(get_current_user_id)

    assert client.post("/habits", json={"name": "Example"}).status_code == 401
    assert client.get("/habits").status_code == 401
    assert client.get("/habits/not-a-tsid").status_code == 401
    assert client.post("/habits/not-a-tsid/deactivate").status_code == 401
    assert client.post("/habits/not-a-tsid/reactivate").status_code == 401


def test_habit_api_lifecycle_response_shape_and_fresh_persistence(api) -> None:
    client, current_owner, owner, _, factory, _ = api
    created = client.post(
        "/habits",
        json={"name": "  Read  ", "description": "  Notes  "},
    )

    assert created.status_code == 201
    body = created.json()
    assert set(body) == {"id", "name", "description", "active"}
    assert body == {
        "id": body["id"],
        "name": "Read",
        "description": "Notes",
        "active": True,
    }
    habit_id = body["id"]

    deactivated = client.post(f"/habits/{habit_id}/deactivate")
    assert deactivated.status_code == 200 and deactivated.json()["active"] is False
    assert client.post(f"/habits/{habit_id}/deactivate").json()["active"] is False
    assert client.get(f"/habits/{habit_id}").json()["active"] is False
    reactivated = client.post(f"/habits/{habit_id}/reactivate")
    assert reactivated.status_code == 200 and reactivated.json()["active"] is True
    assert client.post(f"/habits/{habit_id}/reactivate").json()["active"] is True

    with factory() as session:
        persisted = session.get(HabitModel, habit_id)
        assert persisted is not None
        assert persisted.user_id == owner.value
        assert persisted.active is True
    assert current_owner[0] == owner


def test_habit_api_list_empty_for_fresh_owner(api) -> None:
    client, _, _, _, _, _ = api

    response = client.get("/habits")

    assert response.status_code == 200
    assert response.json() == []


def test_habit_api_validation_duplicate_and_owner_boundaries(api) -> None:
    client, current_owner, owner, other_owner, _, _ = api
    first = client.post("/habits", json={"name": "Read", "description": "   "})
    assert first.status_code == 201
    assert first.json()["description"] is None
    assert client.post("/habits", json={"name": "  Read  "}).status_code == 409
    assert client.post("/habits", json={"name": "read"}).status_code == 201
    assert client.post("/habits", json={"name": "Read", "extra": True}).status_code == 422
    assert client.post("/habits", json={"name": "   "}).status_code == 422
    assert client.post("/habits", json={"name": "x" * 1000}).status_code == 201

    current_owner[0] = other_owner
    assert client.post("/habits", json={"name": "Read"}).status_code == 201
    current_owner[0] = owner


def test_habit_api_list_isolated_ordered_and_includes_inactive(api) -> None:
    client, current_owner, owner, other_owner, _, _ = api
    client.post("/habits", json={"name": "B"})
    client.post("/habits", json={"name": "A"})
    inactive = client.post("/habits", json={"name": "Inactive"}).json()
    client.post(f"/habits/{inactive['id']}/deactivate")
    current_owner[0] = other_owner
    client.post("/habits", json={"name": "Other"})
    current_owner[0] = owner
    listed = client.get("/habits")
    assert listed.status_code == 200
    assert [item["name"] for item in listed.json()] == ["A", "B", "Inactive"]
    assert all(set(item) == {"id", "name", "description", "active"} for item in listed.json())


def test_habit_api_detail_id_and_owner_errors(api) -> None:
    client, current_owner, owner, other_owner, _, _ = api
    created = client.post("/habits", json={"name": "Private"}).json()
    habit_id = created["id"]

    assert client.get(f"/habits/{habit_id}").status_code == 200
    assert client.get("/habits/not-a-tsid").status_code == 422
    assert client.get(f"/habits/{HabitId.new().value}").status_code == 404
    current_owner[0] = other_owner
    assert client.get(f"/habits/{habit_id}").status_code == 404
    assert client.post(f"/habits/{habit_id}/deactivate").status_code == 404
    assert client.post(f"/habits/{habit_id}/reactivate").status_code == 404
    current_owner[0] = owner


def test_habit_completion_authentication_is_required(api) -> None:
    client, _, _, _, _, app = api
    app.dependency_overrides.pop(get_current_user_id)
    habit_id = HabitId.new().value

    assert (
        client.post(
            f"/habits/{habit_id}/completions", json={"record_date": "2026-01-01"}
        ).status_code
        == 401
    )
    assert client.delete(f"/habits/{habit_id}/completions/2026-01-01").status_code == 401


def test_habit_completion_mark_is_idempotent_and_respects_inactive_order(api) -> None:
    client, _, _, _, _, _ = api
    created_habit = client.post("/habits", json={"name": "Completion"}).json()
    habit_id = created_habit["id"]
    body = {"record_date": "2030-01-01"}

    first = client.post(f"/habits/{habit_id}/completions", json=body)
    second = client.post(f"/habits/{habit_id}/completions", json=body)
    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json() == second.json()
    assert set(first.json()) == {"id", "habit_id", "record_date"}
    assert first.json()["habit_id"] == habit_id

    client.post(f"/habits/{habit_id}/deactivate")
    existing_inactive = client.post(f"/habits/{habit_id}/completions", json=body)
    assert existing_inactive.status_code == 200
    assert existing_inactive.json()["id"] == first.json()["id"]

    rejected = client.post(f"/habits/{habit_id}/completions", json={"record_date": "2030-01-02"})
    assert rejected.status_code == 409
    assert rejected.json()["detail"] == "Cannot create a completion for an inactive Habit."
    with api[4]() as session:
        assert session.query(HabitCompletionModel).count() == 1
    assert "owner_id" not in first.json()


def test_habit_completion_mark_validation_and_owner_boundaries(api) -> None:
    client, current_owner, owner, other_owner, _, _ = api
    habit_id = client.post("/habits", json={"name": "Validation"}).json()["id"]

    assert (
        client.post(f"/habits/{habit_id}/completions", json={"record_date": "bad"}).status_code
        == 422
    )
    assert (
        client.post(
            f"/habits/{habit_id}/completions", json={"record_date": "2026-01-01", "extra": True}
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/habits/not-a-tsid/completions", json={"record_date": "2026-01-01"}
        ).status_code
        == 422
    )
    assert client.delete("/habits/not-a-tsid/completions/2026-02-02").status_code == 422
    assert (
        client.post(
            f"/habits/{HabitId.new().value}/completions", json={"record_date": "2026-01-01"}
        ).status_code
        == 404
    )

    current_owner[0] = other_owner
    assert (
        client.post(
            f"/habits/{habit_id}/completions", json={"record_date": "2026-01-01"}
        ).status_code
        == 404
    )
    current_owner[0] = owner


def test_habit_completion_unmark_is_204_repeat_404_and_allows_recreation(api) -> None:
    client, _, _, _, _, _ = api
    habit_id = client.post("/habits", json={"name": "Unmark"}).json()["id"]
    record_date = "2020-01-01"
    marked = client.post(f"/habits/{habit_id}/completions", json={"record_date": record_date})
    assert marked.status_code == 201

    deleted = client.delete(f"/habits/{habit_id}/completions/{record_date}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.delete(f"/habits/{habit_id}/completions/{record_date}").status_code == 404
    recreated = client.post(f"/habits/{habit_id}/completions", json={"record_date": record_date})
    assert recreated.status_code == 201
    assert recreated.json()["id"] != marked.json()["id"]


def test_habit_completion_unmark_validation_and_inactive_correction(api) -> None:
    client, current_owner, owner, other_owner, _, _ = api
    habit_id = client.post("/habits", json={"name": "Correction"}).json()["id"]
    assert (
        client.post(
            f"/habits/{habit_id}/completions", json={"record_date": "2026-02-02"}
        ).status_code
        == 201
    )
    client.post(f"/habits/{habit_id}/deactivate")
    assert client.delete(f"/habits/{habit_id}/completions/2026-02-02").status_code == 204
    assert client.delete(f"/habits/{habit_id}/completions/not-a-date").status_code == 422
    assert client.delete(f"/habits/{HabitId.new().value}/completions/2026-02-02").status_code == 404
    current_owner[0] = other_owner
    assert client.delete(f"/habits/{habit_id}/completions/2026-02-02").status_code == 404
    current_owner[0] = owner


def test_habit_api_missing_habit_lifecycle_returns_not_found(api) -> None:
    client, _, _, _, _, _ = api
    missing_habit_id = HabitId.new().value

    assert client.post(f"/habits/{missing_habit_id}/deactivate").status_code == 404
    assert client.post(f"/habits/{missing_habit_id}/reactivate").status_code == 404
