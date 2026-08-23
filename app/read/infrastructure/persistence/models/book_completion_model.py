import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database import Base


class BookCompletionModel(Base):
    __tablename__ = "book_completions"
    __table_args__ = (
        Index(
            "ix_book_completions_completed_at_book_id",
            "completed_at",
            "book_id",
        ),
    )

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    book_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey("books.id", ondelete="RESTRICT"),
        unique=True,
    )
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
