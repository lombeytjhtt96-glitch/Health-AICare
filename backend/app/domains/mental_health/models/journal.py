"""Journal and reflection models."""

from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, UniqueConstraint, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

from app.models.user import User

class JournalPrompt(Base):
    """Journal writing prompts."""
    __tablename__ = "journal_prompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

from app.models.journal import JournalEntry

class JournalTag(Base):
    """Custom tags for journal entries."""
    __tablename__ = "journal_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    journal_entry_id: Mapped[int] = mapped_column(Integer, ForeignKey("journal_entries.id"), nullable=False, index=True)
    tag_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    journal_entry: Mapped["JournalEntry"] = relationship("JournalEntry", back_populates="tags")

class JournalReflectionPoint(Base):
    """Reflection points within journal entries."""
    __tablename__ = "journal_reflection_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    journal_entry_id: Mapped[int] = mapped_column(Integer, ForeignKey("journal_entries.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reflection_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    journal_entry: Mapped["JournalEntry"] = relationship("JournalEntry", back_populates="reflection_points")
    user: Mapped["User"] = relationship("User")