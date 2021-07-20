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
    def sfEquals(cls, cells_one: Union[str, list], cells_two: [str, list]):
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
    def sfOverlaps(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether the cell/cells overlap
        """
        SF = cls(cells_one, cells_two)
        return region_region_intersection(SF.coll_1.cell_suids, SF.coll_2.cell_suids)

    @classmethod
    def sfDisjoint(cls, cells_one: Union[str, list], cells_two: [str, list]):
        return not cls.sfOverlaps(cells_one, cells_two)


def cell_cell_intersection(cellOne: str, cellTwo: str, return_relationships=False):
    """
    Determines whether two DGGS suid overlap.
    Where suid are of different resolution, they will have different suid lengths. The zip function truncates the longer
    to be the same length as the shorter, producing two lists for comparison. If these lists are equal, the suid overlap.
    :param return_relationships: whether to return a dictionary of relationships between
    :param cellOne: the first DGGS cell
    :param cellTwo: the second DGGS cell
    :return: True if overlaps
    """
    intersection = True
    for i, j in zip(cellOne, cellTwo):
        if i != j:
            intersection = False
            break
    if return_relationships:
        relationships = {}
        if not intersection:
            return False, relationships["disjoint"].append((cellOne, cellTwo))
        else:
            if len(cellOne) < len(cellTwo):
                relationships["contains"].append((cellOne, cellTwo))
            elif len(cellOne) > len(cellTwo):
                relationships["within"].append((cellOne, cellTwo))
            elif len(cellOne) == len(cellTwo):
                relationships["equal"].append((cellOne, cellTwo))
            return True, relationships
    else:
        return intersection

def cell_region_intersection(cell: str, region: set):
    """
    Determine whether a cell overlaps with any cell in a list of suid
    :param cell: a DGGS cell
    :param region: a list of DGGS suid
    :return: True if the cell overlaps the region
    """
    for component_cell in region:
        if cell_cell_intersection(cell, component_cell):
            return True
    return False

def region_region_intersection(regionOne: set, regionTwo: set):
    """
    Determine whether a cell overlaps with any cell in a list of suid
    :param regionOne: a DGGS region
    :param regionTwo: a DGGS region
    :return: True if the regions overlap
    """
    for component_cell in regionOne:
        if cell_region_intersection(component_cell, regionTwo):
            return True
    return False

def canonical_form(cells_one, cells_two):
    # coerces strings and lists of strings to sets of strings, this is to:
    # - remove duplication of cells
    # - facilitate working with one type (set) rather than two or more (strings, tuples, lists etc.)
    cells_one = [cells_one] if isinstance(cells_one, str) else cells_one
    cells_two = [cells_two] if isinstance(cells_two, str) else cells_two
    cells_one = [Cell(cell_str) for cell_str in cells_one]
    cells_two = [Cell(cell_str) for cell_str in cells_two]
    return cells_one, cells_two