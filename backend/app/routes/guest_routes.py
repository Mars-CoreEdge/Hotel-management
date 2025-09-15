"""
Guest management routes for the Grand Hotel Management System
"""
from fastapi import APIRouter, HTTPException
from typing import List
from ..services.guest_service import GuestService
from ..models.guest import GuestCreate, GuestUpdate

router = APIRouter(prefix="/guests", tags=["guests"])
guest_service = GuestService()

@router.get("/", response_model=List[dict])
def get_guests():
    """Get all guests"""
    return guest_service.get_all_guests()

@router.post("/", response_model=dict)
def create_guest(guest_data: GuestCreate):
    """Create a new guest"""
    new_guest = guest_service.create_guest(guest_data)
    return {
        "message": "Guest created successfully",
        "guest": new_guest
    }

@router.put("/{guest_id}", response_model=dict)
def update_guest(guest_id: int, guest_data: GuestUpdate):
    """Update an existing guest"""
    updated_guest = guest_service.update_guest(guest_id, guest_data)
    if not updated_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return {
        "message": "Guest updated successfully",
        "guest": updated_guest
    }

@router.delete("/{guest_id}", response_model=dict)
def delete_guest(guest_id: int):
    """Delete a guest"""
    deleted_guest = guest_service.delete_guest(guest_id)
    if not deleted_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return {"message": f"Deleted guest {deleted_guest['first_name']} {deleted_guest['last_name']}"} 