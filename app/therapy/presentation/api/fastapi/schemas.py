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
    private_note: str | None = Field(default=None, max_length=10_000, repr=False)


class TherapySessionDetailResponse(BaseModel):
    id: str
    therapist_id: str
    therapist_name: str
    occurred_at: datetime
    private_note: str | None = Field(repr=False)


class UpdatePrivateNoteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    private_note: str | None = Field(..., max_length=10_000, repr=False)


class TherapySessionPrivateNoteResponse(BaseModel):
    id: str
    private_note: str | None = Field(repr=False)


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
