"""
Eligibility-based Matching Engine
Follows the principle: Mandatory Eligibility -> Relevance Matching -> Ranking

Implements the Government Schemes Data Structure rules:
    - Mandatory eligibility acts as a hard filter
    - Relevance attributes are used for ranking
"""
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from app.models.entrepreneur import EntrepreneurProfile
from app.utils.constants import LEGACY_STAGE_MAPPING


def _age_group_to_number(age_group: Optional[str]) -> Optional[int]:
    """Convert an age group string to a representative numeric age.

    "18-25" -> 18, "26-35" -> 26, "55+" -> 55, None -> None
    """
    if not age_group:
        return None
    try:
        cleaned = str(age_group).strip()
        if cleaned.endswith("+"):
            return int(float(cleaned[:-1]))
        return int(float(cleaned.split("-")[0]))
    except Exception:
        return None


def _employee_range_to_category(employee_range: Optional[str]) -> Optional[str]:
    """Map employee range to an enterprise category (micro/small/medium)."""
    if not employee_range:
        return None
    try:
        cleaned = str(employee_range).strip()
        if cleaned in ("0", "1", "1-5", "6-10"):
            return "micro"
        if cleaned in ("11-50", "50", "51-100"):
            return "small"
        if cleaned in ("100+", ">100"):
            return "medium"
        return None
    except Exception:
        return None


def _derive_applicant_types(profile: EntrepreneurProfile) -> List[str]:
    """Derive the applicant-type tags for a profile so targeted schemes can score."""
    types = ["entrepreneur"]

    stage = LEGACY_STAGE_MAPPING.get(profile.business_stage, profile.business_stage)

    if profile.business_sector == "agriculture" or "agri" in profile.business_sector:
        types.append("farmer")

    if profile.gender == "female":
        types.append("women_entrepreneur")

    if profile.social_category in ("sc", "st"):
        types.append("shg_member" if not types else "individual")

    if stage in ("idea", "pre_registration", "early_stage"):
        types.append("startup")

    if stage in ("early_stage", "growth", "established"):
        types.append("msme")

    if profile.business_sector in ("textile", "handicrafts"):
        types.append("artisan")

    # Self-help group approximation
    if profile.business_sector == "agriculture" and profile.employee_range in ("1-5", "6-10"):
        types.append("self_help_group")

    return types


