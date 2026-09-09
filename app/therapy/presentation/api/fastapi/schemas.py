from pydantic import BaseModel, ConfigDict, Field


class CreateTherapistRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(max_length=150)


class TherapistResponse(BaseModel):
    id: str
    name: str
    active: bool
