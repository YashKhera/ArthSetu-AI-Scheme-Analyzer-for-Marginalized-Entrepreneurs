"""
Comprehensive Government Schemes Seed Data
Following structured eligibility knowledge base approach
"""
import sys
import os

# Ensure the backend directory is on the path so `app` imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.scheme_v2 import SchemeV2
from app.database import SessionLocal

# ---------------------------------------------------------------------------
# Helper to build scheme dicts compactly with sensible defaults
# ---------------------------------------------------------------------------
_DT = datetime(2026, 9, 7)
_DEFAULT_DOCS = [
    {"name": "Aadhaar Card", "mandatory": True},
    {"name": "PAN Card", "mandatory": True},
    {"name": "Bank account details", "mandatory": True},
    {"name": "Udyam Registration (if applicable)", "mandatory": False},
]


def _scheme(
    name,
    scheme_type,
    ministry,
    primary_sector,
    business_stages,
    supported_purposes,
    benefit_types,
    benefit_description,
    maximum_amount=None,
    short_name=None,
    description=None,
    department=None,
    implementing_agency=None,
    applicant_types=None,
    sub_sectors=None,
    geographic_scope="national",
    states=None,
    business_types=None,
    enterprise_categories=None,
    min_age=18,
    max_age=None,
    gender_eligibility=None,
    social_categories=None,
    funding_required=True,
    eligibility_rules=None,
    required_documents=None,
    application_mode="online",
    official_url=None,
    application_url=None,
    source=None,
    minimum_turnover=None,
    maximum_turnover=None,
    minimum_investment=None,
    maximum_investment=None,
    min_business_age=0,
    max_business_age=None,
    eligibility_summary=None,
    benefits_list=None,
    application_process=None,
):
    """Return a SchemeV2-compatible seed dict with GOVT-data-structure defaults."""
    return {
        "name": name,
        "short_name": short_name,
        "description": description or f"{name}: {benefit_description}",
        "scheme_type": scheme_type,
        "status": "active",
        "ministry": ministry,
        "department": department or ministry,
        "implementing_agency": implementing_agency or ministry,
        "applicant_types": applicant_types or ["entrepreneur", "msme"],
        "business_stages": business_stages,
        "primary_sector": primary_sector,
        "sub_sectors": sub_sectors or [],
        "geographic_scope": geographic_scope,
        "states": states or [],
        "business_types": business_types or ["any"],
        "enterprise_categories": enterprise_categories or ["micro", "small", "medium"],
        "minimum_business_age_months": min_business_age,
        "maximum_business_age_months": max_business_age,
        "minimum_turnover": minimum_turnover,
        "maximum_turnover": maximum_turnover,
        "minimum_investment": minimum_investment,
        "maximum_investment": maximum_investment,
        "minimum_age": min_age,
        "maximum_age": max_age,
        "gender_eligibility": gender_eligibility or ["any"],
        "social_categories": social_categories or ["any"],
        "supported_purposes": supported_purposes,
        "funding_required": funding_required,
        "benefit_types": benefit_types,
        "benefit_description": benefit_description,
        "maximum_amount": maximum_amount,
        "currency": "INR",
        "eligibility_rules": eligibility_rules or [],
        "required_documents": required_documents or _DEFAULT_DOCS,
        "application_mode": application_mode,
        "official_url": official_url,
        "application_url": application_url or official_url,
        "source_name": source or ministry,
        "source_url": official_url or "",
        "last_verified": _DT,
        "eligibility_summary": eligibility_summary or [
            "Indian citizen",
            f"Aged {min_age} or above" if min_age else "Indian citizen",
            "Business located in India",
        ],
        "benefits_list": benefits_list or [benefit_description],
        "application_process": application_process or [
            "Check eligibility criteria online",
            "Prepare the required documents",
            "Apply on the official portal",
            "Track application status and complete verification",
        ],
    }


