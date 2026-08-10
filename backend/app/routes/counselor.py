from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.domains.mental_health.models import Case
from app.schemas.counselor import CaseResponse, ClaimCaseRequest

router = APIRouter(prefix="/api/v1/counselor", tags=["Counselor Case Escalation Workspace"])

@router.get("/cases", response_model=List[CaseResponse])
async def get_escalated_cases(db: AsyncSession = Depends(get_db)):
    stmt = select(Case).order_by(Case.created_at.desc())
    res = await db.execute(stmt)
    cases = res.scalars().all()

    return [
        CaseResponse(
            id=c.id,
            created_at=c.created_at,
            status=c.status.value if hasattr(c.status, 'value') else str(c.status),
            severity=c.severity.value if hasattr(c.severity, 'value') else str(c.severity),
            assigned_to=c.assigned_to,
            user_hash=c.user_hash,
            summary_redacted=c.summary_redacted,
            sla_breach_at=c.sla_breach_at
        )
        for c in cases
    ]


@router.post("/cases/{case_id}/claim", response_model=CaseResponse)
async def claim_case(case_id: str, req: ClaimCaseRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(Case).where(Case.id == case_id)
    res = await db.execute(stmt)
    case = res.scalar_one_or_none()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    case.assigned_to = req.counselor_id
    case.status = "assigned"
    await db.commit()
    await db.refresh(case)

    return CaseResponse(
        id=case.id,
        created_at=case.created_at,
        status=case.status.value if hasattr(case.status, 'value') else str(case.status),
        severity=case.severity.value if hasattr(case.severity, 'value') else str(case.severity),
        assigned_to=case.assigned_to,
        user_hash=case.user_hash,
        summary_redacted=case.summary_redacted,
        sla_breach_at=case.sla_breach_at
    )
