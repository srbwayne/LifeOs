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
from app.therapy.infrastructure.persistence.repositories.therapist_repository import (
    SqlAlchemyTherapistRepository,
)


def test_therapy_session_api_create_detail_history_and_authentication():
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
        payload = {
            "therapist_id": therapist.id.value,
            "occurred_at": "2026-01-01T12:00:00Z",
            "private_note": "  known-sensitive-value  ",
        }
        created = client.post("/therapy/sessions", json=payload)
        assert created.status_code == 201
        body = created.json()
        assert set(body) == {"id", "therapist_id", "therapist_name", "occurred_at", "private_note"}
        assert body["private_note"] == "known-sensitive-value"
        detail = client.get(f"/therapy/sessions/{body['id']}")
        assert (
            detail.status_code == 200 and detail.json()["private_note"] == "known-sensitive-value"
        )
        history = client.get("/therapy/sessions").json()
        assert history["total_items"] == 1 and "private_note" not in history["items"][0]
        assert client.get("/therapy/sessions/not-a-tsid").status_code == 422
    app.dependency_overrides.clear()
    engine.dispose()


def test_therapy_session_api_requires_authentication():
    client = TestClient(create_app())
    assert client.get("/therapy/sessions").status_code == 401


def test_private_note_validation_does_not_echo_oversized_sentinel_before_fix():
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
    sentinel = "known-sensitive-value"
    with TestClient(app) as client:
        response = client.post(
            "/therapy/sessions",
            json={
                "therapist_id": therapist.id.value,
                "occurred_at": "2026-01-01T12:00:00Z",
                "private_note": sentinel * 500,
            },
        )
        assert response.status_code == 422
        assert sentinel not in response.text
    app.dependency_overrides.clear()
    engine.dispose()


def test_private_note_validation_does_not_echo_wrong_type_sentinel_before_fix():
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
    sentinel = "known-sensitive-value"
    with TestClient(app) as client:
        response = client.post(
            "/therapy/sessions",
            json={
                "therapist_id": therapist.id.value,
                "occurred_at": "2026-01-01T12:00:00Z",
                "private_note": {"secret": sentinel},
            },
        )
        assert response.status_code == 422
        assert sentinel not in response.text
    app.dependency_overrides.clear()
    engine.dispose()