class EligibilityEngine:
    """
    Core eligibility evaluation engine.
    Evaluates scheme eligibility rules against a normalized user profile.
    """

    SUPPORTED_OPERATORS = {
        "equals": lambda a, b: a == b,
        "not_equals": lambda a, b: a != b,
        "contains": lambda a, b: b in a if isinstance(a, (list, str)) else False,
        "not_contains": lambda a, b: b not in a if isinstance(a, (list, str)) else True,
        "greater_than": lambda a, b: _safe_float(a) > _safe_float(b),
        "greater_than_or_equal": lambda a, b: _safe_float(a) >= _safe_float(b),
        "less_than": lambda a, b: _safe_float(a) < _safe_float(b),
        "less_than_or_equal": lambda a, b: _safe_float(a) <= _safe_float(b),
        "in": lambda a, b: a in b if isinstance(b, list) else False,
        "not_in": lambda a, b: a not in b if isinstance(b, list) else True,
    }

    @staticmethod
    def evaluate_rule(rule: Dict, profile_data: Dict) -> bool:
        """
        Evaluate a single eligibility rule against normalized profile data.

        Args:
            rule: {"field": "sector.primary", "operator": "equals", "value": "technology"}
            profile_data: Normalized user profile as dictionary

        Returns:
            True if rule passes, False otherwise
        """
        field = rule.get("field")
        operator = rule.get("operator")
        expected_value = rule.get("value")

        if not field or not operator:
            return False

        # Get actual value from profile
        actual_value = EligibilityEngine._get_nested_value(profile_data, field)

        if actual_value is None:
            return False

        # Get operator function
        operator_func = EligibilityEngine.SUPPORTED_OPERATORS.get(operator)
        if not operator_func:
            return False

        try:
            return operator_func(actual_value, expected_value)
        except Exception:
            return False

    @staticmethod
    def _get_nested_value(data: Dict, field: str) -> Any:
        """
        Get nested value from dictionary using dot notation.
        Example: "business.sector" -> data["business"]["sector"]
        """
        keys = field.split(".")
        value = data

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None

            if value is None:
                return None

        return value

    @staticmethod
    def check_mandatory_eligibility(scheme: Any, profile_data: Dict) -> Dict:
        """
        Check all mandatory (required=True) eligibility rules.
        Returns pass/fail status and reasons.

        Returns:
            {
                "eligible": True/False,
                "passed_rules": [...],
                "failed_rules": [...],
                "failure_reasons": [...]
            }
        """
        if not scheme.eligibility_rules:
            return {
                "eligible": True,
                "passed_rules": [],
                "failed_rules": [],
                "failure_reasons": [],
            }

        passed = []
        failed = []
        reasons = []

        for rule in scheme.eligibility_rules:
            if not rule.get("required", True):
                continue  # Skip non-mandatory (preference) rules

            if EligibilityEngine.evaluate_rule(rule, profile_data):
                passed.append(rule)
            else:
                failed.append(rule)
                reasons.append(EligibilityEngine._format_failure_reason(rule))

        eligible = len(failed) == 0

        return {
            "eligible": eligible,
            "passed_rules": passed,
            "failed_rules": failed,
            "failure_reasons": reasons,
        }

    @staticmethod
    def _format_failure_reason(rule: Dict) -> str:
        """Format human-readable failure reason."""
        field = rule.get("field", "")
        operator = rule.get("operator", "")
        value = rule.get("value", "")

        field_labels = {
            "sector.primary": "Business Sector",
            "business.sector": "Business Sector",
            "business.stage": "Business Stage",
            "location.state": "State",
            "business.type": "Business Type",
            "business.age": "Business Age",
            "founder.age": "Age",
            "founder.gender": "Gender",
            "founder.social_category": "Social Category",
            "founder.category": "Social Category",
        }

        field_label = field_labels.get(field, field)

        if operator == "equals":
            return f"{field_label} must be {value}"
        elif operator == "contains":
            return f"{field_label} must include {value}"
        elif operator == "in":
            return f"{field_label} must be one of {value}"
        elif operator == "greater_than_or_equal":
            return f"{field_label} must be at least {value}"
        elif operator == "less_than_or_equal":
            return f"{field_label} must be at most {value}"
        elif operator == "not_equals":
            return f"{field_label} must not be {value}"
        else:
            return f"{field_label} requirement not met"


