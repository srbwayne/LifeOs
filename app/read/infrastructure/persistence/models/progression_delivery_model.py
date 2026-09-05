import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.database import Base


class ProgressionDeliveryModel(Base):
    __tablename__ = "progression_delivery_records"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'DELIVERED', 'FAILED')",
            name="ck_progression_delivery_status",
        ),
        CheckConstraint(
            "attempt_count >= 0",
            name="ck_progression_delivery_attempt_count_nonnegative",
        ),
        Index(
            "ix_progression_delivery_status_created",
            "status",
            "created_at",
        ),
        Index(
            "ix_progression_delivery_subject_created",
            "subject_namespace",
            "subject_external_id",
            "created_at",
            "id",
        ),
    )

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    reading_session_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("reading_sessions.id", ondelete="RESTRICT"), unique=True
    )
    source: Mapped[str] = mapped_column(String(64))
    idempotency_key: Mapped[str] = mapped_column(String(255))
    subject_namespace: Mapped[str] = mapped_column(String(64))
    subject_external_id: Mapped[str] = mapped_column(String(255))
    configuration_key: Mapped[str] = mapped_column(String(255))
    configuration_revision: Mapped[int] = mapped_column(Integer)
    pages_read: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16), default="PENDING")
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    last_attempt_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    delivered_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    last_error: Mapped[str | None] = mapped_column(String(500), nullable=True)
