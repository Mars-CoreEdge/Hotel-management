from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    """User roles enumeration"""
    ADMIN = "admin"
    USER = "user"

class UserRegister(BaseModel):
    """User registration model"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response model"""
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: str

class Token(BaseModel):
    """JWT token model"""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Token data model for JWT payload"""
    email: Optional[str] = None
    role: Optional[UserRole] = None

class PasswordReset(BaseModel):
    """Password reset model"""
    email: EmailStr

class PasswordChange(BaseModel):
    """Password change model"""
    current_password: str
    new_password: str
