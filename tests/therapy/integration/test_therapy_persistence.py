from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.infrastructure.persistence.models.user_model import UserModel
from app.read.infrastructure.persistence.models.book_completion_model import (  # noqa: F401
    BookCompletionModel,
)
from app.read.infrastructure.persistence.models.book_model import BookModel  # noqa: F401
from app.read.infrastructure.persistence.models.progression_delivery_model import (
    ProgressionDeliveryModel,  # noqa: F401
)
from app.read.infrastructure.persistence.models.reading_session_model import (  # noqa: F401
    ReadingSessionModel,
)
from app.shared.domain.identifiers.user_id import UserId
from app.shared.infrastructure.database import Base
from app.therapy.application.dtos.therapist_dto import TherapistDTO
from app.therapy.application.dtos.therapy_session_dto import (
    TherapySessionDetailDTO,
    TherapySessionHistoryItemDTO,
)
from app.therapy.domain.aggregates.therapist import Therapist
from app.therapy.domain.aggregates.therapy_session import TherapySession
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.infrastructure.persistence.mappers.therapist_mapper import TherapistMapper
from app.therapy.infrastructure.persistence.mappers.therapy_session_mapper import (
    TherapySessionMapper,
)
from app.therapy.infrastructure.persistence.models.therapist_model import TherapistModel
from app.therapy.infrastructure.persistence.models.therapy_session_model import (
    TherapySessionModel,
)
from app.therapy.infrastructure.persistence.repositories.therapist_read_repository import (
    SqlAlchemyTherapistReadRepository,
)
from app.therapy.infrastructure.persistence.repositories.therapist_repository import (
    SqlAlchemyTherapistRepository,
)
from app.therapy.infrastructure.persistence.repositories.therapy_session_read_repository import (
    SqlAlchemyTherapySessionReadRepository,
)
from app.therapy.infrastructure.persistence.repositories.therapy_session_repository import (
    SqlAlchemyTherapySessionRepository,
)

UTC_NOW = datetime(2026, 9, 9, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'therapy.db'}")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()


