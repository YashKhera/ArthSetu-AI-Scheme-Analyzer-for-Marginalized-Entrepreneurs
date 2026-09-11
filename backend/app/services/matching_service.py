"""Matching engine service - Core recommendation algorithm"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from app.models.entrepreneur import EntrepreneurProfile
from app.models.scheme import Scheme
from app.models.requirement import Requirement
from app.utils.constants import SCORING_WEIGHTS, MATCH_LEVEL_EXCELLENT, MATCH_LEVEL_STRONG, MATCH_LEVEL_POSSIBLE, MATCH_LEVEL_LOW
from app.utils.helpers import extract_entrepreneur_types, map_business_stage

class MatchingService:

    SCORING_WEIGHTS = SCORING_WEIGHTS

    @staticmethod
    def calculate_match_score(
        profile: EntrepreneurProfile,
        scheme: Scheme,
        requirements: List[Requirement]
    ) -> Dict:
        """
        Calculate match score between profile and scheme.

        Returns:
        {
            "score": 85,
            "level": "Strong Match",
            "matched_criteria": ["sector", "support_type", "location"],
            "gap": "SC/ST status required for maximum benefit"
        }
        """
        score = 0
        matched = []

        # 1. Sector match (30 points)
        if profile.business_sector in scheme.sectors:
            score += MatchingService.SCORING_WEIGHTS["sector"]
            matched.append("sector")

        # 2. Support type match (25 points)
        profile_supports = [req.support_type for req in requirements]
        if any(s in scheme.support_types for s in profile_supports):
            score += MatchingService.SCORING_WEIGHTS["support_type"]
            matched.append("support_type")

        # 3. Location match (15 points)
        if "all" in scheme.states or profile.state in scheme.states:
            score += MatchingService.SCORING_WEIGHTS["location"]
            matched.append("location")

        # 4. Business stage match (10 points)
        mapped_stage = map_business_stage(profile.business_stage)
        if mapped_stage in scheme.business_stages:
            score += MatchingService.SCORING_WEIGHTS["business_stage"]
            matched.append("business_stage")

        # 5. Entrepreneur type match (10 points)
        entrepreneur_types = extract_entrepreneur_types(
            profile.gender,
            profile.social_category,
            profile.age_group
        )
        if any(et in scheme.entrepreneur_types for et in entrepreneur_types):
            score += MatchingService.SCORING_WEIGHTS["entrepreneur_type"]
            matched.append("entrepreneur_type")

        # 6. Business size match (5 points) - based on employee range
        # For MVP, give points if scheme doesn't restrict size
        if "all" in scheme.entrepreneur_types or len(scheme.entrepreneur_types) > 2:
            score += MatchingService.SCORING_WEIGHTS["business_size"]
            matched.append("business_size")

        # Classify score
        if score >= 90:
            level = MATCH_LEVEL_EXCELLENT
        elif score >= 75:
            level = MATCH_LEVEL_STRONG
        elif score >= 60:
            level = MATCH_LEVEL_POSSIBLE
        else:
            level = MATCH_LEVEL_LOW

        # Identify gap
        gap = MatchingService._identify_gap(profile, scheme, entrepreneur_types)

        return {
            "score": score,
            "level": level,
            "matched_criteria": matched,
            "gap": gap
        }

    @staticmethod
    def rank_recommendations(
        profile: EntrepreneurProfile,
        schemes: List[Scheme],
        requirements: List[Requirement],
        min_score: int = 40,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Calculate scores for all schemes and rank by score.

        Returns top schemes sorted by score descending.
        """
        recommendations = []

        for scheme in schemes:
            match_info = MatchingService.calculate_match_score(profile, scheme, requirements)

            # Only include schemes with minimum score
            if match_info["score"] >= min_score:
                recommendations.append({
                    "scheme_id": scheme.id,
                    "scheme_name": scheme.name,
                    **match_info
                })

        # Sort by score descending
        recommendations.sort(key=lambda x: x["score"], reverse=True)

        # Return top recommendations
        return recommendations[:max_results]

    @staticmethod
    def _identify_gap(
        profile: EntrepreneurProfile,
        scheme: Scheme,
        entrepreneur_types: List[str]
    ) -> Optional[str]:
        """Identify missing requirements or potential issues"""
        gaps = []

        # Check if scheme is for specific entrepreneur types not matching profile
        specific_types = ["women", "sc", "st", "youth", "obc"]
        scheme_specific_types = [t for t in scheme.entrepreneur_types if t in specific_types]

        if scheme_specific_types:
            if not any(t in entrepreneur_types for t in scheme_specific_types):
                return f"This scheme prioritizes {', '.join(scheme_specific_types)} entrepreneurs"

        # Check if scheme requires specific registration
        registration_keywords = ["registration", "udyam", "msme", "gst"]
        for eligibility in scheme.eligibility:
            if any(keyword in eligibility.lower() for keyword in registration_keywords):
                gaps.append("Business registration may be required")
                break

        # Check sector mismatch
        if profile.business_sector not in scheme.sectors and "all" not in scheme.sectors:
            return f"Scheme primarily targets {', '.join(scheme.sectors[:2])} sector"

        # Check location restrictions
        if "all" not in scheme.states and profile.state not in scheme.states:
            return f"Scheme available only in {', '.join(scheme.states[:3])}"

        # Return first gap or None
        return gaps[0] if gaps else None

    @staticmethod
    def _extract_entrepreneur_type(profile: EntrepreneurProfile) -> List[str]:
        """Extract entrepreneur categories from profile"""
        return extract_entrepreneur_types(
            profile.gender,
            profile.social_category,
            profile.age_group
        )
