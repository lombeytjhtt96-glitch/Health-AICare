"""
Script untuk membuat test accounts: 5 users, 5 counselors, dan 1 admin.
Menggunakan raw SQL agar tidak terpengaruh schema drift.

Jalankan dari folder backend/ dengan:
  C:\\Python314\\python.exe create_test_accounts.py
"""
import asyncio
import sys
import os
import uuid
import urllib.parse as _urlparse
from datetime import datetime

sys.path.insert(0, str(__file__).rsplit("\\", 1)[0])

from passlib.context import CryptContext  # type: ignore
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# ── Config ────────────────────────────────────────────────────────────────────
_raw_url = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./health_ai.db")

_use_ssl = False
if _raw_url.startswith(("postgresql://", "postgres://", "postgresql+asyncpg://", "postgres+asyncpg://")):
    _parsed = _urlparse.urlparse(_raw_url)
    _qs = _urlparse.parse_qs(_parsed.query, keep_blank_values=True)
    if "sslmode" in _qs:
        _use_ssl = True
        _qs.pop("sslmode", None)
    _qs.pop("channel_binding", None)
    _new_query = _urlparse.urlencode({k: v[0] for k, v in _qs.items()})
    _clean = _parsed._replace(query=_new_query).geturl()
    _clean = _clean.replace("postgresql://", "postgresql+asyncpg://", 1)
    _clean = _clean.replace("postgres://", "postgresql+asyncpg://", 1)
    DATABASE_URL = _clean
else:
    DATABASE_URL = _raw_url

_ENGINE_KWARGS: dict = {}
if _use_ssl:
    import ssl as _ssl
    _ctx = _ssl.create_default_context()
    _ctx.check_hostname = False
    _ctx.verify_mode = _ssl.CERT_NONE
    _ENGINE_KWARGS["connect_args"] = {"ssl": _ctx}

# ── Account definitions ───────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCOUNTS = [
    {"email": "usertesthealthaicare001@gmailhealthaicare.com", "name": "User Test 001", "role": "user",     "password": "Usertesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "usertesthealthaicare002@gmailhealthaicare.com", "name": "User Test 002", "role": "user",     "password": "Usertesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "usertesthealthaicare003@gmailhealthaicare.com", "name": "User Test 003", "role": "user",     "password": "Usertesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "usertesthealthaicare004@gmailhealthaicare.com", "name": "User Test 004", "role": "user",     "password": "Usertesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "usertesthealthaicare005@gmailhealthaicare.com", "name": "User Test 005", "role": "user",     "password": "Usertesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "counselortesthealthaicare001@gmailhealthaicare.com", "name": "Counselor Test 001", "role": "counselor", "password": "Counselortesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "counselortesthealthaicare002@gmailhealthaicare.com", "name": "Counselor Test 002", "role": "counselor", "password": "Counselortesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "counselortesthealthaicare003@gmailhealthaicare.com", "name": "Counselor Test 003", "role": "counselor", "password": "Counselortesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "counselortesthealthaicare004@gmailhealthaicare.com", "name": "Counselor Test 004", "role": "counselor", "password": "Counselortesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "counselortesthealthaicare005@gmailhealthaicare.com", "name": "Counselor Test 005", "role": "counselor", "password": "Counselortesthealthaicare001-005&@gmailhealthaicare.com"},
    {"email": "administratorhealthaicare_khalaf-dev@gmail_administratorhealth-aicare.com", "name": "Administrator Khalaf Dev", "role": "admin", "password": "AdminKhalafDev2026!@#"},
]


async def upsert_account(conn, account: dict) -> None:
    email = account["email"]
    pw_hash = pwd_context.hash(account["password"])
    now = datetime.utcnow()
    checkin = uuid.uuid4().hex

    # Check if user exists
    res = await conn.execute(
        text("SELECT id FROM users WHERE email = :email"),
        {"email": email}
    )
    row = res.fetchone()

    if row:
        user_id = row[0]
        await conn.execute(
            text("""
                UPDATE users SET
                    password_hash = :pw,
                    role = :role,
                    is_active = true,
                    email_verified = true,
                    updated_at = :now
                WHERE id = :uid
            """),
            {"pw": pw_hash, "role": account["role"], "now": now, "uid": user_id}
        )
        print(f"  [UPDATED] {email} ({account['role']})")
    else:
        # Insert new user — include all NOT NULL columns that have no DB default
        res2 = await conn.execute(
            text("""
                INSERT INTO users (
                    email, name, password_hash, role,
                    is_active, email_verified,
                    created_at, updated_at, check_in_code,
                    sentiment_score,
                    current_streak, longest_streak,
                    allow_email_checkins,
                    consent_data_sharing, consent_research,
                    consent_emergency_contact, consent_marketing
                )
                VALUES (
                    :email, :name, :pw, :role,
                    true, true,
                    :now, :now, :code,
                    0.0,
                    0, 0,
                    true,
                    false, false,
                    false, false
                )
                RETURNING id
            """),
            {
                "email": email,
                "name": account["name"],
                "pw": pw_hash,
                "role": account["role"],
                "now": now,
                "code": checkin,
            }
        )
        user_id = res2.fetchone()[0]


        # Create user_profile row (best-effort)
        try:
            parts = account["name"].split(" ", 1)
            fname = parts[0]
            lname = parts[1] if len(parts) > 1 else ""
            await conn.execute(
                text("""
                    INSERT INTO user_profiles (user_id, first_name, last_name, country)
                    VALUES (:uid, :fn, :ln, 'Indonesia')
                    ON CONFLICT (user_id) DO NOTHING
                """),
                {"uid": user_id, "fn": fname, "ln": lname}
            )
        except Exception as e:
            print(f"    [WARN] profile for {email}: {e}")

        print(f"  [CREATED] {email} ({account['role']})")


async def main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=False, **_ENGINE_KWARGS)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    print("\n=== Creating HealthAICare Test Accounts ===\n")
    print(f"DB: {DATABASE_URL[:50]}...\n")

    async with async_session() as session:
        async with session.begin():
            conn = await session.connection()
            for account in ACCOUNTS:
                try:
                    await upsert_account(conn, account)
                except Exception as e:
                    print(f"  [ERROR] {account['email']}: {e}")

    await engine.dispose()

    print("\n=== Summary ===")
    print("Users (5):      usertesthealthaicare001-005@gmailhealthaicare.com")
    print("                pw: Usertesthealthaicare001-005&@gmailhealthaicare.com")
    print("Counselors (5): counselortesthealthaicare001-005@gmailhealthaicare.com")
    print("                pw: Counselortesthealthaicare001-005&@gmailhealthaicare.com")
    print("Admin (1):      administratorhealthaicare_khalaf-dev@gmail_administratorhealth-aicare.com")
    print("                pw: AdminKhalafDev2026!@#")
    print("\nDone.\n")


if __name__ == "__main__":
    asyncio.run(main())
