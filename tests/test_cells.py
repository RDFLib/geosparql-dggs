"""
This Python 3.8 code tests the ``source.dggs_classes`` module.
Beware, these tests cover only some functions and only some scenarios.
Keep adding tests!
CHANGELOG:
- 2021-07-19:   David Habgood (DH): Initial version
"""
import unittest
from _source.dggs_classes import *


class CellValid(unittest.TestCase):
    def test_dggs_geom_format_invalid_1(self):
        with self.assertRaises(ValueError):
            Cell("H123")

    def test_dggs_geom_format_invalid_2(self):
        with self.assertRaises(ValueError):
            Cell("RH")

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

    def test_hemisphere_neighbours_res_1(self):
        self.assertEqual(Cell("P0").neighbours(), "N5 N8 O2 O5 P1 P3 P4")

    def test_zero_neighbours_P(self):
        self.assertEqual(Cell("P").neighbours(), "N O Q S")

    def test_zero_neighbours_N(self):
        self.assertEqual(Cell("N").neighbours(), "O P Q R")


class CellAddition(unittest.TestCase):
    def test_cell_cell_addition(self):
        self.assertEqual(
            (Cell("R4") + Cell("R5")).cell_suids,
            CellCollection(["R4", "R5"]).cell_suids,
        )


class CellSubtraction(unittest.TestCase):
    def test_cell_cell_Subtraction(self):
        self.assertEqual(
            (Cell("R4") - Cell("R44")).cell_suids,
            CellCollection(
                ["R40", "R41", "R42", "R43", "R45", "R46", "R47", "R48"]
            ).cell_suids,
        )


class CellEquality(unittest.TestCase):
    def test_cell_equal_positive(self):
        self.assertEqual(Cell("R4"), Cell("R4"))

    def test_cell_equal_negative(self):
        self.assertNotEqual(Cell("R4"), Cell("R1"))


class CellCollectionEquality(unittest.TestCase):
    def test_cell_collection_equal_positive(self):
        self.assertEqual(CellCollection(["R4", "R3"]), CellCollection(["R3", "R4"]))

    def test_cell_collection_equal_negative(self):
        self.assertNotEqual(
            CellCollection(["R4", "R3"]), CellCollection(["R3123", "R4543"])
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


class CellCollectionNeighbours(unittest.TestCase):
    def test_collection_neighbours(self):
        self.assertEqual(
            CellCollection(["P4", "P5"]).neighbours().cell_suids,
            CellCollection(
                ["P0", "P1", "P2", "P3", "P6", "P7", "P8", "Q0", "Q3", "Q6"]
            ).cell_suids,
        )

    def test_neighbours_at_resolution(self):
        self.assertEqual(
            CellCollection(["P4"]).neighbours(resolution=3).cell_suids,
            CellCollection(
                [
                    "P088",
                    "P166",
                    "P167",
                    "P168",
                    "P176",
                    "P177",
                    "P178",
                    "P186",
                    "P187",
                    "P188",
                    "P266",
                    "P322",
                    "P325",
                    "P328",
                    "P352",
                    "P355",
                    "P358",
                    "P382",
                    "P385",
                    "P388",
                    "P500",
                    "P503",
                    "P506",
                    "P530",
                    "P533",
                    "P536",
                    "P560",
                    "P563",
                    "P566",
                    "P622",
                    "P700",
                    "P701",
                    "P702",
                    "P710",
                    "P711",
                    "P712",
                    "P720",
                    "P721",
                    "P722",
                    "P800",
                ]
            ).cell_suids,
        )


class CellCollectionInstantiation(unittest.TestCase):
    def test_collection_creation(self):
        assert type(CellCollection(["R1", "R4", "R5"])) == CellCollection

    def test_invalid_collection_creation(self):
        with self.assertRaises(ValueError):
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

    def test_collection_cell_subtraction(self):
        assert (CellCollection(["R1"]) - Cell("R12")).cell_suids == [
            "R10",
            "R11",
            "R13",
            "R14",
            "R15",
            "R16",
            "R17",
            "R18",
        ]

    def test_empty_result(self):
        assert (CellCollection(["R1"]) - CellCollection("R1")).cell_suids == []


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


class CellCollectionMatches(unittest.TestCase):
    def test_collection_matches(self):
        self.assertTrue(
            CellCollection(["P4"], crs="auspix", kind="rHEALPix").cell_suids
            == CellCollection(["P4"], crs="auspix", kind="rHEALPix").cell_suids
        )

    def test_collection_not_matches(self):
        with self.assertRaises(ValueError):
            CellCollection(
                ["P4"], crs="auspix", kind="rHEALPix"
            ).cell_suids == CellCollection(
                ["P4"], crs="blahblahblah", kind="rHEALPix"
            ).cell_suids

    def test_collection_not_matches_(self):
        self.assertTrue(
            (CellCollection() + CellCollection(["R1"])).cell_suids
            == CellCollection(["R1"]).cell_suids
        )


if __name__ == "__main__":
    unittest.main()
