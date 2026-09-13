# ruff: noqa: B008

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.composition_root import get_current_user_id
from app.habits.application.commands.create_habit import (
    CreateHabitCommand,
    CreateHabitCommandHandler,
)
from app.habits.application.commands.deactivate_habit import (
    DeactivateHabitCommand,
    DeactivateHabitCommandHandler,
)
from app.habits.application.commands.mark_completion import (
    MarkCompletionCommand,
    MarkCompletionCommandHandler,
)
from app.habits.application.commands.reactivate_habit import (
    ReactivateHabitCommand,
    ReactivateHabitCommandHandler,
)
from app.habits.application.commands.unmark_completion import (
    UnmarkCompletionCommand,
    UnmarkCompletionCommandHandler,
)
from app.habits.application.dtos.habit_checklist_dto import HabitChecklistItemDTO
from app.habits.application.dtos.habit_completion_dto import (
    HabitCompletionDTO,
    HabitCompletionPageDTO,
)
from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.queries.get_checklist import (
    GetChecklistQuery,
    GetChecklistQueryHandler,
)
from app.habits.application.queries.get_habit import GetHabitQuery, GetHabitQueryHandler
from app.habits.application.queries.list_completions import (
    ListCompletionsQuery,
    ListCompletionsQueryHandler,
)
from app.habits.application.queries.list_habits import ListHabitsQuery, ListHabitsQueryHandler
from app.habits.dependencies import (
    get_create_habit_handler,
    get_deactivate_habit_handler,
    get_get_checklist_handler,
    get_get_habit_handler,
    get_list_completions_handler,
    get_list_habits_handler,
    get_mark_completion_handler,
    get_reactivate_habit_handler,
    get_unmark_completion_handler,
)
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.presentation.api.fastapi.schemas import (
    CreateHabitRequest,
    HabitChecklistItemResponse,
    HabitCompletionPageResponse,
    HabitCompletionResponse,
    HabitResponse,
    MarkHabitCompletionRequest,
)
from app.shared.domain.identifiers.user_id import UserId

router = APIRouter(prefix="/habits", tags=["Habits"])


def _response(dto: HabitDTO) -> HabitResponse:
    return HabitResponse(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        active=dto.active,
    )


def _completion_response(dto: HabitCompletionDTO) -> HabitCompletionResponse:
    return HabitCompletionResponse(
        id=dto.id,
        habit_id=dto.habit_id,
        record_date=dto.record_date,
    )


def _checklist_response(dto: HabitChecklistItemDTO) -> HabitChecklistItemResponse:
    return HabitChecklistItemResponse(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        completed=dto.completed,
    )


def _completion_page_response(page: HabitCompletionPageDTO) -> HabitCompletionPageResponse:
    return HabitCompletionPageResponse(
        items=[_completion_response(item) for item in page.items],
        page=page.page,
        size=page.size,
        total_items=page.total_items,
        total_pages=page.total_pages,
    )


def _parse_habit_id(value: str) -> HabitId:
    try:
        return HabitId.from_value(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid habit ID.",
        ) from exc


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    request: CreateHabitRequest,
    user_id: UserId = Depends(get_current_user_id),
    handler: CreateHabitCommandHandler = Depends(get_create_habit_handler),
) -> HabitResponse:
    return _response(
        handler(
            CreateHabitCommand(
                owner_id=user_id,
                name=request.name,
                description=request.description,
            )
        )
    )


@router.get("", response_model=list[HabitResponse])
def list_habits(
    user_id: UserId = Depends(get_current_user_id),
    handler: ListHabitsQueryHandler = Depends(get_list_habits_handler),
) -> list[HabitResponse]:
    return [_response(item) for item in handler(ListHabitsQuery(owner_id=user_id))]


@router.get("/checklist", response_model=list[HabitChecklistItemResponse])
def get_checklist(
    record_date: date,
    user_id: UserId = Depends(get_current_user_id),
    handler: GetChecklistQueryHandler = Depends(get_get_checklist_handler),
) -> list[HabitChecklistItemResponse]:
    return [
        _checklist_response(item)
        for item in handler(GetChecklistQuery(owner_id=user_id, record_date=record_date))
    ]


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: GetHabitQueryHandler = Depends(get_get_habit_handler),
) -> HabitResponse:
    return _response(
        handler(
            GetHabitQuery(
                owner_id=user_id,
                habit_id=_parse_habit_id(habit_id),
            )
        )
    )


@router.post("/{habit_id}/deactivate", response_model=HabitResponse)
def deactivate_habit(
    habit_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: DeactivateHabitCommandHandler = Depends(get_deactivate_habit_handler),
) -> HabitResponse:
    return _response(
        handler(
            DeactivateHabitCommand(
                owner_id=user_id,
                habit_id=_parse_habit_id(habit_id),
            )
        )
    )


@router.post("/{habit_id}/reactivate", response_model=HabitResponse)
def reactivate_habit(
    habit_id: str,
    user_id: UserId = Depends(get_current_user_id),
    handler: ReactivateHabitCommandHandler = Depends(get_reactivate_habit_handler),
) -> HabitResponse:
    return _response(
        handler(
            ReactivateHabitCommand(
                owner_id=user_id,
                habit_id=_parse_habit_id(habit_id),
            )
        )
    )


@router.get(
    "/{habit_id}/completions",
    response_model=HabitCompletionPageResponse,
)
def list_completions(
    habit_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    user_id: UserId = Depends(get_current_user_id),
    handler: ListCompletionsQueryHandler = Depends(get_list_completions_handler),
) -> HabitCompletionPageResponse:
    result = handler(
        ListCompletionsQuery(
            owner_id=user_id,
            habit_id=_parse_habit_id(habit_id),
            page=page,
            size=size,
        )
    )
    return _completion_page_response(result)


@router.post("/{habit_id}/completions", response_model=HabitCompletionResponse)
def mark_completion(
    habit_id: str,
    request: MarkHabitCompletionRequest,
    response: Response,
    user_id: UserId = Depends(get_current_user_id),
    handler: MarkCompletionCommandHandler = Depends(get_mark_completion_handler),
) -> HabitCompletionResponse:
    result = handler(
        MarkCompletionCommand(
            owner_id=user_id,
            habit_id=_parse_habit_id(habit_id),
            record_date=request.record_date,
        )
    )
    if result.created:
        response.status_code = status.HTTP_201_CREATED
    return _completion_response(result.completion)


@router.delete(
    "/{habit_id}/completions/{record_date}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unmark_completion(
    habit_id: str,
    record_date: date,
    user_id: UserId = Depends(get_current_user_id),
    handler: UnmarkCompletionCommandHandler = Depends(get_unmark_completion_handler),
) -> None:
    handler(
        UnmarkCompletionCommand(
            owner_id=user_id,
            habit_id=_parse_habit_id(habit_id),
            record_date=record_date,
        )
    )
