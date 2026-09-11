"""Constants and enums following the Government Schemes Data Structure specification"""

# ---------------------------------------------------------------------------
# Scheme types
# ---------------------------------------------------------------------------
SCHEME_TYPE_FUNDING = "funding"
SCHEME_TYPE_LOAN = "loan"
SCHEME_TYPE_SUBSIDY = "subsidy"
SCHEME_TYPE_GRANT = "grant"
SCHEME_TYPE_TAX_BENEFIT = "tax_benefit"
SCHEME_TYPE_TRAINING = "training"
SCHEME_TYPE_SKILL_DEVELOPMENT = "skill_development"
SCHEME_TYPE_INFRASTRUCTURE = "infrastructure"
SCHEME_TYPE_MARKET_ACCESS = "market_access"
SCHEME_TYPE_CREDIT_SUPPORT = "credit_support"
SCHEME_TYPE_INSURANCE = "insurance"
SCHEME_TYPE_OTHER = "other"

SCHEME_TYPES = [
    SCHEME_TYPE_FUNDING,
    SCHEME_TYPE_LOAN,
    SCHEME_TYPE_SUBSIDY,
    SCHEME_TYPE_GRANT,
    SCHEME_TYPE_TAX_BENEFIT,
    SCHEME_TYPE_TRAINING,
    SCHEME_TYPE_SKILL_DEVELOPMENT,
    SCHEME_TYPE_INFRASTRUCTURE,
    SCHEME_TYPE_MARKET_ACCESS,
    SCHEME_TYPE_CREDIT_SUPPORT,
    SCHEME_TYPE_INSURANCE,
    SCHEME_TYPE_OTHER,
]

# ---------------------------------------------------------------------------
# Applicant types
# ---------------------------------------------------------------------------
APPLICANT_STARTUP = "startup"
APPLICANT_MSME = "msme"
APPLICANT_ENTREPRENEUR = "entrepreneur"
APPLICANT_INDIVIDUAL = "individual"
APPLICANT_WOMEN_ENTREPRENEUR = "women_entrepreneur"
APPLICANT_STUDENT = "student"
APPLICANT_FARMER = "farmer"
APPLICANT_SELF_HELP_GROUP = "self_help_group"
APPLICANT_COOPERATIVE = "cooperative"
APPLICANT_MANUFACTURER = "manufacturer"
APPLICANT_SERVICE_PROVIDER = "service_provider"
APPLICANT_EXPORTER = "exporter"
APPLICANT_ARTISAN = "artisan"

APPLICANT_TYPES = [
    APPLICANT_STARTUP,
    APPLICANT_MSME,
    APPLICANT_ENTREPRENEUR,
    APPLICANT_INDIVIDUAL,
    APPLICANT_WOMEN_ENTREPRENEUR,
    APPLICANT_STUDENT,
    APPLICANT_FARMER,
    APPLICANT_SELF_HELP_GROUP,
    APPLICANT_COOPERATIVE,
    APPLICANT_MANUFACTURER,
    APPLICANT_SERVICE_PROVIDER,
    APPLICANT_EXPORTER,
    APPLICANT_ARTISAN,
]

# ---------------------------------------------------------------------------
# Business stages (normalized - used by schemes AND profiles)
# ---------------------------------------------------------------------------
STAGE_IDEA = "idea"
STAGE_PRE_REGISTRATION = "pre_registration"
STAGE_EARLY_STAGE = "early_stage"
STAGE_GROWTH = "growth"
STAGE_ESTABLISHED = "established"
STAGE_EXPANSION = "expansion"

BUSINESS_STAGES = [
    STAGE_IDEA,
    STAGE_PRE_REGISTRATION,
    STAGE_EARLY_STAGE,
    STAGE_GROWTH,
    STAGE_ESTABLISHED,
    STAGE_EXPANSION,
]

# Map legacy profile stage values to the normalized set above
LEGACY_STAGE_MAPPING = {
    "idea": STAGE_IDEA,
    "planning": STAGE_PRE_REGISTRATION,
    "pre_registration": STAGE_PRE_REGISTRATION,
    "early_stage": STAGE_EARLY_STAGE,
    "existing": STAGE_ESTABLISHED,
    "established": STAGE_ESTABLISHED,
    "growth": STAGE_GROWTH,
    "expanding": STAGE_EXPANSION,
    "expansion": STAGE_EXPANSION,
}

