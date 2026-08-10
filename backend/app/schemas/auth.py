from typing import Optional
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    wallet_address: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class UserProfileResponse(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    role: str
    wallet_address: Optional[str] = None
    current_streak: int
    longest_streak: int
    consent_ai_memory: bool
    consent_data_sharing: bool

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfileResponse
