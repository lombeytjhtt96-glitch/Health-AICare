
import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.user import User
from app.domains.mental_health.models.appointments import Psychologist

async def check():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        print("Users:")
        for u in users:
            print(f"ID: {u.id}, Email: {u.email}, Role: {u.role}")
        
        result = await db.execute(select(Psychologist))
        psychs = result.scalars().all()
        print("\nPsychologists:")
        for p in psychs:
            print(f"ID: {p.id}, User ID: {p.user_id}, Name: {p.name}")

if __name__ == "__main__":
    asyncio.run(check())
