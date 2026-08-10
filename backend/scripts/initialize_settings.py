import asyncio
import os
import sys
from datetime import datetime

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import AsyncSessionLocal
from app.services.system_settings import settings_service

async def seed_settings():
    print("🌱 Seeding initial system settings...")
    
    # Define initial settings by category
    initial_settings = {
        "appearance": {
            "theme_mode": "Dark",
            "accent_colour": "#FFCA40",
            "density": "Comfortable"
        },
        "collaboration": {
            "review_mode": True,
            "notes_visibility": "Counsellors",
            "escalation_playbook": "Standard Playbook v1.0"
        },
        "notifications": {
            "weekly_digest": True,
            "queue_alerts": "Email",
            "incident_webhook": ""
        }
    }

    async with AsyncSessionLocal() as db:
        for category, settings in initial_settings.items():
            print(f"  - Initializing {category} settings...")
            success = await settings_service.update_settings(db, category, settings)
            if success:
                print(f"    ✅ Done.")
            else:
                print(f"    ❌ Failed.")

    print("✨ Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_settings())
