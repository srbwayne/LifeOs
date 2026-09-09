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
from app.therapy.domain.value_objects.therapist_id import TherapistId
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
        assert client.post("/therapy/sessions", json={}).status_code == 401
        assert client.get("/therapy/sessions").status_code == 401
        assert client.get(f"/therapy/sessions/{UserId.new().value}").status_code == 401
    app.dependency_overrides.clear()
    engine.dispose()


def test_private_note_validation_does_not_echo_oversized_value():
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


def test_private_note_validation_does_not_echo_wrong_type_value():
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


def test_session_api_validation_boundaries_and_missing_foreign_contract():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    factory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    app = create_app()
    owner = UserId.new()
    foreign_owner = UserId.new()
    with factory() as db:
        for user in (owner, foreign_owner):
            db.add(
                UserModel(
                    id=user.value,
                    email=f"{user.value}@test",
                    hashed_password="x",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            )
        therapist = Therapist.create(owner, "Dr. A")
        foreign_therapist = Therapist.create(foreign_owner, "Foreign")
        repo = SqlAlchemyTherapistRepository(db)
        repo.save(therapist)
        repo.save(foreign_therapist)
        db.commit()

    def db_override():
        with factory() as db:
            yield db

    app.dependency_overrides[get_db] = db_override
    current = [owner]
    app.dependency_overrides[get_current_user_id] = lambda: current[0]
    with TestClient(app) as client:
        base = {"therapist_id": therapist.id.value, "occurred_at": "2026-01-01T12:00:00Z"}
        assert (
            client.post(
                "/therapy/sessions", json={**base, "owner_id": UserId.new().value}
            ).status_code
            == 422
        )
        assert (
            client.post(
                "/therapy/sessions", json={**base, "user_id": UserId.new().value}
            ).status_code
            == 422
        )
        assert (
            client.post("/therapy/sessions", json={**base, "private_note": "   "}).json()[
                "private_note"
            ]
            is None
        )
        assert (
            client.post(
                "/therapy/sessions", json={**base, "occurred_at": "2026-01-01T12:00:00"}
            ).status_code
            == 422
        )
        assert (
            client.post("/therapy/sessions", json={**base, "therapist_id": "bad"}).status_code
            == 422
        )
        missing = TherapistId.new().value
        missing_response = client.post("/therapy/sessions", json={**base, "therapist_id": missing})
        current[0] = foreign_owner
        foreign_response = client.post(
            "/therapy/sessions", json={**base, "therapist_id": therapist.id.value}
        )
        assert missing_response.status_code == foreign_response.status_code == 404
        assert missing_response.json() == foreign_response.json()
        assert client.get("/therapy/sessions?page=0").status_code == 422
        assert client.get("/therapy/sessions?size=0").status_code == 422
        assert client.get("/therapy/sessions?size=101").status_code == 422
    app.dependency_overrides.clear()
    engine.dispose()


def test_unrelated_validation_error_keeps_normal_detail_structure():
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
    app.dependency_overrides[get_current_user_id] = lambda: UserId.new()
    with TestClient(app) as client:
        response = client.get("/therapy/sessions?page=0")
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"][-1] == "page"
    app.dependency_overrides.clear()
    engine.dispose()
