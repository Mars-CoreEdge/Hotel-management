from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    """Base room model with common attributes"""
    room_number: str
    room_type: str
    price_per_night: float

class RoomCreate(RoomBase):
    """Model for creating a new room"""
    pass

class RoomUpdate(RoomBase):
    """Model for updating an existing room"""
    is_available: bool

class RoomInDB(RoomBase):
    """Model for room as stored in database"""
    id: int
    is_available: bool = True

    class Config:
        from_attributes = True

class RoomResponse(RoomInDB):
    """Model for room response with additional fields"""
    description: Optional[str] = None
    capacity: Optional[str] = None
    amenities: Optional[list] = None

    @classmethod
    def from_db(cls, db_room: dict) -> 'RoomResponse':
        """Create a response model from database room"""
        room_type = db_room['room_type']
        response = cls(**db_room)
        
        # Add customer-friendly descriptions based on room type
        if room_type == 'Single':
            response.description = 'Perfect for solo travelers. Comfortable single bed with modern amenities.'
            response.capacity = '1 Guest'
            response.amenities = ['Free WiFi', 'Air Conditioning', 'Private Bathroom', 'TV']
        elif room_type == 'Double':
            response.description = 'Ideal for couples. Spacious room with queen-size bed and city view.'
            response.capacity = '2 Guests'
            response.amenities = ['Free WiFi', 'Air Conditioning', 'Private Bathroom', 'TV', 'Mini Fridge']
        elif room_type == 'Suite':
            response.description = 'Luxury suite with separate living area. Perfect for extended stays.'
            response.capacity = '2-3 Guests'
            response.amenities = ['Free WiFi', 'Air Conditioning', 'Private Bathroom', 'TV', 'Mini Fridge', 'Seating Area']
        elif room_type == 'Deluxe':
            response.description = 'Premium room with enhanced comfort and elegant furnishings.'
            response.capacity = '2-3 Guests'
            response.amenities = ['Free WiFi', 'Air Conditioning', 'Private Bathroom', 'TV', 'Mini Fridge', 'Balcony']
        elif room_type == 'Presidential':
            response.description = 'Ultimate luxury experience with premium amenities and services.'
            response.capacity = '4 Guests'
            response.amenities = ['Free WiFi', 'Air Conditioning', 'Private Bathroom', 'TV', 'Mini Fridge', 'Balcony', 'Room Service', 'Jacuzzi']
        
        return response 