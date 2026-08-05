from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.shared.infrastructure.database import Base
import datetime

class CharacterModel(Base):
    __tablename__ = "characters"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    player_id: Mapped[str] = mapped_column(String(26), ForeignKey("players.id"), unique=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime)
