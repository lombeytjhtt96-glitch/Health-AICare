from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class QuestTemplateSchema(BaseModel):
    id: int
    code: str
    name: str
    short_description: str
    category: str
    base_xp: int
    base_joy: int

class QuestInstanceSchema(BaseModel):
    id: int
    user_id: int
    template: QuestTemplateSchema
    status: str
    issued_at: datetime
    completed_at: Optional[datetime] = None

class QuestCompleteRequest(BaseModel):
    user_id: int
    quest_instance_id: int

class QuestCompleteResponse(BaseModel):
    status: str
    message: str
    xp_gained: int
    joy_gained: int
    attestation_queued: bool
