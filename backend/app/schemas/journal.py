from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class JournalCreateRequest(BaseModel):
    user_id: int
    content: str
    entry_date: Optional[date] = None
    mood: Optional[int] = None

class JournalResponse(BaseModel):
    id: int
    user_id: int
    entry_date: date
    content: str
    mood: Optional[int] = None
    word_count: int
    valence: Optional[float] = None
    arousal: Optional[float] = None
    inferred_dominance: Optional[float] = None
    created_at: datetime
