import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from app.models.system import SystemSettings
from app.models.user import User

logger = logging.getLogger(__name__)

class SystemSettingsService:
    """Service for managing system-wide configuration settings using DB persistence."""
    
    async def get_all_settings(self, db: AsyncSession) -> List[SystemSettings]:
        """Fetch all system settings from the database."""
        result = await db.execute(select(SystemSettings))
        return list(result.scalars().all())

    async def get_settings_by_category(self, db: AsyncSession, category: str) -> Dict[str, Any]:
        """Fetch all settings for a specific category into a dictionary."""
        result = await db.execute(
            select(SystemSettings).where(SystemSettings.category == category)
        )
        settings = result.scalars().all()
        return {s.key: s.value for s in settings}

    async def get_setting(self, db: AsyncSession, key: str, default: Any = None) -> Any:
        """Fetch a single setting by key."""
        result = await db.execute(
            select(SystemSettings).where(SystemSettings.key == key)
        )
        setting = result.scalar_one_or_none()
        return setting.value if setting else default

    async def update_settings(
        self, 
        db: AsyncSession, 
        category: str, 
        settings: Dict[str, Any],
        user_id: Optional[int] = None
    ) -> bool:
        """Bulk update settings for a category, creating them if they don't exist."""
        try:
            for key, value in settings.items():
                stmt = insert(SystemSettings).values(
                    key=key,
                    value=value,
                    category=category,
                    updated_by=user_id,
                    updated_at=datetime.utcnow()
                ).on_conflict_do_update(
                    index_elements=['key'],
                    set_={
                        'value': value,
                        'updated_by': user_id,
                        'updated_at': datetime.utcnow()
                    }
                )
                await db.execute(stmt)
            
            await db.commit()
            logger.info(f"Updated settings for category '{category}': {list(settings.keys())}")
            return True
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating settings for category '{category}': {e}")
            return False

    async def validate_settings(self, category: str, settings: Dict[str, Any]) -> Dict[str, str]:
        """Validate settings before saving."""
        errors = {}
        
        if category == "appearance":
            if "accent_colour" in settings:
                color = settings["accent_colour"]
                if not isinstance(color, str) or not color.startswith("#") or len(color) != 7:
                    errors["accent_colour"] = "Must be a valid hex color code (e.g., #FFCA40)"
        
        elif category == "collaboration":
            if "review_timeout_hours" in settings:
                timeout = settings["review_timeout_hours"]
                try:
                    t = int(timeout)
                    if t < 1 or t > 168:
                        errors["review_timeout_hours"] = "Must be between 1 and 168 hours"
                except (ValueError, TypeError):
                    errors["review_timeout_hours"] = "Must be a valid integer"
        
        elif category == "notifications":
            if "incident_webhook" in settings and settings["incident_webhook"]:
                url = settings["incident_webhook"]
                if url != "settings not yet implemented" and not url.startswith(("http://", "https://")):
                    errors["incident_webhook"] = "Must be a valid HTTP/HTTPS URL"
        
        return errors

    async def export_settings(self, db: AsyncSession) -> Dict[str, Any]:
        """Export all settings for backup."""
        settings = await self.get_all_settings(db)
        data = {}
        for s in settings:
            if s.category not in data:
                data[s.category] = {}
            data[s.category][s.key] = s.value
        
        data["exported_at"] = datetime.utcnow().isoformat()
        data["version"] = "1.0"
        return data

    async def import_settings(
        self, 
        db: AsyncSession, 
        settings_data: Dict[str, Any],
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Import settings from backup."""
        results = {"success": [], "errors": []}
        
        for category, settings in settings_data.items():
            if category in ["exported_at", "version"]:
                continue
            if isinstance(settings, dict):
                if await self.update_settings(db, category, settings, user_id):
                    results["success"].append(category)
                else:
                    results["errors"].append(category)
                    
        return results

# Global instance
settings_service = SystemSettingsService()