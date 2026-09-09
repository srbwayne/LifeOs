from collections.abc import Iterator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app_factory import create_app
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.composition_root import get_current_user_id
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base, get_db
from app.therapy.domain.value_objects.therapist_id import TherapistId


@pytest.fixture
def api() -> Iterator[tuple[TestClient, sessionmaker[Session], list[UserId], UserId]]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    app = create_app()
    owner = UserId.new()
    with factory() as session:
        session.add(
            UserModel(
                id=owner.value,
                email=f"{owner.value}@test",
                hashed_password="x",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
        session.commit()

    def override_db() -> Iterator[Session]:
        with factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_db
    current_owner = [owner]
    app.dependency_overrides[get_current_user_id] = lambda: current_owner[0]
    with TestClient(app) as client:
        yield client, factory, current_owner, owner
    app.dependency_overrides.clear()
    engine.dispose()


def test_therapist_api_create_list_actions_and_fresh_session(api) -> None:
    client, fresh, current_owner, _ = api
    created = client.post("/therapy/therapists", json={"name": "  Dr. A  "})
    assert created.status_code == 201
    body = created.json()
    assert set(body) == {"id", "name", "active"}
    assert body["name"] == "Dr. A" and body["active"] is True
    therapist_id = body["id"]
    assert client.get(f"/therapy/therapists/{therapist_id}").status_code == 200
    duplicate = client.post("/therapy/therapists", json={"name": "Dr. A"})
    assert duplicate.status_code == 201

    listed = client.get("/therapy/therapists")
    assert listed.status_code == 200 and listed.json()[0] == body
    deactivated = client.post(f"/therapy/therapists/{therapist_id}/deactivate")
    assert deactivated.status_code == 200 and deactivated.json()["active"] is False
    assert client.post(f"/therapy/therapists/{therapist_id}/deactivate").json()["active"] is False
    assert client.post(f"/therapy/therapists/{therapist_id}/reactivate").json()["active"] is True
    with fresh() as session:
        from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel

        persisted = session.get(TherapistModel, therapist_id)
        assert persisted is not None and persisted.active is True


def test_therapist_api_owner_override_and_list_isolation_ordering(api) -> None:
    client, _, current_owner, owner = api
    client.post("/therapy/therapists", json={"name": "B"})
    client.post("/therapy/therapists", json={"name": "A"})
    inactive = client.post("/therapy/therapists", json={"name": "Inactive"}).json()
    client.post(f"/therapy/therapists/{inactive['id']}/deactivate")
    owner_b = UserId.new()
    with api[1]() as session:
        session.add(
            UserModel(
                id=owner_b.value,
                email=f"{owner_b.value}@owner-b.test",
                hashed_password="x",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
        session.commit()
    current_owner[0] = owner_b
    foreign = client.post("/therapy/therapists", json={"name": "Foreign"}).json()
    current_owner[0] = owner
    listed = client.get("/therapy/therapists").json()
    assert [item["name"] for item in listed] == ["A", "B", "Inactive"]
    assert all(set(item) == {"id", "name", "active"} for item in listed)
    assert client.get(f"/therapy/therapists/{foreign['id']}").status_code == 404
    assert client.post(f"/therapy/therapists/{foreign['id']}/deactivate").status_code == 404
    assert client.post(f"/therapy/therapists/{foreign['id']}/reactivate").status_code == 404


def test_therapist_api_valid_owner_override_is_rejected(api) -> None:
    client, _, _, _ = api
    assert (
        client.post(
            "/therapy/therapists", json={"name": "Valid Name", "owner_id": UserId.new().value}
        ).status_code
        == 422
    )


@pytest.mark.parametrize("value", ["malformed", "not-a-tsid"])
def test_therapist_api_invalid_id_is_422(api, value: str) -> None:
    client, _, _, _ = api
    assert client.get(f"/therapy/therapists/{value}").status_code == 422


def test_therapist_api_missing_and_forbidden_fields(api) -> None:
    client, _, _, _ = api
    assert client.get(f"/therapy/therapists/{TherapistId.new().value}").status_code == 404
    assert client.post("/therapy/therapists", json={"name": "", "owner_id": "x"}).status_code == 422
    assert client.post("/therapy/therapists", json={"name": "x" * 151}).status_code == 422
    assert client.delete("/therapy/therapists/foo").status_code == 405


def test_foreign_therapist_is_indistinguishable_from_missing(api) -> None:
    client, fresh, current_owner, _ = api
    created = client.post("/therapy/therapists", json={"name": "Private"}).json()
    therapist_id = created["id"]
    foreign = UserId.new()
    with fresh() as session:
        session.add(
            UserModel(
                id=foreign.value,
                email=f"{foreign.value}@foreign.test",
                hashed_password="x",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
        session.commit()
    current_owner[0] = foreign
    response = client.get(f"/therapy/therapists/{therapist_id}")
    missing = client.get(f"/therapy/therapists/{TherapistId.new().value}")
    assert response.status_code == missing.status_code == 404
    assert response.json() == missing.json() == {"detail": "Therapist not found."}
