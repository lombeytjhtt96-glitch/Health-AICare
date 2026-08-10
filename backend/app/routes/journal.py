from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.domains.mental_health.models import JournalEntry
from app.schemas.journal import JournalCreateRequest, JournalResponse

router = APIRouter(prefix="/api/v1/journal", tags=["Journaling Space"])

def compute_pad_affective(text: str) -> tuple[float, float, float]:
    """Calculate Pleasure, Arousal, Dominance (PAD) scores from text."""
    words = text.lower().split()
    positive_words = ["senang", "bahagia", "tenang", "bersyukur", "semangat", "baik", "lega", "optimis"]
    negative_words = ["sedih", "cemas", "takut", "marah", "kecewa", "lelah", "stres", "putus asa"]

    pos_count = sum(1 for w in words if any(p in w for p in positive_words))
    neg_count = sum(1 for w in words if any(n in w for n in negative_words))
    total = pos_count + neg_count

    if total == 0:
        return 0.0, 0.2, 0.5

    valence = (pos_count - neg_count) / total
    arousal = min(1.0, len(words) / 50.0)
    dominance = 0.5 + (valence * 0.3)
    return round(valence, 2), round(arousal, 2), round(dominance, 2)


@router.post("", response_model=JournalResponse, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(req: JournalCreateRequest, db: AsyncSession = Depends(get_db)):
    entry_date = req.entry_date or date.today()
    word_count = len(req.content.split())
    valence, arousal, dominance = compute_pad_affective(req.content)

    journal = JournalEntry(
        user_id=req.user_id,
        entry_date=entry_date,
        content=req.content,
        mood=req.mood or 3,
        word_count=word_count,
        valence=valence,
        arousal=arousal,
        inferred_dominance=dominance
    )
    db.add(journal)
    await db.commit()
    await db.refresh(journal)

    return JournalResponse(
        id=journal.id,
        user_id=journal.user_id,
        entry_date=journal.entry_date,
        content=journal.content,
        mood=journal.mood,
        word_count=journal.word_count,
        valence=journal.valence,
        arousal=journal.arousal,
        inferred_dominance=journal.inferred_dominance,
        created_at=journal.created_at
    )


@router.get("/{user_id:int}", response_model=List[JournalResponse])
async def get_user_journals(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(JournalEntry).where(JournalEntry.user_id == user_id).order_by(JournalEntry.entry_date.desc())
    res = await db.execute(stmt)
    entries = res.scalars().all()

    return [
        JournalResponse(
            id=j.id,
            user_id=j.user_id,
            entry_date=j.entry_date,
            content=j.content,
            mood=j.mood,
            word_count=j.word_count,
            valence=j.valence,
            arousal=j.arousal,
            inferred_dominance=j.inferred_dominance,
            created_at=j.created_at
        )
        for j in entries
    ]
