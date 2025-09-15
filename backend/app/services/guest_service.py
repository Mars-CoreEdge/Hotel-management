from typing import List, Optional
from ..database.database import Database
from ..models.guest import GuestCreate, GuestUpdate

class GuestService:
    def __init__(self):
        self.db = Database()

    def get_all_guests(self) -> List[dict]:
        """Get all guests from the database"""
        return self.db.get_all_guests()

    def create_guest(self, guest_data: GuestCreate) -> dict:
        """Create a new guest"""
        return self.db.create_guest_in_db(
            first_name=guest_data.first_name,
            last_name=guest_data.last_name,
            email=guest_data.email,
            phone=guest_data.phone
        )

    def update_guest(self, guest_id: int, guest_data: GuestUpdate) -> Optional[dict]:
        """Update an existing guest"""
        return self.db.update_guest_in_db(
            guest_id=guest_id,
            first_name=guest_data.first_name,
            last_name=guest_data.last_name,
            email=guest_data.email,
            phone=guest_data.phone
        )

    def delete_guest(self, guest_id: int) -> Optional[dict]:
        """Delete a guest"""
        return self.db.delete_guest_from_db(guest_id)

    def get_guest_by_id(self, guest_id: int) -> Optional[dict]:
        """Get a guest by their ID"""
        guests = self.db.get_all_guests()
        return next((guest for guest in guests if guest['id'] == guest_id), None)

    def get_guest_by_email(self, email: str) -> Optional[dict]:
        """Get a guest by their email"""
        guests = self.db.get_all_guests()
        return next((guest for guest in guests if guest['email'].lower() == email.lower()), None)

    def find_or_create_guest(self, guest_data: dict) -> dict:
        """Find existing guest by email or create new one"""
        existing_guest = self.get_guest_by_email(guest_data['email'])
        if existing_guest:
            return existing_guest
        
        # Create new guest
        guest_create = GuestCreate(**guest_data)
        return self.create_guest(guest_create) 