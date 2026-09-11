"""Entrepreneur profile schemas"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProfileRequest(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=15)
    state: str = Field(..., min_length=1)
    district: str = Field(..., min_length=1)
    age_group: str = Field(..., description="Age group: 18-25, 26-35, 36-45, 46-55, 55+")
    gender: str = Field(..., description="Gender: male, female, other")
    social_category: str = Field(..., description="Social category: general, obc, sc, st")
    business_name: str = Field(..., min_length=1)
    business_sector: str = Field(..., description="Business sector")
    business_stage: str = Field(..., description="Business stage: idea, planning, existing, expanding")
    annual_income_range: str = Field(..., description="Annual income range")
    employee_range: str = Field(..., description="Employee range")
    support_needed: List[str] = Field(..., description="List of support types needed")

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Rajesh Kumar",
                "phone_number": "9876543210",
                "state": "Delhi",
                "district": "New Delhi",
                "age_group": "26-35",
                "gender": "male",
                "social_category": "general",
                "business_name": "ABC Manufacturing",
                "business_sector": "manufacturing",
                "business_stage": "existing",
                "annual_income_range": "10L-25L",
                "employee_range": "5-10",
                "support_needed": ["machinery", "funding"]
            }
        }

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone_number: str
    state: str
    district: str
    age_group: str
    gender: str
    social_category: str
    business_name: str
    business_sector: str
    business_stage: str
    annual_income_range: str
    employee_range: str
    created_at: datetime
    updated_at: datetime
    support_needed: Optional[List[str]] = []

    class Config:
        from_attributes = True

class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    age_group: Optional[str] = None
    gender: Optional[str] = None
    social_category: Optional[str] = None
    business_name: Optional[str] = None
    business_sector: Optional[str] = None
    business_stage: Optional[str] = None
    annual_income_range: Optional[str] = None
    employee_range: Optional[str] = None
    support_needed: Optional[List[str]] = None
