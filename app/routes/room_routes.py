"""
Room management routes for the Grand Hotel Management System
"""
from fastapi import APIRouter, HTTPException
from typing import List
from ..services.room_service import RoomService
from ..models.room import RoomCreate, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["rooms"])
room_service = RoomService()

@router.get("/", response_model=List[dict])
def get_rooms():
    """Get all rooms"""
    return room_service.get_all_rooms()

@router.get("/available", response_model=List[dict])
def get_available_rooms():
    """Get only available rooms"""
    return room_service.get_available_rooms()

@router.post("/", response_model=dict)
def create_room(room_data: RoomCreate):
    """Create a new room"""
    new_room = room_service.create_room(room_data)
    return {
        "message": "Room created successfully",
        "room": new_room
    }

@router.put("/{room_id}", response_model=dict)
def update_room(room_id: int, room_data: RoomUpdate):
    """Update an existing room"""
    updated_room = room_service.update_room(room_id, room_data)
    if not updated_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "message": "Updated successfully",
        "room": updated_room
    }

@router.delete("/{room_id}", response_model=dict)
def delete_room(room_id: int):
    """Delete a room"""
    deleted_room = room_service.delete_room(room_id)
    if not deleted_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": f"Deleted room {deleted_room['room_number']}"} 