"""Scheme schemas following the Government Schemes Data Structure"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SchemeBasicInfo(BaseModel):
    name: str
    short_name: Optional[str] = None
    description: str
    scheme_type: str
    status: str = "active"


class SchemeGovernmentInfo(BaseModel):
    ministry: str
    department: Optional[str] = None
    implementing_agency: Optional[str] = None


class SchemeTargetBeneficiaries(BaseModel):
    applicant_types: List[str]
    business_stages: List[str]


class SchemeSectorInfo(BaseModel):
    primary: str
    sub_sectors: List[str] = []


class SchemeGeographicEligibility(BaseModel):
    scope: str = "national"
    states: List[str] = []


class SchemeBusinessEligibility(BaseModel):
    business_types: List[str] = []
    enterprise_categories: List[str] = []
    minimum_business_age_months: Optional[int] = None
    maximum_business_age_months: Optional[int] = None


class SchemeFinancialEligibility(BaseModel):
    minimum_turnover: Optional[float] = None
    maximum_turnover: Optional[float] = None
    minimum_investment: Optional[float] = None
    maximum_investment: Optional[float] = None


class SchemeFounderEligibility(BaseModel):
    minimum_age: Optional[int] = None
    maximum_age: Optional[int] = None
    gender: List[str] = ["any"]
    social_categories: List[str] = ["any"]


class SchemeRequirements(BaseModel):
    purposes: List[str] = []
    funding_required: bool = False


class SchemeBenefits(BaseModel):
    type: List[str] = []
    description: str = ""
    maximum_amount: Optional[float] = None
    currency: str = "INR"


class SchemeApplicationInfo(BaseModel):
    mode: str = "online"
    official_url: Optional[str] = None
    application_url: Optional[str] = None


class SchemeSourceInfo(BaseModel):
    source_name: str
    source_url: str
    last_verified: Optional[datetime] = None


class SchemeMetadata(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: int = 1


class SchemeDocument(BaseModel):
    name: str
    mandatory: bool = True


class SchemeResponse(BaseModel):
    """Full structured scheme response following the Government Data Structure."""
    scheme_id: int
    basic_info: SchemeBasicInfo
    government: SchemeGovernmentInfo
    target_beneficiaries: SchemeTargetBeneficiaries
    sector: SchemeSectorInfo
    geography: SchemeGeographicEligibility
    business_eligibility: SchemeBusinessEligibility
    financial_eligibility: SchemeFinancialEligibility
    founder_eligibility: SchemeFounderEligibility
    requirements: SchemeRequirements
    benefits: SchemeBenefits
    eligibility_rules: List[dict] = []
    required_documents: List[SchemeDocument] = []
    application: SchemeApplicationInfo
    source: SchemeSourceInfo
    metadata: SchemeMetadata


class SchemeSummaryResponse(BaseModel):
    """Lightweight scheme representation for list views (results page cards)."""
    scheme_id: int
    name: str
    short_name: Optional[str] = None
    description: str
    scheme_type: str
    ministry: str
    sector: str
    benefit_types: List[str] = []
    benefit_description: str = ""
    maximum_amount: Optional[float] = None
    geographic_scope: str = "national"
    states: List[str] = []
    official_url: Optional[str] = None
    application_url: Optional[str] = None
    match_score: Optional[float] = None
    match_level: Optional[str] = None
    matched_criteria: List[str] = []


class SchemeListResponse(BaseModel):
    schemes: List[SchemeSummaryResponse]
    total: int