import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.core.db import get_db
from app.database import get_async_db


from app.dependencies import get_token_from_request, get_current_active_user, get_admin_user
from app.models.user import User


def _apply_db_override(db_session: AsyncSession):
    async def _override():
        yield db_session

    async def _admin_override():
        return User(id=99, email="admin@example.com", role="admin", name="Admin Test", is_active=True)

    app.dependency_overrides[get_db] = _override
    app.dependency_overrides[get_async_db] = _override
    app.dependency_overrides[get_token_from_request] = lambda: "dummy_token"
    app.dependency_overrides[get_current_active_user] = _admin_override
    app.dependency_overrides[get_admin_user] = _admin_override


@pytest.mark.asyncio
async def test_healthz_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/healthz")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_auth_endpoints(db_session: AsyncSession):
    _apply_db_override(db_session)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            signup_res = await ac.post(
                "/api/v1/auth/signup",
                json={"email": "new_user@example.com", "password": "securepassword123", "name": "User General"}
            )
            assert signup_res.status_code in (200, 201)
            data_signup = signup_res.json()
            assert "user_id" in data_signup

            login_res = await ac.post(
                "/api/v1/auth/login",
                json={"email": "new_user@example.com", "password": "securepassword123"}
            )
            assert login_res.status_code == 200
            assert "access_token" in login_res.json()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_chat_and_history_endpoints(db_session: AsyncSession):
    _apply_db_override(db_session)
    from app.models.user import User
    user = User(id=1, email="chat_test_user@example.com", role="user")
    db_session.add(user)
    await db_session.commit()
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            msg_res = await ac.post(
                "/api/v1/chat/message",
                json={
                    "message": "Saya merasa sedikit lelah dan butuh seseorang untuk bercerita.",
                    "session_id": "session_test_api_001",
                    "user_id": 1,
                    "user_role": "user"
                }
            )
            assert msg_res.status_code == 200, f"msg_res failed with status {msg_res.status_code}: {msg_res.text}"
            msg_data = msg_res.json()
            assert "response" in msg_data
            assert msg_data["session_id"] == "session_test_api_001"

            hist_res = await ac.get("/api/v1/chat/history/session_test_api_001")
            assert hist_res.status_code == 200, f"hist_res failed with status {hist_res.status_code}: {hist_res.text}"
            hist_data = hist_res.json()
            assert len(hist_data["history"]) >= 1
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_journal_endpoints(db_session: AsyncSession):
    _apply_db_override(db_session)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            create_res = await ac.post(
                "/api/v1/journal",
                json={
                    "user_id": 1,
                    "content": "Hari ini berjalan dengan sangat baik dan saya merasa lega serta bersyukur.",
                    "mood": 5
                }
            )
            assert create_res.status_code == 201
            j_data = create_res.json()
            assert j_data["word_count"] > 0
            assert j_data["valence"] > 0

            list_res = await ac.get("/api/v1/journal/1")
            assert list_res.status_code == 200
            assert len(list_res.json()) >= 1
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_quests_and_complete(db_session: AsyncSession):
    _apply_db_override(db_session)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            quests_res = await ac.get("/api/v1/quests/1")
            assert quests_res.status_code == 200
            quests_data = quests_res.json()
            assert len(quests_data) >= 1

            active_inst_id = quests_data[0]["id"]
            complete_res = await ac.post(
                "/api/v1/quests/complete",
                json={"user_id": 1, "quest_instance_id": active_inst_id}
            )
            assert complete_res.status_code == 200
            comp_data = complete_res.json()
            assert comp_data["status"] == "success"
            assert comp_data["xp_gained"] > 0
    finally:
        app.dependency_overrides.clear()





@pytest.mark.asyncio
async def test_counselor_and_admin_autopilot(db_session: AsyncSession):
    _apply_db_override(db_session)
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            cases_res = await ac.get("/api/v1/counselor/cases")
            assert cases_res.status_code == 200, f"cases_res failed with status {cases_res.status_code}: {cases_res.text}"
            cases_data = cases_res.json()
            assert isinstance(cases_data, (list, dict))

            queue_res = await ac.get("/api/v1/admin/autopilot/queue")
            assert queue_res.status_code == 200, f"queue_res failed with status {queue_res.status_code}: {queue_res.text}"
            queue_data = queue_res.json()
            assert isinstance(queue_data, (list, dict))
    finally:
        app.dependency_overrides.clear()

