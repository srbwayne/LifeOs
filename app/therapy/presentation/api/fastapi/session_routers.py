# ruff: noqa: B008

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.composition_root import get_current_user_id
from app.shared.domain.identifiers.user_id import UserId
from app.therapy.application.commands.create_therapy_session import (
    CreateTherapySessionCommand,
    CreateTherapySessionCommandHandler,
)
from app.therapy.application.commands.delete_therapy_session import (
    DeleteTherapySessionCommand,
    DeleteTherapySessionCommandHandler,
)
from app.therapy.application.commands.update_private_note import (
    UpdatePrivateNoteCommand,
    UpdatePrivateNoteCommandHandler,
)
from app.therapy.application.dtos.therapy_session_dto import (
    TherapySessionDetailDTO,
    TherapySessionHistoryPageDTO,
    TherapySessionPrivateNoteDTO,
)
from app.therapy.application.queries.get_therapy_session import (
    GetTherapySessionQuery,
    GetTherapySessionQueryHandler,
)
from app.therapy.application.queries.list_therapy_sessions import (
    ListTherapySessionsQuery,
    ListTherapySessionsQueryHandler,
)
from app.therapy.dependencies import (
    get_create_therapy_session_handler,
    get_delete_therapy_session_handler,
    get_get_therapy_session_handler,
    get_list_therapy_sessions_handler,
    get_update_private_note_handler,
)
from app.therapy.domain.value_objects.therapist_id import TherapistId
from app.therapy.domain.value_objects.therapy_session_id import TherapySessionId
from app.therapy.presentation.api.fastapi.schemas import (
    CreateTherapySessionRequest,
    TherapySessionDetailResponse,
    TherapySessionHistoryItemResponse,
    TherapySessionHistoryPageResponse,
    TherapySessionPrivateNoteResponse,
    UpdatePrivateNoteRequest,
)

session_router = APIRouter(prefix="/therapy/sessions", tags=["Therapy"])


def _id(value: str, cls: type[TherapistId] | type[TherapySessionId], detail: str):
    try:
        return cls.from_value(value)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=detail) from exc


def _detail(dto: TherapySessionDetailDTO) -> TherapySessionDetailResponse:
    return TherapySessionDetailResponse(
        id=dto.id,
        therapist_id=dto.therapist_id,
        therapist_name=dto.therapist_name,
        occurred_at=dto.occurred_at,
        private_note=dto.private_note,
    )


@session_router.post(
    "", response_model=TherapySessionDetailResponse, status_code=status.HTTP_201_CREATED
)
def create_session(
    request: CreateTherapySessionRequest,
    user_id: UserId = Depends(get_current_user_id),
    handler: CreateTherapySessionCommandHandler = Depends(get_create_therapy_session_handler),
) -> TherapySessionDetailResponse:
    therapist_id = _id(request.therapist_id, TherapistId, "Invalid therapist ID.")
    return _detail(
        handler(
            CreateTherapySessionCommand(
                user_id, therapist_id, request.occurred_at, request.private_note
            )
        )
    )


@session_router.get("", response_model=TherapySessionHistoryPageResponse)
def list_sessions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user_id: UserId = Depends(get_current_user_id),
    handler: ListTherapySessionsQueryHandler = Depends(get_list_therapy_sessions_handler),
) -> TherapySessionHistoryPageResponse:
    result: TherapySessionHistoryPageDTO = handler(ListTherapySessionsQuery(user_id, page, size))
    return TherapySessionHistoryPageResponse(
        items=[
            TherapySessionHistoryItemResponse(
                id=item.id,
                therapist_id=item.therapist_id,
                therapist_name=item.therapist_name,
                occurred_at=item.occurred_at,
            )
            for item in result.items
        ],
        page=result.page,
        size=result.size,
        total_items=result.total_items,
        total_pages=result.total_pages,
    )


@session_router.get("/{session_id}", response_model=TherapySessionDetailResponse)
def get_session(
    session_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: GetTherapySessionQueryHandler = Depends(get_get_therapy_session_handler),
) -> TherapySessionDetailResponse:
    parsed = _id(session_id, TherapySessionId, "Invalid therapy session ID.")
    return _detail(handler(GetTherapySessionQuery(user_id, parsed)))


@session_router.patch(
    "/{session_id}/private-note", response_model=TherapySessionPrivateNoteResponse
)
def update_private_note(
    session_id: str,
    request: UpdatePrivateNoteRequest,
    user_id: UserId = Depends(get_current_user_id),
    handler: UpdatePrivateNoteCommandHandler = Depends(get_update_private_note_handler),
) -> TherapySessionPrivateNoteResponse:
    parsed = _id(session_id, TherapySessionId, "Invalid therapy session ID.")
    result: TherapySessionPrivateNoteDTO = handler(
        UpdatePrivateNoteCommand(user_id, parsed, request.private_note)
    )
    return TherapySessionPrivateNoteResponse(id=result.id, private_note=result.private_note)


@session_router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: DeleteTherapySessionCommandHandler = Depends(get_delete_therapy_session_handler),
) -> Response:
    parsed = _id(session_id, TherapySessionId, "Invalid therapy session ID.")
    handler(DeleteTherapySessionCommand(user_id, parsed))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
