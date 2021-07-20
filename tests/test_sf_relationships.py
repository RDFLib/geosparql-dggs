"""
This Python 3.3 code tests the ``processing.processing`` module.
Beware, these tests cover only some functions and only some scenarios.
Keep adding tests!
CHANGELOG:
- 2021-03-17:   David Habgood (DH): Initial version
"""
import unittest
from source import *


class SFRelationships(unittest.TestCase):

    def test_sf_equals(self):
        self.assertTrue(sfEquals('P1', 'P1'))

    def test_sf_not_equals(self):
        self.assertFalse(sfEquals('P1', 'P2'))

    def test_sf_overlaps(self):
        self.assertTrue(sfOverlaps('P1', 'P1'))

    def test_sf_not_overlaps(self):
        self.assertFalse(sfOverlaps('P1', 'P2'))

    def test_sf_overlaps_different_res(self):
        self.assertTrue(sfOverlaps('P100', 'P1'))

    def test_sf_overlaps_list_str(self):
        self.assertTrue(sfOverlaps(['P1', 'P2'], 'P100'))

    def test_sf_not_overlaps_list_str(self):
        self.assertFalse(sfOverlaps(['P1', 'P2'], 'P3'))

    def test_sf_disjoint(self):
        self.assertFalse(sfDisjoint('P1', 'P1'))

    def test_sf_not_disjoint(self):
        self.assertTrue(sfDisjoint('P1', 'P2'))

    def test_sf_disjoint_different_res(self):
        self.assertFalse(sfDisjoint('P100', 'P1'))

    def test_sf_disjoint_list_str(self):
        self.assertFalse(sfDisjoint(['P1', 'P2'], 'P100'))

    def test_sf_disjoint_list_str(self):
        self.assertTrue(sfDisjoint(['P1', 'P2'], 'P3'))

if __name__ == "__main__":
    unittest.main()
