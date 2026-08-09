import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database import Base


class BookModel(Base):
    __tablename__ = "books"
    __table_args__ = (CheckConstraint("total_pages > 0", name="ck_books_total_pages_positive"),)

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(26), ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    total_pages: Mapped[int] = mapped_column(Integer)
    isbn: Mapped[str | None] = mapped_column(String, nullable=True)
    publisher: Mapped[str | None] = mapped_column(String, nullable=True)
    edition: Mapped[str | None] = mapped_column(String, nullable=True)
    cover: Mapped[str | None] = mapped_column(String, nullable=True)
    genre: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)
