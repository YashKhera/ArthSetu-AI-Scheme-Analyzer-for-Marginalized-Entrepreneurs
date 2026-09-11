"""Profile router"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.entrepreneur import ProfileRequest, ProfileResponse, ProfileUpdateRequest
from app.services.profile_service import ProfileService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.requirement import Requirement

router = APIRouter()

@router.post("/profile", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    data: ProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create entrepreneur profile"""
    profile = ProfileService.create_profile(db, current_user.id, data)

    # Get support needs
    requirements = db.query(Requirement).filter(
        Requirement.profile_id == profile.id
    ).all()
    support_needed = [req.support_type for req in requirements]

    # Build response
    response = ProfileResponse.model_validate(profile)
    response.support_needed = support_needed

    return response

@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get entrepreneur profile"""
    profile_data = ProfileService.get_profile_with_requirements(db, current_user.id)

    response = ProfileResponse.model_validate(profile_data["profile"])
    response.support_needed = profile_data["support_needed"]

    return response

@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update entrepreneur profile"""
    profile = ProfileService.update_profile(db, current_user.id, data)

    # Get support needs
    requirements = db.query(Requirement).filter(
        Requirement.profile_id == profile.id
    ).all()
    support_needed = [req.support_type for req in requirements]

    response = ProfileResponse.model_validate(profile)
    response.support_needed = support_needed

    return response
