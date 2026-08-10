from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ChatMessageRequest(BaseModel):
    message: str
    session_id: str
    user_id: int = 1
    user_role: str = "user"

class ChatMessageResponse(BaseModel):
    session_id: str
    response: str
    intent: Optional[str] = None
    risk_level: Optional[int] = 0
    severity: Optional[str] = "low"
    case_created: bool = False
    intervention_plan: Optional[Dict[str, Any]] = None
    emergency_hotlines: Optional[List[Dict[str, str]]] = None

class ChatHistoryResponse(BaseModel):
    session_id: str
    history: List[Dict[str, Any]]