# Comprehensive schemes data following the new structure
SCHEMES_DATA_V2 = [
    {
        # Basic Information
        "name": "PM MUDRA Yojana",
        "short_name": "MUDRA",
        "description": "Pradhan Mantri MUDRA Yojana provides collateral-free loans up to Rs. 10 Lakh to non-corporate, non-farm small/micro enterprises through three categories: Shishu (up to ₹50,000), Kishore (₹50,001 to ₹5 lakh), and Tarun (₹5,00,001 to ₹10 lakh).",
        "scheme_type": "loan",
        "status": "active",

        # Government Information
        "ministry": "Ministry of Finance",
        "department": "Department of Financial Services",
        "implementing_agency": "MUDRA Ltd",

        # Target Beneficiaries
        "applicant_types": ["msme", "entrepreneur", "individual", "self_help_group"],
        "business_stages": ["early_stage", "growth", "established"],

        # Sector Information
        "primary_sector": "all",
        "sub_sectors": ["retail", "services", "manufacturing", "food_processing", "textile", "handicrafts"],

        # Geographic Eligibility
        "geographic_scope": "national",
        "states": [],

        # Business Eligibility
        "business_types": ["sole_proprietorship", "partnership", "llp", "private_limited", "individual"],
        "enterprise_categories": ["micro", "small"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": None,

        # Financial Eligibility
        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        # Founder Eligibility
        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["any"],
        "social_categories": ["any"],

        # Requirements
        "supported_purposes": ["working_capital", "business_start", "business_expansion", "equipment_purchase"],
        "funding_required": True,

        # Benefits
        "benefit_types": ["loan"],
        "benefit_description": "Collateral-free loan up to Rs. 10 Lakh with flexible repayment terms and government guarantee coverage",
        "maximum_amount": 1000000,
        "currency": "INR",

        # Eligibility Rules
        "eligibility_rules": [
            {"field": "founder.age", "operator": "greater_than_or_equal", "value": 18, "required": True},
            {"field": "business.sector", "operator": "not_equals", "value": "agriculture", "required": True}
        ],

        # Required Documents
        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True},
            {"name": "PAN Card", "mandatory": True},
            {"name": "Business plan or proposal", "mandatory": True},
            {"name": "Bank account details", "mandatory": True},
            {"name": "Identity and address proof", "mandatory": True}
        ],

        # Application Information
        "application_mode": "online_and_offline",
        "official_url": "https://www.mudra.org.in",
        "application_url": "https://www.mudra.org.in",

        # Source Information
        "source_name": "MUDRA Official Website",
        "source_url": "https://www.mudra.org.in",
        "last_verified": datetime(2026, 9, 7),

        # Display fields
        "eligibility_summary": [
            "Indian citizen aged 18 years or above",
            "Non-farm business activity",
            "No existing loan default",
            "Valid bank account"
        ],
        "benefits_list": [
            "Collateral-free loan up to Rs. 10 Lakh",
            "Zero processing fee",
            "Government guarantee coverage",
            "Flexible repayment terms"
        ],
        "application_process": [
            "Visit nearest bank or MUDRA portal",
            "Fill application form with business details",
            "Submit required documents",
            "Bank will assess and approve",
            "Loan disbursed to bank account"
        ]
    },
    {
        # Stand-Up India Scheme
        "name": "Stand-Up India Scheme",
        "short_name": "Stand-Up India",
        "description": "Stand-Up India facilitates bank loans between Rs. 10 lakh and Rs. 1 Crore to SC/ST and women entrepreneurs for setting up greenfield enterprises in manufacturing, services, or trading sector.",
        "scheme_type": "loan",
        "status": "active",

        "ministry": "Ministry of Finance",
        "department": "Department of Financial Services",
        "implementing_agency": "SIDBI",

        "applicant_types": ["entrepreneur", "startup"],
        "business_stages": ["idea", "early_stage"],

        "primary_sector": "all",
        "sub_sectors": ["manufacturing", "services", "retail"],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["sole_proprietorship", "partnership", "llp", "private_limited"],
        "enterprise_categories": ["micro", "small"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": 0,  # Greenfield only

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["female", "male"],
        "social_categories": ["sc", "st", "women"],

        "supported_purposes": ["business_start", "equipment_purchase", "working_capital"],
        "funding_required": True,

        "benefit_types": ["loan", "credit_guarantee"],
        "benefit_description": "Composite loan between Rs. 10 lakh to Rs. 1 Crore with credit guarantee and handholding support",
        "maximum_amount": 10000000,
        "currency": "INR",

        "eligibility_rules": [
            {"field": "founder.age", "operator": "greater_than_or_equal", "value": 18, "required": True},
            {"field": "business.stage", "operator": "in", "value": ["idea", "early_stage"], "required": True}
        ],

        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True},
            {"name": "PAN Card", "mandatory": True},
            {"name": "Caste certificate (for SC/ST)", "mandatory": False},
            {"name": "Project report", "mandatory": True},
            {"name": "Business registration documents", "mandatory": True}
        ],

        "application_mode": "online",
        "official_url": "https://www.standupmitra.in",
        "application_url": "https://www.standupmitra.in",

        "source_name": "Stand-Up India Portal",
        "source_url": "https://www.standupmitra.in",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "SC/ST or Woman entrepreneur",
            "Aged 18 years or above",
            "Greenfield project (first-time venture)",
            "Non-farm sector enterprise"
        ],
        "benefits_list": [
            "Loan between Rs. 10 lakh to Rs. 1 Crore",
            "Composite loan (term + working capital)",
            "Credit guarantee coverage (CGFSSI)",
            "Handholding support via Stand-Up Connect"
        ],
        "application_process": [
            "Register on Stand-Up India portal",
            "Complete online application form",
            "Upload project report and documents",
            "Submit to nearest bank branch",
            "Bank assessment and approval",
            "Loan disbursement"
        ]
    },
    {
        # PMEGP
        "name": "Prime Minister's Employment Generation Programme",
        "short_name": "PMEGP",
        "description": "PMEGP is a credit-linked subsidy programme for establishing micro enterprises in the non-farm sector. Provides 15-35% subsidy on project cost.",
        "scheme_type": "subsidy",
        "status": "active",

        "ministry": "Ministry of MSME",
        "department": "Khadi and Village Industries Commission (KVIC)",
        "implementing_agency": "KVIC",

        "applicant_types": ["entrepreneur", "self_help_group", "individual"],
        "business_stages": ["idea", "early_stage"],

        "primary_sector": "all",
        "sub_sectors": ["manufacturing", "services", "retail", "food_processing", "textile", "handicrafts"],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["sole_proprietorship", "partnership", "cooperative", "self_help_group"],
        "enterprise_categories": ["micro"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": 0,

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": 5000000,  # 50 lakh for manufacturing

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["any"],
        "social_categories": ["any"],

        "supported_purposes": ["business_start", "equipment_purchase"],
        "funding_required": True,

        "benefit_types": ["subsidy", "loan"],
        "benefit_description": "15-35% subsidy on project cost with easy bank loan facility. Maximum project cost: Rs. 50 lakh (manufacturing), Rs. 20 lakh (services)",
        "maximum_amount": 1750000,  # 35% of 50 lakh
        "currency": "INR",

        "eligibility_rules": [
            {"field": "founder.age", "operator": "greater_than_or_equal", "value": 18, "required": True},
            {"field": "business.stage", "operator": "equals", "value": "idea", "required": False}
        ],

        "required_documents": [
            {"name": "Educational certificates", "mandatory": True},
            {"name": "Aadhaar Card", "mandatory": True},
            {"name": "PAN Card", "mandatory": True},
            {"name": "Caste certificate (if applicable)", "mandatory": False},
            {"name": "Project report", "mandatory": True},
            {"name": "Bank account details", "mandatory": True}
        ],

        "application_mode": "online",
        "official_url": "https://www.kviconline.gov.in/pmegpeportal",
        "application_url": "https://www.kviconline.gov.in/pmegpeportal/jsp/pmegponline.jsp",

        "source_name": "KVIC PMEGP Portal",
        "source_url": "https://www.kviconline.gov.in/pmegpeportal",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "Applicant above 18 years",
            "Minimum 8th pass for projects above Rs. 10 lakh",
            "New enterprise (not existing business)",
            "No income limit"
        ],
        "benefits_list": [
            "15-35% subsidy on project cost",
            "General category: 25% (urban), 35% (rural)",
            "Special category: 35% everywhere",
            "Easy bank loan with subsidy"
        ],
        "application_process": [
            "Register on PMEGP portal",
            "Fill application with project details",
            "Upload required documents",
            "Submit to implementing agency",
            "Interview and assessment",
            "Bank loan sanctioning",
            "Subsidy disbursement post project setup"
        ]
    },
    {
        # PMFME
        "name": "PM Formalization of Micro Food Processing Enterprises",
        "short_name": "PMFME",
        "description": "PMFME Scheme provides financial, technical and business support for up-gradation of existing micro food processing enterprises with 35% credit-linked capital subsidy.",
        "scheme_type": "subsidy",
        "status": "active",

        "ministry": "Ministry of Food Processing Industries",
        "department": "Ministry of Food Processing Industries",
        "implementing_agency": "State/UT Governments",

        "applicant_types": ["msme", "entrepreneur", "self_help_group"],
        "business_stages": ["established", "growth"],

        "primary_sector": "food_processing",
        "sub_sectors": ["agriculture", "food_processing"],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["sole_proprietorship", "partnership", "llp", "private_limited", "cooperative", "self_help_group"],
        "enterprise_categories": ["micro"],
        "minimum_business_age_months": 1,
        "maximum_business_age_months": None,

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["any"],
        "social_categories": ["any"],

        "supported_purposes": ["business_expansion", "technology_upgrade", "equipment_purchase"],
        "funding_required": True,

        "benefit_types": ["subsidy", "training"],
        "benefit_description": "35% credit-linked capital subsidy up to Rs. 10 lakh with training and marketing support",
        "maximum_amount": 1000000,
        "currency": "INR",

        "eligibility_rules": [
            {"field": "business.sector", "operator": "equals", "value": "food_processing", "required": True},
            {"field": "business.stage", "operator": "in", "value": ["established", "growth"], "required": True}
        ],

        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True},
            {"name": "Udyam Registration Certificate", "mandatory": True},
            {"name": "Bank account details", "mandatory": True},
            {"name": "FSSAI license", "mandatory": True},
            {"name": "Business proof", "mandatory": True},
            {"name": "Project report", "mandatory": True}
        ],

        "application_mode": "online",
        "official_url": "https://pmfme.mofpi.gov.in",
        "application_url": "https://pmfme.mofpi.gov.in",

        "source_name": "PMFME Official Portal",
        "source_url": "https://pmfme.mofpi.gov.in",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "Existing food processing micro enterprise",
            "Udyam registration mandatory",
            "FSSAI license required",
            "Aadhaar card mandatory"
        ],
        "benefits_list": [
            "35% capital subsidy (max Rs. 10 lakh)",
            "Training and capacity building",
            "Cluster-based branding support",
            "Marketing and market linkage support"
        ],
        "application_process": [
            "Register on PMFME portal",
            "Complete online application",
            "Upload Udyam & FSSAI certificates",
            "Submit project proposal",
            "State agency verification",
            "Bank loan processing",
            "Subsidy release after project completion"
        ]
    },
    {
        # Startup India Seed Fund
        "name": "Startup India Seed Fund Scheme",
        "short_name": "SISFS",
        "description": "Startup India Seed Fund Scheme provides financial assistance up to Rs. 50 lakh to DPIIT-recognized startups for proof of concept, prototype development, product trials, and market entry.",
        "scheme_type": "grant",
        "status": "active",

        "ministry": "Department for Promotion of Industry and Internal Trade",
        "department": "DPIIT",
        "implementing_agency": "Selected incubators",

        "applicant_types": ["startup"],
        "business_stages": ["idea", "early_stage"],

        "primary_sector": "technology",
        "sub_sectors": ["software", "hardware", "innovation", "manufacturing", "services"],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["private_limited", "llp"],
        "enterprise_categories": ["startup"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": 24,

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["any"],
        "social_categories": ["any"],

        "supported_purposes": ["research_development", "business_start", "technology_upgrade"],
        "funding_required": True,

        "benefit_types": ["grant", "financial_assistance"],
        "benefit_description": "Seed funding up to Rs. 50 lakh for proof of concept, prototype, and validation",
        "maximum_amount": 5000000,
        "currency": "INR",

        "eligibility_rules": [
            {"field": "business.stage", "operator": "in", "value": ["idea", "early_stage"], "required": True}
        ],

        "required_documents": [
            {"name": "Certificate of Incorporation", "mandatory": True},
            {"name": "DPIIT Recognition Number", "mandatory": True},
            {"name": "Pitch deck", "mandatory": True},
            {"name": "Business plan", "mandatory": True},
            {"name": "Identity proofs of founders", "mandatory": True}
        ],

        "application_mode": "online",
        "official_url": "https://seedfund.startupindia.gov.in",
        "application_url": "https://seedfund.startupindia.gov.in",

        "source_name": "Startup India Portal",
        "source_url": "https://seedfund.startupindia.gov.in",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "DPIIT recognized startup",
            "Incorporated not more than 2 years ago",
            "Working on innovation/product development",
            "Potential for scale and impact"
        ],
        "benefits_list": [
            "Seed funding up to Rs. 50 lakh",
            "Proof of concept grant support",
            "Prototype development funding",
            "Market validation support"
        ],
        "application_process": [
            "Get DPIIT startup recognition",
            "Apply through eligible incubator",
            "Submit pitch deck and business plan",
            "Selection committee review",
            "Due diligence process",
            "Grant agreement signing",
            "Milestone-based fund release"
        ]
    },
    {
        # CGTMSE
        "name": "Credit Guarantee Fund for Micro and Small Enterprises",
        "short_name": "CGTMSE",
        "description": "CGTMSE provides guarantee cover for collateral-free credit facilities extended by banks to MSMEs up to Rs. 5 Crore.",
        "scheme_type": "credit_support",
        "status": "active",

        "ministry": "Ministry of MSME",
        "department": "Ministry of MSME",
        "implementing_agency": "CGTMSE Trust",

        "applicant_types": ["msme"],
        "business_stages": ["established", "growth", "expansion"],

        "primary_sector": "all",
        "sub_sectors": [],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["sole_proprietorship", "partnership", "llp", "private_limited"],
        "enterprise_categories": ["micro", "small"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": None,

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["any"],
        "social_categories": ["any"],

        "supported_purposes": ["working_capital", "business_expansion", "equipment_purchase"],
        "funding_required": True,

        "benefit_types": ["credit_guarantee"],
        "benefit_description": "Collateral-free loans up to Rs. 5 Crore with credit guarantee coverage up to 85%",
        "maximum_amount": 50000000,
        "currency": "INR",

        "eligibility_rules": [],

        "required_documents": [
            {"name": "Udyam Registration", "mandatory": True},
            {"name": "Project report", "mandatory": True},
            {"name": "Bank account statements", "mandatory": True},
            {"name": "ITR (if applicable)", "mandatory": False},
            {"name": "Identity and address proof", "mandatory": True}
        ],

        "application_mode": "offline",
        "official_url": "https://www.cgtmse.in",
        "application_url": "https://www.cgtmse.in",

        "source_name": "CGTMSE Official Website",
        "source_url": "https://www.cgtmse.in",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "Micro or Small Enterprise",
            "Credit facility up to Rs. 5 Crore",
            "Loan from eligible lending institution",
            "No collateral/third party guarantee"
        ],
        "benefits_list": [
            "Collateral-free loans up to Rs. 5 Crore",
            "Credit guarantee coverage up to 85%",
            "Reduced documentation",
            "Faster loan processing"
        ],
        "application_process": [
            "Apply for loan at eligible bank",
            "Bank initiates CGTMSE guarantee",
            "Loan assessment by bank",
            "CGTMSE guarantee approval",
            "Loan sanctioning and disbursement"
        ]
    },
    {
        # National SC-ST Hub
        "name": "National SC-ST Hub Scheme",
        "short_name": "SC-ST Hub",
        "description": "National SC-ST Hub facilitates and supports SC/ST entrepreneurs for setting up and scaling micro, small and medium manufacturing and service enterprises.",
        "scheme_type": "training",
        "status": "active",

        "ministry": "Ministry of MSME",
        "department": "Ministry of MSME",
        "implementing_agency": "NSIC",

        "applicant_types": ["entrepreneur", "msme"],
        "business_stages": ["early_stage", "established", "growth"],

        "primary_sector": "all",
        "sub_sectors": [],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["any"],
        "enterprise_categories": ["micro", "small", "medium"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": None,

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["any"],
        "social_categories": ["sc", "st"],

        "supported_purposes": ["training", "skill_development", "marketing", "market_access"],
        "funding_required": False,

        "benefit_types": ["training", "mentorship", "market_access"],
        "benefit_description": "Marketing support, technology support, training, and tender information for SC/ST entrepreneurs",
        "maximum_amount": None,
        "currency": "INR",

        "eligibility_rules": [
            {"field": "founder.social_category", "operator": "in", "value": ["sc", "st"], "required": True}
        ],

        "required_documents": [
            {"name": "Caste certificate (SC/ST)", "mandatory": True},
            {"name": "Aadhaar Card", "mandatory": True},
            {"name": "PAN Card", "mandatory": True},
            {"name": "Udyam Registration", "mandatory": True},
            {"name": "Business registration documents", "mandatory": True}
        ],

        "application_mode": "online",
        "official_url": "https://www.scsthub.in",
        "application_url": "https://www.scsthub.in",

        "source_name": "National SC-ST Hub Portal",
        "source_url": "https://www.scsthub.in",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "Must belong to SC/ST category",
            "Registered MSME",
            "Caste certificate mandatory",
            "Indian citizen"
        ],
        "benefits_list": [
            "Marketing and tender support",
            "Technology and skill training",
            "Networking opportunities",
            "Government procurement facilitation"
        ],
        "application_process": [
            "Register on SC-ST Hub portal",
            "Upload caste certificate and MSME registration",
            "Complete business profile",
            "Access training and support programs",
            "Apply for tender opportunities"
        ]
    },
    {
        # Women Entrepreneurship Platform
        "name": "Women Entrepreneurship Platform",
        "short_name": "WEP",
        "description": "Women Entrepreneurship Platform brings together government schemes, private partnerships, and resources to support women entrepreneurs with mentorship, funding, and skilling opportunities.",
        "scheme_type": "training",
        "status": "active",

        "ministry": "NITI Aayog",
        "department": "NITI Aayog",
        "implementing_agency": "NITI Aayog",

        "applicant_types": ["women_entrepreneur", "entrepreneur"],
        "business_stages": ["idea", "early_stage", "growth", "established"],

        "primary_sector": "all",
        "sub_sectors": [],

        "geographic_scope": "national",
        "states": [],

        "business_types": ["any"],
        "enterprise_categories": ["any"],
        "minimum_business_age_months": 0,
        "maximum_business_age_months": None,

        "minimum_turnover": None,
        "maximum_turnover": None,
        "minimum_investment": None,
        "maximum_investment": None,

        "minimum_age": 18,
        "maximum_age": None,
        "gender_eligibility": ["female"],
        "social_categories": ["any"],

        "supported_purposes": ["training", "skill_development", "mentorship", "business_start"],
        "funding_required": False,

        "benefit_types": ["training", "mentorship", "market_access"],
        "benefit_description": "Mentorship from successful entrepreneurs, access to incubators, networking, and information on funding schemes",
        "maximum_amount": None,
        "currency": "INR",

        "eligibility_rules": [
            {"field": "founder.gender", "operator": "equals", "value": "female", "required": True}
        ],

        "required_documents": [
            {"name": "Aadhaar Card", "mandatory": True},
            {"name": "PAN Card", "mandatory": True},
            {"name": "Business plan", "mandatory": False},
            {"name": "Educational certificates", "mandatory": False}
        ],

        "application_mode": "online",
        "official_url": "https://wep.gov.in",
        "application_url": "https://wep.gov.in",

        "source_name": "WEP Official Portal",
        "source_url": "https://wep.gov.in",
        "last_verified": datetime(2026, 9, 7),

        "eligibility_summary": [
            "Must be a woman entrepreneur",
            "Indian citizen",
            "Business idea or existing business",
            "Any age above 18"
        ],
        "benefits_list": [
            "Mentorship from successful entrepreneurs",
            "Access to incubators and accelerators",
            "Networking opportunities",
            "Information on funding schemes"
        ],
        "application_process": [
            "Register on WEP portal",
            "Complete entrepreneur profile",
            "Browse available programs and resources",
            "Connect with mentors",
            "Access training modules",
            "Apply for relevant schemes"
        ]
    },

    _scheme(
        "SIDBI SMILE Loan Scheme", "loan", "SIDBI", "all",
        ["early_stage", "growth", "established"],
        ["working_capital", "business_expansion", "equipment_purchase"],
        ["loan"], "Collateral-free loans up to ₹1 crore for new and existing MSMEs for machinery, expansion, and working capital.",
        10000000,
        short_name="SMILE", department="SIDBI", implementing_agency="SIDBI",
        applicant_types=["msme", "entrepreneur"],
        enterprise_categories=["micro", "small", "medium"],
        official_url="https://www.sidbi.in", source="SIDBI",
        eligibility_summary=["Indian MSME", "Udyam registration recommended", "Meets SIDBI credit norms"],
        benefits_list=["Collateral-free finance up to ₹1 crore", "Machinery and expansion support", "Working capital support"],
    ),
    _scheme(
        "PM SVANidhi Scheme", "credit_support", "Ministry of Housing & Urban Affairs", "all",
        ["early_stage", "established"],
        ["working_capital", "business_start"],
        ["loan"], "Micro-credit of ₹10,000-₹50,000 (revolving) for street vendors to restart and grow their vending business.",
        50000,
        short_name="SVANidhi", applicant_types=["individual", "entrepreneur", "self_help_group"],
        enterprise_categories=["micro"], max_age=None,
        eligibility_rules=[{"field": "business.type", "operator": "equals", "value": "street_vendor", "required": False}],
        official_url="https://pmsvanidhi.mohua.gov.in", source="Ministry of Housing & Urban Affairs",
        eligibility_summary=["Street vendor with proof of vending", "Monthly repayment convenient", "Preference to women street vendors"],
        benefits_list=["Working capital up to ₹50,000", "Revolving credit", "Incentives for timely repayment", "Digital transaction rewards"],
    ),
    _scheme(
        "Kisan Credit Card Scheme", "credit_support", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["early_stage", "growth", "established"],
        ["working_capital", "equipment_purchase", "business_start"],
        ["loan"], "Flexible short-term credit for farmers for crop cultivation, post-harvest expenses and farm assets.",
        300000,
        short_name="KCC", applicant_types=["farmer", "individual"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": True}],
        official_url="https://www.rbi.org.in", source="Dept of Agriculture Cooperation",
        eligibility_summary=["Farmer or cultivator", "Valid land/possession documentation", "Operating bank account"],
        benefits_list=["Crop loans and term loans", "Flexible repayment aligned to harvest", "Personal accident insurance cover"],
    ),
    _scheme(
        "NMDFC Term Loan for Minorities", "loan", "Ministry of Minority Affairs", "all",
        ["early_stage", "growth", "established"],
        ["business_start", "business_expansion", "equipment_purchase"],
        ["loan"], "Term loans up to ₹20 lakh for minority community entrepreneurs for setting up or expanding enterprises.",
        2000000,
        short_name="NMDFC Term Loan", implementing_agency="NMDFC",
        applicant_types=["entrepreneur", "msme"],
        social_categories=["minority"],
        eligibility_rules=[{"field": "founder.social_category", "operator": "equals", "value": "minority", "required": True}],
        official_url="https://nmdfc.org", source="NMDFC",
        eligibility_summary=["Must belong to a notified minority community", "Project should be income-generating", "Regular repayment ability"],
        benefits_list=["Loan up to ₹20 lakh", "Lower interest rates", "Repayment up to 10 years"],
    ),
    _scheme(
        "Mumkin Scheme", "loan", "Ministry of Minority Affairs", "all",
        ["pre_registration", "early_stage"],
        ["business_start", "working_capital"],
        ["loan"], "Micro-credit up to ₹50,000 for women from minority communities to start small income-generating activities.",
        50000,
        short_name="Mumkin", implementing_agency="NMDFC",
        applicant_types=["women_entrepreneur", "individual", "self_help_group"],
        enterprise_categories=["micro"], gender_eligibility=["female"],
        social_categories=["minority"],
        eligibility_rules=[
            {"field": "founder.gender", "operator": "equals", "value": "female", "required": True},
            {"field": "founder.social_category", "operator": "equals", "value": "minority", "required": True},
        ],
        official_url="https://nmdfc.org", source="NMDFC",
        eligibility_summary=["Woman from minority community", "Age 18-55", "Basic literacy/entrepreneurial skill"],
        benefits_list=["Micro-credit up to ₹50,000", "Self-help group linkage", "Skill and enterprise orientation"],
    ),
    _scheme(
        "Stree Shakti Package", "loan", "State Bank of India", "all",
        ["early_stage", "growth", "established"],
        ["business_start", "business_expansion", "working_capital"],
        ["loan"], "Collateral-free loans for women entrepreneurs with a 25% interest concession and working capital up to ₹50 lakh.",
        5000000,
        short_name="Stree Shakti", implementing_agency="SBI",
        applicant_types=["women_entrepreneur", "entrepreneur"],
        gender_eligibility=["female"],
        eligibility_rules=[{"field": "founder.gender", "operator": "equals", "value": "female", "required": True}],
        official_url="https://www.sbi.co.in", source="State Bank of India",
        eligibility_summary=["Woman entrepreneur or self-employed woman", "Business operating or project ready", "Women in SHG or training programme preferred"],
        benefits_list=["Collateral-free loans", "25% interest concession", "Working capital up to ₹50 lakh", "Term loans for expansion"],
    ),
    _scheme(
        "Annapurna Scheme", "loan", "State Bank of India", "food_processing",
        ["early_stage", "growth", "established"],
        ["working_capital", "equipment_purchase", "business_start"],
        ["loan"], "Loans up to ₹5 lakh for women running food catering and canteen units - covers kitchen equipment and working capital.",
        500000,
        applicant_types=["women_entrepreneur", "entrepreneur"],
        sub_sectors=["food_processing", "services"],
        gender_eligibility=["female"],
        eligibility_rules=[{"field": "founder.gender", "operator": "equals", "value": "female", "required": True}],
        official_url="https://www.sbi.co.in", source="State Bank of India",
        eligibility_summary=["Woman entrepreneur in food catering", "Small food/beverage unit", "No collateral needed under scheme"],
        benefits_list=["Loan up to ₹5 lakh", "Kitchen and utensils finance", "Working capital component"],
    ),
    _scheme(
        "NSIC Raw Material Assistance", "credit_support", "Ministry of Micro, Small & Medium Enterprises", "all",
        ["early_stage", "growth", "established"],
        ["working_capital", "business_expansion"],
        ["credit_guarantee", "financial_assistance"], "Assistance to micro and small enterprises for procuring raw materials without blocking working capital.",
        10000000,
        short_name="NSIC RMFS", implementing_agency="NSIC",
        applicant_types=["msme", "manufacturer"],
        enterprise_categories=["micro", "small"],
        official_url="https://nsic.co.in", source="NSIC",
        eligibility_summary=["Registered micro/small enterprise", "Factory/unit engaged in manufacturing", "Payment track record"],
        benefits_list=["Raw material procurement finance", "Facilitated bulk procurement", "Reduced working capital pressure"],
    ),
    _scheme(
        "NHFDC Loan for Persons with Disabilities", "loan", "Ministry of Social Justice & Empowerment", "all",
        ["early_stage", "growth", "established"],
        ["business_start", "business_expansion", "equipment_purchase"],
        ["loan", "subsidy"], "Loans with capital subsidy for persons with disabilities to set up self-employment and business ventures.",
        1000000,
        short_name="NHFDC", implementing_agency="NHFDC",
        applicant_types=["entrepreneur", "individual"],
        enterprise_categories=["micro", "small"],
        official_url="https://www.nhfdc.nic.in", source="NHFDC",
        eligibility_summary=["Person with disability (40%+ disability)", "Age 18-55", "Viable enterprise proposal"],
        benefits_list=["Loan up to ₹10 lakh", "Capital subsidy on eligible projects", "Priority to women with disabilities", "Vocational training support"],
    ),
    _scheme(
        "NSFDC Loan for SC Entrepreneurs", "loan", "Ministry of Social Justice & Empowerment", "all",
        ["early_stage", "growth", "established"],
        ["business_start", "business_expansion", "equipment_purchase"],
        ["loan", "subsidy"], "Loans with capital subsidy for Scheduled Caste entrepreneurs for income-generating activities.",
        3600000,
        short_name="NSFDC", implementing_agency="NSFDC",
        applicant_types=["entrepreneur", "msme"],
        social_categories=["sc", "st"],
        eligibility_rules=[{"field": "founder.social_category", "operator": "in", "value": ["sc", "st"], "required": True}],
        official_url="https://nsfdc.gov.in", source="NSFDC",
        eligibility_summary=["SC/ST entrepreneur", "Age 18-55", "Viable enterprise/project proposal"],
        benefits_list=["Term loans up to ₹36 lakh", "25% capital subsidy on eligible projects", "Working capital support", "Lower interest rates"],
    ),
    _scheme(
        "NSKFDC Loan for Sanitation Workers", "loan", "Ministry of Social Justice & Empowerment", "all",
        ["pre_registration", "early_stage", "growth"],
        ["business_start", "business_expansion"],
        ["loan", "grant"], "Loans and grants for sanitation workers and their dependants for alternative livelihood and enterprise.",
        1000000,
        short_name="NSKFDC", implementing_agency="NSKFDC",
        applicant_types=["entrepreneur", "individual"],
        social_categories=["sc", "st", "obc"],
        eligibility_rules=[{"field": "founder.social_category", "operator": "in", "value": ["sc", "st"], "required": False}],
        official_url="https://nskfdc.nic.in", source="NSKFDC",
        eligibility_summary=["Sanitation worker or dependent", "Age 18-55", "Has paid ₹1,000 as community kaamgaar fee"],
        benefits_list=["Micro-loans up to ₹10 lakh", "Capital subsidy under NAMASTE", "Skill training for alternate livelihood"],
    ),
    _scheme(
        "Atal Innovation Mission", "grant", "NITI Aayog", "technology",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["grant", "mentorship"], "Grants and incubation support for innovators, tinkering labs, and early-stage startups.",
        None,
        short_name="AIM", sub_sectors=["technology", "education"],
        applicant_types=["startup", "student", "entrepreneur"],
        enterprise_categories=["startup", "micro"],
        min_age=14,
        official_url="https://aim.gov.in", source="NITI Aayog",
        eligibility_summary=["Innovator/startup with a working solution", "Registered with relevant institute (ATL/ATIC/AB)", "Scalable social or commercial idea"],
        benefits_list=["Seed and grant support", "Incubator access", "Mentorship from industry experts", "Innovation challenge networks"],
    ),
    _scheme(
        "NIDHI Science & Technology Entrepreneurs Park", "grant", "Ministry of Science & Technology", "technology",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "research_development"],
        ["grant", "infrastructure"], "Incubation support with seed grant for science and technology startups at recognized STEPs.",
        5000000,
        short_name="NIDHI-STEP", department="Department of Science & Technology",
        applicant_types=["startup", "entrepreneur"],
        enterprise_categories=["startup", "micro"],
        official_url="https://dst.gov.in", source="DST",
        eligibility_summary=["Technology-based idea", "Incubated at a recognized STEP", "Anti (rural/social) innovations preferred"],
        benefits_list=["Seed funding up to ₹50 lakh fund", "Incubation infrastructure", "Knowledge and mentoring network"],
    ),
    _scheme(
        "AGRI-UDAAN Excellence in Agribusiness", "grant", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["idea", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["grant", "mentorship"], "A 6-month accelerator for food & agri-tech startups with grants up to ₹30 lakh and investor access.",
        3000000,
        short_name="AGRI-UDAAN", sub_sectors=["food_processing", "technology"],
        applicant_types=["startup", "farmer"],
        enterprise_categories=["startup", "micro"],
        official_url="https://agri-udaan.aic-ccmb.in", source="ICAR/Agri Accelerator Network",
        eligibility_summary=["Registered agri/food-tech startup", "Working prototype or early revenue", "Willing to join accelerator program"],
        benefits_list=["Grant up to ₹30 lakh", "6-month accelerator engagement", "Networking with agri-industry", "Investor pitching platform"],
    ),
    _scheme(
        "PLI Scheme for Food Processing Industry", "funding", "Ministry of Food Processing Industries", "food_processing",
        ["early_stage", "growth", "established"],
        ["business_expansion", "equipment_purchase", "technology_upgrade"],
        ["financial_assistance"], "Production Linked Incentive for food processing units - 4-6% incentive on incremental sales of specified products.",
        None,
        short_name="PLI Food", applicant_types=["msme", "manufacturer", "entrepreneur"],
        sub_sectors=["food_processing", "agriculture"],
        official_url="https://mofpi.gov.in", source="MoFPI",
        eligibility_summary=["Registered food processing unit", "Minimum investment thresholds met", "Products in notified categories"],
        benefits_list=["Incentive on incremental sales", "Encourages value-added food products", "Employment generation support"],
    ),
    _scheme(
        "Electronics Manufacturing Clusters 2.0", "subsidy", "Ministry of Electronics & IT", "manufacturing",
        ["early_stage", "growth", "established"],
        ["infrastructure", "business_expansion", "technology_upgrade"],
        ["subsidy", "infrastructure"], "Capital subsidy for establishing world-class electronics manufacturing infrastructure and clusters.",
        350000000,
        short_name="EMC 2.0", sub_sectors=["technology"],
        applicant_types=["manufacturer", "msme"],
        enterprise_categories=["micro", "small", "medium", "large"],
        min_business_age=6,
        official_url="https://www.meity.gov.in", source="MeitY",
        eligibility_summary=["Unit within an approved EMC", "Electronics manufacturing activity", "Meets state sops and land requirements"],
        benefits_list=["Capital subsidy up to 50%", "Common infrastructure support", "Anchor unit incentives"],
    ),
    _scheme(
        "Agriculture Infrastructure Fund", "credit_support", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["early_stage", "growth", "established"],
        ["infrastructure", "equipment_purchase", "technology_upgrade"],
        ["loan", "interest_subsidy"], "Medium-long term loans up to ₹2 crore for post-harvest and farm infrastructure with 3% interest subvention.",
        20000000,
        short_name="AIF", sub_sectors=["food_processing", "agriculture"],
        applicant_types=["farmer", "cooperative", "msme", "self_help_group"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://agriinfra.dac.gov.in", source="DAC&FW",
        eligibility_summary=["Farmer/farm groups/agri-entrepreneurs", "Project for post-harvest infra", "Bankable project report"],
        benefits_list=["Loans up to ₹2 crore", "3% interest subvention", "Credit guarantee coverage", "Benefit for community farming assets"],
    ),
    _scheme(
        "PM-KUSUM Solar Pump Scheme", "subsidy", "Ministry of New & Renewable Energy", "renewable_energy",
        ["early_stage", "growth"],
        ["equipment_purchase", "green_energy", "technology_upgrade"],
        ["subsidy"], "Subsidies for solar pumps and small solar power plants for farmers (up to 30-60% central subsidy).",
        2500000,
        short_name="PM-KUSUM", sub_sectors=["agriculture"],
        applicant_types=["farmer", "individual", "cooperative"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://pmkusum.mnre.gov.in", source="MNRE",
        eligibility_summary=["Farmer with own cultivable land", "Solar pump/plant configuration", "State-level sanction within targets"],
        benefits_list=["Central + state subsidy", "Reduced diesel/electric cost", "Surplus power sell-back option"],
    ),
    _scheme(
        "PM Surya Ghar Muft Bijli Yojana", "subsidy", "Ministry of New & Renewable Energy", "renewable_energy",
        ["growth", "established"],
        ["green_energy", "technology_upgrade"],
        ["subsidy"], "Subsidy for rooftop solar installations (₹30,000-₹78,000) for households and small businesses.",
        78000,
        short_name="PM Surya Ghar", applicant_types=["individual", "entrepreneur", "msme"],
        official_url="https://pmsuryaghar.gov.in", source="MNRE",
        eligibility_summary=["Owns rooftop premises", "Registered electricity consumer", "Employs DISCOM-empaneled vendor"],
        benefits_list=["Direct subsidy ₹30k-₹78k", "Lower power bills", "Net metering benefit"],
    ),
    _scheme(
        "Dairy Entrepreneurship Development Scheme", "subsidy", "Ministry of Fisheries, Animal Husbandry & Dairying", "agriculture",
        ["early_stage", "growth"],
        ["business_start", "equipment_purchase", "business_expansion"],
        ["subsidy", "loan"], "Capital subsidy (25-33%) on bank loans for dairy entrepreneurship - dairy farming, processing and vending units.",
        1200000,
        short_name="DEDS", sub_sectors=["agriculture"],
        applicant_types=["farmer", "entrepreneur", "self_help_group"],
        official_url="https://www.nddb.coop", source="NDDB/DAHD",
        eligibility_summary=["Bankable dairy project", "Loan from eligible financial institution", "SC/ST/women get higher subsidy"],
        benefits_list=["25-33% capital subsidy", "Bank loan linkage", "Yardstick-based project funding"],
    ),
    _scheme(
        "Mission for Integrated Development of Horticulture", "subsidy", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["early_stage", "growth", "established"],
        ["equipment_purchase", "technology_upgrade", "infrastructure"],
        ["subsidy"], "Subsidies for horticulture - greenhouses, drip irrigation, nurseries, and post-harvest infrastructure.",
        1000000,
        short_name="MIDH", sub_sectors=["agriculture", "food_processing"],
        applicant_types=["farmer", "entrepreneur", "cooperative"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://midh.gov.in", source="NHB/DAC",
        eligibility_summary=["Horticulturist or farmer group", "Technical feasibility of project", "State/DPD guidelines"],
        benefits_list=["Subsidy on greenhouses & polyhouses", "Drip/sprinkler support", "Post-harvest infrastructure subsidy"],
    ),
    _scheme(
        "Raising and Accelerating MSME Performance", "funding", "Ministry of Micro, Small & Medium Enterprises", "all",
        ["early_stage", "growth", "established"],
        ["technology_upgrade", "green_energy", "business_expansion"],
        ["financial_assistance"], "World Bank-assisted programme supporting MSME technology upgradation, green investments and access to finance.",
        None,
        short_name="RAMP", applicant_types=["msme", "manufacturer", "entrepreneur"],
        enterprise_categories=["micro", "small", "medium"],
        official_url="https://www.msme.gov.in", source="MSME Ministry",
        eligibility_summary=["Registered MSME", "Willing to modernize/decarbonise", "Meets programme scheme criteria"],
        benefits_list=["Field technology upgradation support", "Green/energy efficiency incentives", "Access to finance facilitation"],
    ),
    _scheme(
        "Zero Defect Zero Effect MSME Certification", "subsidy", "Ministry of Micro, Small & Medium Enterprises", "all",
        ["early_stage", "growth", "established"],
        ["technology_upgrade", "green_energy", "training"],
        ["subsidy", "training"], "Financial incentives for MSMEs adopting ZED quality and environmental standards with 80-100% fees reimbursement.",
        100000,
        short_name="ZED", applicant_types=["msme", "manufacturer"],
        enterprise_categories=["micro", "small", "medium"],
        official_url="https://zed.msme.gov.in", source="QCI/MSME",
        eligibility_summary=["Registered MSME", "Undertakes ZED assessment", "Completes improvement roadmap"],
        benefits_list=["80-100% certification fee reimbursement", "Priority for government procurement", "Quality & green standard badge"],
    ),
    _scheme(
        "PM-KISAN Samman Nidhi", "funding", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["early_stage", "growth", "established"],
        ["business_start", "working_capital"],
        ["financial_assistance"], "Direct income support of ₹6,000 per year to farmer families for cultivation and input needs.",
        6000,
        short_name="PM-KISAN", applicant_types=["farmer"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": True}],
        official_url="https://pmkisan.gov.in", source="DAC&FW",
        eligibility_summary=["Farmer family with cultivable land", "Eligible exclusions respected", "Aadhaar-linked bank account"],
        benefits_list=["₹6,000 per year in three instalments", "Direct benefit transfer"],
    ),
    _scheme(
        "Startup India Tax Exemption", "tax_benefit", "Ministry of Commerce & Industry", "technology",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["tax_benefit"], "Three-year income tax holiday and capital gains exemption for DPIIT-recognised startups.",
        None,
        short_name="Startup India Tax", department="DPIIT",
        applicant_types=["startup"],
        eligibility_rules=[{"field": "business.stage", "operator": "in", "value": ["idea", "pre_registration", "early_stage"], "required": False}],
        official_url="https://www.startupindia.gov.in", source="DPIIT",
        eligibility_summary=["DPIIT-recognised startup", "Incorporated after 2016 (per norms)", "Under 10 years old"],
        benefits_list=["3-year income tax holiday", "Angel tax relaxation", "Capital gains exemption"],
    ),
_scheme(
        "PM Vishwakarma Yojana", "loan", "Ministry of Micro, Small & Medium Enterprises", "handicrafts",
        ["early_stage", "growth", "established"],
        ["business_start", "business_expansion", "equipment_purchase", "training"],
        ["loan", "training"], "Skill training with stipend and collateral-free loans of ₹10,000-₹3 lakh for artisans in 18 traditional trades.",
        300000,
        short_name="PM Vishwakarma", sub_sectors=["handicrafts", "textile", "manufacturing", "services"],
        applicant_types=["artisan", "entrepreneur", "individual"],
        enterprise_categories=["micro"],
        official_url="https://pmvishwakarma.gov.in", source="MSME Ministry",
        eligibility_summary=["Artisan practising a traditional trade", "Age 18 or above", "Not availed similar loan under other schemes"],
        benefits_list=["Skill certification + stipend", "Collateral-free loan up to ₹3 lakh", "Tool-kit incentive", "Digital payments incentives"],
    ),
    _scheme(
        "Pradhan Mantri Kaushal Vikas Yojana 4.0", "training", "Ministry of Skill Development & Entrepreneurship", "all",
        ["idea", "pre_registration", "early_stage"],
        ["training", "skill_development", "employment"],
        ["training"], "Industry-relevant skill training with certification and placement support for youth.",
        None,
        short_name="PMKVY 4.0", applicant_types=["student", "individual", "entrepreneur"],
        max_age=45,
        official_url="https://www.pmkvyofficial.org", source="MSDE",
        eligibility_summary=["Youth aged 15-45", "Willing to complete assessed training", "Meets sectoral course criteria"],
        benefits_list=["Free skill training", "Government certification", "Placement assistance", "Special focus on new-age skills"],
    ),
    _scheme(
        "National Apprenticeship Promotion Scheme", "training", "Ministry of Skill Development & Entrepreneurship", "all",
        ["early_stage", "growth"],
        ["training", "skill_development", "employment"],
        ["training", "financial_assistance"], "Support for engaging apprentices with stipend and basic training subsidies.",
        None,
        short_name="NAPS", applicant_types=["msme", "entrepreneur", "manufacturer"],
        official_url="https://naps.gov.in", source="MSDE",
        eligibility_summary=["Unit with basic apprenticeship infrastructure", "Engages registered apprentices", "Fills training obligations"],
        benefits_list=["Stipend reimbursement (25% of stipend)", "Basic training cost subsidy", "Skilled workforce pipeline"],
    ),
    _scheme(
        "Deen Dayal Upadhyaya Grameen Kaushalya Yojana", "training", "Ministry of Rural Development", "all",
        ["idea", "pre_registration"],
        ["training", "skill_development", "employment"],
        ["training"], "Skills training and placement for rural poor youth (15-35) with post-placement support.",
        None,
        short_name="DDU-GKY", applicant_types=["individual", "student", "entrepreneur"],
        max_age=35,
        official_url="https://ddugky.gov.in", source="MoRD",
        eligibility_summary=["Rural youth aged 15-35", "BPL/NRLM-linked families", "Complete residential or non-residential training"],
        benefits_list=["Free residential skill training", "Placement-linked", "Post-placement support"],
    ),
    _scheme(
        "Micro Enterprise Development Programme", "training", "NABARD", "all",
        ["idea", "pre_registration", "early_stage"],
        ["training", "skill_development", "business_start"],
        ["training", "mentorship"], "NABARD capacity-building training to help rural entrepreneurs start and grow micro enterprises.",
        None,
        short_name="MEDP", applicant_types=["self_help_group", "individual", "farmer", "entrepreneur"],
        enterprise_categories=["micro"],
        official_url="https://www.nabard.org", source="NABARD",
        eligibility_summary=["Rural entrepreneur or SHG member", "Motivation for micro enterprise", "Through NABARD-sponsored agency"],
        benefits_list=["Free training programme", "Credit/finance linkage guidance", "Enterprise planning support"],
    ),
    _scheme(
        "Rural Entrepreneurship Development Programme", "training", "NABARD", "all",
        ["idea", "pre_registration"],
        ["training", "skill_development", "business_start"],
        ["training"], "NABARD REDP training to develop entrepreneurship skills among rural youth and women.",
        None,
        short_name="REDP", applicant_types=["individual", "women_entrepreneur", "self_help_group"],
        enterprise_categories=["micro"],
        official_url="https://www.nabard.org", source="NABARD",
        eligibility_summary=["Rural youth/women", "Basic education level", "Eligible as per REDP norms"],
        benefits_list=["One-week entrepreneurship training", "Business idea clinic", "Linkage with financial institutions"],
    ),
    _scheme(
        "Nai Roshni Leadership & Skill Training", "training", "Ministry of Minority Affairs", "all",
        ["idea", "pre_registration"],
        ["training", "skill_development", "women_entrepreneurship"],
        ["training"], "Leadership and livelihood training for women from minority communities.",
        None,
        short_name="Nai Roshni", applicant_types=["women_entrepreneur", "individual", "self_help_group"],
        gender_eligibility=["female"], social_categories=["minority"],
        eligibility_rules=[
            {"field": "founder.gender", "operator": "equals", "value": "female", "required": True},
            {"field": "founder.social_category", "operator": "equals", "value": "minority", "required": True},
        ],
        official_url="https://minorityaffairs.gov.in", source="Ministry of Minority Affairs",
        eligibility_summary=["Woman from minority community", "Age 18-50", "Participation in leadership/livelihood training"],
        benefits_list=["Leadership training", "Livelihood skill development", "Financial literacy sessions"],
    ),
    _scheme(
        "PM Fasal Bima Yojana", "insurance", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["early_stage", "growth", "established"],
        ["business_start", "working_capital"],
        ["insurance"], "Crop insurance with low premium for farmers covering kharif, rabi and commercial crops.",
        None,
        short_name="PMFBY", applicant_types=["farmer", "individual"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": True}],
        official_url="https://pmfby.gov.in", source="DAC&FW",
        eligibility_summary=["Farmer cultivating notified crop", "Enrols before cut-off date", "Pays prescribed premium share"],
        benefits_list=["Coverage for notified crops", "Low premium (max 2% kharif/1.5% rabi)", "Sum insured equal to loan amount for borrowers"],
    ),
    _scheme(
        "Pradhan Mantri Suraksha Bima Yojana", "insurance", "Ministry of Finance", "all",
        ["early_stage", "growth", "established"],
        ["business_start", "working_capital"],
        ["insurance"], "Personal accident insurance cover of ₹2 lakh at ₹20 per year for bank account holders.",
        200000,
        short_name="PMSBY", applicant_types=["individual", "entrepreneur", "artisan", "farmer"],
        official_url="https://jansuraksha.gov.in", source="Dept of Financial Services",
        eligibility_summary=["Indian citizen age 18-70", "Savings bank account", "Provides nominee consent"],
        benefits_list=["₹2 lakh coverage (death/disability)", "Annual premium only ₹20", "Auto-debit renewal"],
    ),
    _scheme(
        "Government e-Marketplace Support", "market_access", "Ministry of Commerce & Industry", "all",
        ["early_stage", "growth", "established"],
        ["market_access", "marketing", "business_expansion"],
        ["market_access", "financial_assistance"], "GeM registration support and 10-15% mobilisation advance on orders for micro and small sellers.",
        None,
        short_name="GeM", implementing_agency="GeM",
        applicant_types=["msme", "entrepreneur", "manufacturer", "cooperative"],
        enterprise_categories=["micro", "small"],
        official_url="https://gem.gov.in", source="GeM",
        eligibility_summary=["Registered on GeM portal", "MSME/Startup recognized for incentives", "Sells notified product category"],
        benefits_list=["Direct government order access", "Mobilisation advance (10-15%)", "No/zero fee for micro sellers", "Digital payments (pooled account)"],
    ),
    _scheme(
        "National Agriculture Market", "market_access", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["early_stage", "growth", "established"],
        ["market_access", "marketing", "business_expansion"],
        ["market_access"], "Electronic national trading platform connecting APMC mandis for transparent price discovery.",
        None,
        short_name="e-NAM", sub_sectors=["agriculture", "food_processing"],
        applicant_types=["farmer", "cooperative", "entrepreneur"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://www.enam.gov.in", source="DAC&FW",
        eligibility_summary=["Farmer/licenced trader in e-NAM mandi", "Valid Aadhaar-linked wallet", "Produces agri commodities"],
        benefits_list=["Better price discovery", "Pan-India mandi access", "Digital payments", "Quality assaying support"],
    ),
    _scheme(
        "Trade Receivables Discounting System", "market_access", "Reserve Bank of India", "fintech",
        ["early_stage", "growth", "established"],
        ["working_capital", "business_expansion"],
        ["financial_assistance", "market_access"], "Invoice discounting exchange where MSMEs can sell receivables early to financiers at competitive rates.",
        None,
        short_name="TReDS", sub_sectors=["services", "manufacturing", "technology"],
        applicant_types=["msme", "manufacturer", "entrepreneur"],
        enterprise_categories=["micro", "small", "medium"],
        official_url="https://tre-ds.in", source="RBI",
        eligibility_summary=["Registered MSME with corporate/factoring-eligible buyers", "Has unpaid invoices", "Onboarded on an approved TReDS platform"],
        benefits_list=["Early invoice payment (0-90 days)", "Competitive discounting rates", "No collateral required"],
    ),
    _scheme(
        "National Handloom Development Programme", "subsidy", "Ministry of Textiles", "textile",
        ["early_stage", "growth", "established"],
        ["equipment_purchase", "business_expansion", "technology_upgrade"],
        ["subsidy", "credit_guarantee"], "Margin money subsidy and credit support for weavers and handloom enterprises.",
        200000,
        short_name="NHDP", sub_sectors=["handicrafts", "textile"],
        applicant_types=["artisan", "weaver", "self_help_group"],
        eligibility_rules=[{"field": "sector.primary", "operator": "in", "value": ["textile", "handicrafts"], "required": False}],
        official_url="https://handlooms.nic.in", source="M/o Textiles",
        eligibility_summary=["Weaver/artisan or handloom unit", "Member of a weaver cooperative optional", "Meets NHDP credit norms"],
        benefits_list=["Margin money subsidy", "Working capital credit", "Design and technology support"],
    ),
    _scheme(
        "Comprehensive Handloom Cluster Development Scheme", "subsidy", "Ministry of Textiles", "textile",
        ["growth", "established"],
        ["infrastructure", "technology_upgrade", "market_access"],
        ["subsidy", "infrastructure", "market_access"], "Integrated support for handloom clusters - infrastructure, credit, and market development.",
        None,
        short_name="CHCDS", sub_sectors=["handicrafts", "textile"],
        applicant_types=["artisan", "self_help_group", "cooperative"],
        official_url="https://handlooms.nic.in", source="M/o Textiles",
        eligibility_summary=["Handloom cluster with critical mass", "Cluster-level implementing agency", "Comprehensive cluster plan"],
        benefits_list=["Cluster infrastructure development", "Credit facilitation", "Marketing and branding support"],
    ),
    _scheme(
        "Ambedkar Hastshilp Vikas Yojana", "subsidy", "Ministry of Textiles", "handicrafts",
        ["early_stage", "growth", "established"],
        ["skill_development", "infrastructure", "market_access"],
        ["subsidy", "training"], "Capacity building, skill upgradation and infrastructure for handicraft clusters and artisans.",
        300000,
        short_name="AHVY", sub_sectors=["handicrafts"],
        applicant_types=["artisan", "self_help_group"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "handicrafts", "required": False}],
        official_url="https://handicrafts.nic.in", source="M/o Textiles",
        eligibility_summary=["Handicraft artisan or cluster", "Duly registered under concerned authority", "Cluster-based proposal"],
        benefits_list=["Skill upgradation training", "Common facility centres", "Design intervention and exhibition support"],
    ),
    _scheme(
        "Integrated Wool Development Programme", "subsidy", "Ministry of Textiles", "textile",
        ["early_stage", "growth"],
        ["equipment_purchase", "technology_upgrade"],
        ["subsidy"], "Support for wool processing, spinning, shearing training and wool-based enterprise development.",
        400000,
        short_name="IWDP", sub_sectors=["handicrafts", "agriculture"],
        applicant_types=["artisan", "entrepreneur", "self_help_group"],
        official_url="https://woolboard.nic.in", source="M/o Textiles",
        eligibility_summary=["Wool-based enterprise or artisan", "Located in wool-growing region", "Project under IWDP components"],
        benefits_list=["Equipment/machinery subsidy", "Wool processing training", "Market linkage support"],
    ),
    _scheme(
        "Interest Equalization Scheme for Exporters", "credit_support", "Ministry of Commerce & Industry", "export",
        ["growth", "established"],
        ["export", "working_capital", "business_expansion"],
        ["interest_subsidy"], "2-3% interest subvention on pre- and post-shipment rupee export credit for MSME exporters.",
        None,
        short_name="IES", applicant_types=["exporter", "msme", "manufacturer"],
        sub_sectors=["manufacturing", "handicrafts", "food_processing"],
        official_url="https://commerce.gov.in", source="DGFT",
        eligibility_summary=["Merchant/manufacturer exporter", "MSME or specified tariff line", "Exports under bank credit"],
        benefits_list=["2-3% interest subvention", "Benefit on export credit", "Covers 410+ tariff lines"],
    ),
    _scheme(
        "Export Promotion Capital Goods Scheme", "tax_benefit", "Ministry of Commerce & Industry", "export",
        ["growth", "established"],
        ["export", "equipment_purchase", "technology_upgrade"],
        ["tax_benefit"], "Zero or 3% customs duty on capital goods imported for export production subject to export obligation.",
        None,
        short_name="EPCG", applicant_types=["exporter", "manufacturer", "msme"],
        sub_sectors=["manufacturing", "technology", "food_processing"],
        official_url="https://www.dgft.gov.in", source="DGFT",
        eligibility_summary=["Exporter with export performance", "Import capital goods under scheme", "Meets export obligation (4-6x duty saved)"],
        benefits_list=["Concessional customs duty", "Technology modernisation", "Export obligation allows flexi-use"],
    ),
_scheme(
        "STPI Incubation & Nurturing", "grant", "Ministry of Electronics & IT", "technology",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "infrastructure", "technology_upgrade"],
        ["grant", "infrastructure", "mentorship"], "Software Technology Parks of India incubators provide seed funding, infrastructure, and mentorship to tech startups.",
        500000,
        short_name="STPI Incubator", sub_sectors=["technology", "fintech"],
        applicant_types=["startup", "entrepreneur"],
        enterprise_categories=["startup", "micro"],
        official_url="https://www.stpi.in", source="STPI",
        eligibility_summary=["Registered startup", "Technology-based product/idea", "Selected by STPI incubation committee"],
        benefits_list=["Seed funding up to ₹5 lakh", "Incubation infrastructure", "Mentorship & market connect"],
    ),
    _scheme(
        "ASPIRE - Scheme for Innovation & Rural Industries", "funding", "Ministry of Micro, Small & Medium Enterprises", "manufacturing",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "research_development", "training"],
        ["grant", "infrastructure", "training"], "A Scheme for Promotion of Innovation, Rural Industries and Entrepreneurship through incubation centres.",
        5000000,
        short_name="ASPIRE", sub_sectors=["handicrafts", "agriculture", "food_processing"],
        applicant_types=["startup", "entrepreneur", "individual"],
        official_url="https://www.msme.gov.in", source="MSME Ministry",
        eligibility_summary=["Rural or small-town entrepreneur", "Viable business idea", "Through aspiring incubation centre"],
        benefits_list=["Incubation support", "Seed funding access", "Training and entrepreneurship development"],
    ),
    _scheme(
        "Coir Vikas Yojana", "subsidy", "Ministry of Micro, Small & Medium Enterprises", "handicrafts",
        ["early_stage", "growth"],
        ["equipment_purchase", "business_start", "technology_upgrade"],
        ["subsidy"], "Subsidy (25-30%) for setting up and modernising coir processing and fibre units.",
        500000,
        short_name="CVY", implementing_agency="Coir Board",
        applicant_types=["artisan", "entrepreneur", "self_help_group", "cooperative"],
        sub_sectors=["handicrafts", "manufacturing"],
        official_url="https://coirboard.gov.in", source="Coir Board",
        eligibility_summary=["Coir-unit project", "SC/ST/women get higher subsidy", "Bankable project under CVY"],
        benefits_list=["25-30% capital subsidy", "Marginalised group upliftment", "Employment generation in coir areas"],
    ),
    _scheme(
        "Swadesh Darshan Scheme", "infrastructure", "Ministry of Tourism", "tourism",
        ["growth", "established"],
        ["infrastructure", "business_expansion"],
        ["infrastructure", "financial_assistance"], "Development of tourism circuits and infrastructure benefiting local tourism enterprises and homestays.",
        None,
        short_name="Swadesh Darshan", sub_sectors=["tourism", "services"],
        applicant_types=["entrepreneur", "msme", "cooperative"],
        official_url="https://tourism.gov.in", source="M/o Tourism",
        eligibility_summary=["Tourism enterprise near identified circuit", "Registered business", "Coexists within approved project scope"],
        benefits_list=["Improved tourism infrastructure", "Increased visitor footfall", "Ancillary business opportunities"],
    ),
    _scheme(
        "Incredible India Tourist Facilitator", "training", "Ministry of Tourism", "tourism",
        ["idea", "pre_registration", "early_stage"],
        ["training", "skill_development", "employment"],
        ["training"], "Free training and certification for tourist facilitators, guides and local tourism service providers.",
        20000,
        short_name="IITF", sub_sectors=["tourism", "services"],
        applicant_types=["individual", "entrepreneur"],
        min_age=18,
        official_url="https://tourism.gov.in", source="M/o Tourism",
        eligibility_summary=["Indian citizen", "Basic education (10th pass)", "Interest in tourism services"],
        benefits_list=["Free training programme", "Certification", "Assured guidance for tourism careers"],
    ),
    _scheme(
        "Open Network for Digital Commerce", "market_access", "DPIIT", "retail",
        ["early_stage", "growth", "established"],
        ["market_access", "digital_transformation", "marketing"],
        ["market_access", "training"], "ONDC onboarding support helping small retailers and sellers go digital and reach more buyers at zero commissions.",
        None,
        short_name="ONDC", sub_sectors=["retail", "services", "food_processing"],
        applicant_types=["entrepreneur", "msme", "self_help_group"],
        enterprise_categories=["micro", "small"],
        official_url="https://ondc.org", source="ONDC",
        eligibility_summary=["Any seller, store or home-based business", "Onboards via any ONDC app", "Willing to digitise catalogue & fulfilment"],
        benefits_list=["Open e-commerce access", "Zero/negligible commissions", "Minority-language support", "Same-day onboarding"],
    ),
    _scheme(
        "Samarth Skill Development in Textiles", "training", "Ministry of Textiles", "textile",
        ["idea", "pre_registration", "early_stage"],
        ["training", "skill_development", "employment"],
        ["training", "financial_assistance"], "Training, entrepreneurship and placement support in handloom, spinning and textile value chains.",
        80000,
        short_name="Samarth", sub_sectors=["handicrafts", "textile", "manufacturing"],
        applicant_types=["artisan", "individual", "student", "entrepreneur"],
        eligibility_rules=[{"field": "sector.primary", "operator": "in", "value": ["textile", "handicrafts"], "required": False}],
        official_url="https://samarth-textiles.gov.in", source="M/o Textiles",
        eligibility_summary=["Aspirant in textiles sector", "80% attendance in training", "Completes assessment"],
        benefits_list=["Free skilling + certification", "Stipend during training", "Placement & enterprise support"],
    ),
    _scheme(
        "Mukhyamantri Business Loan Yojana (Delhi)", "loan", "Govt of NCT of Delhi", "all",
        ["early_stage", "growth", "established"],
        ["business_start", "business_expansion", "working_capital"],
        ["loan"], "Interest-subsidised business loans up to ₹5 lakh for women entrepreneurs (18-60) resident of Delhi.",
        500000,
        short_name="Delhi MBLY", geographic_scope="state", states=["Delhi"],
        applicant_types=["women_entrepreneur", "entrepreneur"],
        gender_eligibility=["female"],
        eligibility_rules=[
            {"field": "location.state", "operator": "equals", "value": "Delhi", "required": True},
            {"field": "founder.gender", "operator": "equals", "value": "female", "required": True},
        ],
        official_url="https://mktv.delhigovt.nic.in", source="Delhi Govt MSDE",
        eligibility_summary=["Woman aged 18-60", "Delhi resident for 5+ years", "Annual family income below ₹3 lakh"],
        benefits_list=["Loan up to ₹5 lakh", "Interest subsidy", "For business setup/expansion"],
    ),
    _scheme(
        "Chief Minister's Employment Generation Programme (Maharashtra)", "loan", "Govt of Maharashtra", "all",
        ["early_stage", "growth"],
        ["business_start", "equipment_purchase", "business_expansion"],
        ["loan", "subsidy"], "Loans with capital subsidy for micro enterprises of young entrepreneurs (18-45) in Maharashtra.",
        2500000,
        short_name="CMEGP MH", geographic_scope="state", states=["Maharashtra"],
        applicant_types=["entrepreneur", "individual", "msme"],
        enterprise_categories=["micro", "small"],
        eligibility_rules=[{"field": "location.state", "operator": "equals", "value": "Maharashtra", "required": True}],
        official_url="https://mahaaiti.maharashtra.gov.in", source="Maharashtra Govt",
        eligibility_summary=["Age 18-45", "Maharashtra resident", "New or existing micro enterprise"],
        benefits_list=["Bank loan with margin contribution", "Capital subsidy up to 30%", "Priority to SC/ST/women"],
    ),
    _scheme(
        "Udyogini Scheme (Karnataka)", "subsidy", "Govt of Karnataka", "all",
        ["early_stage", "growth"],
        ["business_start", "business_expansion", "equipment_purchase"],
        ["subsidy", "loan"], "Financial assistance and bank loan subsidy for women micro-entrepreneurs (18-55) in Karnataka.",
        50000,
        short_name="Udyogini KA", geographic_scope="state", states=["Karnataka"],
        applicant_types=["women_entrepreneur", "self_help_group", "individual"],
        enterprise_categories=["micro"],
        gender_eligibility=["female"],
        eligibility_rules=[
            {"field": "location.state", "operator": "equals", "value": "Karnataka", "required": True},
            {"field": "founder.gender", "operator": "equals", "value": "female", "required": True},
        ],
        official_url="https://www.karnataka.gov.in", source="Karnataka Govt",
        eligibility_summary=["Woman aged 18-55", "Karnataka resident", "Family income within scheme limits"],
        benefits_list=["20-25% capital subsidy on loan", "Bank credit linkage", "Skill development support"],
    ),
    _scheme(
        "Elevate Startup Programme (Karnataka)", "grant", "Govt of Karnataka", "technology",
        ["idea", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["grant", "mentorship"], "Grants up to ₹50 lakh for innovative startups selected through a rigorous evaluation process in Karnataka.",
        5000000,
        short_name="Elevate KA", geographic_scope="state", states=["Karnataka"],
        applicant_types=["startup", "entrepreneur"],
        enterprise_categories=["startup", "micro", "small"],
        eligibility_rules=[{"field": "location.state", "operator": "equals", "value": "Karnataka", "required": True}],
        official_url="https://startupkarnataka.com", source="Karnataka Startup Cell",
        eligibility_summary=["Startup registered in Karnataka", "Innovative/scaleable idea", "Clears Elevate evaluation round"],
        benefits_list=["Grant up to ₹50 lakh", "Incubation & mentorship", "Investor connect"],
    ),
    _scheme(
        "Mukhyamantri Yuva Udyami Vikas Abhiyan (UP)", "loan", "Govt of Uttar Pradesh", "all",
        ["early_stage", "growth"],
        ["business_start", "business_expansion", "equipment_purchase"],
        ["loan", "subsidy"], "Loans with interest/capital subsidy for youth (18-40) entrepreneurs of Uttar Pradesh.",
        5000000,
        short_name="YUVA UP", geographic_scope="state", states=["Uttar Pradesh"],
        applicant_types=["entrepreneur", "individual"],
        enterprise_categories=["micro", "small"],
        eligibility_rules=[{"field": "location.state", "operator": "equals", "value": "Uttar Pradesh", "required": True}],
        official_url="https://msme.up.gov.in", source="UP MSME Dept",
        eligibility_summary=["Youth aged 18-40", "UP resident", "Own micro/small enterprise or new project"],
        benefits_list=["Loan up to ₹40 lakh", "Up to 30% capital subsidy", "No personal surety in many cases"],
    ),
    _scheme(
        "StartupTN Seed Fund & Incubation", "grant", "Govt of Tamil Nadu", "technology",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["grant", "mentorship", "infrastructure"], "Seed fund, incubator support and stipend for early-stage startups in Tamil Nadu.",
        1000000,
        short_name="StartupTN", geographic_scope="state", states=["Tamil Nadu"],
        applicant_types=["startup", "entrepreneur"],
        enterprise_categories=["startup", "micro"],
        eligibility_rules=[{"field": "location.state", "operator": "equals", "value": "Tamil Nadu", "required": True}],
        official_url="https://startup.tn.gov.in", source="StartupTN",
        eligibility_summary=["Early-stage startup from Tamil Nadu", "Registered / in incubation", "Selected via AcceleratorTN cohort"],
        benefits_list=["Seed grant", "Incubation and co-working", "Mentorship from industry leaders"],
    ),
    _scheme(
        "iCreate Incubation (Gujarat)", "grant", "Govt of Gujarat", "technology",
        ["idea", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["grant", "mentorship", "infrastructure"], "iCreate provides incubation, mentorship and funding to high-impact startups in Gujarat.",
        2500000,
        short_name="iCreate", geographic_scope="state", states=["Gujarat"],
        applicant_types=["startup", "entrepreneur"],
        enterprise_categories=["startup", "micro"],
        eligibility_rules=[{"field": "location.state", "operator": "equals", "value": "Gujarat", "required": True}],
        official_url="https://icreate.org.in", source="iCreate Gujarat",
        eligibility_summary=["Innovative startup", "Gujarat-linked founder or unit", "Meets iCreate evaluation criteria"],
        benefits_list=["Quarterly innovation funding", "World-class incubation", "Mentorship & investor network"],
    ),
    _scheme(
        "Start-up Assam Seed & Incubation", "grant", "Govt of Assam", "technology",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "research_development", "technology_upgrade"],
        ["grant", "mentorship", "infrastructure"], "Seed funding, incubation and policy support for startups in Assam.",
        1000000,
        short_name="Start-up Assam", geographic_scope="state", states=["Assam"],
        applicant_types=["startup", "entrepreneur"],
        enterprise_categories=["startup", "micro"],
        eligibility_rules=[{"field": "location.state", "operator": "equals", "value": "Assam", "required": True}],
        official_url="https://startup.assam.gov.in", source="Assam Startup Cell",
        eligibility_summary=["Startup registered/domiciled in Assam", "Valid business idea", "Admitted to incubation support"],
        benefits_list=["Seed support", "Incubation facility access", "Preferential market access in state"],
    ),
    _scheme(
        "Mukhyamantri Udyami Yojana (Bihar)", "loan", "Govt of Bihar", "all",
        ["early_stage", "growth"],
        ["business_start", "business_expansion", "equipment_purchase"],
        ["loan", "subsidy"], "Loans with 50% capital subsidy (up to ₹10 lakh) for youths (18-35) of Bihar.",
        1000000,
        short_name="MUY Bihar", geographic_scope="state", states=["Bihar"],
        applicant_types=["entrepreneur", "individual"],
        enterprise_categories=["micro", "small"],
        eligibility_rules=[
            {"field": "location.state", "operator": "equals", "value": "Bihar", "required": True},
            {"field": "founder.age", "operator": "less_than_or_equal", "value": 35, "required": False},
        ],
        official_url="https://udyami.bihar.gov.in", source="Bihar Govt",
        eligibility_summary=["Youth aged 18-35", "Bihar resident", "New enterprise or viable project"],
        benefits_list=["Up to 50% capital subsidy", "Loan up to ₹10 lakh", "Bank-linked disbursal"],
    ),
    _scheme(
        "Mukhyamantri Yuva Udyami Yojana (Madhya Pradesh)", "loan", "Govt of Madhya Pradesh", "all",
        ["early_stage", "growth"],
        ["business_start", "business_expansion", "working_capital"],
        ["loan", "subsidy"], "Loans up to ₹40 lakh with 15-25% interest subsidy for youth (18-35) in Madhya Pradesh.",
        4000000,
        short_name="MYY MP", geographic_scope="state", states=["Madhya Pradesh"],
        applicant_types=["entrepreneur", "individual"],
        enterprise_categories=["micro", "small", "medium"],
        eligibility_rules=[
            {"field": "location.state", "operator": "equals", "value": "Madhya Pradesh", "required": True},
            {"field": "founder.age", "operator": "less_than_or_equal", "value": 35, "required": False},
        ],
        official_url="https://muyvmp.mponline.gov.in", source="MP Govt",
        eligibility_summary=["Youth aged 18-35", "MP resident", "Own micro/small enterprise or new project"],
        benefits_list=["Loan up to ₹40 lakh", "15-25% interest subsidy", "No collateral for smaller loans"],
    ),
    _scheme(
        "National Urban Livelihoods Mission", "funding", "Ministry of Housing & Urban Affairs", "all",
        ["idea", "early_stage"],
        ["business_start", "training", "working_capital"],
        ["financial_assistance", "training", "subsidy"], "Self-employment support for urban poor - subsidies, skilling and SHG-based enterprise development.",
        None,
        short_name="Deendayal NULM", applicant_types=["individual", "self_help_group", "entrepreneur"],
        enterprise_categories=["micro"],
        official_url="https://nulm.gov.in", source="MoHUA",
        eligibility_summary=["Urban poor household", "Age 18-55", "Families covered under NULM identification"],
        benefits_list=["Self-employment subsidy", "Skill training with stipend", "SHG bank linkage", "Tool-kit grants"],
    ),
    _scheme(
        "Deendayal Antyodaya - National Rural Livelihoods Mission", "funding", "Ministry of Rural Development", "all",
        ["idea", "pre_registration", "early_stage"],
        ["business_start", "training", "working_capital"],
        ["financial_assistance", "training"], "SHG-based enterprise and livelihood support for rural poor families across India.",
        None,
        short_name="NRLM (Aajeevika)", applicant_types=["self_help_group", "individual", "women_entrepreneur"],
        enterprise_categories=["micro"],
        official_url="https://aajeevika.gov.in", source="MoRD",
        eligibility_summary=["Rural poor family under NRLM", "SHG membership", "Enterprise readiness"],
        benefits_list=["Revolving fund & CIF support", "Skill & enterprise training", "Bank credit linkage"],
    ),
    _scheme(
        "Pradhan Mantri Matsya Sampada Yojana", "subsidy", "Ministry of Fisheries, Animal Husbandry & Dairying", "agriculture",
        ["early_stage", "growth"],
        ["business_start", "equipment_purchase", "business_expansion"],
        ["subsidy", "loan"], "Subsidies for fisheries entrepreneurs - aquaculture, boats, cold chain and processing units.",
        2000000,
        short_name="PMMSY", sub_sectors=["agriculture", "food_processing"],
        applicant_types=["farmer", "entrepreneur", "cooperative", "self_help_group"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://pmmsy.dof.gov.in", source="DAHD",
        eligibility_summary=["Fisher/fishery entrepreneur", "Viable fisheries project", "Bank/agency financing in place"],
        benefits_list=["Capital subsidy up to 40%", "Aquaculture development support", "Cold-chain & processing incentives"],
    ),
    _scheme(
        "Agri-clinics & Agri-Business Centres", "training", "Ministry of Agriculture & Farmers Welfare", "agriculture",
        ["idea", "pre_registration", "early_stage"],
        ["training", "business_start", "technology_upgrade"],
        ["training", "loan", "mentorship"], "Training and loan/extension support for agriculture graduates to establish agri-ventures and clinics.",
        2000000,
        short_name="ACABC", applicant_types=["entrepreneur", "farmer", "individual"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://agriclinics.net", source="DAC&FW",
        eligibility_summary=["Agriculture graduate or equivalent", "Completes recommended training", "Willing to set up agri-enterprise"],
        benefits_list=["2-month training support", "Bank loan eligibility", "Mentoring & extension connect"],
    ),
    _scheme(
        "National Livestock Mission", "subsidy", "Ministry of Fisheries, Animal Husbandry & Dairying", "agriculture",
        ["early_stage", "growth"],
        ["business_start", "equipment_purchase", "business_expansion"],
        ["subsidy"], "Assistance for poultry, sheep, piggery and fodder enterprises under various NLM sub-schemes.",
        1000000,
        short_name="NLM", sub_sectors=["agriculture"],
        applicant_types=["farmer", "entrepreneur", "self_help_group", "cooperative"],
        eligibility_rules=[{"field": "sector.primary", "operator": "equals", "value": "agriculture", "required": False}],
        official_url="https://dahd.nic.in", source="DAHD",
        eligibility_summary=["Livestock enterprise project", "Backyard to commercial scale", "Loan/bank finance for project"],
        benefits_list=["Capital subsidy on units", "Training & breed improvement support", "Fodder development grants"],
    ),
]


def seed_schemes_v2(db: Session = None, force: bool = False):
    """Seed database with comprehensive scheme data"""
    if db is None:
        db = SessionLocal()

    try:
        # Check if schemes already exist
        existing_count = db.query(SchemeV2).count()
        if existing_count > 0 and not force:
            print(f"Database already has {existing_count} schemes (v2). Skipping seed.")
            return

        if existing_count > 0 and force:
            print(f"Reseeding: removing {existing_count} existing schemes (v2).")
            db.query(SchemeV2).delete()
            db.commit()

        print("Seeding government schemes (v2 - structured eligibility)...")

        schemes = [SchemeV2(**scheme_data) for scheme_data in SCHEMES_DATA_V2]
        db.add_all(schemes)
        db.commit()

        print(f"[OK] Successfully seeded {len(schemes)} government schemes!")
        print("\nSchemes added:")
        for scheme in schemes:
            print(f"  - {scheme.name} ({scheme.scheme_type})")

    except Exception as e:
        print(f"[ERROR] Error seeding schemes: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys as _sys
    force = "--force" in _sys.argv
    print("=" * 60)
    print("Starting V2 Scheme Database Seeding" + (" (force reseed)" if force else ""))
    print("=" * 60)
    seed_schemes_v2(force=force)
    print("=" * 60)
    print("Seeding complete!")
    print("=" * 60)
