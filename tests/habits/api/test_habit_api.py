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
    assert (
        client.get(f"/habits/{HabitId.new().value}/streak?evaluation_date=2026-09-14").status_code
        == 401
    )


def test_habit_streak_api_covers_current_date_owner_and_inactive_semantics(api) -> None:
    client, current_owner, owner, other_owner, _, app = api
    created = client.post("/habits", json={"name": "Streak"}).json()
    habit_id = created["id"]
    client.post(f"/habits/{habit_id}/completions", json={"record_date": "2026-09-12"})
    client.post(f"/habits/{habit_id}/completions", json={"record_date": "2026-09-14"})

    active = client.get(f"/habits/{habit_id}/streak?evaluation_date=2026-09-14")
    assert active.status_code == 200
    assert active.json() == {
        "habit_id": habit_id,
        "current_streak": 1,
        "evaluation_date": "2026-09-14",
    }
    fallback = client.get(f"/habits/{habit_id}/streak?evaluation_date=2026-09-13")
    assert fallback.status_code == 200
    assert fallback.json()["current_streak"] == 1
    minimum = client.get(f"/habits/{habit_id}/streak?evaluation_date=0001-01-01")
    assert minimum.status_code == 200
    assert minimum.json() == {
        "habit_id": habit_id,
        "current_streak": 0,
        "evaluation_date": "0001-01-01",
    }
    assert (
        client.get(f"/habits/{habit_id}/streak?evaluation_date=2020-01-01").json()["current_streak"]
        == 0
    )
    assert (
        client.get(f"/habits/{habit_id}/streak?evaluation_date=2030-01-01").json()["current_streak"]
        == 0
    )
    assert client.get(f"/habits/{habit_id}/streak").status_code == 422
    assert client.get(f"/habits/{habit_id}/streak?evaluation_date=bad").status_code == 422
    assert client.get("/habits/not-a-tsid/streak?evaluation_date=2026-09-14").status_code == 422
    assert (
        client.get(f"/habits/{HabitId.new().value}/streak?evaluation_date=2026-09-14").status_code
        == 404
    )

    current_owner[0] = other_owner
    assert client.get(f"/habits/{habit_id}/streak?evaluation_date=2026-09-14").status_code == 404
    current_owner[0] = owner
    client.post(f"/habits/{habit_id}/deactivate")
    inactive = client.get(f"/habits/{habit_id}/streak?evaluation_date=2026-09-14")
    assert inactive.status_code == 200
    assert inactive.json()["current_streak"] is None


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
    assert client.get(f"/habits/{habit_id}/completions").status_code == 401
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


def test_habit_checklist_auth_validation_and_current_active_projection(api) -> None:
    client, current_owner, owner, other_owner, _, app = api
    app.dependency_overrides.pop(get_current_user_id)
    assert client.get("/habits/checklist?record_date=2026-01-01").status_code == 401
    app.dependency_overrides[get_current_user_id] = lambda: current_owner[0]
    assert client.get("/habits/checklist").status_code == 422
    assert client.get("/habits/checklist?record_date=not-a-date").status_code == 422

    completed = client.post("/habits", json={"name": "Completed", "description": " Notes "}).json()
    client.post("/habits", json={"name": "Empty"})
    assert (
        client.post(
            f"/habits/{completed['id']}/completions", json={"record_date": "2026-01-01"}
        ).status_code
        == 201
    )
    current_owner[0] = other_owner
    foreign = client.post("/habits", json={"name": "Foreign"}).json()
    assert (
        client.post(
            f"/habits/{foreign['id']}/completions", json={"record_date": "2026-01-01"}
        ).status_code
        == 201
    )
    current_owner[0] = owner

    checklist = client.get("/habits/checklist?record_date=2026-01-01")
    assert checklist.status_code == 200
    assert [item["name"] for item in checklist.json()] == ["Completed", "Empty"]
    assert checklist.json()[0] == {
        "id": completed["id"],
        "name": "Completed",
        "description": "Notes",
        "completed": True,
    }
    assert checklist.json()[1]["completed"] is False
    assert all(set(item) == {"id", "name", "description", "completed"} for item in checklist.json())
    assert client.get("/habits/checklist?record_date=2030-01-01").status_code == 200

    client.post(f"/habits/{completed['id']}/deactivate")
    assert all(
        item["id"] != completed["id"]
        for item in client.get("/habits/checklist?record_date=2026-01-01").json()
    )
    client.post(f"/habits/{completed['id']}/reactivate")
    restored = client.get("/habits/checklist?record_date=2026-01-01").json()
    assert next(item for item in restored if item["id"] == completed["id"])["completed"] is True


def test_habit_completion_history_is_paginated_and_survives_deactivation(api) -> None:
    client, _, _, _, _, _ = api
    habit_id = client.post("/habits", json={"name": "History"}).json()["id"]
    for day in range(21):
        assert (
            client.post(
                f"/habits/{habit_id}/completions",
                json={"record_date": f"2026-01-{day + 1:02d}"},
            ).status_code
            == 201
        )

    default = client.get(f"/habits/{habit_id}/completions")
    assert default.status_code == 200
    assert default.json()["page"] == 1 and default.json()["size"] == 20
    assert default.json()["total_items"] == 21 and default.json()["total_pages"] == 2
    assert set(default.json()["items"][0]) == {"id", "habit_id", "record_date"}
    assert default.json()["items"][0]["record_date"] == "2026-01-21"
    assert client.get(f"/habits/{habit_id}/completions?page=2&size=20").json()["items"]
    assert client.get(f"/habits/{habit_id}/completions?page=3&size=20").json()["items"] == []
    assert client.get(f"/habits/{habit_id}/completions?page=0").status_code == 422
    assert client.get(f"/habits/{habit_id}/completions?size=0").status_code == 422
    assert client.get(f"/habits/{habit_id}/completions?size=101").status_code == 422
    client.post(f"/habits/{habit_id}/deactivate")
    inactive_history = client.get(f"/habits/{habit_id}/completions?size=2")
    assert inactive_history.status_code == 200
    assert inactive_history.json()["total_items"] == 21


def test_habit_completion_history_owner_and_id_validation(api) -> None:
    client, current_owner, owner, other_owner, _, _ = api
    habit_id = client.post("/habits", json={"name": "Private history"}).json()["id"]
    assert client.get(f"/habits/{HabitId.new().value}/completions").status_code == 404
    assert client.get("/habits/not-a-tsid/completions").status_code == 422
    current_owner[0] = other_owner
    assert client.get(f"/habits/{habit_id}/completions").status_code == 404
    current_owner[0] = owner
    empty = client.get(f"/habits/{habit_id}/completions")
    assert empty.status_code == 200
    assert empty.json() == {
        "items": [],
        "page": 1,
        "size": 20,
        "total_items": 0,
        "total_pages": 0,
    }


def test_habit_api_missing_habit_lifecycle_returns_not_found(api) -> None:
    client, _, _, _, _, _ = api
    missing_habit_id = HabitId.new().value

    assert client.post(f"/habits/{missing_habit_id}/deactivate").status_code == 404
    assert client.post(f"/habits/{missing_habit_id}/reactivate").status_code == 404
