from datetime import date

from pydantic import BaseModel, ConfigDict


class CreateHabitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str | None = None


class HabitResponse(BaseModel):
    id: str
    name: str
    description: str | None
    active: bool


class MarkHabitCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_date: date


class HabitCompletionResponse(BaseModel):
    id: str
    habit_id: str
    record_date: date


class HabitChecklistItemResponse(BaseModel):
    id: str
    name: str
    description: str | None
    completed: bool


class HabitCompletionPageResponse(BaseModel):
    items: list[HabitCompletionResponse]
    page: int
    size: int
    total_items: int
    total_pages: int
