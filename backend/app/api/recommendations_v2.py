"""
Updated Recommendations API endpoint using eligibility-based matching engine
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.entrepreneur import EntrepreneurProfile
from app.models.scheme_v2 import SchemeV2
from app.services.eligibility_engine import MatchingEngineV2
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class RecommendationRequest(BaseModel):
    """Request model for getting recommendations"""
    sector: Optional[str] = None
    state: Optional[str] = None
    business_stage: Optional[str] = None
    annual_income_range: Optional[str] = None
    entrepreneur_type: Optional[str] = None
    support_needs: List[str] = []
    description: Optional[str] = None
    min_score: Optional[float] = 40.0
    max_results: Optional[int] = 15


class SchemeResponse(BaseModel):
    """Response model for scheme in recommendations"""
    id: int
    name: str
    short_name: Optional[str]
    description: str
    scheme_type: str
    ministry: str
    department: Optional[str]

    # Display fields
    primary_sector: str
    business_stages: List[str]
    geographic_scope: str
    states: List[str]

    # Benefits
    benefit_types: List[str]
    benefit_description: str
    maximum_amount: Optional[float]

    # Application
    application_url: Optional[str]
    official_url: Optional[str]

    # Display lists
    eligibility_summary: Optional[List[str]]
    benefits_list: Optional[List[str]]
    application_process: Optional[List[str]]
    required_documents: List[dict]

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    """Single recommendation with match details"""
    scheme: SchemeResponse
    match_score: float
    match_level: str
    matched_criteria: List[str]
    score_breakdown: dict


class RecommendationsListResponse(BaseModel):
    """List of recommendations"""
    recommendations: List[RecommendationResponse]
    total_count: int
    filters_applied: dict


@router.post("", response_model=RecommendationsListResponse)
async def get_recommendations_v2(
    request: RecommendationRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized scheme recommendations using eligibility-based matching.

    Workflow:
    1. Fetch user's entrepreneur profile
    2. Get all active schemes
    3. Apply mandatory eligibility filtering
    4. Calculate relevance scores
    5. Rank and return top matches
    """

    # Get user's profile
    profile = db.query(EntrepreneurProfile).filter(
        EntrepreneurProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete your profile first"
        )

    # Override profile data with request data if provided
    if request.sector:
        profile.business_sector = request.sector
    if request.state:
        profile.state = request.state
    if request.business_stage:
        profile.business_stage = request.business_stage
    if request.annual_income_range:
        profile.annual_income_range = request.annual_income_range

    # Get all active schemes
    schemes = db.query(SchemeV2).filter(
        SchemeV2.status == "active"
    ).all()

    if not schemes:
        return RecommendationsListResponse(
            recommendations=[],
            total_count=0,
            filters_applied={
                "min_score": request.min_score,
                "max_results": request.max_results
            }
        )

    # Extract user requirements from support_needs
    requirements = request.support_needs or []

    # Use eligibility-based matching engine
    recommendations = MatchingEngineV2.get_recommendations(
        schemes=schemes,
        profile=profile,
        requirements=requirements,
        min_relevance_score=request.min_score,
        max_results=request.max_results
    )

    # Format response
    formatted_recommendations = []
    for rec in recommendations:
        scheme = rec["scheme"]

        formatted_recommendations.append(
            RecommendationResponse(
                scheme=SchemeResponse(
                    id=scheme.id,
                    name=scheme.name,
                    short_name=scheme.short_name,
                    description=scheme.description,
                    scheme_type=scheme.scheme_type,
                    ministry=scheme.ministry,
                    department=scheme.department,
                    primary_sector=scheme.primary_sector,
                    business_stages=scheme.business_stages,
                    geographic_scope=scheme.geographic_scope,
                    states=scheme.states,
                    benefit_types=scheme.benefit_types,
                    benefit_description=scheme.benefit_description,
                    maximum_amount=scheme.maximum_amount,
                    application_url=scheme.application_url,
                    official_url=scheme.official_url,
                    eligibility_summary=scheme.eligibility_summary,
                    benefits_list=scheme.benefits_list,
                    application_process=scheme.application_process,
                    required_documents=scheme.required_documents
                ),
                match_score=rec["match_score"],
                match_level=rec["match_level"],
                matched_criteria=rec["matched_criteria"],
                score_breakdown=rec["score_breakdown"]
            )
        )

    return RecommendationsListResponse(
        recommendations=formatted_recommendations,
        total_count=len(formatted_recommendations),
        filters_applied={
            "min_score": request.min_score,
            "max_results": request.max_results,
            "sector": request.sector,
            "state": request.state
        }
    )


@router.get("/schemes/{scheme_id}", response_model=SchemeResponse)
async def get_scheme_details(
    scheme_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific scheme"""

    scheme = db.query(SchemeV2).filter(
        SchemeV2.id == scheme_id,
        SchemeV2.status == "active"
    ).first()

    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )

    return SchemeResponse(
        id=scheme.id,
        name=scheme.name,
        short_name=scheme.short_name,
        description=scheme.description,
        scheme_type=scheme.scheme_type,
        ministry=scheme.ministry,
        department=scheme.department,
        primary_sector=scheme.primary_sector,
        business_stages=scheme.business_stages,
        geographic_scope=scheme.geographic_scope,
        states=scheme.states,
        benefit_types=scheme.benefit_types,
        benefit_description=scheme.benefit_description,
        maximum_amount=scheme.maximum_amount,
        application_url=scheme.application_url,
        official_url=scheme.official_url,
        eligibility_summary=scheme.eligibility_summary,
        benefits_list=scheme.benefits_list,
        application_process=scheme.application_process,
        required_documents=scheme.required_documents
    )


@router.get("/schemes", response_model=List[SchemeResponse])
async def list_all_schemes(
    sector: Optional[str] = None,
    state: Optional[str] = None,
    scheme_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    List all active schemes with optional filtering.
    Note: This returns schemes without personalized matching.
    """

    query = db.query(SchemeV2).filter(SchemeV2.status == "active")

    # Apply filters
    if sector:
        query = query.filter(
            (SchemeV2.primary_sector == sector) | (SchemeV2.primary_sector == "all")
        )

    if scheme_type:
        query = query.filter(SchemeV2.scheme_type == scheme_type)

    # Note: State filtering with JSON array requires database-specific syntax
    # For SQLite, we'll skip this filter in the query

    schemes = query.offset(skip).limit(limit).all()

    # Manual state filtering if provided
    if state:
        schemes = [
            s for s in schemes
            if not s.states or state in s.states or s.geographic_scope == "national"
        ]

    return [
        SchemeResponse(
            id=scheme.id,
            name=scheme.name,
            short_name=scheme.short_name,
            description=scheme.description,
            scheme_type=scheme.scheme_type,
            ministry=scheme.ministry,
            department=scheme.department,
            primary_sector=scheme.primary_sector,
            business_stages=scheme.business_stages,
            geographic_scope=scheme.geographic_scope,
            states=scheme.states,
            benefit_types=scheme.benefit_types,
            benefit_description=scheme.benefit_description,
            maximum_amount=scheme.maximum_amount,
            application_url=scheme.application_url,
            official_url=scheme.official_url,
            eligibility_summary=scheme.eligibility_summary,
            benefits_list=scheme.benefits_list,
            application_process=scheme.application_process,
            required_documents=scheme.required_documents
        )
        for scheme in schemes
    ]
