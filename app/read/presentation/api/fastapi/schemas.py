from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateBookRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    author: str
    total_pages: int
    isbn: str | None = None
    publisher: str | None = None
    edition: str | None = None
    cover: str | None = None
    genre: str | None = None
    language: str | None = None


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    total_pages: int
    isbn: str | None
    publisher: str | None
    edition: str | None
    cover: str | None
    genre: str | None
    language: str | None


class CreateReadingSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start_page: int
    end_page: int
    started_at: datetime
    ended_at: datetime
    notes: str | None = None


class ReadingSessionResponse(BaseModel):
    id: str
    book_id: str
    start_page: int
    end_page: int
    pages_read: int
    started_at: datetime
    ended_at: datetime
    notes: str | None