class RelevanceScorer:
    """
    Calculate relevance score for schemes that pass mandatory eligibility.
    Follows priority: Sector > Purpose > Stage > Location > Type > Size
    """

    # Scoring weights (total = 100)
    WEIGHTS = {
        "sector_match": 30,
        "purpose_match": 25,
        "stage_match": 15,
        "location_match": 10,
        "entrepreneur_type": 10,
        "business_size": 10,
    }

    @staticmethod
    def calculate_relevance_score(
        scheme: Any, profile_data: Dict, requirements: List[str]
    ) -> Dict:
        """
        Calculate how relevant a scheme is to the user's profile.
        Only called for schemes that passed mandatory eligibility.

        Returns:
            {
                "score": 85,
                "breakdown": {...},
                "matched_criteria": [...]
            }
        """
        score = 0
        breakdown = {}
        matched = []

        # 1. Sector match (30 points)
        sector_score = RelevanceScorer._score_sector(
            scheme.primary_sector,
            scheme.sub_sectors or [],
            profile_data.get("business", {}).get("sector"),
        )
        if sector_score > 0:
            score += sector_score
            matched.append("sector")
        breakdown["sector"] = sector_score

        # 2. Purpose match (25 points)
        purpose_score = RelevanceScorer._score_purposes(
            scheme.supported_purposes or [],
            requirements,
        )
        if purpose_score > 0:
            score += purpose_score
            matched.append("purpose")
        breakdown["purpose"] = purpose_score

        # 3. Business stage match (15 points)
        stage_score = RelevanceScorer._score_stage(
            scheme.business_stages or [],
            profile_data.get("business", {}).get("stage"),
        )
        if stage_score > 0:
            score += stage_score
            matched.append("stage")
        breakdown["stage"] = stage_score

        # 4. Location match (10 points)
        location_score = RelevanceScorer._score_location(
            scheme.geographic_scope,
            scheme.states or [],
            profile_data.get("location", {}).get("state"),
        )
        if location_score > 0:
            score += location_score
            matched.append("location")
        breakdown["location"] = location_score

        # 5. Entrepreneur type (10 points)
        entrepreneur_score = RelevanceScorer._score_entrepreneur_type(
            scheme.applicant_types or [],
            scheme.gender_eligibility or ["any"],
            scheme.social_categories or ["any"],
            profile_data.get("founder", {}),
        )
        if entrepreneur_score > 0:
            score += entrepreneur_score
            matched.append("entrepreneur_type")
        breakdown["entrepreneur_type"] = entrepreneur_score

        # 6. Business size (10 points)
        size_score = RelevanceScorer._score_business_size(
            scheme.enterprise_categories or [],
            profile_data.get("business", {}),
        )
        if size_score > 0:
            score += size_score
            matched.append("business_size")
        breakdown["business_size"] = size_score

        return {
            "score": round(score, 2),
            "breakdown": breakdown,
            "matched_criteria": matched,
        }

    @staticmethod
    def _score_sector(primary_sector: str, sub_sectors: List[str], user_sector: str) -> float:
        if not user_sector:
            return 0

        if primary_sector == "all" or user_sector == "all":
            return RelevanceScorer.WEIGHTS["sector_match"] * 0.5

        if user_sector == primary_sector:
            return RelevanceScorer.WEIGHTS["sector_match"]

        if sub_sectors and user_sector in sub_sectors:
            return RelevanceScorer.WEIGHTS["sector_match"] * 0.8

        return 0

    @staticmethod
    def _score_purposes(scheme_purposes: List[str], user_requirements: List[str]) -> float:
        if not user_requirements:
            return 0

        if not scheme_purposes:
            return RelevanceScorer.WEIGHTS["purpose_match"] * 0.3

        # Map legacy support types to normalized purposes
        purpose_aliases = {
            "loan": ["working_capital", "business_expansion", "business_start"],
            "funding": ["working_capital", "financial_assistance", "business_expansion"],
            "subsidy": ["equipment_purchase", "business_expansion", "technology_upgrade"],
            "grant": ["research_development", "business_start", "technology_upgrade"],
            "training": ["training", "skill_development"],
            "equipment": ["equipment_purchase"],
            "machinery": ["equipment_purchase"],
            "mentorship": ["training", "skill_development", "market_access"],
        }

        matched_requirements = 0
        for req in user_requirements:
            candidate_purposes = [req] + purpose_aliases.get(req, [])
            if any(p in scheme_purposes for p in candidate_purposes):
                matched_requirements += 1

        match_ratio = matched_requirements / len(user_requirements)
        return RelevanceScorer.WEIGHTS["purpose_match"] * min(match_ratio, 1.0)

    @staticmethod
    def _score_stage(scheme_stages: List[str], user_stage: str) -> float:
        if not user_stage:
            return 0

        if not scheme_stages or "all" in scheme_stages:
            return RelevanceScorer.WEIGHTS["stage_match"] * 0.5

        if user_stage in scheme_stages:
            return RelevanceScorer.WEIGHTS["stage_match"]

        return 0

    @staticmethod
    def _score_location(scope: str, scheme_states: List[str], user_state: str) -> float:
        if scope == "national" or not scheme_states:
            return RelevanceScorer.WEIGHTS["location_match"]

        if user_state and user_state in scheme_states:
            return RelevanceScorer.WEIGHTS["location_match"]

        return 0

    @staticmethod
    def _score_entrepreneur_type(
        applicant_types: List[str],
        gender_eligibility: List[str],
        social_categories: List[str],
        founder_data: Dict,
    ) -> float:
        score = 0
        max_score = RelevanceScorer.WEIGHTS["entrepreneur_type"]

        # Check if the scheme is unrestricted
        if "any" in applicant_types or "general" in applicant_types or not applicant_types:
            score += max_score * 0.5

        user_gender = founder_data.get("gender")
        if user_gender and ("any" in gender_eligibility or user_gender in gender_eligibility):
            score += max_score * 0.25

        user_category = founder_data.get("social_category")
        if user_category and ("any" in social_categories or user_category in social_categories):
            score += max_score * 0.25

        return min(score, max_score)

    @staticmethod
    def _score_business_size(enterprise_categories: List[str], business_data: Dict) -> float:
        if not enterprise_categories or "any" in enterprise_categories:
            return RelevanceScorer.WEIGHTS["business_size"]

        user_category = business_data.get("enterprise_category")
        if user_category and user_category in enterprise_categories:
            return RelevanceScorer.WEIGHTS["business_size"]

        # For MVP, give a partial score when a category cannot be derived
        return RelevanceScorer.WEIGHTS["business_size"] * 0.5


