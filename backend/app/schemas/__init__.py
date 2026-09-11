"""Import all schemas"""
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse
from app.schemas.entrepreneur import ProfileRequest, ProfileResponse, ProfileUpdateRequest
from app.schemas.scheme import SchemeResponse, SchemeListResponse
from app.schemas.recommendation import RecommendationRequest, RecommendationItem, RecommendationResponse
from app.schemas.common import ErrorResponse, SuccessResponse

__all__ = [
    "RegisterRequest",
    "LoginRequest",
    "AuthResponse",
    "UserResponse",
    "ProfileRequest",
    "ProfileResponse",
    "ProfileUpdateRequest",
    "SchemeResponse",
    "SchemeListResponse",
    "RecommendationRequest",
    "RecommendationItem",
    "RecommendationResponse",
    "ErrorResponse",
    "SuccessResponse"
]
