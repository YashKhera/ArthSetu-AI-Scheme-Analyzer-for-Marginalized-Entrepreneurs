"""Serializers that convert SchemeV2 models into the Government Schemes Data Structure."""
from typing import Any, Dict


def serialize_scheme_full(scheme: Any) -> Dict:
    """
    Convert a SchemeV2 row into the complete structured scheme object.

    Matches the "Government Schemes Data Structure" spec:
        basic_info / government / target_beneficiaries / sector / geography /
        business_eligibility / financial_eligibility / founder_eligibility /
        requirements / benefits / eligibility_rules / required_documents /
        application / source / metadata
    """
    return {
        "scheme_id": scheme.id,
        "basic_info": {
            "name": scheme.name,
            "short_name": scheme.short_name,
            "description": scheme.description,
            "scheme_type": scheme.scheme_type,
            "status": scheme.status,
        },
        "government": {
            "ministry": scheme.ministry,
            "department": scheme.department,
            "implementing_agency": scheme.implementing_agency,
        },
        "target_beneficiaries": {
            "applicant_types": scheme.applicant_types or [],
            "business_stages": scheme.business_stages or [],
        },
        "sector": {
            "primary": scheme.primary_sector,
            "sub_sectors": scheme.sub_sectors or [],
        },
        "geography": {
            "scope": scheme.geographic_scope,
            "states": scheme.states or [],
        },
        "business_eligibility": {
            "business_types": scheme.business_types or [],
            "enterprise_categories": scheme.enterprise_categories or [],
            "minimum_business_age_months": scheme.minimum_business_age_months,
            "maximum_business_age_months": scheme.maximum_business_age_months,
        },
        "financial_eligibility": {
            "minimum_turnover": scheme.minimum_turnover,
            "maximum_turnover": scheme.maximum_turnover,
            "minimum_investment": scheme.minimum_investment,
            "maximum_investment": scheme.maximum_investment,
        },
        "founder_eligibility": {
            "minimum_age": scheme.minimum_age,
            "maximum_age": scheme.maximum_age,
            "gender": scheme.gender_eligibility or ["any"],
            "social_categories": scheme.social_categories or ["any"],
        },
        "requirements": {
            "purposes": scheme.supported_purposes or [],
            "funding_required": scheme.funding_required,
        },
        "benefits": {
            "type": scheme.benefit_types or [],
            "description": scheme.benefit_description,
            "maximum_amount": scheme.maximum_amount,
            "currency": scheme.currency,
        },
        "eligibility_rules": scheme.eligibility_rules or [],
        "required_documents": scheme.required_documents or [],
        "application": {
            "mode": scheme.application_mode,
            "official_url": scheme.official_url,
            "application_url": scheme.application_url,
        },
        "source": {
            "source_name": scheme.source_name,
            "source_url": scheme.source_url,
            "last_verified": (
                scheme.last_verified.isoformat() if scheme.last_verified else None
            ),
        },
        "metadata": {
            "created_at": scheme.created_at.isoformat() if scheme.created_at else None,
            "updated_at": scheme.updated_at.isoformat() if scheme.updated_at else None,
            "version": scheme.version,
        },
    }


def serialize_scheme_summary(scheme: Any) -> Dict:
    """Convert a SchemeV2 row into a lightweight card used on results/search pages."""
    return {
        "scheme_id": scheme.id,
        "name": scheme.name,
        "short_name": scheme.short_name,
        "description": scheme.description,
        "scheme_type": scheme.scheme_type,
        "ministry": scheme.ministry,
        "sector": scheme.primary_sector,
        "benefit_types": scheme.benefit_types or [],
        "benefit_description": scheme.benefit_description,
        "maximum_amount": scheme.maximum_amount,
        "geographic_scope": scheme.geographic_scope,
        "states": scheme.states or [],
        "official_url": scheme.official_url,
        "application_url": scheme.application_url,
    }


def serialize_scheme_recommendation(scheme: Any) -> Dict:
    """Convert a SchemeV2 row into the rich shape used inside recommendation items."""
    return {
        "id": scheme.id,
        "name": scheme.name,
        "short_name": scheme.short_name,
        "description": scheme.description,
        "scheme_type": scheme.scheme_type,
        "ministry": scheme.ministry,
        "department": scheme.department,
        "implementing_agency": scheme.implementing_agency,
        "primary_sector": scheme.primary_sector,
        "sub_sectors": scheme.sub_sectors or [],
        "applicant_types": scheme.applicant_types or [],
        "business_stages": scheme.business_stages or [],
        "geographic_scope": scheme.geographic_scope,
        "states": scheme.states or [],
        "enterprise_categories": scheme.enterprise_categories or [],
        "minimum_business_age_months": scheme.minimum_business_age_months,
        "maximum_business_age_months": scheme.maximum_business_age_months,
        "minimum_turnover": scheme.minimum_turnover,
        "maximum_turnover": scheme.maximum_turnover,
        "minimum_investment": scheme.minimum_investment,
        "maximum_investment": scheme.maximum_investment,
        "minimum_age": scheme.minimum_age,
        "maximum_age": scheme.maximum_age,
        "gender_eligibility": scheme.gender_eligibility or ["any"],
        "social_categories": scheme.social_categories or ["any"],
        "supported_purposes": scheme.supported_purposes or [],
        "funding_required": scheme.funding_required,
        "benefit_types": scheme.benefit_types or [],
        "benefit_description": scheme.benefit_description,
        "maximum_amount": scheme.maximum_amount,
        "eligibility_rules": scheme.eligibility_rules or [],
        "required_documents": scheme.required_documents or [],
        "application_mode": scheme.application_mode,
        "official_url": scheme.official_url,
        "application_url": scheme.application_url,
        "source_name": scheme.source_name,
        "source_url": scheme.source_url,
        "eligibility_summary": scheme.eligibility_summary,
        "benefits_list": scheme.benefits_list,
        "application_process": scheme.application_process,
    }