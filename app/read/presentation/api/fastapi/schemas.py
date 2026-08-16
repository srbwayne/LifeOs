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


class ReadingHistoryItemResponse(BaseModel):
    id: str
    book_id: str
    book_title: str
    start_page: int
    end_page: int
    pages_read: int
    started_at: datetime
    ended_at: datetime
    notes: str | None


class ReadingHistoryPageResponse(BaseModel):
    items: list[ReadingHistoryItemResponse]
    page: int
    size: int
    total_items: int
    total_pages: int


class ReadingProgressResponse(BaseModel):
    book_id: str
    total_pages: int
    unique_pages_read: int
    highest_page_reached: int | None
    percentage: float
    completed: bool


class PageIntervalResponse(BaseModel):
    start_page: int
    end_page: int


class ReadingInsightsResponse(BaseModel):
    book_id: str
    remaining_pages: int
    gaps: list[PageIntervalResponse]
    last_page_reached_with_gaps: bool
    full_coverage_confirmed: bool


class ReadingStatisticsResponse(BaseModel):
    total_books: int
    books_with_reading_sessions: int
    total_reading_sessions: int
    total_pages_read: int
    average_pages_per_session: str
