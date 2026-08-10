import enum
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB as PostgresJSONB

# Provide a JSONB-compatible type that gracefully degrades to the generic
# SQLAlchemy JSON type when running against SQLite (used in tests).
JSONBCompat = PostgresJSONB().with_variant(JSON(), "sqlite")

class AgentRoleEnum(str, enum.Enum):
    user = "user"
    student = "student"
    counselor = "counselor"
    admin = "admin"
    super_admin = "super_admin"

class CaseStatusEnum(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    waiting = "waiting"
    resolved = "resolved"
    closed = "closed"

class CaseSeverityEnum(str, enum.Enum):
    low = "low"
    med = "med"
    high = "high"
    critical = "critical"

class AutopilotActionType(str, enum.Enum):
    create_checkin = "create_checkin"
    create_case = "create_case"
    mint_badge = "mint_badge"
    publish_attestation = "publish_attestation"
    grant_badge_nft = "grant_badge_nft"
    issue_badge = "issue_badge"
    anchor_attestation = "anchor_attestation"
    escalate_case = "escalate_case"
    sync_state = "sync_state"
    add_game_xp = "add_game_xp"
    book_counseling_appointment = "book_counseling_appointment"
    create_escalation_ticket = "create_escalation_ticket"
    export_clinical_data = "export_clinical_data"
    modify_token_balance = "modify_token_balance"
    record_attestation = "record_attestation"
    escalate_crisis = "escalate_crisis"
    send_checkin = "send_checkin"

class AutopilotPolicyDecision(str, enum.Enum):
    allow = "allow"
    require_approval = "require_approval"
    deny = "deny"
    auto_execute = "auto_execute"
    auto_approved = "auto_approved"
    require_human_approval = "require_human_approval"
    reject = "reject"

class AutopilotActionStatus(str, enum.Enum):
    queued = "queued"
    awaiting_approval = "awaiting_approval"
    approved = "approved"
    rejected = "rejected"
    running = "running"
    confirmed = "confirmed"
    failed = "failed"
    dead_letter = "dead_letter"
    executing = "executing"
    completed = "completed"
    pending_approval = "pending_approval"

__all__ = [
    "JSONBCompat",
    "AgentRoleEnum",
    "CaseStatusEnum",
    "CaseSeverityEnum",
    "AutopilotActionType",
    "AutopilotPolicyDecision",
    "AutopilotActionStatus",
]
