from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateTherapistRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(max_length=150)


class TherapistResponse(BaseModel):
    id: str
    name: str
    active: bool


class CreateTherapySessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    therapist_id: str
    occurred_at: datetime
    private_note: str | None = Field(default=None, max_length=10_000)


class TherapySessionDetailResponse(BaseModel):
    id: str
    therapist_id: str
    therapist_name: str
    occurred_at: datetime
    private_note: str | None


class TherapySessionHistoryItemResponse(BaseModel):
    id: str
    therapist_id: str
    therapist_name: str
    occurred_at: datetime


class TherapySessionHistoryPageResponse(BaseModel):
    items: list[TherapySessionHistoryItemResponse]
    page: int
    size: int
    total_items: int
    total_pages: int
