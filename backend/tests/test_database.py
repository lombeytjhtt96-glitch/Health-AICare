import pytest
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import (
    User, AgentUser, Conversation, Case,
    UserScreeningProfile, ConversationRiskAssessment, TriageAssessment,
    QuestTemplate, QuestInstance, AttestationRecord, AutopilotAction, JournalEntry
)
from app.database.types import (
    AgentRoleEnum, CaseStatusEnum, CaseSeverityEnum,
    AutopilotActionType, AutopilotPolicyDecision, AutopilotActionStatus
)

@pytest.mark.asyncio
async def test_user_creation_and_query(db_session: AsyncSession):
    user = User(
        email="test_user@example.com",
        name="User Test",
        role="user",
        wallet_address="0x1234567890abcdef1234567890abcdef12345678",
        current_streak=3,
        longest_streak=7,
        consent_ai_memory=True,
        consent_data_sharing=False
    )
    db_session.add(user)
    await db_session.commit()

    res = await db_session.execute(select(User).where(User.email == "test_user@example.com"))
    fetched_user = res.scalar_one_or_none()

    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.name == "User Test"
    assert fetched_user.current_streak == 3
    assert fetched_user.consent_ai_memory is True


@pytest.mark.asyncio
async def test_agent_user_and_case(db_session: AsyncSession):
    counselor = AgentUser(id="counselor_dr_budi", role=AgentRoleEnum.counselor)
    user = User(email="patient@example.com", name="Pasien Test")
    db_session.add_all([counselor, user])
    await db_session.commit()

    case = Case(
        severity=CaseSeverityEnum.high,
        status=CaseStatusEnum.new,
        assigned_to=counselor.id,
        user_hash="hash_anon_12345",
        summary_redacted="Ringkasan kasus terdisosiasi PII"
    )
    db_session.add(case)
    await db_session.commit()

    res = await db_session.execute(select(Case).where(Case.user_hash == "hash_anon_12345"))
    fetched_case = res.scalar_one_or_none()

    assert fetched_case is not None
    assert fetched_case.severity == CaseSeverityEnum.high
    assert fetched_case.assigned_to == "counselor_dr_budi"


@pytest.mark.asyncio
async def test_conversation_and_risk_assessment(db_session: AsyncSession):
    user = User(email="chat_user@example.com", name="User Chat")
    db_session.add(user)
    await db_session.commit()

    conv = Conversation(
        user_id=user.id,
        session_id="session_abc_123",
        conversation_id="conv_xyz_789",
        message="Saya merasa kewalahan dengan tugas skripsi.",
        response="Saya memahami perasaan kamu. Mari kita bicarakan secara perlahan."
    )
    db_session.add(conv)
    await db_session.commit()

    risk_assess = ConversationRiskAssessment(
        conversation_id="conv_xyz_789",
        session_id="session_abc_123",
        user_id=user.id,
        overall_risk_level="low",
        risk_trend="stable",
        conversation_summary="Stress akademik tugas akhir",
        reasoning="Pesan mengandung ekspresi kelelahan namun tidak ada ideasi bahaya.",
        pleasure=-0.3,
        arousal=0.6,
        dominance=-0.2
    )
    db_session.add(risk_assess)
    await db_session.commit()

    res = await db_session.execute(
        select(ConversationRiskAssessment).where(ConversationRiskAssessment.session_id == "session_abc_123")
    )
    fetched_risk = res.scalar_one_or_none()

    assert fetched_risk is not None
    assert fetched_risk.overall_risk_level == "low"
    assert fetched_risk.pleasure == -0.3


@pytest.mark.asyncio
async def test_screening_and_triage(db_session: AsyncSession):
    user = User(email="screening_user@example.com", name="User Screening")
    db_session.add(user)
    await db_session.commit()

    profile = UserScreeningProfile(
        user_id=user.id,
        profile_data={"phq9": 6, "gad7": 4, "dass21": 8},
        overall_risk="low",
        requires_attention=False,
        total_messages_analyzed=15
    )
    triage = TriageAssessment(
        user_id=user.id,
        risk_score=0.25,
        confidence_score=0.92,
        severity_level="low",
        risk_factors=["academic_stress"],
        recommended_action="suggest_cbt_workbook",
        processing_time_ms=120
    )
    db_session.add_all([profile, triage])
    await db_session.commit()

    res_p = await db_session.execute(select(UserScreeningProfile).where(UserScreeningProfile.user_id == user.id))
    fetched_p = res_p.scalar_one_or_none()

    assert fetched_p is not None
    assert fetched_p.profile_data["phq9"] == 6


@pytest.mark.asyncio
async def test_quest_and_attestation(db_session: AsyncSession):
    user = User(email="quest_user@example.com", name="User Quest")
    template = QuestTemplate(
        code="TEST_QUEST_01",
        name="Test Quest",
        short_description="Deskripsi quest test",
        category="wellness",
        base_xp=10,
        base_joy=5
    )
    db_session.add_all([user, template])
    await db_session.commit()

    instance = QuestInstance(
        user_id=user.id,
        template_id=template.id,
        status="completed",
        completed_at=datetime.now()
    )
    db_session.add(instance)
    await db_session.commit()

    attestation = AttestationRecord(
        quest_instance_id=instance.id,
        hashed_payload="0xabcd1234efgh5678",
        tx_hash="0x9999888877776666555544443333222211110000",
        status="confirmed"
    )
    db_session.add(attestation)
    await db_session.commit()

    res_a = await db_session.execute(select(AttestationRecord).where(AttestationRecord.quest_instance_id == instance.id))
    fetched_a = res_a.scalar_one_or_none()

    assert fetched_a is not None
    assert fetched_a.status == "confirmed"
    assert fetched_a.hashed_payload == "0xabcd1234efgh5678"


@pytest.mark.asyncio
async def test_autopilot_action_and_journal(db_session: AsyncSession):
    user = User(email="autopilot_user@example.com", name="User Autopilot")
    db_session.add(user)
    await db_session.commit()

    action = AutopilotAction(
        action_type=AutopilotActionType.grant_badge_nft,
        risk_level="low",
        policy_decision=AutopilotPolicyDecision.auto_approved,
        status=AutopilotActionStatus.queued,
        idempotency_key="idempotency_key_001",
        payload_hash="hash_001",
        payload_json={"badge_id": 1, "recipient": "0x123"}
    )
    journal = JournalEntry(
        user_id=user.id,
        entry_date=date.today(),
        content="Hari ini saya merasa lebih tenang setelah bermeditasi.",
        mood=4,
        word_count=10,
        valence=0.8,
        arousal=0.3,
        inferred_dominance=0.7
    )
    db_session.add_all([action, journal])
    await db_session.commit()

    res_act = await db_session.execute(select(AutopilotAction).where(AutopilotAction.idempotency_key == "idempotency_key_001"))
    fetched_act = res_act.scalar_one_or_none()

    assert fetched_act is not None
    assert fetched_act.action_type == AutopilotActionType.grant_badge_nft
    assert fetched_act.policy_decision == AutopilotPolicyDecision.auto_approved

    res_j = await db_session.execute(select(JournalEntry).where(JournalEntry.user_id == user.id))
    fetched_j = res_j.scalar_one_or_none()

    assert fetched_j is not None
    assert fetched_j.word_count == 10
    assert fetched_j.valence == 0.8
