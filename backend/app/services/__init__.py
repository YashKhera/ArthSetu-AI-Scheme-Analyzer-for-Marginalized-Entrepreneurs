"""Import all services"""
from app.services.auth_service import AuthService
from app.services.profile_service import ProfileService
from app.services.scheme_service import SchemeService
from app.services.matching_service import MatchingService
from app.services.ai_service import AIService

__all__ = [
    "AuthService",
    "ProfileService",
    "SchemeService",
    "MatchingService",
    "AIService"
]
