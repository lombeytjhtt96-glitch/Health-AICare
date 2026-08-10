from datetime import datetime
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.conversation import Conversation

class UserScreeningProfile(Base):
    __tablename__ = "user_screening_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    profile_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    overall_risk: Mapped[str] = mapped_column(String(50), default="none", nullable=False)
    requires_attention: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    total_messages_analyzed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_sessions_analyzed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_intervention_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User")


class ConversationRiskAssessment(Base):
    __tablename__ = "conversation_risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[str] = mapped_column(String(255), nullable=False)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    overall_risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_trend: Mapped[str] = mapped_column(String(50), nullable=False)
    conversation_summary: Mapped[str] = mapped_column(Text, nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    pleasure: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    arousal: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    dominance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    user_context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    protective_factors: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    concerns: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    recommended_actions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    should_invoke_cma: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    message_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    conversation_duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    analysis_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    raw_assessment: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User")


class TriageAssessment(Base):
    __tablename__ = "triage_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("conversations.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    severity_level: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_factors: Mapped[Optional[List[Any]]] = mapped_column(JSON, nullable=True)
    recommended_action: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    assessment_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    conversation: Mapped[Optional["Conversation"]] = relationship("Conversation")
    user: Mapped[Optional["User"]] = relationship("User")