# ---------------------------------------------------------------------------
# Business sectors (normalized)
# ---------------------------------------------------------------------------
SECTOR_AGRICULTURE = "agriculture"
SECTOR_TECHNOLOGY = "technology"
SECTOR_MANUFACTURING = "manufacturing"
SECTOR_SERVICES = "services"
SECTOR_HEALTHCARE = "healthcare"
SECTOR_EDUCATION = "education"
SECTOR_FINTECH = "fintech"
SECTOR_RETAIL = "retail"
SECTOR_TEXTILE = "textile"
SECTOR_FOOD_PROCESSING = "food_processing"
SECTOR_TOURISM = "tourism"
SECTOR_LOGISTICS = "logistics"
SECTOR_RENEWABLE_ENERGY = "renewable_energy"
SECTOR_CONSTRUCTION = "construction"
SECTOR_EXPORT = "export"
SECTOR_HANDICRAFTS = "handicrafts"

SECTORS = [
    SECTOR_AGRICULTURE,
    SECTOR_TECHNOLOGY,
    SECTOR_MANUFACTURING,
    SECTOR_SERVICES,
    SECTOR_HEALTHCARE,
    SECTOR_EDUCATION,
    SECTOR_FINTECH,
    SECTOR_RETAIL,
    SECTOR_TEXTILE,
    SECTOR_FOOD_PROCESSING,
    SECTOR_TOURISM,
    SECTOR_LOGISTICS,
    SECTOR_RENEWABLE_ENERGY,
    SECTOR_CONSTRUCTION,
    SECTOR_EXPORT,
    SECTOR_HANDICRAFTS,
]

# ---------------------------------------------------------------------------
# Geographic scope
# ---------------------------------------------------------------------------
GEO_SCOPE_NATIONAL = "national"
GEO_SCOPE_STATE = "state"
GEO_SCOPE_DISTRICT = "district"
GEO_SCOPE_REGION = "region"
GEO_SCOPE_SPECIAL_ZONE = "special_zone"

GEOGRAPHIC_SCOPES = [
    GEO_SCOPE_NATIONAL,
    GEO_SCOPE_STATE,
    GEO_SCOPE_DISTRICT,
    GEO_SCOPE_REGION,
    GEO_SCOPE_SPECIAL_ZONE,
]

# ---------------------------------------------------------------------------
# Business types
# ---------------------------------------------------------------------------
BUSINESS_TYPE_SOLE_PROPRIETORSHIP = "sole_proprietorship"
BUSINESS_TYPE_PARTNERSHIP = "partnership"
BUSINESS_TYPE_LLP = "llp"
BUSINESS_TYPE_PRIVATE_LIMITED = "private_limited"
BUSINESS_TYPE_PUBLIC_LIMITED = "public_limited"
BUSINESS_TYPE_COOPERATIVE = "cooperative"
BUSINESS_TYPE_SELF_HELP_GROUP = "self_help_group"
BUSINESS_TYPE_INDIVIDUAL = "individual"

BUSINESS_TYPES = [
    BUSINESS_TYPE_SOLE_PROPRIETORSHIP,
    BUSINESS_TYPE_PARTNERSHIP,
    BUSINESS_TYPE_LLP,
    BUSINESS_TYPE_PRIVATE_LIMITED,
    BUSINESS_TYPE_PUBLIC_LIMITED,
    BUSINESS_TYPE_COOPERATIVE,
    BUSINESS_TYPE_SELF_HELP_GROUP,
    BUSINESS_TYPE_INDIVIDUAL,
]

# ---------------------------------------------------------------------------
# Enterprise categories
# ---------------------------------------------------------------------------
ENTERPRISE_MICRO = "micro"
ENTERPRISE_SMALL = "small"
ENTERPRISE_MEDIUM = "medium"
ENTERPRISE_LARGE = "large"
ENTERPRISE_STARTUP = "startup"

ENTERPRISE_CATEGORIES = [
    ENTERPRISE_MICRO,
    ENTERPRISE_SMALL,
    ENTERPRISE_MEDIUM,
    ENTERPRISE_LARGE,
    ENTERPRISE_STARTUP,
]

# ---------------------------------------------------------------------------
# Purposes / user requirements
# ---------------------------------------------------------------------------
PURPOSE_BUSINESS_START = "business_start"
PURPOSE_WORKING_CAPITAL = "working_capital"
PURPOSE_BUSINESS_EXPANSION = "business_expansion"
PURPOSE_EQUIPMENT_PURCHASE = "equipment_purchase"
PURPOSE_TECHNOLOGY_UPGRADE = "technology_upgrade"
PURPOSE_RESEARCH_DEVELOPMENT = "research_development"
PURPOSE_EXPORT = "export"
PURPOSE_MARKETING = "marketing"
PURPOSE_TRAINING = "training"
PURPOSE_SKILL_DEVELOPMENT = "skill_development"
PURPOSE_INFRASTRUCTURE = "infrastructure"
PURPOSE_EMPLOYMENT = "employment"
PURPOSE_WOMEN_ENTREPRENEURSHIP = "women_entrepreneurship"
PURPOSE_GREEN_ENERGY = "green_energy"
PURPOSE_DIGITAL_TRANSFORMATION = "digital_transformation"

