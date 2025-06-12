"""
Booking management routes for the Grand Hotel Management System
"""
from fastapi import APIRouter, HTTPException
from typing import List
from ..services.booking_service import BookingService
from ..models.booking import BookingCreate

router = APIRouter(prefix="/bookings", tags=["bookings"])
booking_service = BookingService()

@router.get("/", response_model=List[dict])
def get_bookings():
    """Get all bookings"""
    return booking_service.get_all_bookings()

@router.post("/", response_model=dict)
def create_booking(booking_data: BookingCreate):
    """Create a new booking"""
    try:
        new_booking = booking_service.create_booking(booking_data)
        return {
            "message": "Booking created successfully",
            "booking": new_booking
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{booking_id}", response_model=dict)
def cancel_booking(booking_id: int):
    """Cancel a booking"""
    cancelled_booking = booking_service.cancel_booking(booking_id)
    if not cancelled_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": f"Cancelled booking for {cancelled_booking['guest_name']}"} 