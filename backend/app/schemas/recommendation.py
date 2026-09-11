"""Recommendation schemas following the Government Schemes Data Structure"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RecommendationRequest(BaseModel):
    """RequestBody for POST /api/recommendations"""
    sector: Optional[str] = None
    state: Optional[str] = None
    business_stage: Optional[str] = None
    annual_income_range: Optional[str] = None
    entrepreneur_type: Optional[str] = None
    support_needs: List[str] = []
    description: Optional[str] = None
    min_score: Optional[float] = Field(40.0, ge=0, le=100)
    max_results: Optional[int] = Field(10, ge=1, le=50)


class SchemeListInfo(BaseModel):
    id: int
    name: str
    short_name: Optional[str] = None
    description: str
    scheme_type: str
    ministry: str
    department: Optional[str] = None
    implementing_agency: Optional[str] = None
    primary_sector: str
    sub_sectors: List[str] = []
    applicant_types: List[str] = []
    business_stages: List[str] = []
    geographic_scope: str = "national"
    states: List[str] = []
    enterprise_categories: List[str] = []
    minimum_business_age_months: Optional[int] = None
    maximum_business_age_months: Optional[int] = None
    minimum_turnover: Optional[float] = None
    maximum_turnover: Optional[float] = None
    minimum_investment: Optional[float] = None
    maximum_investment: Optional[float] = None
    minimum_age: Optional[int] = None
    maximum_age: Optional[int] = None
    gender_eligibility: List[str] = ["any"]
    social_categories: List[str] = ["any"]
    supported_purposes: List[str] = []
    funding_required: bool = False
    benefit_types: List[str] = []
    benefit_description: str = ""
    maximum_amount: Optional[float] = None
    eligibility_rules: List[dict] = []
    required_documents: List[dict] = []
    application_mode: str = "online"
    official_url: Optional[str] = None
    application_url: Optional[str] = None
    source_name: str = ""
    source_url: str = ""
    eligibility_summary: Optional[List[str]] = None
    benefits_list: Optional[List[str]] = None
    application_process: Optional[List[str]] = None

    class Config:
        from_attributes = True


class RecommendationItem(BaseModel):
    scheme_rank: int = Field(..., ge=1)
    scheme: SchemeListInfo
    match_score: float = Field(..., ge=0, le=100)
    match_level: str
    matched_criteria: List[str] = []
    score_breakdown: Dict[str, float] = {}
    possible_gap: Optional[str] = None
    explanation: str = ""


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    total_count: int
    profile_summary: Dict[str, Any]
    filters_applied: Dict[str, Any] = {}


class RecommendationItemLegacy(BaseModel):
    """Legacy flat recommendation shape kept for backward compatibility."""
    scheme_id: int
    scheme_name: str
    match_score: float
    match_level: str
    matched_criteria: List[str]
    possible_gap: Optional[str] = None
    explanation: str = ""
    source_url: Optional[str] = None
    application_url: Optional[str] = None