PURPOSES = [
    PURPOSE_BUSINESS_START,
    PURPOSE_WORKING_CAPITAL,
    PURPOSE_BUSINESS_EXPANSION,
    PURPOSE_EQUIPMENT_PURCHASE,
    PURPOSE_TECHNOLOGY_UPGRADE,
    PURPOSE_RESEARCH_DEVELOPMENT,
    PURPOSE_EXPORT,
    PURPOSE_MARKETING,
    PURPOSE_TRAINING,
    PURPOSE_SKILL_DEVELOPMENT,
    PURPOSE_INFRASTRUCTURE,
    PURPOSE_EMPLOYMENT,
    PURPOSE_WOMEN_ENTREPRENEURSHIP,
    PURPOSE_GREEN_ENERGY,
    PURPOSE_DIGITAL_TRANSFORMATION,
]

# ---------------------------------------------------------------------------
# Benefit types
# ---------------------------------------------------------------------------
BENEFIT_GRANT = "grant"
BENEFIT_LOAN = "loan"
BENEFIT_SUBSIDY = "subsidy"
BENEFIT_INTEREST_SUBSIDY = "interest_subsidy"
BENEFIT_TAX_BENEFIT = "tax_benefit"
BENEFIT_CREDIT_GUARANTEE = "credit_guarantee"
BENEFIT_TRAINING = "training"
BENEFIT_MENTORSHIP = "mentorship"
BENEFIT_INFRASTRUCTURE = "infrastructure"
BENEFIT_MARKET_ACCESS = "market_access"
BENEFIT_FINANCIAL_ASSISTANCE = "financial_assistance"

BENEFIT_TYPES = [
    BENEFIT_GRANT,
    BENEFIT_LOAN,
    BENEFIT_SUBSIDY,
    BENEFIT_INTEREST_SUBSIDY,
    BENEFIT_TAX_BENEFIT,
    BENEFIT_CREDIT_GUARANTEE,
    BENEFIT_TRAINING,
    BENEFIT_MENTORSHIP,
    BENEFIT_INFRASTRUCTURE,
    BENEFIT_MARKET_ACCESS,
    BENEFIT_FINANCIAL_ASSISTANCE,
]

# ---------------------------------------------------------------------------
# Founder eligibility
# ---------------------------------------------------------------------------
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_OTHER = "other"
GENDER_ANY = "any"

GENDERS = [GENDER_MALE, GENDER_FEMALE, GENDER_OTHER, GENDER_ANY]

SOCIAL_CATEGORY_GENERAL = "general"
SOCIAL_CATEGORY_OBC = "obc"
SOCIAL_CATEGORY_SC = "sc"
SOCIAL_CATEGORY_ST = "st"
SOCIAL_CATEGORY_MINORITY = "minority"
SOCIAL_CATEGORY_ANY = "any"

SOCIAL_CATEGORIES = [
    SOCIAL_CATEGORY_GENERAL,
    SOCIAL_CATEGORY_OBC,
    SOCIAL_CATEGORY_SC,
    SOCIAL_CATEGORY_ST,
    SOCIAL_CATEGORY_MINORITY,
    SOCIAL_CATEGORY_ANY,
]

# ---------------------------------------------------------------------------
# Rule operators
# ---------------------------------------------------------------------------
SUPPORTED_RULE_OPERATORS = [
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "greater_than",
    "greater_than_or_equal",
    "less_than",
    "less_than_or_equal",
    "in",
    "not_in",
]

# ---------------------------------------------------------------------------
# Match levels and scoring weights (0-100)
# ---------------------------------------------------------------------------
MATCH_LEVEL_EXCELLENT = "Excellent Match"
MATCH_LEVEL_STRONG = "Strong Match"
MATCH_LEVEL_GOOD = "Good Match"
MATCH_LEVEL_POSSIBLE = "Possible Match"
MATCH_LEVEL_LOW = "Low Match"

SCORING_WEIGHTS = {
    "sector": 30,
    "support_type": 25,
    "location": 15,
    "business_stage": 10,
    "entrepreneur_type": 10,
    "business_size": 5,
    "registration": 5,
}

# ---------------------------------------------------------------------------
# Legacy profile option values (kept for form dropdowns / validation)
# ---------------------------------------------------------------------------
AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "55+"]

INCOME_RANGES = ["<1L", "1L-5L", "5L-10L", "10L-25L", "25L-50L", "50L-1Cr", "1Cr+"]

EMPLOYEE_RANGES = ["0", "1-5", "6-10", "11-50", "51-100", "100+"]

SUPPORT_TYPES = [
    "loan",
    "subsidy",
    "grant",
    "training",
    "equipment",
    "machinery",
    "funding",
    "mentorship",
]