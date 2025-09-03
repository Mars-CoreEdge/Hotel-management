from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from ..services.supabase_profile_service import SupabaseProfileService
from ..models.profile import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/profile", tags=["profile"])
security = HTTPBearer()

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile_data: ProfileCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new user profile"""
    profile_service = SupabaseProfileService()
    return await profile_service.create_or_update_profile(credentials.credentials, profile_data)

@router.get("/", response_model=Optional[ProfileResponse])
async def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current user's profile"""
    profile_service = SupabaseProfileService()
    return await profile_service.get_profile(credentials.credentials)

@router.put("/", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update current user's profile"""
    profile_service = SupabaseProfileService()
    return await profile_service.update_profile(credentials.credentials, profile_data)

@router.delete("/")
async def delete_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Delete current user's profile"""
    profile_service = SupabaseProfileService()
    success = await profile_service.delete_profile(credentials.credentials)
    if success:
        return {"message": "Profile deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile"
        )
