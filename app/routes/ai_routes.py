"""
AI service routes for the Grand Hotel Management System
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])

# Initialize AI service lazily to ensure environment variables are loaded
def get_ai_service():
    return AIService()

class AIMessageCreate(BaseModel):
    """Model for AI chat messages"""
    message: str
    conversation_history: Optional[list] = []

class AIBookingLookup(BaseModel):
    """Model for AI booking lookup"""
    email: str

@router.post("/chat", response_model=dict)
def ai_chat(chat_data: AIMessageCreate):
    """Chat with AI reception assistant"""
    ai_service = get_ai_service()
    
    if not ai_service.openai_client:
        return {
            "success": False,
            "response": "AI Reception service is currently unavailable. Please contact our human staff for assistance.",
            "error": "AI service not configured"
        }
    
    try:
        response = ai_service.chat_with_ai(
            chat_data.message, 
            chat_data.conversation_history
        )
        return response
    except Exception as e:
        return {
            "success": False,
            "response": "I apologize for the technical difficulty. Please try again or contact our staff.",
            "error": str(e)
        }

@router.get("/hotel-status", response_model=dict)
def get_ai_hotel_status():
    """Get current hotel status for AI context"""
    try:
        ai_service = get_ai_service()
        hotel_data = ai_service.get_hotel_data()
        return {
            "success": True,
            "data": hotel_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/booking-lookup", response_model=dict)
def ai_booking_lookup(lookup_data: AIBookingLookup):
    """Look up booking information via AI"""
    try:
        ai_service = get_ai_service()
        booking_info = ai_service.get_booking_info(lookup_data.email)
        return {
            "success": True,
            "data": booking_info
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 