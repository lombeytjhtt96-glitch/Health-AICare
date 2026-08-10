import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.main import app
from app.core.db import get_db
from app.database import get_async_db
from app.models import User, AutopilotAction, AttestationRecord


@pytest.mark.asyncio
async def test_carequest_game_completion_flow(db_session: AsyncSession):
    async def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    app.dependency_overrides[get_async_db] = _override

    try:
        # Seed test user
        user_test = User(id=1, email="gamer@example.com", name="Gamer Test", current_streak=0, longest_streak=0)
        db_session.add(user_test)
        await db_session.commit()

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            # 1. Query user quests to get active QuestInstance
            quests_res = await ac.get("/api/v1/quests/1")
            assert quests_res.status_code == 200
            quests_data = quests_res.json()
            assert len(quests_data) >= 1

            target_instance_id = quests_data[0]["id"]

            # 2. Complete CareQuest typing game
            complete_res = await ac.post(
                "/api/v1/quests/complete",
                json={"user_id": 1, "quest_instance_id": target_instance_id}
            )
            assert complete_res.status_code == 200
            comp_data = complete_res.json()
            assert comp_data["status"] == "success"
            assert comp_data["xp_gained"] > 0
            assert comp_data["attestation_queued"] is True

            # 3. Verify user streak updated in DB
            stmt_user = select(User).where(User.id == 1)
            res_u = await db_session.execute(stmt_user)
            user = res_u.scalar_one_or_none()
            assert user is not None
            assert user.current_streak >= 1

            # 4. Verify Autopilot Action created and confirmed
            stmt_act = select(AutopilotAction).where(AutopilotAction.idempotency_key == f"quest_complete_{target_instance_id}")
            res_act = await db_session.execute(stmt_act)
            action = res_act.scalar_one_or_none()
            assert action is not None
            assert action.status.value in ("confirmed", "queued")

            # 5. Verify Attestation Record created
            stmt_att = select(AttestationRecord).where(AttestationRecord.quest_instance_id == target_instance_id)
            res_att = await db_session.execute(stmt_att)
            attestation = res_att.scalar_one_or_none()
            assert attestation is not None
            assert attestation.status == "confirmed"
    finally:
        app.dependency_overrides.clear()
