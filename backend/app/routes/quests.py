from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.models import QuestTemplate, QuestInstance, User, AutopilotAction, AttestationRecord
from app.database.types import AutopilotActionType, AutopilotPolicyDecision, AutopilotActionStatus
from app.schemas.quests import QuestInstanceSchema, QuestTemplateSchema, QuestCompleteRequest, QuestCompleteResponse
from app.services.autopilot_policy_engine import policy_engine
from app.services.attestation_service import attestation_service

router = APIRouter(prefix="/api/v1/quests", tags=["CareQuest RPG Gamification"])

@router.get("/{user_id}", response_model=List[QuestInstanceSchema])
async def get_user_quests(user_id: int, db: AsyncSession = Depends(get_db)):
    # Ensure user has active quest instances
    stmt_active = select(QuestInstance).where(
        QuestInstance.user_id == user_id,
        QuestInstance.status == "active"
    )
    res_active = await db.execute(stmt_active)
    instances = res_active.scalars().all()

    if not instances:
        # Assign initial active quest if none exists
        stmt_t = select(QuestTemplate)
        res_t = await db.execute(stmt_t)
        templates = res_t.scalars().all()
        
        if not templates:
            # Auto-seed default templates if database is empty
            default_tmpls = [
                QuestTemplate(code="DAILY_JOURNAL_STREAK", name="Catatan Refleksi Diri", short_description="Tulis 1 entri jurnal harian.", category="reflection", base_xp=20, base_joy=10),
                QuestTemplate(code="GROUNDING_54321", name="Latihan Grounding 5-4-3-2-1", short_description="Lakukan teknik sensorik 5-4-3-2-1.", category="wellness", base_xp=25, base_joy=15),
                QuestTemplate(code="CAREQUEST_TYPING_GAME", name="Tantangan CareQuest Typing", short_description="Kalahkan monster kecemasan.", category="support", base_xp=30, base_joy=20)
            ]
            db.add_all(default_tmpls)
            await db.commit()
            
            res_t = await db.execute(stmt_t)
            templates = res_t.scalars().all()

        for t in templates:
            inst = QuestInstance(user_id=user_id, template_id=t.id, status="active")
            db.add(inst)
        await db.commit()
        
        res_active = await db.execute(stmt_active)
        instances = res_active.scalars().all()

    result = []
    for inst in instances:
        res_tmpl = await db.execute(select(QuestTemplate).where(QuestTemplate.id == inst.template_id))
        tmpl = res_tmpl.scalar_one()
        result.append(
            QuestInstanceSchema(
                id=inst.id,
                user_id=inst.user_id,
                template=QuestTemplateSchema(
                    id=tmpl.id,
                    code=tmpl.code,
                    name=tmpl.name,
                    short_description=tmpl.short_description,
                    category=tmpl.category,
                    base_xp=tmpl.base_xp,
                    base_joy=tmpl.base_joy
                ),
                status=inst.status,
                issued_at=inst.issued_at,
                completed_at=inst.completed_at
            )
        )
    return result


@router.post("/complete", response_model=QuestCompleteResponse)
async def complete_quest(req: QuestCompleteRequest, db: AsyncSession = Depends(get_db)):
    stmt_inst = select(QuestInstance).where(
        QuestInstance.id == req.quest_instance_id,
        QuestInstance.user_id == req.user_id
    )
    res_inst = await db.execute(stmt_inst)
    instance = res_inst.scalar_one_or_none()

    if not instance:
        raise HTTPException(status_code=404, detail="Quest instance not found")

    if instance.status == "completed":
        return QuestCompleteResponse(
            status="already_completed",
            message="Quest sudah pernah diseleshealth_ain sebelumnya.",
            xp_gained=0,
            joy_gained=0,
            attestation_queued=False
        )

    # Fetch template rewards
    stmt_tmpl = select(QuestTemplate).where(QuestTemplate.id == instance.template_id)
    res_tmpl = await db.execute(stmt_tmpl)
    template = res_tmpl.scalar_one()

    # Update instance status
    instance.status = "completed"
    instance.completed_at = datetime.now(timezone.utc)
    
    # Update User streak
    stmt_u = select(User).where(User.id == req.user_id)
    res_u = await db.execute(stmt_u)
    user = res_u.scalar_one_or_none()
    if user:
        user.current_streak += 1
        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak

    # Create Low Risk Autopilot Action for on-chain badge/attestation
    payload = {
        "user_id": req.user_id,
        "quest_instance_id": instance.id,
        "quest_code": template.code,
        "xp_gained": template.base_xp
    }
    payload_hash = attestation_service.compute_payload_hash(payload)
    dec, stat, req_rev, risk = policy_engine.evaluate_action(AutopilotActionType.add_game_xp, payload)

    action = AutopilotAction(
        action_type=AutopilotActionType.add_game_xp,
        risk_level=risk,
        policy_decision=dec,
        status=stat,
        idempotency_key=f"quest_complete_{instance.id}",
        payload_hash=payload_hash,
        payload_json=payload
    )
    attestation = AttestationRecord(
        quest_instance_id=instance.id,
        counselor_id=req.user_id,
        hashed_payload=payload_hash,
        status="confirmed",
        extra_data={"payload": payload}
    )
    db.add_all([action, attestation])
    await db.commit()

    # Immediately submit attestation record
    await attestation_service.submit_attestation(db, action.id)

    return QuestCompleteResponse(
        status="success",
        message=f"Selamat! Quest '{template.name}' berhasil diseleshealth_ain.",
        xp_gained=template.base_xp,
        joy_gained=template.base_joy,
        attestation_queued=True
    )
