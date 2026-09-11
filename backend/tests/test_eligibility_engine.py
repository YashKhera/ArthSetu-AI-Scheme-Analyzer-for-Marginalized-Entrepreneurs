"""Unit tests for the eligibility-based matching engine."""
import unittest
from types import SimpleNamespace

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.entrepreneur import EntrepreneurProfile
from app.services.eligibility_engine import (
    EligibilityEngine,
    RelevanceScorer,
    MatchingEngineV2,
    _age_group_to_number,
    _employee_range_to_category,
)


def build_profile(**overrides):
    """Build an EntrepreneurProfile with sensible defaults.""" 
    defaults = dict(
        user_id=1,
        full_name="Test User",
        phone_number="9876543210",
        state="Delhi",
        district="New Delhi",
        age_group="26-35",
        gender="female",
        social_category="general",
        business_name="Fresh Foods",
        business_sector="food_processing",
        business_stage="existing",
        annual_income_range="5L-10L",
        employee_range="1-5",
    )
    defaults.update(overrides)
    return EntrepreneurProfile(**defaults)


def build_scheme(**overrides):
    """Build a fake scheme object without touching the DB."""
    defaults = dict(
        id=99,
        name="Test Scheme",
        short_name="TEST",
        description="A generic test scheme",
        scheme_type="loan",
        ministry="Ministry of MSME",
        primary_sector="all",
        sub_sectors=[],
        applicant_types=["entrepreneur"],
        business_stages=["all"],
        geographic_scope="national",
        states=[],
        enterprise_categories=["micro"],
        supported_purposes=["working_capital", "business_expansion"],
        gender_eligibility=["any"],
        social_categories=["any"],
        eligibility_rules=[],
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


class TestAgeGroupConversion(unittest.TestCase):
    def test_lower_bound(self):
        self.assertEqual(_age_group_to_number("18-25"), 18)

    def test_upperplus(self):
        self.assertEqual(_age_group_to_number("55+"), 55)

    def test_none(self):
        self.assertIsNone(_age_group_to_number(None))

    def test_garbage(self):
        self.assertIsNone(_age_group_to_number("unknown"))


class TestEmployeeRangeToCategory(unittest.TestCase):
    def test_micro(self):
        self.assertEqual(_employee_range_to_category("1-5"), "micro")
        self.assertEqual(_employee_range_to_category("6-10"), "micro")

    def test_small(self):
        self.assertEqual(_employee_range_to_category("11-50"), "small")

    def test_medium(self):
        self.assertEqual(_employee_range_to_category("100+"), "medium")

    def test_none(self):
        self.assertIsNone(_employee_range_to_category(None))


class TestEligibilityEngine(unittest.TestCase):
    def test_mandatory_rule_pass(self):
        scheme = build_scheme(
            eligibility_rules=[
                {"field": "business.sector", "operator": "equals", "value": "food_processing", "required": True}
            ]
        )
        profile_data = {"business": {"sector": "food_processing"}}
        result = EligibilityEngine.check_mandatory_eligibility(scheme, profile_data)
        self.assertTrue(result["eligible"])
        self.assertEqual(len(result["passed_rules"]), 1)

    def test_mandatory_rule_fail(self):
        scheme = build_scheme(
            eligibility_rules=[
                {"field": "business.sector", "operator": "equals", "value": "food_processing", "required": True}
            ]
        )
        profile_data = {"business": {"sector": "technology"}}
        result = EligibilityEngine.check_mandatory_eligibility(scheme, profile_data)
        self.assertFalse(result["eligible"])
        self.assertEqual(len(result["failed_rules"]), 1)
        self.assertTrue(any("Sector" in r for r in result["failure_reasons"]))

    def test_optional_rules_are_skipped(self):
        scheme = build_scheme(
            eligibility_rules=[
                {"field": "business.sector", "operator": "equals", "value": "food_processing", "required": False}
            ]
        )
        profile_data = {"business": {"sector": "technology"}}
        result = EligibilityEngine.check_mandatory_eligibility(scheme, profile_data)
        self.assertTrue(result["eligible"])

    def test_no_rules_is_eligible(self):
        result = EligibilityEngine.check_mandatory_eligibility(build_scheme(), {})
        self.assertTrue(result["eligible"])


class TestRelevanceScorer(unittest.TestCase):
    def test_full_sector_match(self):
        scheme = build_scheme(primary_sector="food_processing", supported_purposes=[])
        profile_data = {"business": {"sector": "food_processing", "stage": "established"},
                        "location": {"state": "Delhi"},
                        "founder": {"gender": "female", "social_category": "general"}}
        score = RelevanceScorer.calculate_relevance_score(scheme, profile_data, [])
        self.assertGreaterEqual(score["score"], 40)
        self.assertIn("sector", score["matched_criteria"])

    def test_purpose_match_scoring(self):
        scheme = build_scheme(supported_purposes=["working_capital"])
        score = RelevanceScorer.calculate_relevance_score(scheme, {}, ["loan"])
        self.assertGreater(score["breakdown"].get("purpose", 0), 0)

    def test_location_national(self):
        scheme = build_scheme(geographic_scope="national")
        profile_data = {"business": {"sector": "all", "stage": "established"},
                        "location": {"state": "Maharashtra"},
                        "founder": {"gender": "male", "social_category": "general"}}
        result = RelevanceScorer.calculate_relevance_score(scheme, profile_data, [])
        self.assertEqual(result["breakdown"]["location"], relevance_location_weight())


def relevance_location_weight():
    return RelevanceScorer.WEIGHTS["location_match"]


class TestMatchingEngine(unittest.TestCase):
    def test_food_processing_woman_gets_pmfme_first(self):
        pmfme = build_scheme(
            id=4,
            name="PMFME",
            primary_sector="food_processing",
            sub_sectors=["agriculture"],
            business_stages=["established", "expansion"],
            supported_purposes=["business_expansion", "equipment_purchase"],
            eligibility_rules=[
                {"field": "business.sector", "operator": "equals", "value": "food_processing", "required": True}
            ],
        )
        mudra = build_scheme(id=1, name="MUDRA", primary_sector="all",
                             supported_purposes=["working_capital", "business_start", "business_expansion"])
        cgtmse = build_scheme(id=6, name="CGTMSE", primary_sector="all",
                              supported_purposes=["working_capital", "business_expansion"])
        wep = build_scheme(id=8, name="WEP", primary_sector="all",
                           applicant_types=["women_entrepreneur"],
                           gender_eligibility=["female"],
                           supported_purposes=["training", "skill_development"])

        profile = build_profile()  # food_processing, female, Delhi, existing

        recs = MatchingEngineV2.get_recommendations(
            schemes=[wep, cgtmse, mudra, pmfme],
            profile=profile,
            requirements=["machinery", "funding"],
            min_relevance_score=0,
        )

        self.assertGreater(len(recs), 0)
        # Best matched scheme must be the sector-specific PMFME
        self.assertEqual(recs[0]["scheme"].name, "PMFME")
        self.assertEqual(recs[0]["match_level"], "Excellent Match")

    def test_mandatory_eligibility_filters_scheme(self):
        tech_only = build_scheme(
            id=5,
            name="SISFS",
            primary_sector="technology",
            eligibility_rules=[
                {"field": "business.sector", "operator": "equals", "value": "technology", "required": True}
            ],
        )
        profile = build_profile(business_sector="agriculture")
        recs = MatchingEngineV2.get_recommendations(
            schemes=[tech_only],
            profile=profile,
            requirements=[],
            min_relevance_score=0,
        )
        self.assertEqual(recs, [])

    def test_min_score_filter(self):
        generic = build_scheme(id=1, name="Generic", primary_sector="all",
                               supported_purposes=["working_capital"])
        profile = build_profile()
        recs = MatchingEngineV2.get_recommendations(
            schemes=[generic],
            profile=profile,
            requirements=[],
            min_relevance_score=100,
        )
        self.assertEqual(recs, [])


if __name__ == "__main__":
    unittest.main()