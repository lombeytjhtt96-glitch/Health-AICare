from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class AutopilotActionResponse(BaseModel):
    id: int
    action_type: str
    risk_level: str
    policy_decision: str
    status: str
    idempotency_key: str
    payload_hash: str
    payload_json: Dict[str, Any]
    requires_human_review: bool
    approved_by: Optional[int] = None
    approval_notes: Optional[str] = None
    tx_hash: Optional[str] = None
    created_at: datetime

class ActionReviewRequest(BaseModel):
    admin_id: int
    approval_notes: Optional[str] = None
