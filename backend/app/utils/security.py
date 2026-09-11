"""Security utilities for password hashing and JWT"""
from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from app.config import settings

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    # Truncate password if longer than 72 bytes
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_reset_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create a short-lived password-reset token (typ=reset)"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": str(user_id), "typ": "reset", "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def decode_reset_token(token: str) -> Optional[dict]:
    """Decode and verify a password-reset token (must be typ=reset)"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("typ") != "reset":
            return None
        return payload
    except JWTError:
        return None

def create_oauth_state_token(expires_delta: Optional[timedelta] = None) -> str:
    """Create a short-lived signed state token for the OAuth round-trip."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=10)

    import secrets
    expire = datetime.utcnow() + expires_delta
    to_encode = {"typ": "oauth-state", "nonce": secrets.token_urlsafe(16), "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_oauth_state_token(token: str) -> bool:
    """Validate a signed OAuth state token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("typ") == "oauth-state" and bool(payload.get("nonce"))
    except JWTError:
        return False