class MatchingEngineV2:
    """
    Complete matching workflow: Eligibility -> Relevance -> Ranking
    """

    @staticmethod
    def get_recommendations(
        schemes: List[Any],
        profile: EntrepreneurProfile,
        requirements: List[str],
        min_relevance_score: float = 40.0,
        max_results: int = 10,
    ) -> List[Dict]:
        """
        Main recommendation engine.

        Workflow:
        1. Normalize profile to standardized dict
        2. Filter schemes by mandatory eligibility (hard filter)
        3. Calculate relevance scores for eligible schemes
        4. Rank by relevance score
        5. Return top N recommendations
        """
        profile_data = MatchingEngineV2._profile_to_dict(profile)

        recommendations = []

        for scheme in schemes:
            # Step 1: Check mandatory eligibility
            eligibility_check = EligibilityEngine.check_mandatory_eligibility(scheme, profile_data)

            if not eligibility_check["eligible"]:
                continue

            # Step 2: Calculate relevance score
            relevance = RelevanceScorer.calculate_relevance_score(scheme, profile_data, requirements)

            # Step 3: Filter by minimum score
            if relevance["score"] < min_relevance_score:
                continue

            # Step 4: Build recommendation
            recommendations.append({
                "scheme_id": scheme.id,
                "scheme_name": scheme.name,
                "match_score": relevance["score"],
                "matched_criteria": relevance["matched_criteria"],
                "score_breakdown": relevance["breakdown"],
                "match_level": MatchingEngineV2._classify_score(relevance["score"]),
                "scheme": scheme,
            })

        # Step 5: Sort by relevance score (descending)
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)

        # Step 6: Return top N
        return recommendations[:max_results]

    @staticmethod
    def _profile_to_dict(profile: EntrepreneurProfile) -> Dict:
        """Normalize an EntrepreneurProfile into a dictionary the rule engine can test."""
        stage = LEGACY_STAGE_MAPPING.get(profile.business_stage, profile.business_stage)

        return {
            "business": {
                "sector": profile.business_sector,
                "stage": stage,
                "type": getattr(profile, "business_type", None),
                "annual_income": profile.annual_income_range,
                "employees": profile.employee_range,
                "enterprise_category": _employee_range_to_category(profile.employee_range),
            },
            "location": {
                "state": profile.state,
                "district": profile.district,
            },
            "founder": {
                "age": _age_group_to_number(profile.age_group),
                "age_group": profile.age_group,
                "gender": profile.gender,
                "social_category": profile.social_category,
                "applicant_types": _derive_applicant_types(profile),
            },
        }

    @staticmethod
    def _classify_score(score: float) -> str:
        if score >= 85:
            return "Excellent Match"
        elif score >= 70:
            return "Strong Match"
        elif score >= 55:
            return "Good Match"
        elif score >= 40:
            return "Possible Match"
        else:
            return "Low Match"


def _safe_float(value) -> Optional[float]:
    """Safely cast a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None