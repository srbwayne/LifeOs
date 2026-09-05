import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.application.ports.progression_delivery_repository import (
    ProgressionDeliveryIntent,
)
from app.read.infrastructure.persistence.models.book_model import BookModel
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,
)
from app.read.infrastructure.persistence.models.reading_session_model import (
    ReadingSessionModel,
)
from app.read.infrastructure.persistence.repositories.progression_delivery_repository import (
    SqlAlchemyProgressionDeliveryRepository,
)
from app.shared.domain.tsid import new_tsid
from app.shared.infrastructure.database import Base


def _intent(session_id: str) -> ProgressionDeliveryIntent:
    return ProgressionDeliveryIntent(
        id=new_tsid(),
        reading_session_id=session_id,
        source="lifeos",
        idempotency_key=session_id,
        subject_namespace="lifeos",
        subject_external_id=new_tsid(),
        configuration_key="reading",
        configuration_revision=2,
        pages_read=30,
    )


def test_delivery_record_persists_immutable_facts_and_status_transitions() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_id = new_tsid()
    with Session(engine) as session:
        user_id = new_tsid()
        book_id = new_tsid()
        now = datetime.datetime.now()
        session.add(
            UserModel(
                id=user_id,
                email=f"{new_tsid()}@example.com",
                hashed_password="hash",
                created_at=now,
                updated_at=now,
            )
        )
        session.add(
            BookModel(
                id=book_id,
                user_id=user_id,
                title="Book",
                author="Author",
                total_pages=100,
            )
        )
        session.flush()
        session.add(
            ReadingSessionModel(
                id=session_id,
                user_id=user_id,
                book_id=book_id,
                start_page=1,
                end_page=30,
                started_at=datetime.datetime.now(datetime.timezone.utc),
                ended_at=datetime.datetime.now(datetime.timezone.utc),
            )
        )
        session.flush()
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        intent = _intent(session_id)
        repository.save(intent)
        session.commit()

        loaded = repository.get_by_id(intent.id)
        assert loaded is not None
        assert loaded.pages_read == 30
        assert loaded.configuration_revision == 2
        assert loaded.status == "PENDING"

        delivered_at = datetime.datetime.now(datetime.timezone.utc)
        repository.mark_delivered(intent.id, delivered_at)
        session.commit()
        persisted = session.get(ProgressionDeliveryModel, intent.id)
        assert persisted is not None
        assert persisted.status == "DELIVERED"
        assert persisted.attempt_count == 1
        assert persisted.last_attempt_at == delivered_at.replace(tzinfo=None)
        assert persisted.delivered_at == delivered_at.replace(tzinfo=None)

    inspector = inspect(engine)
    assert "progression_delivery_records" in inspector.get_table_names()
    indexes = {index["name"] for index in inspector.get_indexes("progression_delivery_records")}
    assert "ix_progression_delivery_subject_created" in indexes
    Base.metadata.drop_all(engine)


def test_duplicate_identity_is_rejected_by_database() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_id = new_tsid()
    with Session(engine) as session:
        repository = SqlAlchemyProgressionDeliveryRepository(session)
        first = _intent(session_id)
        second = ProgressionDeliveryIntent(
            id=new_tsid(),
            reading_session_id=new_tsid(),
            source=first.source,
            idempotency_key=first.idempotency_key,
            subject_namespace=first.subject_namespace,
            subject_external_id=first.subject_external_id,
            configuration_key=first.configuration_key,
            configuration_revision=first.configuration_revision,
            pages_read=31,
        )
        repository.save(first)
        repository.save(second)
        try:
            session.flush()
        except Exception:
            session.rollback()
        else:
            raise AssertionError("duplicate identity must fail")
    Base.metadata.drop_all(engine)
