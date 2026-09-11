"""Auth schemas"""
from pydantic import BaseModel, Field, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password (min 6 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Registered email address")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=6, description="New password (min 6 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "new_password": "newsecurepassword123"
            }
        }

class MessageResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "If an account exists with that email, reset instructions have been sent."
            }
        }

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com"
            }
        }
