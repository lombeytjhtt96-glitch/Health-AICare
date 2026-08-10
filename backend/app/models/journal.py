from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, Text, Date, DateTime, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.domains.mental_health.models.journal import JournalPrompt, JournalReflectionPoint, JournalTag

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    prompt_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("journal_prompts.id"), nullable=True)
    mood: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    arousal: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    inferred_dominance: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="journal_entries")
    prompt: Mapped[Optional["JournalPrompt"]] = relationship("JournalPrompt")
    reflection_points: Mapped[List["JournalReflectionPoint"]] = relationship("JournalReflectionPoint", back_populates="journal_entry", cascade="all, delete-orphan")
    tags: Mapped[List["JournalTag"]] = relationship("JournalTag", back_populates="journal_entry", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('user_id', 'entry_date', name='_user_entry_date_uc'),)
