"""
This Python 3.3 code tests the ``source.dggs_classes`` module.
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
            Cell("H123")

    def test_dggs_geom_format_invalid_2(self):
        with self.assertRaises(ValueError):
            Cell("RH")

    # def test_dggs_geom_compression_1(self):
    #     assert Cell(['P012', 'N013']).suid == ['N013', 'P012']

    def test_dggs_geom_single_cell(self):
        assert Cell("P012").suid == ("P", 0, 1, 2)


class CellNeighbour(unittest.TestCase):
    def test_neighbour_up(self):
        self.assertEqual(Cell("R41").neighbour("up").suid, ("R", 1, 7))

    def test_neighbour_down(self):
        self.assertEqual(Cell("R47").neighbour("down").suid, ("R", 7, 1))

    def test_neighbour_left(self):
        self.assertEqual(Cell("R43").neighbour("left").suid, ("R", 3, 5))

    def test_neighbour_right(self):
        self.assertEqual(Cell("R45").neighbour("right").suid, ("R", 5, 3))


class CellNeighbours(unittest.TestCase):
    def test_neighbours(self):
        self.assertEqual(
            Cell("R4").neighbours().cell_suids,
            CellCollection(["R0", "R1", "R2", "R3", "R5", "R6", "R7", "R8"]).cell_suids,
        )


class CellCollectionNeighbours(unittest.TestCase):
    def test_collection_neighbours(self):
        self.assertEqual(
            CellCollection(["P4", "P5"]).neighbours().cell_suids,
            CellCollection(
                ["P0", "P1", "P2", "P3", "P6", "P7", "P8", "Q0", "Q3", "Q6"]
            ).cell_suids,
        )


class CellBorder(unittest.TestCase):
    def test_border_no_resolution_specified(self):
        self.assertEqual(
            Cell("R").border().suid,
            Cell("R").suid,
        )

    def test_border_no_resolution_1(self):
        self.assertEqual(
            Cell("R").border(resolution=1).cell_suids,
            CellCollection(["R0", "R1", "R2", "R3", "R5", "R6", "R7", "R8"]).cell_suids,
        )

    def test_border_no_resolution_2(self):
        self.assertEqual(
            Cell("R").border(resolution=2).cell_suids,
            CellCollection(
                [
                    "R00",
                    "R01",
                    "R02",
                    "R03",
                    "R06",
                    "R10",
                    "R11",
                    "R12",
                    "R20",
                    "R21",
                    "R22",
                    "R25",
                    "R28",
                    "R30",
                    "R33",
                    "R36",
                    "R52",
                    "R55",
                    "R58",
                    "R60",
                    "R63",
                    "R66",
                    "R67",
                    "R68",
                    "R76",
                    "R77",
                    "R78",
                    "R82",
                    "R85",
                    "R86",
                    "R87",
                    "R88",
                ]
            ).cell_suids,
        )


class CellCollectionInstantiation(unittest.TestCase):
    def test_collection_creation(self):
        assert type(CellCollection(["R1", "R4", "R5"])) == CellCollection

    def test_invalid_collection_creation(self):
        with self.assertRaises(AssertionError):
            CellCollection(["R1", "frog"])

    def test_deduplication(self):
        self.assertEqual(
            (CellCollection(["R4", "R1", "R5", "R5"]).cell_suids), ["R1", "R4", "R5"]
        )

    def test_absorb(self):
        self.assertEqual((CellCollection(["R1", "R12", "R123"]).cell_suids), ["R1"])


class CellCollectionsOperations(unittest.TestCase):
    def test_collection_addition(self):
        assert (CellCollection(["R1"]) + CellCollection(["R2"])).cell_suids == [
            "R1",
            "R2",
        ]

    def test_collection_subtraction(self):
        assert set(
            (CellCollection(["R1", "R2"]) - CellCollection(["R12"])).cell_suids
        ) == set(["R10", "R11", "R13", "R14", "R15", "R16", "R17", "R18", "R2"])

    # def test_collection_cell_subtraction(self):
    #     assert (CellCollection(["R1"]) - Cell(["R12"])).cell_suids == [
    #         "R10", "R11", "R13", "R14", "R15", "R16", "R17", "R18"
    #     ]
    #


class CellChildren(unittest.TestCase):
    def test_collection_children(self):
        assert [cell.__str__() for cell in Cell("R").children()] == [
            "R0",
            "R1",
            "R2",
            "R3",
            "R4",
            "R5",
            "R6",
            "R7",
            "R8",
        ]


class CellOverlaps(unittest.TestCase):
    def test_overlaps_true(self):
        self.assertTrue(Cell("R1").overlaps(Cell("R12")))

    def test_overlaps_false(self):
        self.assertFalse(Cell("R2").overlaps(Cell("R12")))


if __name__ == "__main__":
    unittest.main()
