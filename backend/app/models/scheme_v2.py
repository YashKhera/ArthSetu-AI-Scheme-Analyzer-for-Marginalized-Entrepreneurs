"""Enhanced Scheme model following comprehensive data structure"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SchemeV2(Base):
    """
    Comprehensive scheme model with structured eligibility knowledge base.
    Follows the principle: Government Scheme → Eligibility → Matching → Recommendation
    """
    __tablename__ = "schemes_v2"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Information
    name = Column(String, index=True, nullable=False)
    short_name = Column(String, nullable=True)
    description = Column(String, nullable=False)
    scheme_type = Column(String, nullable=False, index=True)  # funding, loan, subsidy, grant, etc.
    status = Column(String, default="active", index=True)  # active, inactive, suspended

    # Government Information
    ministry = Column(String, nullable=False)
    department = Column(String, nullable=True)
    implementing_agency = Column(String, nullable=True)

    # Target Beneficiaries (JSON arrays)
    applicant_types = Column(JSON, nullable=False)  # ["startup", "msme", "entrepreneur"]
    business_stages = Column(JSON, nullable=False)  # ["idea", "early_stage", "growth"]

    # Sector Information (JSON)
    primary_sector = Column(String, nullable=False, index=True)
    sub_sectors = Column(JSON, nullable=True)  # ["software", "it", "innovation"]

    # Geographic Eligibility (JSON)
    geographic_scope = Column(String, nullable=False)  # national, state, district
    states = Column(JSON, nullable=False)  # ["Delhi", "Maharashtra"] or [] for national

    # Business Eligibility (JSON)
    business_types = Column(JSON, nullable=True)  # ["private_limited", "llp", "partnership"]
    enterprise_categories = Column(JSON, nullable=True)  # ["micro", "small", "medium"]
    minimum_business_age_months = Column(Integer, nullable=True)
    maximum_business_age_months = Column(Integer, nullable=True)

    # Financial Eligibility
    minimum_turnover = Column(Float, nullable=True)
    maximum_turnover = Column(Float, nullable=True)
    minimum_investment = Column(Float, nullable=True)
    maximum_investment = Column(Float, nullable=True)

    # Founder Eligibility (JSON)
    minimum_age = Column(Integer, nullable=True)
    maximum_age = Column(Integer, nullable=True)
    gender_eligibility = Column(JSON, nullable=True)  # ["any"] or ["female", "male"]
    social_categories = Column(JSON, nullable=True)  # ["any"] or ["sc", "st", "obc"]

    # Requirements (JSON)
    supported_purposes = Column(JSON, nullable=False)  # ["working_capital", "expansion"]
    funding_required = Column(Boolean, default=True)

    # Benefits (JSON)
    benefit_types = Column(JSON, nullable=False)  # ["loan", "subsidy", "grant"]
    benefit_description = Column(String, nullable=False)
    maximum_amount = Column(Float, nullable=True)
    currency = Column(String, default="INR")

    # Eligibility Rules (JSON array of rule objects)
    eligibility_rules = Column(JSON, nullable=True)
    """
    Example:
    [
        {
            "field": "sector.primary",
            "operator": "equals",
            "value": "technology",
            "required": true
        }
    ]
    """

    # Required Documents (JSON array)
    required_documents = Column(JSON, nullable=False)
    """
    Example:
    [
        {"name": "PAN Card", "mandatory": true},
        {"name": "Aadhaar", "mandatory": true}
    ]
    """

    # Application Information
    application_mode = Column(String, nullable=False)  # online, offline, online_and_offline
    official_url = Column(String, nullable=True)
    application_url = Column(String, nullable=True)

    # Source Information (JSON)
    source_name = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    last_verified = Column(DateTime, nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)

    # Additional display fields
    eligibility_summary = Column(JSON, nullable=True)  # Human-readable eligibility points
    benefits_list = Column(JSON, nullable=True)  # Human-readable benefits list
    application_process = Column(JSON, nullable=True)  # Step-by-step application process

    def __repr__(self):
        return f"<SchemeV2 {self.name} - {self.status}>"


class EligibilityRule(Base):
    """
    Separate table for complex eligibility rules if needed.
    Can be used for advanced rule evaluation.
    """
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(Integer, index=True, nullable=False)

    field = Column(String, nullable=False)  # "sector.primary", "business.turnover"
    operator = Column(String, nullable=False)  # equals, contains, greater_than, etc.
    value = Column(String, nullable=False)  # The value to compare against
    required = Column(Boolean, default=True)  # Is this a mandatory rule?

    rule_type = Column(String, default="eligibility")  # eligibility, preference, ranking
    weight = Column(Integer, default=0)  # For ranking/scoring

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EligibilityRule {self.field} {self.operator} {self.value}>"
