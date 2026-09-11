"""Unit tests for app.utils.serializers (Government Data Structure output)."""
import unittest
from types import SimpleNamespace
from datetime import datetime

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.serializers import (
    serialize_scheme_full,
    serialize_scheme_summary,
    serialize_scheme_recommendation,
)


def build_scheme_obj(**overrides):
    defaults = dict(
        id=1,
        name="PM MUDRA Yojana",
        short_name="MUDRA",
        description="Collateral-free loans for micro enterprises.",
        scheme_type="loan",
        status="active",
        ministry="Ministry of Finance",
        department="DFS",
        implementing_agency="SIDBI",
        applicant_types=["entrepreneur", "msme"],
        business_stages=["pre_registration", "established", "expansion"],
        primary_sector="all",
        sub_sectors=["retail", "services"],
        geographic_scope="national",
        states=[],
        business_types=["micro"],
        enterprise_categories=["micro", "small"],
        minimum_business_age_months=0,
        maximum_business_age_months=None,
        minimum_turnover=None,
        maximum_turnover=10000000,
        minimum_investment=0,
        maximum_investment=1000000,
        minimum_age=18,
        maximum_age=65,
        gender_eligibility=["any"],
        social_categories=["any"],
        supported_purposes=["working_capital", "business_start", "business_expansion"],
        funding_required=True,
        benefit_types=["loan"],
        benefit_description="Collateral-free loan up to Rs 10 lakh",
        maximum_amount=1000000,
        currency="INR",
        eligibility_rules=[{"field": "founder.age", "operator": "greater_than_or_equal", "value": 18, "required": True}],
        required_documents=[{"name": "Aadhaar Card", "mandatory": True}],
        application_mode="online",
        official_url="https://www.mudra.org.in",
        application_url="https://www.mudra.org.in",
        source_name="MUDRA",
        source_url="https://www.mudra.org.in",
        last_verified=datetime(2026, 1, 1),
        created_at=datetime(2025, 1, 1),
        updated_at=datetime(2026, 1, 1),
        version=2,
        eligibility_summary=["Indian citizen 18+", "Non-farm enterprise"],
        benefits_list=["Collateral-free loan", "Low interest"],
        application_process=["Apply online", "Submit documents"],
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


class TestSerializeSchemeFull(unittest.TestCase):
    def setUp(self):
        self.data = serialize_scheme_full(build_scheme_obj())

    def test_has_all_government_structure_sections(self):
        expected = {
            "scheme_id", "basic_info", "government", "target_beneficiaries",
            "sector", "geography", "business_eligibility", "financial_eligibility",
            "founder_eligibility", "requirements", "benefits", "eligibility_rules",
            "required_documents", "application", "source", "metadata",
        }
        self.assertEqual(set(self.data.keys()), expected)

    def test_basic_info(self):
        self.assertEqual(self.data["basic_info"]["name"], "PM MUDRA Yojana")
        self.assertEqual(self.data["basic_info"]["scheme_type"], "loan")

    def test_government_and_geography(self):
        self.assertEqual(self.data["government"]["ministry"], "Ministry of Finance")
        self.assertEqual(self.data["geography"]["scope"], "national")

    def test_financial_eligibility(self):
        self.assertEqual(self.data["financial_eligibility"]["maximum_turnover"], 10000000)

    def test_benefits(self):
        self.assertEqual(self.data["benefits"]["type"], ["loan"])
        self.assertEqual(self.data["benefits"]["maximum_amount"], 1000000)

    def test_source_serialized_iso(self):
        self.assertEqual(self.data["source"]["last_verified"], "2026-01-01T00:00:00")


class TestSerializeSchemeSummary(unittest.TestCase):
    def test_summary_shape(self):
        data = serialize_scheme_summary(build_scheme_obj())
        self.assertIn("scheme_id", data)
        self.assertIn("name", data)
        self.assertIn("maximum_amount", data)
        # Summary should stay flat and lightweight
        self.assertNotIn("basic_info", data)


class TestSerializeSchemeRecommendation(unittest.TestCase):
    def test_recommendation_shape(self):
        data = serialize_scheme_recommendation(build_scheme_obj())
        self.assertEqual(data["id"], 1)
        self.assertIn("primary_sector", data)
        self.assertIn("benefit_types", data)
        self.assertIn("application_url", data)
        self.assertIn("required_documents", data)

    def test_returns_applicable_enums(self):
        data = serialize_scheme_recommendation(build_scheme_obj())
        self.assertIsInstance(data["business_stages"], list)
        self.assertIn("established", data["business_stages"])


if __name__ == "__main__":
    unittest.main()