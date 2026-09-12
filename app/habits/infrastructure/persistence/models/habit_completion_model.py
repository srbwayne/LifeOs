import datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database import Base


class HabitCompletionModel(Base):
    __tablename__ = "habit_completions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "habit_id"],
            ["habits.user_id", "habits.id"],
            ondelete="RESTRICT",
            name="fk_habit_completions_owner_habit",
        ),
        UniqueConstraint(
            "user_id",
            "habit_id",
            "record_date",
            name="uq_habit_completions_user_habit_record_date",
        ),
        Index(
            "ix_habit_completions_user_record_habit",
            "user_id",
            "record_date",
            "habit_id",
        ),
    )

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    habit_id: Mapped[str] = mapped_column(String(26), nullable=False)
    record_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now
    )
