import datetime

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database import Base


class TherapySessionModel(Base):
    __tablename__ = "therapy_sessions"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "therapist_id"],
            ["therapists.user_id", "therapists.id"],
            ondelete="RESTRICT",
            name="fk_therapy_sessions_owner_therapist",
        ),
        Index("ix_therapy_sessions_user_occurred_id", "user_id", "occurred_at", "id"),
    )

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    therapist_id: Mapped[str] = mapped_column(String(26), nullable=False)
    occurred_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    private_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now
    )
