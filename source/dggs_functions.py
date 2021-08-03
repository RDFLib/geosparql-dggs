from typing import Union
from source.dggs_classes import Cell, CellCollection

"""
geof:sfEquals(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(TFFFTFFFT)

geof:sfDisjoint(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(FF*FF****)

geof:sfIntersects(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(FT******* F**T***** F***T****)

geof:sfTouches(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(FT******* F**T***** F***T****)

geof:sfCrosses(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(T*T***T**) for P/L, P/A, L/A; (0*T***T**) for L/L

geof:sfWithin(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(T*F**F***)

geof:sfContains(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(T*****FF*)

geof:sfOverlaps(geom1: ogc:geomLiteral, geom2: ogc:geomLiteral): xsd:boolean
(T*T***T**) for A/A, P/P; (1*T***T**) for L/L
"""


# Assumes suid are given as lists of suid or single suid


class DGGSsfRelationships:
    def __init__(
        self, cell_or_cells_1: Union[str, list], cell_or_cells_2: Union[str, list]
    ):
        self.coll_1 = CellCollection(cell_or_cells_1)
        self.coll_2 = CellCollection(cell_or_cells_2)

    @classmethod
    def sfEqualsBool(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether the cell/cells is/are equal
        """
        SF = cls(cells_one, cells_two)
        if SF.coll_1.cell_suids == SF.coll_2.cell_suids:
            return True
        return False

    @classmethod
    def sfContains(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether cells_one contains cells_two
        """
        # first check cells_one and cells_two are not equal
        SF = cls(cells_one, cells_two)
        if not cls.sfEqualsBool(SF.coll_1.cell_suids, SF.coll_2.cell_suids):
            # then if cells_one + cells_two = cells_one, cells_one must contain cells_two
            if (SF.coll_1 + SF.coll_2).cell_suids == SF.coll_1.cell_suids:
                return True
        return False

    @classmethod
    def sfWithin(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether cells_one is within cells_two
        """
        # first check cells_one and cells_two are not equal
        SF = cls(cells_one, cells_two)
        if not cls.sfEqualsBool(SF.coll_1.cell_suids, SF.coll_2.cell_suids):
            # then if cells_one + cells_two = cells_two, cells_two must contain cells_one
            if (SF.coll_1 + SF.coll_2).cell_suids == SF.coll_2.cell_suids:
                return True
        return False

    @classmethod
    def sfOverlapsBool(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether the cell/cells overlap
        """
        # implemented as a negative test for disjoint, equals, contains, and within
        if (
            not cls.sfDisjoint(cells_one, cells_two)
            and not cls.sfEqualsBool(cells_one, cells_two)
            and not cls.sfContains(cells_one, cells_two)
            and not cls.sfWithin(cells_one, cells_two)
        ):
            return True
        return False

    @classmethod
    def sfDisjoint(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether cells_one and cells_two are disjoint i.e. no kind of spatial relationship
        """
        SF = cls(cells_one, cells_two)
        return not region_region_intersection(
            SF.coll_1.cell_suids, SF.coll_2.cell_suids
        )

    @classmethod
    def sfIntersects(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether cells_one and cells_two are disjoint i.e. no kind of spatial relationship
        """
        if cls.sfEqualsBool(cells_one, cells_two):
            return True
        elif cls.sfContains(cells_one, cells_two):
            return True
        elif cls.sfWithin(cells_one, cells_two):
            return True
        elif cls.sfOverlapsBool(cells_one, cells_two):
            return True
        return False

    @classmethod
    def sfTouches(cls, cells_one: Union[str, list], cells_two: [str, list]):
        SF = cls(cells_one, cells_two)
        if SF.coll_1.max_resolution > SF.coll_2.max_resolution:
            max_resolution = SF.coll_1.max_resolution
        else:
            max_resolution = SF.coll_2.max_resolution
        if len(SF.coll_1) < len(SF.coll_2):
            smaller_collection_neighbours = SF.coll_1.neighbours(max_resolution)
            larger_collection = cells_two
        else:
            smaller_collection_neighbours = SF.coll_2.neighbours(max_resolution)
            larger_collection = cells_one
        if cls.sfIntersects(
            smaller_collection_neighbours.cell_suids, larger_collection
        ):
            return True
        return False

    # could be implemented by shifting a geometry by one cell (of the lowest resolution of the cells making up that
    # collection) in each of north/south/east/west then seeing if THESE new shapes intersect the second geometry.
    # (Shift the smaller geometry for efficiency).
    # This would require a "shift" method which has not yet been written ..


def region_region_intersection(region_one: list, region_two: list):
    """
    Determines whether two DGGS suid overlap.
    Where suid are of different resolution, they will have different suid lengths. The zip function truncates the longer
    to be the same length as the shorter, producing two lists for comparison. If these lists are equal, the suid overlap.
    :param return_relationships: whether to return a dictionary of relationships between
    :param cell_one: the first DGGS cell
    :param cell_two: the second DGGS cell
    :return: True if overlaps
    """
    for cell_one in region_one:
        for cell_two in region_two:
            for i, j in zip(cell_one, cell_two):
                if i != j:
                    return False
    return True
    #         intersects = False
    #         relationships["disjoint"].append((cell_one, cell_two))
    #         break
    # if intersects:
    #     if len(cell_one) < len(cell_two):
    #         relationships["contains"].append((cell_one, cell_two))
    #     elif len(cell_one) > len(cell_two):
    #         relationships["within"].append((cell_one, cell_two))
    #     elif len(cell_one) == len(cell_two):
    #         relationships["equal"].append((cell_one, cell_two))
    # summary = set(relationships.keys())
    # if summary == {'contains', 'equal'} or summary == {'contains', 'disjoint'} or summary == {'contains', 'equal',
    #                                                                                           'disjoint'}:
    #     summary = {'contains'}
    # elif summary == {'within', 'equal'} or summary == {'within', 'disjoint'} summary == {'within', 'equal',
    #                                                                                           'disjoint'}:
    #     summary = {'within'}
    #
    #     return_rel = 'contains'
    # if summary == {'within'}:
    #     return_rel = 'within'
    # if summary == {'within', 'contains'}
    #     return_rel = 'overlaps'
    # if len()

    # if return_relationships:
    #     if not intersection:
    #         return False, relationships["disjoint"].append((cell_one, cell_two))
    #     else:
    #         if len(cell_one) < len(cell_two):
    #             relationships["contains"].append((cell_one, cell_two))
    #         elif len(cell_one) > len(cell_two):
    #             relationships["within"].append((cell_one, cell_two))
    #         elif len(cell_one) == len(cell_two):
    #             relationships["equal"].append((cell_one, cell_two))
    #         return True, relationships
    # else:
    #     return intersection


# def cell_region_intersection(cell: str, region: set, return_relationships=False, relationships={}):
#     """
#     Determine whether a cell overlaps with any cell in a list of suid
#     :param cell: a DGGS cell
#     :param region: a list of DGGS suid
#     :return: True if the cell overlaps the region
#     """
#     for component_cell in region:
#         if cell_cell_intersection(cell, component_cell):
#             return True
#     return False
#
# def region_region_intersection(regionOne: set, regionTwo: set, return_relationships=False, relationships={}):
#     """
#     Determine whether a cell overlaps with any cell in a list of suid
#     :param regionOne: a DGGS region
#     :param regionTwo: a DGGS region
#     :return: True if the regions overlap
#     """
#     for component_cell in regionOne:
#         if cell_region_intersection(component_cell, regionTwo):
#             return True
#     return False


# def canonical_form(cells_one, cells_two):
#     # coerces strings and lists of strings to sets of strings, this is to:
#     # - remove duplication of cells
#     # - facilitate working with one type (set) rather than two or more (strings, tuples, lists etc.)
#     cells_one = [cells_one] if isinstance(cells_one, str) else cells_one
#     cells_two = [cells_two] if isinstance(cells_two, str) else cells_two
#     cells_one = [Cell(cell_str) for cell_str in cells_one]
#     cells_two = [Cell(cell_str) for cell_str in cells_two]
#     return cells_one, cells_two
