from collections import defaultdict
from typing import Union, List
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
    def __init__(self, cell_or_collection_1: Union[str, list], cell_or_collection_2: Union[str, list]):
        cells_list_1, cells_list_2 = canonical_form(cell_or_collection_1, cell_or_collection_2)
        self.coll_1 = CellCollection(cells_list_1)
        self.coll_2 = CellCollection(cells_list_2)

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
    def sfOverlapsBool(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether the cell/cells overlap
        """
        SF = cls(cells_one, cells_two)
        return region_region_intersection(SF.coll_1.cell_suids, SF.coll_2.cell_suids)

    @classmethod
    def sfDisjointBool(cls, cells_one: Union[str, list], cells_two: [str, list]):
        SF = cls(cells_one, cells_two)
        return not region_region_intersection(SF.coll_1.cell_suids, SF.coll_2.cell_suids)


def region_region_intersection(region_one: list, region_two: list, query):
    """
    Determines whether two DGGS suid overlap.
    Where suid are of different resolution, they will have different suid lengths. The zip function truncates the longer
    to be the same length as the shorter, producing two lists for comparison. If these lists are equal, the suid overlap.
    :param return_relationships: whether to return a dictionary of relationships between
    :param cell_one: the first DGGS cell
    :param cell_two: the second DGGS cell
    :return: True if overlaps
    """
    relationships = defaultdict(list)
    for cell_one in region_one:
        for cell_two in region_two:
            intersects = True
            for i, j in zip(cell_one, cell_two):
                if i != j:
                    intersects = False
                    relationships["disjoint"].append((cell_one, cell_two))
                    break
            if intersects:
                if len(cell_one) < len(cell_two):
                    relationships["contains"].append((cell_one, cell_two))
                elif len(cell_one) > len(cell_two):
                    relationships["within"].append((cell_one, cell_two))
                elif len(cell_one) == len(cell_two):
                    relationships["equal"].append((cell_one, cell_two))
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

def canonical_form(cells_one, cells_two):
    # coerces strings and lists of strings to sets of strings, this is to:
    # - remove duplication of cells
    # - facilitate working with one type (set) rather than two or more (strings, tuples, lists etc.)
    cells_one = [cells_one] if isinstance(cells_one, str) else cells_one
    cells_two = [cells_two] if isinstance(cells_two, str) else cells_two
    cells_one = [Cell(cell_str) for cell_str in cells_one]
    cells_two = [Cell(cell_str) for cell_str in cells_two]
    return cells_one, cells_two