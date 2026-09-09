# ruff: noqa: B008

from fastapi import APIRouter, Depends, HTTPException, status

from app.composition_root import get_current_user_id
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
from app.therapy.application.queries.get_therapist import (
    GetTherapistQuery,
    GetTherapistQueryHandler,
)
from app.therapy.application.queries.list_therapists import (
    ListTherapistsQuery,
    ListTherapistsQueryHandler,
)
from app.therapy.dependencies import (
    get_create_therapist_handler,
    get_deactivate_therapist_handler,
    get_get_therapist_handler,
    get_list_therapists_handler,
    get_reactivate_therapist_handler,
)
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.presentation.api.fastapi.schemas import (
    CreateTherapistRequest,
    TherapistResponse,
)

router = APIRouter(prefix="/therapy/therapists", tags=["Therapy"])


def _response(dto: TherapistDTO) -> TherapistResponse:
    return TherapistResponse(id=dto.id, name=dto.name, active=dto.active)


def _parse_therapist_id(value: str) -> TherapistId:
    try:
        return TherapistId.from_value(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid therapist ID.",
        ) from exc


@router.post("", response_model=TherapistResponse, status_code=status.HTTP_201_CREATED)
def create_therapist(
    request: CreateTherapistRequest,
    user_id: UserId = Depends(get_current_user_id),
    handler: CreateTherapistCommandHandler = Depends(get_create_therapist_handler),
) -> TherapistResponse:
    return _response(handler(CreateTherapistCommand(owner_id=user_id, name=request.name)))


@router.get("", response_model=list[TherapistResponse])
def list_therapists(
    user_id: UserId = Depends(get_current_user_id),
    handler: ListTherapistsQueryHandler = Depends(get_list_therapists_handler),
) -> list[TherapistResponse]:
    return [_response(item) for item in handler(ListTherapistsQuery(owner_id=user_id))]


@router.get("/{therapist_id}", response_model=TherapistResponse)
def get_therapist(
    therapist_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: GetTherapistQueryHandler = Depends(get_get_therapist_handler),
) -> TherapistResponse:
    return _response(
        handler(
            GetTherapistQuery(
                owner_id=user_id,
                therapist_id=_parse_therapist_id(therapist_id),
            )
        )
    )


@router.post("/{therapist_id}/deactivate", response_model=TherapistResponse)
def deactivate_therapist(
    therapist_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: DeactivateTherapistCommandHandler = Depends(get_deactivate_therapist_handler),
) -> TherapistResponse:
    return _response(
        handler(
            DeactivateTherapistCommand(
                owner_id=user_id,
                therapist_id=_parse_therapist_id(therapist_id),
            )
        )
    )


@router.post("/{therapist_id}/reactivate", response_model=TherapistResponse)
def reactivate_therapist(
    therapist_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: ReactivateTherapistCommandHandler = Depends(get_reactivate_therapist_handler),
) -> TherapistResponse:
    return _response(
        handler(
            ReactivateTherapistCommand(
                owner_id=user_id,
                therapist_id=_parse_therapist_id(therapist_id),
            )
        )
    )
