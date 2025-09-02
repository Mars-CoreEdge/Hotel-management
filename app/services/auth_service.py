from supabase import create_client, Client
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

from ..config.settings import settings
from ..models.auth_models import UserRegister, UserLogin, UserResponse, Token, TokenData, UserRole

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Security scheme for JWT tokens
security = HTTPBearer()

# Standalone dependency functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    token_data = AuthService.verify_token(token)
    
    try:
        # Get user from Supabase
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Get user metadata
        user_metadata = user_response.user.user_metadata or {}
        role = UserRole(user_metadata.get("role", "user"))
        
        return UserResponse(
            id=user_response.user.id,
            email=user_response.user.email,
            first_name=user_metadata.get("first_name", ""),
            last_name=user_metadata.get("last_name", ""),
            phone=user_metadata.get("phone"),
            role=role,
            is_active=user_response.user.email_confirmed_at is not None,
            created_at=user_response.user.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

class AuthService:
    """Authentication service for handling user authentication and authorization"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """Verify JWT token and return token data"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            email: str = payload.get("sub")
            role: str = payload.get("role")
            
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return TokenData(email=email, role=UserRole(role) if role else None)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    async def register_user(user_data: UserRegister) -> UserResponse:
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = supabase.auth.admin.list_users()
            for user in existing_user.users:
                if user.email == user_data.email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="User with this email already exists"
                    )
            
            # Create user in Supabase Auth
            auth_response = supabase.auth.admin.create_user({
                "email": user_data.email,
                "password": user_data.password,
                "email_confirm": True,
                "user_metadata": {
                    "first_name": user_data.first_name,
                    "last_name": user_data.last_name,
                    "phone": user_data.phone,
                    "role": user_data.role.value
                }
            })
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user"
                )
            
            # Return user response
            return UserResponse(
                id=auth_response.user.id,
                email=auth_response.user.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone=user_data.phone,
                role=user_data.role,
                is_active=auth_response.user.email_confirmed_at is not None,
                created_at=auth_response.user.created_at
            )
            
        except Exception as e:
            if "already exists" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to register user: {str(e)}"
            )
    
    @staticmethod
    async def login_user(user_data: UserLogin) -> Token:
        """Authenticate user and return JWT token"""
        try:
            # Sign in user with Supabase
            auth_response = supabase.auth.sign_in_with_password({
                "email": user_data.email,
                "password": user_data.password
            })
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            # Get user metadata
            user_metadata = auth_response.user.user_metadata or {}
            role = UserRole(user_metadata.get("role", "user"))
            
            # Create user response
            user_response = UserResponse(
                id=auth_response.user.id,
                email=auth_response.user.email,
                first_name=user_metadata.get("first_name", ""),
                last_name=user_metadata.get("last_name", ""),
                phone=user_metadata.get("phone"),
                role=role,
                is_active=auth_response.user.email_confirmed_at is not None,
                created_at=auth_response.user.created_at
            )
            
            # Create access token
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = AuthService.create_access_token(
                data={"sub": user_response.email, "role": user_response.role.value},
                expires_delta=access_token_expires
            )
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                user=user_response
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    

    

    
    @staticmethod
    async def logout_user(token: str):
        """Logout user by invalidating token"""
        try:
            # Sign out user from Supabase
            supabase.auth.sign_out()
            return {"message": "Successfully logged out"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to logout: {str(e)}"
            )

# Standalone dependency function for admin role requirement
async def require_admin_role(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Require admin role for protected endpoints"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
