from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime

from ..database.database import get_db
from ..models.database_models import UserProfile
from ..models.profile import ProfileCreate, ProfileUpdate, ProfileResponse

class ProfileService:
    """Service for managing user profiles"""
    
    @staticmethod
    async def create_profile(db: Session, user_id: str, profile_data: ProfileCreate) -> ProfileResponse:
        """Create a new user profile"""
        try:
            # Check if profile already exists for this user
            existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if existing_profile:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Profile already exists for this user"
                )
            
            # Check if email is already taken by another user
            existing_email = db.query(UserProfile).filter(
                UserProfile.email == profile_data.email,
                UserProfile.user_id != user_id
            ).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use by another user"
                )
            
            # Create new profile
            db_profile = UserProfile(
                user_id=user_id,
                first_name=profile_data.first_name,
                last_name=profile_data.last_name,
                email=profile_data.email,
                phone=profile_data.phone,
                country=profile_data.country,
                age=profile_data.age,
                profile_picture_url=profile_data.profile_picture_url
            )
            
            db.add(db_profile)
            db.commit()
            db.refresh(db_profile)
            
            return ProfileResponse.model_validate(db_profile)
            
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile creation failed due to data constraints"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create profile: {str(e)}"
            )
    
    @staticmethod
    async def get_profile_by_user_id(db: Session, user_id: str) -> Optional[ProfileResponse]:
        """Get profile by user ID"""
        try:
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if not profile:
                return None
            
            return ProfileResponse.model_validate(profile)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve profile: {str(e)}"
            )
    
    @staticmethod
    async def update_profile(db: Session, user_id: str, profile_data: ProfileUpdate) -> ProfileResponse:
        """Update an existing profile"""
        try:
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Update fields if provided
            update_data = profile_data.dict(exclude_unset=True)
            
            # Check email uniqueness if email is being updated
            if 'email' in update_data:
                existing_email = db.query(UserProfile).filter(
                    UserProfile.email == update_data['email'],
                    UserProfile.user_id != user_id
                ).first()
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already in use by another user"
                    )
            
            for field, value in update_data.items():
                setattr(profile, field, value)
            
            profile.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(profile)
            
            return ProfileResponse.model_validate(profile)
            
        except HTTPException:
            raise
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile update failed due to data constraints"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update profile: {str(e)}"
            )
    
    @staticmethod
    async def delete_profile(db: Session, user_id: str) -> bool:
        """Delete a user profile"""
        try:
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            db.delete(profile)
            db.commit()
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete profile: {str(e)}"
            )
