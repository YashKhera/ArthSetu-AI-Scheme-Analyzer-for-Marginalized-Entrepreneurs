"""Authentication service"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_reset_token,
    decode_reset_token,
)

class AuthService:

    @staticmethod
    def register(db: Session, email: str, password: str) -> User:
        """Create new user"""
        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash password
        password_hash = hash_password(password)

        # Create user
        user = User(
            email=email,
            password_hash=password_hash
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> User:
        """Authenticate user"""
        # Find user by email
        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        return user

    @staticmethod
    def create_access_token(user_id: int) -> str:
        """Generate JWT token"""
        return create_access_token(user_id)

    @staticmethod
    def forgot_password(db: Session, email: str) -> str:
        """Issue a password-reset token for a user (if one exists)."""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return create_reset_token(user.id)

    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> User:
        """Validate a reset token and set a new password."""
        payload = decode_reset_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        user.password_hash = hash_password(new_password)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_or_create_oauth_user(db: Session, email: str, name: str) -> User:
        """Return the existing user for an OAuth email, or create one.

        OAuth users have no usable password (password login is disabled for
        them unless they later use the forgot-password flow).
        """
        email = email.lower().strip()
        user = db.query(User).filter(User.email == email).first()

        if not user:
            unusable_hash = hash_password("#oauth-no-password-" + secrets.token_urlsafe(16))
            user = User(email=email, password_hash=unusable_hash)
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user
