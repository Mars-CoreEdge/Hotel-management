from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional, Generator
from datetime import datetime

class Database:
    def __init__(self):
        DATABASE_URL = "sqlite:///hotel.db"
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Get a database session"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    def get_all_rooms(self) -> List[dict]:
        """Get all rooms"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Room
            rooms = session.query(Room).all()
            return [self._room_to_dict(room) for room in rooms]
        finally:
            session.close()

    def get_available_rooms(self) -> List[dict]:
        """Get only available rooms"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Room
            rooms = session.query(Room).filter(Room.is_available == True).all()
            return [self._room_to_dict(room) for room in rooms]
        finally:
            session.close()

    def create_room_in_db(self, room_number: str, room_type: str, price_per_night: float) -> dict:
        """Create new room"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Room
            new_room = Room(
                room_number=room_number,
                room_type=room_type,
                price_per_night=price_per_night
            )
            session.add(new_room)
            session.commit()
            session.refresh(new_room)
            return self._room_to_dict(new_room)
        finally:
            session.close()

    def update_room_in_db(self, room_id: int, room_number: str, room_type: str,
                         price_per_night: float, is_available: bool) -> Optional[dict]:
        """Update room"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Room
            room = session.query(Room).filter(Room.id == room_id).first()
            if not room:
                return None

            room.room_number = room_number
            room.room_type = room_type
            room.price_per_night = price_per_night
            room.is_available = is_available
            session.commit()
            return self._room_to_dict(room)
        finally:
            session.close()

    def delete_room_from_db(self, room_id: int) -> Optional[dict]:
        """Delete room"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Room
            room = session.query(Room).filter(Room.id == room_id).first()
            if not room:
                return None

            room_dict = self._room_to_dict(room)
            session.delete(room)
            session.commit()
            return room_dict
        finally:
            session.close()

    def get_available_rooms_for_dates(self, check_in_date: str, check_out_date: str) -> List[dict]:
        """Get available rooms for specific dates"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Room, Booking
            
            # Convert string dates to datetime objects
            check_in = datetime.fromisoformat(check_in_date)
            check_out = datetime.fromisoformat(check_out_date)
            
            # Get all rooms
            all_rooms = session.query(Room).all()
            
            # Get bookings that overlap with the requested dates
            overlapping_bookings = session.query(Booking).filter(
                Booking.status == 'confirmed',
                Booking.check_in_date < check_out,
                Booking.check_out_date > check_in
            ).all()
            
            # Get room IDs that are booked during this period
            booked_room_ids = {booking.room_id for booking in overlapping_bookings}
            
            # Filter out booked rooms
            available_rooms = []
            for room in all_rooms:
                if room.id not in booked_room_ids and room.is_available:
                    available_rooms.append(self._room_to_dict(room))
            
            return available_rooms
        finally:
            session.close()

    def get_all_guests(self) -> List[dict]:
        """Get all guests"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Guest
            guests = session.query(Guest).all()
            return [self._guest_to_dict(guest) for guest in guests]
        finally:
            session.close()

    def create_guest_in_db(self, first_name: str, last_name: str, email: str, phone: str = None) -> dict:
        """Create new guest"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Guest
            new_guest = Guest(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            session.add(new_guest)
            session.commit()
            session.refresh(new_guest)
            return self._guest_to_dict(new_guest)
        finally:
            session.close()

    def update_guest_in_db(self, guest_id: int, first_name: str, last_name: str,
                          email: str, phone: str = None) -> Optional[dict]:
        """Update guest"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Guest
            guest = session.query(Guest).filter(Guest.id == guest_id).first()
            if not guest:
                return None

            guest.first_name = first_name
            guest.last_name = last_name
            guest.email = email
            guest.phone = phone
            session.commit()
            return self._guest_to_dict(guest)
        finally:
            session.close()

    def delete_guest_from_db(self, guest_id: int) -> Optional[dict]:
        """Delete guest"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Guest
            guest = session.query(Guest).filter(Guest.id == guest_id).first()
            if not guest:
                return None

            guest_dict = self._guest_to_dict(guest)
            session.delete(guest)
            session.commit()
            return guest_dict
        finally:
            session.close()

    def get_all_bookings(self) -> List[dict]:
        """Get all bookings with guest and room details"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Booking
            bookings = session.query(Booking).all()
            return [self._booking_to_dict(booking) for booking in bookings if booking.guest and booking.room]
        finally:
            session.close()

    def create_booking_in_db(self, guest_id: int, room_id: int, check_in_date: str,
                           check_out_date: str, total_price: float) -> dict:
        """Create new booking"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Booking
            
            # Convert string dates to datetime objects if needed
            if isinstance(check_in_date, str):
                check_in_date = datetime.fromisoformat(check_in_date.replace('Z', '+00:00'))
            if isinstance(check_out_date, str):
                check_out_date = datetime.fromisoformat(check_out_date.replace('Z', '+00:00'))

            new_booking = Booking(
                guest_id=guest_id,
                room_id=room_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                total_price=total_price
            )
            session.add(new_booking)
            session.commit()
            session.refresh(new_booking)
            return self._booking_to_dict(new_booking)
        finally:
            session.close()

    def delete_booking_from_db(self, booking_id: int) -> Optional[dict]:
        """Cancel/Delete booking"""
        session = self.SessionLocal()
        try:
            from ..models.database_models import Booking
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                return None

            booking_dict = self._booking_to_dict(booking)
            session.delete(booking)
            session.commit()
            return booking_dict
        finally:
            session.close()

    def _room_to_dict(self, room) -> dict:
        """Convert Room model to dictionary"""
        return {
            "id": room.id,
            "room_number": room.room_number,
            "room_type": room.room_type,
            "price_per_night": room.price_per_night,
            "is_available": room.is_available
        }

    def _guest_to_dict(self, guest) -> dict:
        """Convert Guest model to dictionary"""
        return {
            "id": guest.id,
            "first_name": guest.first_name,
            "last_name": guest.last_name,
            "email": guest.email,
            "phone": guest.phone,
            "created_at": guest.created_at.isoformat() if guest.created_at else None
        }

    def _booking_to_dict(self, booking) -> dict:
        """Convert Booking model to dictionary"""
        return {
            "id": booking.id,
            "guest_id": booking.guest_id,
            "room_id": booking.room_id,
            "guest_name": f"{booking.guest.first_name} {booking.guest.last_name}",
            "guest_email": booking.guest.email,
            "room_number": booking.room.room_number,
            "room_type": booking.room.room_type,
            "check_in_date": booking.check_in_date.isoformat() if booking.check_in_date else None,
            "check_out_date": booking.check_out_date.isoformat() if booking.check_out_date else None,
            "total_price": booking.total_price,
            "status": booking.status,
            "created_at": booking.created_at.isoformat() if booking.created_at else None
        }

# Create a global database instance
database = Database()

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session"""
    session = database.SessionLocal()
    try:
        yield session
    finally:
        session.close()