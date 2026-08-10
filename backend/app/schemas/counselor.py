"""Counselor profile schemas for admin and counselor management."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


# ========================================
# Extended Profile Schemas
# ========================================

class EducationItem(BaseModel):
    """Single education entry."""
    degree: str
    institution: str
    year: Optional[int] = None
    field_of_study: Optional[str] = None

class CertificationItem(BaseModel):
    """Single certification entry."""
    name: str
    issuing_organization: str
    year: Optional[int] = None
    expiry_date: Optional[str] = None

class AvailabilitySlot(BaseModel):
    """Time slot for availability."""
    day: str  # monday, tuesday, etc.
    start_time: str  # "09:00"
    end_time: str  # "17:00"
    is_available: bool = True


# ========================================
# Base Counselor Schemas
# ========================================

class CounselorBase(BaseModel):
    """Base schema for Counselor data."""
    name: str = Field(..., min_length=1, max_length=255)
    specialization: Optional[List[str]] = Field(default_factory=list)
    image_url: Optional[str] = None
    is_available: bool = True
    bio: Optional[str] = None
    years_of_experience: Optional[int] = Field(None, ge=0, le=70)
    languages: Optional[Any] = Field(default_factory=list)
    consultation_fee: Optional[float] = Field(None, ge=0)
    
    @field_validator('languages', 'specialization', mode='before')
    @classmethod
    def validate_list_fields(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [s.strip() for s in v.split(',') if s.strip()]
        return v


class CounselorCreate(CounselorBase):
    """Schema for creating a Counselor profile (admin only)."""
    user_id: int = Field(..., description="User ID to link Counselor profile to")
    education: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    certifications: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    availability_schedule: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class CounselorUpdate(BaseModel):
    """Schema for updating Counselor profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    specialization: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    bio: Optional[str] = None
    years_of_experience: Optional[int] = Field(None, ge=0, le=70)
    languages: Optional[List[str]] = None
    consultation_fee: Optional[float] = Field(None, ge=0)
    license_number: Optional[str] = None
    phone: Optional[str] = None
    years_experience: Optional[int] = Field(None, ge=0, le=70)
    education: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    availability_schedule: Optional[List[Dict[str, Any]]] = None


class CounselorAvailabilityToggle(BaseModel):
    """Schema for toggling Counselor availability."""
    is_available: bool


# ========================================
# Response Schemas
# ========================================

