import asyncio
import sys
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import get_async_db, AsyncSessionLocal
from app.models.user import User
from app.domains.mental_health.models import Psychologist as CounselorProfile
from app.schemas.counselor import CounselorCreate, CounselorUpdate

async def test_counselor_lifecycle():
    print("🚀 Starting Counselor Lifecycle Test...")
    
    async with AsyncSessionLocal() as db:
        # 1. Find a test user (ideally with role 'counselor')
        result = await db.execute(select(User).where(User.role == 'counselor').limit(1))
        test_user = result.scalar_one_or_none()
        
        if not test_user:
            print("❌ No counselor user found for testing. Please ensure at least one user has the 'counselor' role.")
            return

        print(f"✅ Using test user: {test_user.email} (ID: {test_user.id})")

        # 2. Ensure no existing profile (cleanup)
        existing = await db.execute(select(CounselorProfile).where(CounselorProfile.user_id == test_user.id))
        existing_profile = existing.scalar_one_or_none()
        if existing_profile:
            print(f"🧹 Removing existing profile for user {test_user.id}")
            await db.delete(existing_profile)
            await db.commit()

        # 3. Create a profile
        print("📝 Creating new counselor profile...")
        new_profile = CounselorProfile(
            user_id=test_user.id,
            name="Test Counselor",
            specialization="Testing",
            is_available=True,
            bio="Initial bio text"
        )
        db.add(new_profile)
        await db.commit()
        await db.refresh(new_profile)
        profile_id = new_profile.id
        print(f"✅ Created profile with ID: {profile_id}")

        # 4. Update the bio and schedule
        print("🆙 Updating profile bio and schedule...")
        new_bio = "This is a detailed professional bio with specific expertise in testing."
        new_schedule = [
            {"day": "Monday", "start_time": "09:00:00", "end_time": "12:00:00", "is_available": True},
            {"day": "Wednesday", "start_time": "14:00:00", "end_time": "17:00:00", "is_available": True}
        ]
        
        # Use the update endpoint logic simulation
        new_profile.bio = new_bio
        new_profile.availability_schedule = new_schedule
        await db.commit()
        await db.refresh(new_profile)

        # 5. Verify persistence
        print("🔍 Verifying bio and schedule persistence...")
        # Start a fresh context to avoid session cache
        async with AsyncSessionLocal() as db_verify:
            result = await db_verify.execute(select(CounselorProfile).where(CounselorProfile.id == profile_id))
            p = result.scalar_one_or_none()
            
            bio_ok = p and p.bio == new_bio
            schedule_ok = p and p.availability_schedule == new_schedule
            
            if bio_ok:
                print("✅ SUCCESS: Bio persisted correctly!")
            else:
                print(f"❌ FAILURE: Bio did not persist. Expected: '{new_bio}', Found: '{p.bio if p else 'None'}'")
            
            if schedule_ok:
                print("✅ SUCCESS: Schedule persisted correctly!")
            else:
                print(f"❌ FAILURE: Schedule did not persist. Found: {p.availability_schedule if p else 'None'}")

        # 6. Test clearing the schedule
        print("🧹 Testing clearing the schedule...")
        new_profile.availability_schedule = []
        await db.commit()
        await db.refresh(new_profile)
        
        async with AsyncSessionLocal() as db_clear:
            result = await db_clear.execute(select(CounselorProfile).where(CounselorProfile.id == profile_id))
            p = result.scalar_one_or_none()
            if p and p.availability_schedule == []:
                print("✅ SUCCESS: Schedule cleared correctly!")
            else:
                print(f"❌ FAILURE: Schedule not cleared. Found: {p.availability_schedule if p else 'None'}")

        # 7. Verify Deletion
        print("🗑️ Testing deletion...")
        async with AsyncSessionLocal() as db_del:
            result = await db_del.execute(select(CounselorProfile).where(CounselorProfile.id == profile_id))
            p = result.scalar_one_or_none()
            if p:
                await db_del.delete(p)
                await db_del.commit()
                print("✅ Profile deleted.")
            
            # Verify it's gone
            result = await db_del.execute(select(CounselorProfile).where(CounselorProfile.id == profile_id))
            p = result.scalar_one_or_none()
            if not p:
                print("✅ SUCCESS: Profile is truly gone.")
            else:
                print("❌ FAILURE: Profile still exists after deletion.")


if __name__ == "__main__":
    asyncio.run(test_counselor_lifecycle())
