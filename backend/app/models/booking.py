from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    """Base booking model with common attributes"""
    guest_id: int
    room_id: int
    check_in_date: str  # ISO format string
    check_out_date: str  # ISO format string
    total_price: float

class BookingCreate(BookingBase):
    """Model for creating a new booking"""
    pass

class BookingUpdate(BaseModel):
    """Model for updating an existing booking"""
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    total_price: Optional[float] = None
    status: Optional[str] = None

class BookingInDB(BookingBase):
    """Model for booking as stored in database"""
    id: int
    status: str = "confirmed"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BookingResponse(BookingInDB):
    """Model for booking response with additional fields"""
    guest_name: Optional[str] = None
    guest_email: Optional[str] = None
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    confirmation_number: Optional[str] = None

    @classmethod
    def from_db(cls, db_booking: dict) -> 'BookingResponse':
        """Create a response model from database booking"""
        response = cls(**db_booking)
        response.confirmation_number = f"BK{db_booking['id']:06d}"
        return response

class CustomerBookingCreate(BaseModel):
    """Model for customer booking creation"""
    room_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    check_in_date: str
    check_out_date: str
    total_price: float
    notes: Optional[str] = None 