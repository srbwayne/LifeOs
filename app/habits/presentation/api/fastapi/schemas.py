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
