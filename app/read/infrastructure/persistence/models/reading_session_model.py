import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database import Base


class ReadingSessionModel(Base):
    __tablename__ = "reading_sessions"
    __table_args__ = (
        CheckConstraint("start_page >= 1", name="ck_reading_sessions_start_page_positive"),
        CheckConstraint(
            "end_page >= start_page",
            name="ck_reading_sessions_end_page_not_before_start",
        ),
        CheckConstraint(
            "ended_at >= started_at",
            name="ck_reading_sessions_end_not_before_start_time",
        ),
        Index(
            "ix_reading_sessions_user_book",
            "user_id",
            "book_id",
        ),
        Index(
            "ix_reading_sessions_user_started_id",
            "user_id",
            "started_at",
            "id",
        ),
    )

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(26), ForeignKey("users.id"))
    book_id: Mapped[str] = mapped_column(String(26), ForeignKey("books.id"))
    start_page: Mapped[int] = mapped_column(Integer)
    end_page: Mapped[int] = mapped_column(Integer)
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.now,
    )
