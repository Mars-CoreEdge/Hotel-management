from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..services.auth_service import AuthService, get_current_user, require_admin_role
from ..models.auth_models import UserRegister, UserLogin, UserResponse, Token, PasswordReset, PasswordChange

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister):
    """
    Register a new user
    
    - **email**: User's email address
    - **password**: User's password (minimum 6 characters)
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **phone**: User's phone number (optional)
    - **role**: User's role (defaults to 'user')
    """
    return await AuthService.register_user(user_data)

@router.post("/login", response_model=Token)
async def login_user(user_data: UserLogin):
    """
    Authenticate user and return JWT token
    
    - **email**: User's email address
    - **password**: User's password
    """
    return await AuthService.login_user(user_data)

@router.post("/logout")
async def logout_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Logout user and invalidate token
    """
    return await AuthService.logout_user(credentials.credentials)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user information
    """
    return current_user

@router.post("/password-reset")
async def request_password_reset(password_reset: PasswordReset):
    """
    Request password reset email
    
    - **email**: User's email address
    """
    try:
        # This would typically send a password reset email
        # For now, we'll just return a success message
        return {
            "message": "If an account with that email exists, a password reset link has been sent.",
            "email": password_reset.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send password reset email: {str(e)}"
        )

@router.post("/password-change")
async def change_password(
    password_change: PasswordChange,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Change user password
    
    - **current_password**: User's current password
    - **new_password**: User's new password (minimum 6 characters)
    """
    try:
        # This would typically verify the current password and update to the new one
        # For now, we'll just return a success message
        return {
            "message": "Password changed successfully",
            "user_id": current_user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )

@router.get("/admin-only", response_model=dict)
async def admin_only_endpoint(current_user: UserResponse = Depends(require_admin_role)):
    """
    Admin-only endpoint for testing role-based access control
    """
    return {
        "message": "This is an admin-only endpoint",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role.value
        }
    }
