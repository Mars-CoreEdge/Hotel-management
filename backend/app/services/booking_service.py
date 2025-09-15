from typing import List, Optional
from datetime import datetime
from ..database.database import Database
from ..models.booking import BookingCreate, BookingUpdate, CustomerBookingCreate
from ..services.guest_service import GuestService
from ..services.room_service import RoomService

class BookingService:
    def __init__(self):
        self.db = Database()
        self.guest_service = GuestService()
        self.room_service = RoomService()

    def get_all_bookings(self) -> List[dict]:
        """Get all bookings from the database"""
        return self.db.get_all_bookings()

    def create_booking(self, booking_data: BookingCreate) -> dict:
        """Create a new booking"""
        return self.db.create_booking_in_db(
            guest_id=booking_data.guest_id,
            room_id=booking_data.room_id,
            check_in_date=booking_data.check_in_date,
            check_out_date=booking_data.check_out_date,
            total_price=booking_data.total_price
        )

    def cancel_booking(self, booking_id: int) -> Optional[dict]:
        """Cancel a booking"""
        return self.db.delete_booking_from_db(booking_id)

    def get_booking_by_id(self, booking_id: int) -> Optional[dict]:
        """Get a booking by its ID"""
        bookings = self.db.get_all_bookings()
        return next((booking for booking in bookings if booking['id'] == booking_id), None)

    def get_bookings_by_email(self, email: str) -> List[dict]:
        """Get all bookings for a customer by email"""
        all_bookings = self.db.get_all_bookings()
        customer_bookings = [
            booking for booking in all_bookings 
            if booking.get('guest_email', '').lower() == email.lower()
        ]
        
        # Add confirmation numbers
        for booking in customer_bookings:
            booking['confirmation_number'] = f"BK{booking['id']:06d}"
        
        return customer_bookings

    def create_customer_booking(self, booking_data: CustomerBookingCreate) -> dict:
        """Create a booking from customer interface"""
        # Validate dates
        try:
            check_in_date = datetime.fromisoformat(booking_data.check_in_date)
            check_out_date = datetime.fromisoformat(booking_data.check_out_date)
            
            if check_in_date >= check_out_date:
                raise ValueError("Check-out date must be after check-in date")
            
            if check_in_date.date() < datetime.now().date():
                raise ValueError("Check-in date cannot be in the past")
                
        except ValueError as e:
            raise ValueError(f"Invalid date: {str(e)}")

        # Check room availability
        if not self._is_room_available(booking_data.room_id, booking_data.check_in_date, booking_data.check_out_date):
            raise ValueError("Room is not available for the selected dates")

        # Find or create guest
        guest_data = {
            'first_name': booking_data.first_name,
            'last_name': booking_data.last_name,
            'email': booking_data.email,
            'phone': booking_data.phone
        }
        guest = self.guest_service.find_or_create_guest(guest_data)

        # Create booking
        booking_create = BookingCreate(
            guest_id=guest['id'],
            room_id=booking_data.room_id,
            check_in_date=booking_data.check_in_date,
            check_out_date=booking_data.check_out_date,
            total_price=booking_data.total_price
        )
        
        new_booking = self.create_booking(booking_create)
        new_booking['confirmation_number'] = f"BK{new_booking['id']:06d}"
        
        return new_booking

    def cancel_customer_booking(self, booking_id: int, customer_email: str) -> Optional[dict]:
        """Cancel a customer booking with email verification"""
        # Verify the booking belongs to this customer
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return None
            
        if booking.get('guest_email', '').lower() != customer_email.lower():
            return None
            
        return self.cancel_booking(booking_id)

    def check_room_availability(self, check_in: str, check_out: str) -> dict:
        """Check which rooms are available for specific dates"""
        try:
            check_in_date = datetime.fromisoformat(check_in)
            check_out_date = datetime.fromisoformat(check_out)
        except:
            raise ValueError("Invalid date format. Use YYYY-MM-DD format")

        all_rooms = self.room_service.get_all_rooms()
        all_bookings = self.get_all_bookings()
        
        available_rooms = []
        occupied_rooms = {}
        
        for room in all_rooms:
            if not room['is_available']:
                continue
                
            room_available = True
            room_occupied_dates = []
            
            # Check if room has conflicting bookings
            for booking in all_bookings:
                if booking['room_id'] == room['id'] and booking['status'] == 'confirmed':
                    try:
                        booking_checkin = datetime.fromisoformat(booking['check_in_date'])
                        booking_checkout = datetime.fromisoformat(booking['check_out_date'])
                        
                        # Check for date overlap
                        if not (check_out_date <= booking_checkin or check_in_date >= booking_checkout):
                            room_available = False
                        
                        room_occupied_dates.append({
                            'check_in': booking['check_in_date'],
                            'check_out': booking['check_out_date'],
                            'guest': booking.get('guest_name', 'Unknown')
                        })
                    except:
                        continue
            
            if room_available:
                available_rooms.append(room['id'])
            else:
                occupied_rooms[room['id']] = room_occupied_dates
        
        return {
            "check_in_date": check_in,
            "check_out_date": check_out,
            "available_rooms": available_rooms,
            "occupied_rooms": occupied_rooms,
            "total_available": len(available_rooms)
        }

    def _is_room_available(self, room_id: int, check_in_date: str, check_out_date: str) -> bool:
        """Check if a specific room is available for given dates"""
        try:
            check_in = datetime.fromisoformat(check_in_date)
            check_out = datetime.fromisoformat(check_out_date)
        except:
            return False

        all_bookings = self.get_all_bookings()
        
        for booking in all_bookings:
            if booking['room_id'] == room_id and booking['status'] == 'confirmed':
                try:
                    booking_checkin = datetime.fromisoformat(booking['check_in_date'])
                    booking_checkout = datetime.fromisoformat(booking['check_out_date'])
                    
                    # Check for date overlap
                    if not (check_out <= booking_checkin or check_in >= booking_checkout):
                        return False
                except:
                    continue
        
        return True 