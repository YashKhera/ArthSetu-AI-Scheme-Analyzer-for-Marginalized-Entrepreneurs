"""Seed data for government schemes"""
import sys
import os

# Ensure the backend directory is on the path so `app` imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models.scheme import Scheme
from app.database import SessionLocal

# Government schemes data
SCHEMES_DATA = [
    {
        "name": "PM MUDRA Yojana",
        "department": "Ministry of Finance, Government of India",
        "description": "Pradhan Mantri MUDRA Yojana provides loans up to Rs. 10 Lakh to non-corporate, non-farm small/micro enterprises. These loans are collateral-free and classify into three categories: Shishu (up to ₹50,000), Kishore (₹50,001 to ₹5 lakh), and Tarun (₹5,00,001 to ₹10 lakh).",
        "sectors": ["retail", "services", "manufacturing", "food_processing", "textile", "handicrafts"],
        "states": ["all"],
        "business_stages": ["planning", "existing", "expanding"],
        "support_types": ["loan"],
        "entrepreneur_types": ["general", "women", "sc", "st", "youth", "obc"],
        "benefits": [
            "Collateral-free loan up to Rs. 10 Lakh",
            "Zero processing fee",
            "Government guarantee coverage",
            "Flexible repayment terms"
        ],
        "eligibility": [
            "Indian citizen aged 18+",
            "No existing loan default",
            "Business registered or documented",
            "Valid bank account"
        ],
        "documents": [
            "Aadhaar Card",
            "PAN Card",
            "Business plan or proposal",
            "Bank account details",
            "Identity and address proof"
        ],
        "application_url": "https://www.mudra.org.in"
    },
    {
        "name": "Stand-Up India Scheme",
        "department": "Ministry of Finance, Government of India",
        "description": "Stand-Up India facilitates bank loans between Rs. 10 lakh and Rs. 1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
        "sectors": ["manufacturing", "services", "retail", "food_processing", "textile"],
        "states": ["all"],
        "business_stages": ["planning", "existing"],
        "support_types": ["loan"],
        "entrepreneur_types": ["women", "sc", "st"],
        "benefits": [
            "Loan between Rs. 10 lakh to Rs. 1 Crore",
            "Composite loan including term loan and working capital",
            "Credit Guarantee Fund for Standup India Scheme (CGFSSI)",
            "Handholding support through Stand-Up Connect Centers"
        ],
        "eligibility": [
            "Must be SC/ST and/or Woman entrepreneur",
            "Aged 18 years or above",
            "Loan for greenfield project (first-time venture)",
            "Non-farm sector enterprise"
        ],
        "documents": [
            "Aadhaar Card",
            "PAN Card",
            "Caste certificate (for SC/ST)",
            "Project report",
            "Business registration documents"
        ],
        "application_url": "https://www.standupmitra.in"
    },
    {
        "name": "PMEGP - Prime Minister Employment Generation Programme",
        "department": "Ministry of MSME, Government of India",
        "description": "PMEGP is a credit-linked subsidy programme for generation of employment opportunities through establishment of micro enterprises in non-farm sector. Subsidy ranges from 15% to 35% of project cost.",
        "sectors": ["manufacturing", "services", "retail", "food_processing", "textile", "handicrafts"],
        "states": ["all"],
        "business_stages": ["planning"],
        "support_types": ["subsidy", "loan"],
        "entrepreneur_types": ["general", "women", "sc", "st", "youth", "obc"],
        "benefits": [
            "15-35% subsidy on project cost",
            "Maximum project cost: Rs. 50 lakh (manufacturing), Rs. 20 lakh (services)",
            "Margin money subsidy: 25-35% for general category, 35% for special categories",
            "Easy bank loan facility"
        ],
        "eligibility": [
            "Applicant above 18 years",
            "Minimum 8th pass for projects above Rs. 10 lakh",
            "No income limit for setting up projects",
            "Self Help Groups eligible"
        ],
        "documents": [
            "Educational certificates",
            "Aadhaar Card",
            "PAN Card",
            "Caste certificate (if applicable)",
            "Project report",
            "Bank account details"
        ],
        "application_url": "https://www.kviconline.gov.in/pmegpeportal"
    },
    {
        "name": "PMFME - PM Formalization of Micro Food Processing Enterprises",
        "department": "Ministry of Food Processing Industries",
        "description": "PMFME Scheme provides financial, technical and business support for up-gradation of existing micro food processing enterprises. Focus on cluster-based approach with credit-linked capital subsidy of 35% for individuals and groups.",
        "sectors": ["food_processing", "agriculture"],
        "states": ["all"],
        "business_stages": ["existing", "expanding"],
        "support_types": ["subsidy", "loan", "training"],
        "entrepreneur_types": ["general", "women", "sc", "st", "youth", "obc"],
        "benefits": [
            "35% credit-linked capital subsidy",
            "Maximum subsidy of Rs. 10 lakh per unit",
            "Training and handholding support",
            "Cluster-based branding and marketing support"
        ],
        "eligibility": [
            "Existing food processing micro enterprises",
            "Must have Aadhaar card",
            "Udyam registration required",
            "Must be in food processing business"
        ],
        "documents": [
            "Aadhaar Card",
            "Udyam Registration Certificate",
            "Bank account details",
            "FSSAI license",
            "Business proof",
            "Project report"
        ],
        "application_url": "https://pmfme.mofpi.gov.in"
    },
    {
        "name": "Startup India Seed Fund Scheme",
        "department": "Department for Promotion of Industry and Internal Trade",
        "description": "Startup India Seed Fund Scheme (SISFS) aims to provide financial assistance to startups for proof of concept, prototype development, product trials, market entry and commercialization.",
        "sectors": ["technology", "manufacturing", "services", "healthcare", "education"],
        "states": ["all"],
        "business_stages": ["idea", "planning"],
        "support_types": ["grant", "funding"],
        "entrepreneur_types": ["general", "women", "youth"],
        "benefits": [
            "Seed funding up to Rs. 50 lakh",
            "Grant support for proof of concept",
            "Validation of prototype",
            "Market entry support"
        ],
        "eligibility": [
            "DPIIT recognized startup",
            "Incorporated not more than 2 years ago",
            "Working towards innovation/development of product",
            "Must have business idea with potential"
        ],
        "documents": [
            "Certificate of Incorporation",
            "DPIIT Recognition Number",
            "Pitch deck",
            "Business plan",
            "Identity proofs of founders"
        ],
        "application_url": "https://seedfund.startupindia.gov.in"
    },
    {
        "name": "CGTMSE - Credit Guarantee Scheme",
        "department": "Ministry of MSME, Government of India",
        "description": "Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE) provides guarantee cover for collateral-free credit facilities extended by banks to MSMEs.",
        "sectors": ["manufacturing", "services", "retail", "food_processing", "textile", "handicrafts"],
        "states": ["all"],
        "business_stages": ["existing", "expanding"],
        "support_types": ["loan"],
        "entrepreneur_types": ["general", "women", "sc", "st", "youth", "obc"],
        "benefits": [
            "Collateral-free loans up to Rs. 5 Crore",
            "Credit guarantee coverage up to 85%",
            "Reduced documentation",
            "Faster loan processing"
        ],
        "eligibility": [
            "Micro and Small Enterprise",
            "Credit facility up to Rs. 5 Crore",
            "Loan from eligible lending institution",
            "No collateral/third party guarantee"
        ],
        "documents": [
            "Udyam Registration",
            "Project report",
            "Bank account statements",
            "ITR (if applicable)",
            "Identity and address proof"
        ],
        "application_url": "https://www.cgtmse.in"
    },
    {
        "name": "National SC-ST Hub Scheme",
        "department": "Ministry of MSME, Government of India",
        "description": "The National SC-ST Hub aims to facilitate and support SC/ST entrepreneurs for setting up micro, small and medium manufacturing and service enterprises.",
        "sectors": ["manufacturing", "services", "retail", "food_processing", "textile", "handicrafts"],
        "states": ["all"],
        "business_stages": ["planning", "existing", "expanding"],
        "support_types": ["training", "mentorship", "funding"],
        "entrepreneur_types": ["sc", "st"],
        "benefits": [
            "Marketing support",
            "Technology support",
            "Training and skill development",
            "Tender information and support"
        ],
        "eligibility": [
            "Must belong to SC/ST category",
            "Registered MSME",
            "Caste certificate mandatory"
        ],
        "documents": [
            "Caste certificate (SC/ST)",
            "Aadhaar Card",
            "PAN Card",
            "Udyam Registration",
            "Business registration documents"
        ],
        "application_url": "https://www.scsthub.in"
    },
    {
        "name": "National Rural Livelihood Mission (NRLM)",
        "department": "Ministry of Rural Development",
        "description": "NRLM aims to create efficient and effective institutional platforms for the rural poor enabling them to increase household income through sustainable livelihood enhancements and improved access to financial services.",
        "sectors": ["agriculture", "handicrafts", "services", "food_processing"],
        "states": ["all"],
        "business_stages": ["planning", "existing"],
        "support_types": ["loan", "subsidy", "training"],
        "entrepreneur_types": ["general", "women", "sc", "st", "obc"],
        "benefits": [
            "Financial assistance to Self Help Groups",
            "Revolving Fund support",
            "Community Investment Fund",
            "Skill development training"
        ],
        "eligibility": [
            "Rural poor households",
            "Member of Self Help Group (SHG)",
            "Below Poverty Line or vulnerable categories"
        ],
        "documents": [
            "Aadhaar Card",
            "Ration Card",
            "Income certificate",
            "SHG membership proof",
            "Bank account details"
        ],
        "application_url": "https://aajeevika.gov.in"
    },
    {
        "name": "MSME Support & Outreach Programme",
        "department": "Ministry of MSME, Government of India",
        "description": "Comprehensive support programme for MSMEs including access to credit, technology upgradation, marketing assistance, and skill development initiatives.",
        "sectors": ["manufacturing", "services", "retail", "food_processing", "textile", "technology"],
        "states": ["all"],
        "business_stages": ["existing", "expanding"],
        "support_types": ["loan", "training", "equipment", "mentorship"],
        "entrepreneur_types": ["general", "women", "sc", "st", "youth", "obc"],
        "benefits": [
            "Technology upgradation support",
            "Marketing assistance",
            "Quality certification support",
            "Skill development programmes"
        ],
        "eligibility": [
            "Registered MSME",
            "Udyam Registration",
            "Valid business operations"
        ],
        "documents": [
            "Udyam Registration Certificate",
            "PAN Card",
            "GST Registration",
            "Bank account details",
            "Business proof"
        ],
        "application_url": "https://msme.gov.in"
    },
    {
        "name": "Women Entrepreneurship Platform (WEP)",
        "department": "NITI Aayog, Government of India",
        "description": "A unified platform that brings together government schemes, private partnerships, and resources to support women entrepreneurs across India with mentorship, funding, and skilling opportunities.",
        "sectors": ["all"],
        "states": ["all"],
        "business_stages": ["idea", "planning", "existing", "expanding"],
        "support_types": ["training", "mentorship", "funding"],
        "entrepreneur_types": ["women"],
        "benefits": [
            "Mentorship from successful entrepreneurs",
            "Access to incubators and accelerators",
            "Networking opportunities",
            "Information on funding schemes"
        ],
        "eligibility": [
            "Must be a woman entrepreneur",
            "Indian citizen",
            "Business idea or existing business"
        ],
        "documents": [
            "Aadhaar Card",
            "PAN Card",
            "Business plan",
            "Educational certificates"
        ],
        "application_url": "https://wep.gov.in"
    }
]

def seed_schemes(db: Session = None):
    """Populate database with initial scheme dataset"""
    if db is None:
        db = SessionLocal()

    try:
        # Check if schemes already exist
        existing_count = db.query(Scheme).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} schemes. Skipping seed.")
            return

        print("Seeding government schemes...")

        schemes = [Scheme(**scheme_data) for scheme_data in SCHEMES_DATA]
        db.add_all(schemes)
        db.commit()

        print(f"Successfully seeded {len(schemes)} government schemes!")

    except Exception as e:
        print(f"Error seeding schemes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeding...")
    seed_schemes()
    print("Seeding complete!")
