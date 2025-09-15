from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProfileBase(BaseModel):
    """Base profile model with common attributes"""
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None
    profile_picture_url: Optional[str] = None

class ProfileCreate(ProfileBase):
    """Model for creating a new profile"""
    pass

class ProfileUpdate(BaseModel):
    """Model for updating an existing profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None
    profile_picture_url: Optional[str] = None

class ProfileInDB(ProfileBase):
    """Model for profile as stored in database"""
    id: int
    user_id: str  # Supabase user ID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProfileResponse(ProfileInDB):
    """Model for profile response"""
    pass
