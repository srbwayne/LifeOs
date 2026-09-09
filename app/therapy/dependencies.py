# ruff: noqa: B008

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.application.event_bus import IEventBus, InMemoryEventBus
from app.shared.application.unit_of_work import IUnitOfWork
from app.shared.infrastructure.database import get_db
from app.shared.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from app.therapy.application.commands.create_therapist import CreateTherapistCommandHandler
from app.therapy.application.commands.deactivate_therapist import DeactivateTherapistCommandHandler
from app.therapy.application.commands.reactivate_therapist import ReactivateTherapistCommandHandler
from app.therapy.application.ports.therapist_read_repository import ITherapistReadRepository
from app.therapy.application.queries.get_therapist import GetTherapistQueryHandler
from app.therapy.application.queries.list_therapists import ListTherapistsQueryHandler
from app.therapy.domain.ports.therapist_repository import ITherapistRepository
from app.therapy.infrastructure.persistence.repositories.therapist_read_repository import (
    SqlAlchemyTherapistReadRepository,
)
from app.therapy.infrastructure.persistence.repositories.therapist_repository import (
    SqlAlchemyTherapistRepository,
)


def get_therapist_repository(db: Session = Depends(get_db)) -> ITherapistRepository:
    return SqlAlchemyTherapistRepository(db)


def get_therapist_read_repository(db: Session = Depends(get_db)) -> ITherapistReadRepository:
    return SqlAlchemyTherapistReadRepository(db)


def get_therapy_event_bus() -> IEventBus:
    return InMemoryEventBus()


def get_therapy_uow(
    db: Session = Depends(get_db),
    event_bus: IEventBus = Depends(get_therapy_event_bus),
) -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db, event_bus)


def get_create_therapist_handler(
    repository: ITherapistRepository = Depends(get_therapist_repository),
    unit_of_work: IUnitOfWork = Depends(get_therapy_uow),
) -> CreateTherapistCommandHandler:
    return CreateTherapistCommandHandler(repository, unit_of_work)


def get_get_therapist_handler(
    repository: ITherapistRepository = Depends(get_therapist_repository),
) -> GetTherapistQueryHandler:
    return GetTherapistQueryHandler(repository)


def get_list_therapists_handler(
    repository: ITherapistReadRepository = Depends(get_therapist_read_repository),
) -> ListTherapistsQueryHandler:
    return ListTherapistsQueryHandler(repository)


def get_deactivate_therapist_handler(
    repository: ITherapistRepository = Depends(get_therapist_repository),
    unit_of_work: IUnitOfWork = Depends(get_therapy_uow),
) -> DeactivateTherapistCommandHandler:
    return DeactivateTherapistCommandHandler(repository, unit_of_work)


def get_reactivate_therapist_handler(
    repository: ITherapistRepository = Depends(get_therapist_repository),
    unit_of_work: IUnitOfWork = Depends(get_therapy_uow),
) -> ReactivateTherapistCommandHandler:
    return ReactivateTherapistCommandHandler(repository, unit_of_work)
