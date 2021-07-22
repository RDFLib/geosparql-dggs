"""
This Python 3.3 code tests the ``processing.processing`` module.
Beware, these tests cover only some functions and only some scenarios.
Keep adding tests!
CHANGELOG:
- 2021-03-17:   David Habgood (DH): Initial version
"""
import unittest
from source.dggs_classes import *


class CellValid(unittest.TestCase):

    def test_dggs_geom_format_invalid_1(self):
        with self.assertRaises(AssertionError):
            Cell('H123', crs='auspix', kind='rHEALPix')

    def test_dggs_geom_format_invalid_2(self):
        with self.assertRaises(AssertionError):
            Cell('HH', crs='auspix', kind='rHEALPix')

    # def test_dggs_geom_compression_1(self):
    #     assert Cell(['P012', 'N013'], kind='rHEALPix').suid == ['N013', 'P012']

    def test_dggs_geom_single_cell(self):
        assert Cell('P012', crs='auspix', kind='rHEALPix').suid == ('P', 0, 1, 2)


class CellNeighbour(unittest.TestCase):

    def test_neighbour_up(self):
        self.assertEqual(
            Cell('R41', kind='rHEALPix').neighbour('up').suid, ('R', 1, 7))

    def test_neighbour_down(self):
        self.assertEqual(
            Cell('R47', kind='rHEALPix').neighbour('down').suid, ('R', 7, 1))

    def test_neighbour_left(self):
        self.assertEqual(
            Cell('R43', kind='rHEALPix').neighbour('left').suid, ('R', 3, 5))

    def test_neighbour_right(self):
        self.assertEqual(
            Cell('R45', kind='rHEALPix').neighbour('right').suid, ('R', 5, 3))


class CellNeighbours(unittest.TestCase):

    def test_neighbours(self):
        self.assertEqual(
            Cell('R4', kind='rHEALPix').neighbours_suids(),
            {('R', 1), ('R', 3), ('R', 5), ('R', 7)}
            )


class CellCollections(unittest.TestCase):

    def test_collection_creation(self):
        assert type(CellCollection(['R1', 'R4', 'R5'])) == CellCollection

    def test_invalid_collection_creation(self):
        with self.assertRaises(AssertionError):
            CellCollection(['R1', 'frog'])

    def test_deduplication(self):
        self.assertEqual((CellCollection(['R4', 'R1', 'R5', 'R5']).cell_suids),
                         ['R1', 'R4', 'R5'])

    def test_resolution_repitition(self):
        self.assertEqual((CellCollection(['R1', 'R12', 'R123']).cell_suids),
                         ['R1'])


if __name__ == "__main__":
    unittest.main()
