"""
This Python 3.3 code tests the ``sources.dggs_functions`` module.
Beware, these tests cover only some functions and only some scenarios.
Keep adding tests!
CHANGELOG:
- 2021-03-17:   David Habgood (DH): Initial version
"""
import unittest
from source import *


class SFRelationships(unittest.TestCase):

    # equals
    def test_sf_equals(self):
        self.assertTrue(sfEquals("P1", "P1"))

    def test_sf_not_equals(self):
        self.assertFalse(sfEquals("P1", "P2"))

    # overlaps
    def test_sf_overlaps(self):
        self.assertFalse(sfOverlaps(["P1", "P2"], ["P2", "P3"]))

    def test_sf_not_overlaps_equal(self):
        self.assertFalse(sfOverlaps("P1", "P1"))

    def test_sf_not_overlaps_disjoint(self):
        self.assertFalse(sfOverlaps("P1", "P2"))

    def test_sf_not_overlaps_within(self):
        self.assertFalse(sfOverlaps("P100", "P1"))

    def test_sf_not_overlaps_contains(self):
        self.assertFalse(sfOverlaps("P1", "P100"))

    # disjoint
    def test_sf_disjoint(self):
        self.assertFalse(sfDisjoint("P1", "P1"))

    def test_sf_not_disjoint(self):
        self.assertTrue(sfDisjoint("P1", "P2"))

    def test_sf_disjoint_different_res(self):
        self.assertFalse(sfDisjoint("P100", "P1"))

    def test_sf_disjoint_list_str(self):
        self.assertFalse(sfDisjoint(["P1", "P2"], "P100"))

    def test_sf_disjoint_list_str(self):
        self.assertTrue(sfDisjoint(["P1", "P2"], "P3"))

    # contains
    def test_sf_contains(self):
        self.assertTrue(sfContains("P1", "P123"))

    def test_sf_not_contains_within(self):
        self.assertFalse(sfContains("P1", ["P1", "P2"]))

    def test_sf_not_contains_equal(self):
        self.assertFalse(sfContains("P1", "P1"))

    def test_sf_not_contains_overlaps(self):
        self.assertFalse(sfContains(["P1", "P2"], ["P2", "P3"]))

    # within
    def test_sf_within(self):
        self.assertTrue(sfWithin("P1", ["P1", "P2"]))

    def test_sf_not_within_contains(self):
        self.assertFalse(sfWithin("P1", "P123"))

    def test_sf_not_within_equal(self):
        self.assertFalse(sfWithin("P1", "P1"))

    def test_sf_not_within_overlaps(self):
        self.assertFalse(sfWithin(["P1", "P2"], ["P2", "P3"]))


if __name__ == "__main__":
    unittest.main()
