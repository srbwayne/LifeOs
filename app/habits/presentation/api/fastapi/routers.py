# ruff: noqa: B008

from fastapi import APIRouter, Depends, HTTPException, status

from app.composition_root import get_current_user_id
from app.habits.application.commands.create_habit import (
    CreateHabitCommand,
    CreateHabitCommandHandler,
)
from app.habits.application.commands.deactivate_habit import (
    DeactivateHabitCommand,
    DeactivateHabitCommandHandler,
)
from app.habits.application.commands.reactivate_habit import (
    ReactivateHabitCommand,
    ReactivateHabitCommandHandler,
)
from app.habits.application.dtos.habit_dto import HabitDTO
from app.habits.application.queries.get_habit import GetHabitQuery, GetHabitQueryHandler
from app.habits.application.queries.list_habits import ListHabitsQuery, ListHabitsQueryHandler
from app.habits.dependencies import (
    get_create_habit_handler,
    get_deactivate_habit_handler,
    get_get_habit_handler,
    get_list_habits_handler,
    get_reactivate_habit_handler,
)
from app.habits.domain.value_objects.habit_id import HabitId
from app.habits.presentation.api.fastapi.schemas import CreateHabitRequest, HabitResponse
from app.shared.domain.identifiers.user_id import UserId

router = APIRouter(prefix="/habits", tags=["Habits"])


def _response(dto: HabitDTO) -> HabitResponse:
    return HabitResponse(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        active=dto.active,
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
