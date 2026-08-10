import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from app.database.types import CaseStatusEnum, CaseSeverityEnum

if TYPE_CHECKING:
    from app.domains.mental_health.models.cases import CaseNote
    from app.models.system import CaseAssignment
    from app.models.agent_user import AgentUser

class Case(Base):
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    status: Mapped[CaseStatusEnum] = mapped_column(
        SAEnum(CaseStatusEnum, name="case_status_enum", native_enum=False),
        nullable=False,
        default=CaseStatusEnum.new
    )
    severity: Mapped[CaseSeverityEnum] = mapped_column(
        SAEnum(CaseSeverityEnum, name="case_severity_enum", native_enum=False),
        nullable=False
    )
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String(255),
        ForeignKey("agent_users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    user_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    conversation_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True
    )
    summary_redacted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sla_breach_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    closure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    notes: Mapped[List["CaseNote"]] = relationship(
        "CaseNote",
        back_populates="case",
        cascade="all, delete-orphan",
    )
    assignments: Mapped[List["CaseAssignment"]] = relationship(
        "CaseAssignment",
        back_populates="case",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="CaseAssignment.assigned_at.desc()",
    )
    assignee: Mapped[Optional["AgentUser"]] = relationship(
        "AgentUser",
        foreign_keys=[assigned_to],
    )