def add_user(session: Session, user_id: UserId) -> None:
    session.add(
        UserModel(
            id=user_id.to_persistence(),
            email=f"{user_id.value}@example.test",
            hashed_password="hash",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    )


def create_therapist(session: Session, owner_id: UserId, name: str = "Therapist") -> Therapist:
    therapist = Therapist.create(owner_id, name)
    SqlAlchemyTherapistRepository(session).save(therapist)
    session.flush()
    return therapist


def create_session(
    session: Session,
    owner_id: UserId,
    therapist_id: TherapistId,
    occurred_at: datetime,
    note: str | None = None,
) -> TherapySession:
    therapy_session = TherapySession.create(
        owner_id=owner_id,
        therapist_id=therapist_id,
        occurred_at=occurred_at,
        now=UTC_NOW,
        private_note=note,
    )
    SqlAlchemyTherapySessionRepository(session).save(therapy_session)
    session.flush()
    return therapy_session


def test_mapper_round_trips_therapist_and_session_without_new_ids(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    therapist = Therapist.create(owner_id, "  Example  ")
    therapist_model = TherapistMapper.to_persistence(therapist)
    session.add(therapist_model)
    session.flush()

    restored_therapist_model = session.get(TherapistModel, therapist.id.value)
    assert restored_therapist_model is not None
    restored_therapist = TherapistMapper.to_domain(restored_therapist_model)
    assert restored_therapist.id == therapist.id
    assert restored_therapist.name == "Example"

    occurred_at = datetime(2026, 9, 8, 9, 0, tzinfo=timezone(timedelta(hours=-3)))
    therapy_session = TherapySession.create(
        owner_id, therapist.id, occurred_at, UTC_NOW, "  private  "
    )
    therapy_model = TherapySessionMapper.to_persistence(therapy_session)
    session.add(therapy_model)
    session.flush()

    restored_session_model = session.get(TherapySessionModel, therapy_session.id.value)
    assert restored_session_model is not None
    restored_session = TherapySessionMapper.to_domain(restored_session_model)
    assert restored_session.id == therapy_session.id
    assert restored_session.occurred_at == datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)
    assert restored_session.private_note == "private"


def test_therapist_repository_is_owner_scoped_and_persists_active_state(session: Session) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    therapist = create_therapist(session, owner_a)
    repository = SqlAlchemyTherapistRepository(session)

    assert repository.get_by_id_and_owner(therapist.id, owner_a) == therapist
    assert repository.get_by_id_and_owner(therapist.id, owner_b) is None

    therapist.deactivate()
    repository.save(therapist)
    session.flush()
    restored = repository.get_by_id_and_owner(therapist.id, owner_a)
    assert restored is not None
    assert restored.active is False


def test_therapist_repository_rejects_owner_transfer_and_rename(session: Session) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    therapist = create_therapist(session, owner_a, "Original")
    repository = SqlAlchemyTherapistRepository(session)

    forged_owner = Therapist.restore(therapist.id, owner_b, "Original", True)
    with pytest.raises(ValueError):
        repository.save(forged_owner)
    session.flush()

    persisted = session.get(TherapistModel, therapist.id.value)
    assert persisted is not None
    assert persisted.user_id == owner_a.value
    assert persisted.name == "Original"

    forged_name = Therapist.restore(therapist.id, owner_a, "Changed", True)
    with pytest.raises(ValueError):
        repository.save(forged_name)
    session.flush()

    persisted = session.get(TherapistModel, therapist.id.value)
    assert persisted is not None
    assert persisted.user_id == owner_a.value
    assert persisted.name == "Original"


def test_therapy_session_repository_supports_owner_scope_update_and_delete(
    session: Session,
) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    therapist = create_therapist(session, owner_a)
    therapy_session = create_session(session, owner_a, therapist.id, UTC_NOW, "Initial")
    repository = SqlAlchemyTherapySessionRepository(session)

    assert repository.get_by_id_and_owner(therapy_session.id, owner_a) is not None
    assert repository.get_by_id_and_owner(therapy_session.id, owner_b) is None

    therapy_session.update_private_note("Updated")
    repository.save(therapy_session)
    session.flush()
    restored = repository.get_by_id_and_owner(therapy_session.id, owner_a)
    assert restored is not None
    assert restored.private_note == "Updated"

    repository.delete(therapy_session)
    session.flush()
    assert repository.get_by_id_and_owner(therapy_session.id, owner_a) is None


def test_therapy_session_repository_rejects_structural_mutations(session: Session) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    therapist_a = create_therapist(session, owner_a, "A")
    therapist_b = create_therapist(session, owner_b, "B")
    therapy_session = create_session(session, owner_a, therapist_a.id, UTC_NOW, "Original")
    repository = SqlAlchemyTherapySessionRepository(session)

    forged_owner = TherapySession.restore(
        therapy_session.id, owner_b, therapist_b.id, UTC_NOW, "Forged"
    )
    with pytest.raises(ValueError):
        repository.save(forged_owner)
    session.flush()

    forged_therapist = TherapySession.restore(
        therapy_session.id, owner_a, TherapistId.new(), UTC_NOW, "Forged"
    )
    with pytest.raises(ValueError):
        repository.save(forged_therapist)
    session.flush()

    forged_time = TherapySession.restore(
        therapy_session.id,
        owner_a,
        therapist_a.id,
        UTC_NOW - timedelta(minutes=1),
        "Forged",
    )
    with pytest.raises(ValueError):
        repository.save(forged_time)
    session.flush()

    persisted = session.get(TherapySessionModel, therapy_session.id.value)
    assert persisted is not None
    assert persisted.user_id == owner_a.value
    assert persisted.therapist_id == therapist_a.id.value
    assert persisted.occurred_at == UTC_NOW.replace(tzinfo=None)
    assert persisted.private_note == "Original"


def test_therapy_session_detail_dto_repr_does_not_expose_private_note() -> None:
    secret = "known-sensitive-value"
    dto = TherapySessionDetailDTO("session", "therapist", "Name", UTC_NOW, secret)

    assert secret not in repr(dto)


def test_database_rejects_cross_owner_composite_therapist_reference(session: Session) -> None:
    owner_a = UserId.new()
    owner_b = UserId.new()
    add_user(session, owner_a)
    add_user(session, owner_b)
    therapist = create_therapist(session, owner_a)

    session.add(
        TherapySessionModel(
            id=TherapySessionId.new().value,
            user_id=owner_b.value,
            therapist_id=therapist.id.value,
            occurred_at=UTC_NOW,
            private_note=None,
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_therapist_delete_is_restricted_when_referenced(session: Session) -> None:
    owner_id = UserId.new()
    add_user(session, owner_id)
    therapist = create_therapist(session, owner_id)
    create_session(session, owner_id, therapist.id, UTC_NOW)

    session.delete(session.get(TherapistModel, therapist.id.value))
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_read_repositories_are_scoped_ordered_and_minimize_private_note(session: Session) -> None:
    owner_id = UserId.new()
    other_owner = UserId.new()
    add_user(session, owner_id)
    add_user(session, other_owner)
    therapist_b = create_therapist(session, owner_id, "B")
    therapist_a = create_therapist(session, owner_id, "A")
    inactive = create_therapist(session, owner_id, "Inactive")
    inactive.deactivate()
    SqlAlchemyTherapistRepository(session).save(inactive)
    other_therapist = create_therapist(session, other_owner, "Other")

    therapist_items = SqlAlchemyTherapistReadRepository(session).list_by_owner(owner_id)
    assert therapist_items == (
        TherapistDTO(therapist_a.id.value, "A", True),
        TherapistDTO(therapist_b.id.value, "B", True),
        TherapistDTO(inactive.id.value, "Inactive", False),
    )

    older = create_session(
        session, owner_id, therapist_b.id, UTC_NOW - timedelta(days=2), "Older private"
    )
    newer = create_session(
        session, owner_id, therapist_a.id, UTC_NOW - timedelta(days=1), "Newer private"
    )
    create_session(session, other_owner, other_therapist.id, UTC_NOW, "Other private")
    read_repository = SqlAlchemyTherapySessionReadRepository(session)

    assert read_repository.count_by_owner(owner_id) == 2
    history = read_repository.list_page_by_owner(owner_id, 0, 1)
    assert history == (
        TherapySessionHistoryItemDTO(newer.id.value, therapist_a.id.value, "A", newer.occurred_at),
    )
    assert not hasattr(history[0], "private_note")
    assert read_repository.list_page_by_owner(owner_id, 1, 1)[0].id == older.id.value

    detail = read_repository.get_by_id_and_owner(newer.id, owner_id)
    assert detail == TherapySessionDetailDTO(
        newer.id.value, therapist_a.id.value, "A", newer.occurred_at, "Newer private"
    )
    assert read_repository.get_by_id_and_owner(newer.id, other_owner) is None


def test_history_projection_sql_does_not_select_private_note() -> None:
    assert (
        "private_note"
        not in SqlAlchemyTherapySessionReadRepository.list_page_by_owner.__code__.co_names
    )
