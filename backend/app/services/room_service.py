from typing import List, Optional
from ..database.database import Database
from ..models.room import RoomCreate, RoomUpdate

class RoomService:
    def __init__(self):
        self.db = Database()

    def get_all_rooms(self) -> List[dict]:
        """Get all rooms from the database"""
        return self.db.get_all_rooms()

    def get_available_rooms(self) -> List[dict]:
        """Get only available rooms"""
        return self.db.get_available_rooms()

    def create_room(self, room_data: RoomCreate) -> dict:
        """Create a new room"""
        return self.db.create_room_in_db(
            room_number=room_data.room_number,
            room_type=room_data.room_type,
            price_per_night=room_data.price_per_night
        )

    def update_room(self, room_id: int, room_data: RoomUpdate) -> Optional[dict]:
        """Update an existing room"""
        return self.db.update_room_in_db(
            room_id=room_id,
            room_number=room_data.room_number,
            room_type=room_data.room_type,
            price_per_night=room_data.price_per_night,
            is_available=room_data.is_available
        )

    def delete_room(self, room_id: int) -> Optional[dict]:
        """Delete a room"""
        return self.db.delete_room_from_db(room_id)

    def get_room_by_id(self, room_id: int) -> Optional[dict]:
        """Get a room by its ID"""
        rooms = self.db.get_all_rooms()
        return next((room for room in rooms if room['id'] == room_id), None)

    def get_available_rooms_for_dates(self, check_in_date: str, check_out_date: str) -> List[dict]:
        """Get available rooms for specific dates"""
        return self.db.get_available_rooms_for_dates(check_in_date, check_out_date) 