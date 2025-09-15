from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..database.database import get_db
from ..services.profile_service import ProfileService
from ..services.auth_service import get_current_user
from ..models.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from ..models.auth_models import UserResponse
from ..config.settings import settings

router = APIRouter(prefix="/profile", tags=["profile"])

# Development helper function for when auth is not available
async def get_current_user_dev() -> UserResponse:
    """Development fallback for authentication"""
    return UserResponse(
        id="dev-user-123",
        email="dev@example.com",
        first_name="Dev",
        last_name="User",
        phone=None,
        role="user",
        is_active=True,
        created_at="2024-01-01T00:00:00Z"
    )

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new user profile"""
    return await ProfileService.create_profile(db, current_user.id, profile_data)

@router.get("/", response_model=Optional[ProfileResponse])
async def get_profile(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    return await ProfileService.get_profile_by_user_id(db, current_user.id)

# Temporary development endpoint without authentication
@router.get("/test", response_model=Optional[ProfileResponse])
async def get_profile_test(db: Session = Depends(get_db)):
    """Get profile for testing (no auth required)"""
    return await ProfileService.get_profile_by_user_id(db, "dev-user-123")

@router.post("/test", response_model=ProfileResponse)
async def create_profile_test(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    """Create profile for testing (no auth required)"""
    return await ProfileService.create_profile(db, "dev-user-123", profile_data)

@router.put("/test", response_model=ProfileResponse)
async def update_profile_test(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update profile for testing (no auth required)"""
    return await ProfileService.update_profile(db, "dev-user-123", profile_data)

@router.delete("/test")
async def delete_profile_test(db: Session = Depends(get_db)):
    """Delete profile for testing (no auth required)"""
    success = await ProfileService.delete_profile(db, "dev-user-123")
    if success:
        return {"message": "Profile deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile"
        )

@router.put("/", response_model=ProfileResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    return await ProfileService.update_profile(db, current_user.id, profile_data)

@router.delete("/")
async def delete_profile(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete current user's profile"""
    success = await ProfileService.delete_profile(db, current_user.id)
    if success:
        return {"message": "Profile deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile"
        )

# Development endpoints (no authentication required)
@router.get("/dev", response_model=Optional[ProfileResponse])
async def get_profile_dev(db: Session = Depends(get_db)):
    """Get profile for development (no auth required)"""
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return await ProfileService.get_profile_by_user_id(db, "dev-user-123")

@router.post("/dev", response_model=ProfileResponse)
async def create_profile_dev(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    """Create profile for development (no auth required)"""
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return await ProfileService.create_profile(db, "dev-user-123", profile_data)
