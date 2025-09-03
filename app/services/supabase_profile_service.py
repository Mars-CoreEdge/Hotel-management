from supabase import create_client, Client
from fastapi import HTTPException, status
from typing import Optional
from ..config.settings import settings
from ..models.profile import ProfileCreate, ProfileUpdate, ProfileResponse
import json

class SupabaseProfileService:
    """Profile service using Supabase database directly"""
    
    def __init__(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Supabase not configured"
            )
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    
    async def get_profile(self, access_token: str) -> Optional[ProfileResponse]:
        """Get user profile using Supabase function"""
        try:
            # Set the auth token for this request
            self.supabase.auth.set_session(access_token, "")
            
            # Call the Supabase function
            result = self.supabase.rpc('get_user_profile').execute()
            
            if result.data:
                return ProfileResponse.model_validate(result.data)
            return None
            
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None
    
    async def create_or_update_profile(self, access_token: str, profile_data: ProfileCreate) -> ProfileResponse:
        """Create or update user profile using Supabase function"""
        try:
            # Set the auth token for this request
            self.supabase.auth.set_session(access_token, "")
            
            # Call the Supabase function
            result = self.supabase.rpc('upsert_user_profile', {
                'p_first_name': profile_data.first_name,
                'p_last_name': profile_data.last_name,
                'p_email': profile_data.email,
                'p_phone': profile_data.phone,
                'p_country': profile_data.country,
                'p_age': profile_data.age,
                'p_profile_picture_url': profile_data.profile_picture_url
            }).execute()
            
            if result.data:
                return ProfileResponse.model_validate(result.data)
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create/update profile"
                )
                
        except Exception as e:
            print(f"Error creating/updating profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create/update profile: {str(e)}"
            )
    
    async def update_profile(self, access_token: str, profile_data: ProfileUpdate) -> ProfileResponse:
        """Update user profile using Supabase function"""
        try:
            # Set the auth token for this request
            self.supabase.auth.set_session(access_token, "")
            
            # Call the Supabase function
            result = self.supabase.rpc('upsert_user_profile', {
                'p_first_name': profile_data.first_name,
                'p_last_name': profile_data.last_name,
                'p_email': profile_data.email,
                'p_phone': profile_data.phone,
                'p_country': profile_data.country,
                'p_age': profile_data.age,
                'p_profile_picture_url': profile_data.profile_picture_url
            }).execute()
            
            if result.data:
                return ProfileResponse.model_validate(result.data)
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update profile"
                )
                
        except Exception as e:
            print(f"Error updating profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update profile: {str(e)}"
            )
    
    async def delete_profile(self, access_token: str) -> bool:
        """Delete user profile using Supabase function"""
        try:
            # Set the auth token for this request
            self.supabase.auth.set_session(access_token, "")
            
            # Call the Supabase function
            result = self.supabase.rpc('delete_user_profile').execute()
            
            return result.data if result.data is not None else False
            
        except Exception as e:
            print(f"Error deleting profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete profile: {str(e)}"
            )