class UserBasicInfo(BaseModel):
    """Basic user information for Counselor response."""
    id: int
    email: str
    name: Optional[str] = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class CounselorResponse(CounselorBase):
    """Complete Counselor profile response."""
    id: int
    user_id: Optional[int] = None
    email: Optional[str] = None # Surface from nested User
    rating: float = 0.0
    total_reviews: int = 0
    total_patients: int = 0
    total_sessions: int = 0
    joined_date: str = Field(default_factory=lambda: datetime.now().isoformat())
    years_experience: Optional[int] = None # Alias for frontend
    license_number: Optional[str] = None
    education: Optional[Any] = Field(default_factory=list)
    certifications: Optional[Any] = Field(default_factory=list)
    availability: Optional[Dict[str, List[str]]] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
    user: Optional[UserBasicInfo] = None

    @model_validator(mode='before')
    @classmethod
    def transform_fields(cls, data: Any) -> Any:
        # 1. SPECIALIZATION Handling
        spec = None
        if isinstance(data, dict):
            spec = data.get('specialization')
        else:
            spec = getattr(data, 'specialization', None)
        
        target_spec = []
        if isinstance(spec, list):
            target_spec = spec
        elif isinstance(spec, str):
            target_spec = [s.strip() for s in spec.split(',') if s.strip()]
        
        # 2. AVAILABILITY Handling
        avail_schedule = None
        if isinstance(data, dict):
            avail_schedule = data.get('availability_schedule') or data.get('availability')
        else:
            avail_schedule = getattr(data, 'availability_schedule', None) or getattr(data, 'availability', None)
        
        target_avail = {}
        if isinstance(avail_schedule, dict):
            target_avail = avail_schedule
        elif isinstance(avail_schedule, list):
            for item in avail_schedule:
                if isinstance(item, dict):
                    day = item.get("day", "unknown").lower()
                    start = item.get("start_time")
                    end = item.get("end_time")
                    is_avail = item.get("is_available", True)
                    
                    if is_avail and start and end:
                        if day not in target_avail:
                            target_avail[day] = []
                        target_avail[day].append(f"{start} - {end}")

        # Apply transformations
        if isinstance(data, dict):
            data['specialization'] = target_spec
            data['availability'] = target_avail
        else:
            # For ORM objects, we can't always set attributes directly if they aren't in the model
            # But Pydantic will read from this returned dict/object
            # It's safest to return a dict for Pydantic to consume if we are modifying it
            result = {}
            # Copy basic attributes from ORM object if it's an object
            for field_name in cls.model_fields:
                if field_name not in ['specialization', 'availability']:
                    result[field_name] = getattr(data, field_name, None)
            
            # Map specific ORM names if they differ
            if not result.get('years_of_experience'):
                result['years_of_experience'] = getattr(data, 'years_of_experience', 0)
            
            result['specialization'] = target_spec
            result['availability'] = target_avail
            
            # Ensure required fields have valid defaults if missing from ORM
            if result.get('total_patients') is None: result['total_patients'] = 0
            if result.get('total_sessions') is None: result['total_sessions'] = 0
            if result.get('rating') is None: result['rating'] = 0.0
            if result.get('total_reviews') is None: result['total_reviews'] = 0
            if result.get('joined_date') is None:
                created_at = result.get('created_at')
                result['joined_date'] = created_at.isoformat() if created_at else datetime.now().isoformat()
            
            # Frontend compatibility: years_experience vs years_of_experience
            yoe = getattr(data, 'years_of_experience', 0) or 0
            result['years_of_experience'] = yoe
            result['years_experience'] = yoe
            
            # Surface email from nested user object
            user = result.get('user')
            if user:
                if isinstance(user, dict):
                    result['email'] = user.get('email')
                else:
                    result['email'] = getattr(user, 'email', None)

            return result
            
        return data

    model_config = {
        "from_attributes": True
    }


class CounselorListItem(BaseModel):
    """Simplified Counselor info for list views."""
    id: int
    user_id: Optional[int] = None
    name: str
    specialization: Optional[List[str]] = Field(default_factory=list)
    image_url: Optional[str] = None
    is_available: bool
    years_of_experience: Optional[int] = None
    rating: float = 0.0
    total_reviews: int = 0
    consultation_fee: Optional[float] = None

    @field_validator('specialization', mode='before')
    @classmethod
    def validate_specialization(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return [s.strip() for s in v.split(',') if s.strip()]
        return v

    class Config:
        from_attributes = True


class CounselorListResponse(BaseModel):
    """Paginated list of counselors."""
    counselors: List[CounselorListItem]
    total: int
    page: int
    page_size: int
    total_pages: int


# ========================================
# Statistics Schemas
# ========================================

class CounselorStats(BaseModel):
    """Statistics for a Counselor."""
    total_appointments: int
    upcoming_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    total_patients: int
    average_rating: float
    total_reviews: int


class CounselorDashboardStats(BaseModel):
    """Dashboard statistics for counselor role."""
    profile_completion_percentage: float
    this_week_appointments: int
    upcoming_appointments: int
    total_revenue: float
    average_rating: float
    total_reviews: int
    total_patients: int
    total_completed_appointments: int

# ========================================
# Helper Schemas
# ========================================

class CounselorUser(BaseModel):
    """Schema for a user who can be assigned as a counselor."""
    id: int
    email: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CaseResponse(BaseModel):
    """Schema for case response in counselor workspace."""
    id: str
    created_at: datetime
    status: str
    severity: str
    assigned_to: Optional[str] = None
    user_hash: str
    summary_redacted: Optional[str] = None
    sla_breach_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClaimCaseRequest(BaseModel):
    """Schema for claiming a case in counselor workspace."""
    counselor_id: str

