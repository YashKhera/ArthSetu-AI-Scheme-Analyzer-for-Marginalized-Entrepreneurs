"""Unit tests for app.utils.constants"""
import unittest

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.constants import (
    LEGACY_STAGE_MAPPING,
    SUPPORTED_RULE_OPERATORS,
    SCORING_WEIGHTS,
    STAGE_IDEA,
    STAGE_PRE_REGISTRATION,
    STAGE_ESTABLISHED,
    STAGE_EXPANSION,
    MATCH_LEVEL_EXCELLENT,
    MATCH_LEVEL_STRONG,
    MATCH_LEVEL_GOOD,
    MATCH_LEVEL_POSSIBLE,
    MATCH_LEVEL_LOW,
)


class TestLegacyStageMapping(unittest.TestCase):
    def test_legacy_values_map_to_normalized(self):
        self.assertEqual(LEGACY_STAGE_MAPPING["idea"], STAGE_IDEA)
        self.assertEqual(LEGACY_STAGE_MAPPING["planning"], STAGE_PRE_REGISTRATION)
        self.assertEqual(LEGACY_STAGE_MAPPING["existing"], STAGE_ESTABLISHED)
        self.assertEqual(LEGACY_STAGE_MAPPING["expanding"], STAGE_EXPANSION)

    def test_normalized_values_are_stable(self):
        self.assertEqual(LEGACY_STAGE_MAPPING["pre_registration"], STAGE_PRE_REGISTRATION)
        self.assertEqual(LEGACY_STAGE_MAPPING["established"], STAGE_ESTABLISHED)
        self.assertEqual(LEGACY_STAGE_MAPPING["expansion"], STAGE_EXPANSION)

    def test_unknown_stage_is_not_mapped(self):
        self.assertEqual(LEGACY_STAGE_MAPPING.get("nonexistent"), None)


class TestOperatorsAndWeights(unittest.TestCase):
    def test_supported_operators_includes_core(self):
        for op in ["equals", "not_equals", "contains", "in", "greater_than_or_equal"]:
            self.assertIn(op, SUPPORTED_RULE_OPERATORS, f"missing operator {op}")

    def test_match_levels_coverage(self):
        levels = [MATCH_LEVEL_EXCELLENT, MATCH_LEVEL_STRONG, MATCH_LEVEL_GOOD, MATCH_LEVEL_POSSIBLE, MATCH_LEVEL_LOW]
        self.assertEqual(len(levels), 5)
        self.assertIn("Excellent Match", levels)

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(SCORING_WEIGHTS.values()), 100)


if __name__ == "__main__":
    unittest.main()