import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.domains.mental_health.models import Conversation
from app.models.case import Case
from app.models.screening import ConversationRiskAssessment
from app.agents.health_ai_orchestrator_graph import health_ai_graph
from app.agents.graph_state import HealthAIOrchestratorState
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatHistoryResponse

router = APIRouter(prefix="/api/v1/chat", tags=["Agentic Chat"])

@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(req: ChatMessageRequest, db: AsyncSession = Depends(get_db)):
    conv_id = str(uuid.uuid4())
    user_hash = f"user_hash_{req.user_id}"

    # Construct initial state
    initial_state: HealthAIOrchestratorState = {
        "user_id": req.user_id,
        "user_role": req.user_role,
        "session_id": req.session_id,
        "user_hash": user_hash,
        "message": req.message,
        "conversation_history": []
    }

    # Execute LangGraph Multi-Agent Orchestrator
    final_state = await health_ai_graph.ainvoke(initial_state, config={"configurable": {"thread_id": req.session_id, "db": db}})

    response_text = final_state.get("final_response", "Maaf, saya belum dapat memproses pesan Anda.")
    intent = final_state.get("intent", "general_support")
    risk_level = final_state.get("risk_level", 0)
    severity = final_state.get("severity", "low")
    case_created = final_state.get("case_created", False)

    # Persist Conversation
    conv = Conversation(
        user_id=req.user_id,
        session_id=req.session_id,
        conversation_id=conv_id,
        message=req.message,
        response=response_text
    )
    db.add(conv)
    await db.commit()

    # If Case was created by CMA (risk_level == 3), persist Case record
    if case_created:
        case = Case(
            severity=severity,
            status="new",
            assigned_to=final_state.get("assigned_counsellor_id", "default-counselor-01"),
            user_hash=user_hash,
            session_id=req.session_id,
            conversation_id=conv.id,
            summary_redacted=final_state.get("redacted_message", req.message)
        )
        db.add(case)
        await db.commit()

    # Persist Risk Assessment
    risk_record = ConversationRiskAssessment(
        conversation_id=conv_id,
        session_id=req.session_id,
        user_id=req.user_id,
        overall_risk_level=str(severity),
        risk_trend="stable",
        conversation_summary=f"Intent: {intent}, Risk Level: {risk_level}",
        reasoning=f"Evaluated via Health-AI LangGraph decision node.",
        pleasure=0.0,
        arousal=0.5,
        dominance=0.5
    )
    db.add(risk_record)
    await db.commit()

    return ChatMessageResponse(
        session_id=req.session_id,
        response=response_text,
        intent=intent,
        risk_level=risk_level,
        severity=severity,
        case_created=case_created,
        intervention_plan=final_state.get("intervention_plan"),
        emergency_hotlines=final_state.get("emergency_hotlines")
    )


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Conversation).where(Conversation.session_id == session_id).order_by(Conversation.timestamp.asc())
    res = await db.execute(stmt)
    records = res.scalars().all()

    history = [
        {
            "id": r.id,
            "message": r.message,
            "response": r.response,
            "timestamp": r.timestamp.isoformat()
        }
        for r in records
    ]

    return ChatHistoryResponse(
        session_id=session_id,
        history=history
    )
