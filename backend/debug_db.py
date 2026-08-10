import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.domains.mental_health.models import Psychologist
import os
from dotenv import load_dotenv

# Load env from parent dir
load_dotenv("../.env")

async def check_data():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found")
        return
    
    engine = create_async_engine(database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        result = await session.execute(select(Psychologist).limit(5))
        psychologists = result.scalars().all()
        for p in psychologists:
            print(f"ID: {p.id}, UserID: {p.user_id}")
            print(f"  Languages: {p.languages} (Type: {type(p.languages)})")
            print(f"  Education: {p.education} (Type: {type(p.education)})")
            print(f"  Availability: {p.availability_schedule} (Type: {type(p.availability_schedule)})")
            print("-" * 20)

if __name__ == "__main__":
    asyncio.run(check_data())
