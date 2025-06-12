from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class GuestBase(BaseModel):
    """Base guest model with common attributes"""
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class GuestCreate(GuestBase):
    """Model for creating a new guest"""
    pass

class GuestUpdate(GuestBase):
    """Model for updating an existing guest"""
    pass

class GuestInDB(GuestBase):
    """Model for guest as stored in database"""
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class GuestResponse(GuestInDB):
    """Model for guest response"""
    full_name: Optional[str] = None

    @classmethod
    def from_db(cls, db_guest: dict) -> 'GuestResponse':
        """Create a response model from database guest"""
        response = cls(**db_guest)
        response.full_name = f"{db_guest['first_name']} {db_guest['last_name']}"
        return response 