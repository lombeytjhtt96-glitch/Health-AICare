"""Assessment and triage models."""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime

if TYPE_CHECKING:
    from .conversations import Conversation
    from app.models.user import User

from app.models.screening import TriageAssessment, UserScreeningProfile, ConversationRiskAssessment