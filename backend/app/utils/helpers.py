"""Helper utilities"""
import re
from typing import List, Optional

def clean_string(text: str) -> str:
    """Clean and normalize string"""
    if not text:
        return ""
    return text.strip().lower()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate Indian phone number"""
    pattern = r'^[6-9]\d{9}$'
    cleaned = re.sub(r'[^\d]', '', phone)
    return bool(re.match(pattern, cleaned))

def normalize_list(items: List[str]) -> List[str]:
    """Normalize list of strings"""
    return [clean_string(item) for item in items if item]

def extract_entrepreneur_types(gender: str, social_category: str, age_group: str) -> List[str]:
    """Extract entrepreneur type categories from profile"""
    types = ["general"]

    if gender == "female":
        types.append("women")

    if social_category == "sc":
        types.append("sc")
    elif social_category == "st":
        types.append("st")
    elif social_category == "obc":
        types.append("obc")

    # Youth category (18-35)
    if age_group in ["18-25", "26-35"]:
        types.append("youth")

    return types

def map_business_stage(stage: str) -> str:
    """Map business stage to scheme-compatible format"""
    stage_mapping = {
        "idea": "planning",
        "planning": "planning",
        "existing": "existing",
        "expanding": "expanding"
    }
    return stage_mapping.get(clean_string(stage), "planning")
