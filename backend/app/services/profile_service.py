"""Profile service"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.entrepreneur import EntrepreneurProfile
from app.models.requirement import Requirement
from app.schemas.entrepreneur import ProfileRequest, ProfileUpdateRequest

class ProfileService:

    @staticmethod
    def create_profile(db: Session, user_id: int, data: ProfileRequest) -> EntrepreneurProfile:
        """Create user profile"""
        # Check if profile already exists
        existing_profile = db.query(EntrepreneurProfile).filter(
            EntrepreneurProfile.user_id == user_id
        ).first()

        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Profile already exists for this user"
            )

        # Create profile record
        profile = EntrepreneurProfile(
            user_id=user_id,
            full_name=data.full_name,
            phone_number=data.phone_number,
            state=data.state,
            district=data.district,
            age_group=data.age_group,
            gender=data.gender,
            social_category=data.social_category,
            business_name=data.business_name,
            business_sector=data.business_sector,
            business_stage=data.business_stage,
            annual_income_range=data.annual_income_range,
            employee_range=data.employee_range
        )

        db.add(profile)
        db.flush()  # Get profile ID

        # Create requirement records
        for support_type in data.support_needed:
            requirement = Requirement(
                profile_id=profile.id,
                support_type=support_type
            )
            db.add(requirement)

        db.commit()
        db.refresh(profile)

        return profile

    @staticmethod
    def get_profile(db: Session, user_id: int) -> EntrepreneurProfile:
        """Fetch user profile"""
        profile = db.query(EntrepreneurProfile).filter(
            EntrepreneurProfile.user_id == user_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )

        return profile

    @staticmethod
    def update_profile(db: Session, user_id: int, data: ProfileUpdateRequest) -> EntrepreneurProfile:
        """Update user profile"""
        profile = ProfileService.get_profile(db, user_id)

        # Update fields if provided
        update_data = data.model_dump(exclude_unset=True)

        # Handle support_needed separately
        support_needed = update_data.pop('support_needed', None)

        # Update profile fields
        for field, value in update_data.items():
            setattr(profile, field, value)

        # Update requirements if provided
        if support_needed is not None:
            # Delete existing requirements
            db.query(Requirement).filter(Requirement.profile_id == profile.id).delete()

            # Create new requirements
            for support_type in support_needed:
                requirement = Requirement(
                    profile_id=profile.id,
                    support_type=support_type
                )
                db.add(requirement)

        db.commit()
        db.refresh(profile)

        return profile

    @staticmethod
    def get_profile_with_requirements(db: Session, user_id: int) -> dict:
        """Get profile with support needs"""
        profile = ProfileService.get_profile(db, user_id)

        # Get requirements
        requirements = db.query(Requirement).filter(
            Requirement.profile_id == profile.id
        ).all()

        support_needed = [req.support_type for req in requirements]

        return {
            "profile": profile,
            "support_needed": support_needed
        }
