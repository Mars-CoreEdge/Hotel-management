"""
Database Service for Grand Hotel Management System
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, Room, Guest, Booking
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///hotel.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def get_all_rooms():
    """Get all rooms"""
    session = SessionLocal()
    rooms = session.query(Room).all()
    
    # Convert to dictionaries
    result = []
    for room in rooms:
        result.append({
            "id": room.id,
            "room_number": room.room_number,
            "room_type": room.room_type,
            "price_per_night": room.price_per_night,
            "is_available": room.is_available
        })
    
    session.close()
    return result

def get_available_rooms():
    """Get only available rooms"""
    session = SessionLocal()
    rooms = session.query(Room).filter(Room.is_available == True).all()
    
    # Convert to dictionaries
    result = []
    for room in rooms:
        result.append({
            "id": room.id,
            "room_number": room.room_number,
            "room_type": room.room_type,
            "price_per_night": room.price_per_night,
            "is_available": room.is_available
        })
    
    session.close()
    return result

def create_room_in_db(room_number, room_type, price_per_night):
    """Create new room"""
    session = SessionLocal()
    
    # Create new room object
    new_room = Room(room_number=room_number, room_type=room_type, price_per_night=price_per_night)
    session.add(new_room)
    session.commit()
    session.refresh(new_room)  # Get the auto-generated ID
    
    result = {
        "id": new_room.id,
        "room_number": new_room.room_number,
        "room_type": new_room.room_type,
        "price_per_night": new_room.price_per_night,
        "is_available": new_room.is_available
    }
    
    session.close()
    return result

def update_room_in_db(room_id, room_number, room_type, price_per_night, is_available):
    """Update room"""
    session = SessionLocal()
    
    # Find the room
    room = session.query(Room).filter(Room.id == room_id).first()
    
    if room is None:
        session.close()
        return None
    
    # Update the room
    room.room_number = room_number
    room.room_type = room_type
    room.price_per_night = price_per_night
    room.is_available = is_available
    session.commit()
    
    result = {
        "id": room.id,
        "room_number": room.room_number,
        "room_type": room.room_type,
        "price_per_night": room.price_per_night,
        "is_available": room.is_available
    }
    
    session.close()
    return result

def delete_room_from_db(room_id):
    """Delete room"""
    session = SessionLocal()
    
    # Find the room
    room = session.query(Room).filter(Room.id == room_id).first()
    
    if room is None:
        session.close()
        return None
    
    # Store room info before deletion
    result = {
        "id": room.id,
        "room_number": room.room_number,
        "room_type": room.room_type,
        "price_per_night": room.price_per_night,
        "is_available": room.is_available
    }
    
    # Delete the room
    session.delete(room)
    session.commit()
    session.close()
    
    return result

def get_all_guests():
    """Get all guests"""
    session = SessionLocal()
    guests = session.query(Guest).all()
    
    # Convert to dictionaries
    result = []
    for guest in guests:
        result.append({
            "id": guest.id,
            "first_name": guest.first_name,
            "last_name": guest.last_name,
            "email": guest.email,
            "phone": guest.phone,
            "created_at": guest.created_at.isoformat() if guest.created_at else None
        })
    
    session.close()
    return result

def create_guest_in_db(first_name, last_name, email, phone=None):
    """Create new guest"""
    session = SessionLocal()
    
    # Create new guest object
    new_guest = Guest(first_name=first_name, last_name=last_name, email=email, phone=phone)
    session.add(new_guest)
    session.commit()
    session.refresh(new_guest)  # Get the auto-generated ID
    
    result = {
        "id": new_guest.id,
        "first_name": new_guest.first_name,
        "last_name": new_guest.last_name,
        "email": new_guest.email,
        "phone": new_guest.phone,
        "created_at": new_guest.created_at.isoformat() if new_guest.created_at else None
    }
    
    session.close()
    return result

def update_guest_in_db(guest_id, first_name, last_name, email, phone=None):
    """Update guest"""
    session = SessionLocal()
    
    # Find the guest
    guest = session.query(Guest).filter(Guest.id == guest_id).first()
    
    if guest is None:
        session.close()
        return None
    
    # Update the guest
    guest.first_name = first_name
    guest.last_name = last_name
    guest.email = email
    guest.phone = phone
    session.commit()
    
    result = {
        "id": guest.id,
        "first_name": guest.first_name,
        "last_name": guest.last_name,
        "email": guest.email,
        "phone": guest.phone,
        "created_at": guest.created_at.isoformat() if guest.created_at else None
    }
    
    session.close()
    return result

def delete_guest_from_db(guest_id):
    """Delete guest"""
    session = SessionLocal()
    
    # Find the guest
    guest = session.query(Guest).filter(Guest.id == guest_id).first()
    
    if guest is None:
        session.close()
        return None
    
    # Store guest info before deletion
    result = {
        "id": guest.id,
        "first_name": guest.first_name,
        "last_name": guest.last_name,
        "email": guest.email,
        "phone": guest.phone,
        "created_at": guest.created_at.isoformat() if guest.created_at else None
    }
    
    # Delete the guest
    session.delete(guest)
    session.commit()
    session.close()
    
    return result

def get_all_bookings():
    """Get all bookings with guest and room details"""
    session = SessionLocal()
    bookings = session.query(Booking).all()
    
    # Convert to dictionaries with related data
    result = []
    for booking in bookings:
        # Check if related guest and room exist
        if booking.guest is None or booking.room is None:
            print(f"Warning: Booking {booking.id} has missing guest or room, skipping...")
            continue
            
        result.append({
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
        })
    
    session.close()
    return result

def create_booking_in_db(guest_id, room_id, check_in_date, check_out_date, total_price):
    """Create new booking"""
    session = SessionLocal()
    
    # Convert string dates to datetime objects if needed
    if isinstance(check_in_date, str):
        check_in_date = datetime.fromisoformat(check_in_date.replace('Z', '+00:00'))
    if isinstance(check_out_date, str):
        check_out_date = datetime.fromisoformat(check_out_date.replace('Z', '+00:00'))
    
    # Create new booking object
    new_booking = Booking(
        guest_id=guest_id,
        room_id=room_id,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        total_price=total_price
    )
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)  # Get the auto-generated ID
    
    result = {
        "id": new_booking.id,
        "guest_id": new_booking.guest_id,
        "room_id": new_booking.room_id,
        "guest_name": f"{new_booking.guest.first_name} {new_booking.guest.last_name}",
        "guest_email": new_booking.guest.email,
        "room_number": new_booking.room.room_number,
        "room_type": new_booking.room.room_type,
        "check_in_date": new_booking.check_in_date.isoformat() if new_booking.check_in_date else None,
        "check_out_date": new_booking.check_out_date.isoformat() if new_booking.check_out_date else None,
        "total_price": new_booking.total_price,
        "status": new_booking.status,
        "created_at": new_booking.created_at.isoformat() if new_booking.created_at else None
    }
    
    session.close()
    return result

def delete_booking_from_db(booking_id):
    """Cancel/Delete booking"""
    session = SessionLocal()
    
    # Find the booking
    booking = session.query(Booking).filter(Booking.id == booking_id).first()
    
    if booking is None:
        session.close()
        return None
    
    # Store booking info before deletion
    result = {
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
    
    # Delete the booking
    session.delete(booking)
    session.commit()
    session.close()
    
    return result

def get_available_rooms_for_dates(check_in_date, check_out_date):
    """Get available rooms for specific date range"""
    session = SessionLocal()
    
    # Convert string dates to datetime objects if needed
    if isinstance(check_in_date, str):
        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
    if isinstance(check_out_date, str):
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
    
    # Get all rooms
    all_rooms = session.query(Room).all()
    
    # Get all bookings that overlap with the requested dates
    overlapping_bookings = session.query(Booking).filter(
        Booking.status == 'confirmed',
        Booking.check_in_date < check_out_date,
        Booking.check_out_date > check_in_date
    ).all()
    
    # Get room IDs that are booked during this period
    booked_room_ids = {booking.room_id for booking in overlapping_bookings}
    
    # Filter out booked rooms
    available_rooms = []
    for room in all_rooms:
        if room.id not in booked_room_ids:
            available_rooms.append({
                "id": room.id,
                "room_number": room.room_number,
                "room_type": room.room_type,
                "price_per_night": room.price_per_night,
                "is_available": room.is_available
            })
    
    session.close()
    return available_rooms

def add_guest(guest_data):
    """Add a new guest (wrapper for AI compatibility)"""
    # Parse name if it's provided as full name
    if 'name' in guest_data:
        name_parts = guest_data['name'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
    else:
        first_name = guest_data.get('first_name', '')
        last_name = guest_data.get('last_name', '')
    
    result = create_guest_in_db(
        first_name=first_name,
        last_name=last_name,
        email=guest_data['email'],
        phone=guest_data.get('phone')
    )
    return result['id']

def add_booking(booking_data):
    """Add a new booking (wrapper for AI compatibility)"""
    result = create_booking_in_db(
        guest_id=booking_data['guest_id'],
        room_id=booking_data['room_id'],
        check_in_date=booking_data['check_in_date'],
        check_out_date=booking_data['check_out_date'],
        total_price=booking_data['total_price']
    )
    return result['id']

def cancel_booking(booking_id):
    """Cancel a booking (wrapper for AI compatibility)"""
    result = delete_booking_from_db(booking_id)
    return result is not None 