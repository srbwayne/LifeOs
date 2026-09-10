from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.app_factory import create_app
from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.composition_root import get_current_user_id
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base, get_db
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel
from app.therapy.infrastructure.persistence.models.therapy_session_model import TherapySessionModel
from app.therapy.infrastructure.persistence.repositories.therapist_repository import (
    SqlAlchemyTherapistRepository,
)


def test_private_note_update_and_delete_api_with_disposable_db():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    app = create_app()
    owner = UserId.new()
    with factory() as db:
        db.add(
            UserModel(
                id=owner.value,
                email=f"{owner.value}@test",
                hashed_password="x",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
        therapist = Therapist.create(owner, "Dr. A")
        SqlAlchemyTherapistRepository(db).save(therapist)
        db.commit()

    def db_override():
        with factory() as db:
            yield db

    app.dependency_overrides[get_db] = db_override
    app.dependency_overrides[get_current_user_id] = lambda: owner
    with TestClient(app) as client:
        created = client.post(
            "/therapy/sessions",
            json={
                "therapist_id": therapist.id.value,
                "occurred_at": "2026-01-01T12:00:00Z",
                "private_note": "known-sensitive-value",
            },
        ).json()
        sid = created["id"]
        updated = client.patch(
            f"/therapy/sessions/{sid}/private-note", json={"private_note": "  revised  "}
        )
        assert (
            updated.status_code == 200
            and set(updated.json()) == {"id", "private_note"}
            and updated.json()["private_note"] == "revised"
        )
        assert (
            client.patch(
                f"/therapy/sessions/{sid}/private-note", json={"private_note": None}
            ).json()["private_note"]
            is None
        )
        assert (
            client.patch(
                f"/therapy/sessions/{sid}/private-note", json={"private_note": "   "}
            ).json()["private_note"]
            is None
        )
        assert client.patch(f"/therapy/sessions/{sid}/private-note", json={}).status_code == 422
        oversized = client.patch(
            f"/therapy/sessions/{sid}/private-note",
            json={"private_note": "known-sensitive-value" * 500},
        )
        wrong_type = client.patch(
            f"/therapy/sessions/{sid}/private-note",
            json={"private_note": {"secret": "known-sensitive-value"}},
        )
        assert oversized.status_code == wrong_type.status_code == 422
        assert (
            "known-sensitive-value" not in oversized.text
            and "known-sensitive-value" not in wrong_type.text
        )
        assert (
            client.patch(
                f"/therapy/sessions/{sid}/private-note", json={"private_note": "final"}
            ).status_code
            == 200
        )
        deactivate_response = client.post(f"/therapy/therapists/{therapist.id.value}/deactivate")
        assert deactivate_response.status_code == 200
        inactive_update = client.patch(
            f"/therapy/sessions/{sid}/private-note", json={"private_note": "after inactive"}
        )
        assert inactive_update.status_code == 200
        deleted = client.delete(f"/therapy/sessions/{sid}")
        assert deleted.status_code == 204 and deleted.content == b""
        assert client.get(f"/therapy/sessions/{sid}").status_code == 404
        assert sid not in {item["id"] for item in client.get("/therapy/sessions").json()["items"]}
        assert client.delete(f"/therapy/sessions/{sid}").status_code == 404
    with factory() as db:
        assert db.get(TherapySessionModel, sid) is None
        assert db.get(TherapistModel, therapist.id.value) is not None
    app.dependency_overrides.clear()
    engine.dispose()


def test_private_note_routes_require_authentication_with_disposable_db():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    app = create_app()

    def db_override():
        with factory() as db:
            yield db

    app.dependency_overrides[get_db] = db_override
    with TestClient(app) as client:
        sid = TherapySessionId.new().value
        assert (
            client.patch(
                f"/therapy/sessions/{sid}/private-note", json={"private_note": "x"}
            ).status_code
            == 401
        )
        assert client.delete(f"/therapy/sessions/{sid}").status_code == 401
    app.dependency_overrides.clear()
    engine.dispose()
