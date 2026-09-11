"""Recommendations router - Core matching endpoint using eligibility-based engine"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.entrepreneur import EntrepreneurProfile
from app.models.scheme_v2 import SchemeV2
from app.models.requirement import Requirement
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationItem,
    SchemeListInfo,
)
from app.services.eligibility_engine import MatchingEngineV2
from app.services.ai_service import AIService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.serializers import serialize_scheme_recommendation

router = APIRouter()


def _get_or_build_profile(db: Session, user_id: int, data: RecommendationRequest):
    """
    Fetch the user's saved profile, patching it with any inline request data.
    Falls back to a temporary in-memory profile when none exists yet.
    """
    profile = db.query(EntrepreneurProfile).filter(
        EntrepreneurProfile.user_id == user_id
    ).first()

    if profile is None:
        profile = EntrepreneurProfile(
            user_id=user_id,
            full_name="",
            phone_number="",
            state=data.state or "",
            district="",
            age_group="26-35",
            gender=(
                "female" if data.entrepreneur_type in ("women", "female") else
                "male" if data.entrepreneur_type == "male" else "other"
            ),
            social_category=(
                data.entrepreneur_type if data.entrepreneur_type in ("general", "obc", "sc", "st")
                else "general"
            ),
            business_name="",
            business_sector=data.sector or "",
            business_stage=data.business_stage or "idea",
            annual_income_range=data.annual_income_range or "5L-10L",
            employee_range="1-5",
        )

    # Patch existing profile with request overrides
    if data.sector:
        profile.business_sector = data.sector
    if data.state:
        profile.state = data.state
    if data.business_stage:
        profile.business_stage = data.business_stage
    if data.annual_income_range:
        profile.annual_income_range = data.annual_income_range

    return profile


@router.post("/recommendations", response_model=RecommendationResponse)
def get_recommendations(
    data: RecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get personalized scheme recommendations.

    Workflow (per Government Schemes Data Structure):
    1. Build/normalize the user profile
    2. Mandatory eligibility filter (hard filter)
    3. Relevance matching
    4. Ranking by score
    5. AI or rule-based explanation for each top match
    """
    profile = _get_or_build_profile(db, current_user.id, data)

    requirements = data.support_needs or []
    if not requirements:
        # Pull stored requirements from profile if available
        stored = db.query(Requirement).filter(
            Requirement.profile_id == profile.id
        ).all() if profile.id else []
        requirements = [r.support_type for r in stored]

    schemes = db.query(SchemeV2).filter(SchemeV2.status == "active").all()

    ranked = MatchingEngineV2.get_recommendations(
        schemes=schemes,
        profile=profile,
        requirements=requirements,
        min_relevance_score=data.min_score,
        max_results=data.max_results,
    )

    ai_service = AIService()
    items: List[RecommendationItem] = []

    for rank, rec in enumerate(ranked, start=1):
        scheme = rec["scheme"]
        scheme_dict = serialize_scheme_recommendation(scheme)

        explanation = ""
        try:
            explanation = ai_service.generate_explanation_v2(
                profile_data={
                    "sector": profile.business_sector,
                    "state": profile.state,
                    "stage": profile.business_stage,
                    "name": profile.full_name,
                },
                scheme=scheme,
                matched_criteria=rec["matched_criteria"],
                score=rec["match_score"],
            )
        except Exception:
            explanation = ai_service._generate_fallback_explanation_v2(
                scheme, rec["matched_criteria"], rec["match_score"]
            )

        items.append(
            RecommendationItem(
                scheme_rank=rank,
                scheme=SchemeListInfo(**scheme_dict),
                match_score=rec["match_score"],
                match_level=rec["match_level"],
                matched_criteria=rec["matched_criteria"],
                score_breakdown=rec["score_breakdown"],
                possible_gap=None,
                explanation=explanation,
            )
        )

    profile_summary = {
        "sector": profile.business_sector,
        "state": profile.state,
        "business_stage": profile.business_stage,
        "annual_income_range": profile.annual_income_range,
        "entrepreneur_type": data.entrepreneur_type,
        "support_needs": requirements,
    }

    return RecommendationResponse(
        recommendations=items,
        total_count=len(items),
        profile_summary=profile_summary,
        filters_applied={
            "min_score": data.min_score,
            "max_results": data.max_results,
        },
    )