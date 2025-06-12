from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..services.booking_service import BookingService
from ..services.room_service import RoomService
from ..services.email_service import EmailService
from ..models.booking import CustomerBookingCreate
from ..models.room import RoomResponse

router = APIRouter(prefix="/customer", tags=["customer"])
booking_service = BookingService()
room_service = RoomService()
email_service = EmailService()

@router.get("/rooms/available", response_model=List[dict])
def get_available_rooms_for_customers():
    """Get available rooms with full details for customer booking"""
    available_rooms = room_service.get_available_rooms()
    
    # Add customer-friendly descriptions
    enhanced_rooms = []
    for room in available_rooms:
        room_response = RoomResponse.from_db(room)
        enhanced_rooms.append(room_response.dict())
    
    return enhanced_rooms

@router.get("/rooms/availability")
def check_rooms_availability(check_in: str = Query(...), check_out: str = Query(...)):
    """Check which rooms are available for specific date range"""
    try:
        return booking_service.check_room_availability(check_in, check_out)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/book", response_model=dict)
def create_customer_booking(booking_data: CustomerBookingCreate):
    """Create a booking from customer interface"""
    try:
        new_booking = booking_service.create_customer_booking(booking_data)
        
        # Send confirmation email if email service is available
        if email_service.is_configured():
            try:
                guest_data = {
                    "first_name": booking_data.first_name,
                    "last_name": booking_data.last_name,
                    "email": booking_data.email
                }
                
                email_booking_data = {
                    "confirmation_number": new_booking['confirmation_number'],
                    "room_number": new_booking['room_number'],
                    "room_type": new_booking['room_type'],
                    "check_in_date": booking_data.check_in_date,
                    "check_out_date": booking_data.check_out_date,
                    "total_price": booking_data.total_price
                }
                
                # Send customer confirmation email
                customer_email_sent = email_service.send_booking_confirmation(email_booking_data, guest_data)
                
                # Send admin notification email
                admin_email_sent = email_service.send_admin_booking_notification(email_booking_data, guest_data)
                
            except Exception as e:
                print(f"❌ Email sending error: {e}")
        
        return {
            "message": "Booking created successfully!",
            "booking": new_booking,
            "booking_id": new_booking['id'],
            "confirmation_number": new_booking['confirmation_number'],
            "email_sent": email_service.is_configured()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bookings/{email}", response_model=List[dict])
def get_customer_bookings(email: str):
    """Get all bookings for a customer by email"""
    return booking_service.get_bookings_by_email(email)

@router.delete("/booking/{booking_id}", response_model=dict)
def cancel_customer_booking(booking_id: int, customer_email: str = Query(...)):
    """Cancel a customer booking (with email verification)"""
    cancelled_booking = booking_service.cancel_customer_booking(booking_id, customer_email)
    
    if not cancelled_booking:
        raise HTTPException(
            status_code=404, 
            detail="Booking not found or you don't have permission to cancel it"
        )
    
    confirmation_number = f"BK{booking_id:06d}"
    
    # Send cancellation confirmation email if email service is available
    if email_service.is_configured():
        try:
            # Extract guest data from booking
            guest_name_parts = cancelled_booking['guest_name'].split(' ', 1)
            guest_data = {
                "first_name": guest_name_parts[0] if guest_name_parts else "Guest",
                "last_name": guest_name_parts[1] if len(guest_name_parts) > 1 else "",
                "email": customer_email
            }
            
            email_booking_data = {
                "confirmation_number": confirmation_number,
                "room_number": cancelled_booking['room_number'],
                "room_type": cancelled_booking['room_type'],
                "check_in_date": cancelled_booking['check_in_date'],
                "check_out_date": cancelled_booking['check_out_date'],
                "total_price": cancelled_booking['total_price']
            }
            
            # Send customer cancellation email
            customer_email_sent = email_service.send_cancellation_confirmation(email_booking_data, guest_data)
            
            # Send admin cancellation notification
            admin_email_sent = email_service.send_admin_cancellation_notification(email_booking_data, guest_data)
            
        except Exception as e:
            print(f"❌ Email sending error: {e}")
    
    return {
        "message": "Booking cancelled successfully",
        "booking": cancelled_booking,
        "confirmation_number": confirmation_number,
        "email_sent": email_service.is_configured()
    } 