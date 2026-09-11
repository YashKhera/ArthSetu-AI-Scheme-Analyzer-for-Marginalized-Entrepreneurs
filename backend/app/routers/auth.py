"""Authentication router"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    MessageResponse,
)
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter()
logger = logging.getLogger("arthsetu.auth")

@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Create user
    user = AuthService.register(db, data.email, data.password)

    # Generate token
    access_token = AuthService.create_access_token(user.id)

    return AuthResponse(access_token=access_token)

@router.post("/auth/login", response_model=AuthResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user"""
    # Authenticate user
    user = AuthService.login(db, data.email, data.password)

    # Generate token
    access_token = AuthService.create_access_token(user.id)

    return AuthResponse(access_token=access_token)

@router.get("/auth/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email
    )

@router.post("/auth/forgot-password", response_model=MessageResponse)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Request a password reset link for an existing account.

    Always returns the same message to avoid account enumeration.
    No email transport is configured yet, so in development the reset
    token is logged to the server console (replace with email delivery
    in production).
    """
    reset_token = AuthService.forgot_password(db, data.email)

    if reset_token and settings.ENVIRONMENT == "development":
        reset_url = f"{settings.FRONTEND_URL}/reset-password.html?token={reset_token}"
        logger.info("Password reset link for %s: %s", data.email, reset_url)

    return MessageResponse(
        message="If an account exists with that email, reset instructions have been sent."
    )

@router.post("/auth/reset-password", response_model=MessageResponse)
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Set a new password using a valid reset token."""
    AuthService.reset_password(db, data.token, data.new_password)

    return MessageResponse(message="Password reset successfully. You can now log in with your new password.")
