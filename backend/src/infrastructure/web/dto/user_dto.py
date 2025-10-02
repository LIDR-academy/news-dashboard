"""User DTOs for web layer."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    """Base user DTO."""
    email: EmailStr
    username: str
    is_active: bool = True


class UserCreate(BaseModel):
    """DTO for creating a user."""
    email: EmailStr
    username: str
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    """DTO for user response."""
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """DTO for user login."""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    """DTO for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """DTO for token data."""
    username: Optional[str] = None


class LogoutResponse(BaseModel):
    """DTO for logout response."""
    message: str
    success: bool


class UserProfileUpdateRequest(BaseModel):
    """DTO for updating user profile."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newemail@example.com",
                "username": "newusername"
            }
        }


class ChangePasswordRequest(BaseModel):
    """DTO for changing password."""
    current_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (minimum 6 characters)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "oldpassword123",
                "new_password": "newpassword123"
            }
        }


class PasswordChangeResponse(BaseModel):
    """DTO for password change response."""
    message: str
    success: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Password changed successfully",
                "success": True
            }
        }