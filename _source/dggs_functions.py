from typing import Union
from _source.dggs_classes import CellCollection


class DGGSsfRelationships:
    def __init__(
        self, cell_or_cells_1: Union[str, list], cell_or_cells_2: Union[str, list]
    ):
        self.coll_1 = CellCollection(cell_or_cells_1)
        self.coll_2 = CellCollection(cell_or_cells_2)

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
    def sfContains(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether cells_one contains cells_two
        """
        # first check cells_one and cells_two are not equal
        SF = cls(cells_one, cells_two)
        if not cls.sfEquals(SF.coll_1.cell_suids, SF.coll_2.cell_suids):
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
        if not cls.sfEquals(SF.coll_1.cell_suids, SF.coll_2.cell_suids):
            # then if cells_one + cells_two = cells_two, cells_two must contain cells_one
            if (SF.coll_1 + SF.coll_2).cell_suids == SF.coll_2.cell_suids:
                return True
        return False

    @classmethod
    def sfOverlaps(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether the cell/cells overlap
        """
        # implemented as a negative test for disjoint, equals, contains, and within
        if (
            not cls.sfDisjoint(cells_one, cells_two)
            and not cls.sfEquals(cells_one, cells_two)
            and not cls.sfContains(cells_one, cells_two)
            and not cls.sfWithin(cells_one, cells_two)
            and not cls.sfTouches(cells_one, cells_two)
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
        if (
            not region_region_intersection(SF.coll_1.cell_suids, SF.coll_2.cell_suids)
            and not cls.sfTouches(cells_one, cells_two)
        ):
            return True
        return False

    @classmethod
    def sfIntersects(cls, cells_one: Union[str, list], cells_two: [str, list]):
        """
        :param cells_one: a string or list of strings representing cells
        :param cells_two: a string or list of strings representing cells
        :return: boolean as to whether cells_one and cells_two are disjoint i.e. no kind of spatial relationship
        """
        if cls.sfEquals(cells_one, cells_two):
            return True
        elif cls.sfContains(cells_one, cells_two):
            return True
        elif cls.sfWithin(cells_one, cells_two):
            return True
        elif cls.sfOverlaps(cells_one, cells_two):
            return True
        elif cls.sfTouches(cells_one, cells_two):
            return True
        return False

    @classmethod
    def sfTouches(cls, cells_one: Union[str, list], cells_two: [str, list]):
        # if the geometries are equal, they do not touch, this scenario is not covered by the other processing
        if cls.sfEquals(cells_one, cells_two):
            return False
        # if the geometries have regional intersection, they do not touch, they have some other spatial relationship
        # TODO confirm whether this is desired behaviour.
        if region_region_intersection(cells_one, cells_two):
            return False
        SF = cls(cells_one, cells_two)
        # find the max resolution (smallest cells) among the two geometries
        if SF.coll_1.max_resolution > SF.coll_2.max_resolution:
            max_resolution = SF.coll_1.max_resolution
        else:
            max_resolution = SF.coll_2.max_resolution
        # estimate which geometry is smaller based on their lengths
        if len(SF.coll_1) < len(SF.coll_2):
            smaller_collection_neighbours = SF.coll_1.neighbours(max_resolution)
            larger_collection = cells_two
        else:
            smaller_collection_neighbours = SF.coll_2.neighbours(max_resolution)
            larger_collection = cells_one
        # if the neighbouring cells of a geometry are common to the other geometry then they touch
        # with the caveat that we must use neighbours at the maximum (smallest cells) resolution
        # .. and we need to filter on geometries that overlap in the first place
        if common_cells(smaller_collection_neighbours.cell_suids, larger_collection):
            return True
        return False


def dggs_cell_overlap(cell_one: str, cell_two: str):
    """
    Determines whether two DGGS cells overlap.
    Where cells are of different resolution, they will have different suid lengths. The zip function truncates the longer
    to be the same length as the shorter, producing two lists for comparison. If these lists are equal, the cells overlap.
    :param cell_one: the first DGGS cell
    :param cell_two: the second DGGS cell
    :return: True if overlaps
    """
    for i, j in zip(cell_one, cell_two):
        if i != j:
            return False
    return True


def dggs_cell_region_overlap(cell: str, region: list):
    """
    Determine whether a cell overlaps with any cell in a list of cells
    :param cell: a DGGS cell
    :param region: a list of DGGS cells
    :return: True if any overlapping cells
    """
    for component_cell in region:
        if dggs_cell_overlap(cell, component_cell):
            return True
    return False

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
    if isinstance(region_one, str):
        region_one = [region_one]
    if isinstance(region_two, str):
        region_two = [region_two]
    for cell_one in region_one:
        if dggs_cell_region_overlap(cell_one, region_two):
            return True
    return False

def common_cells(region_one: list, region_two: list):
    """
    Determines whether there are any cells in common between two lists of cells
    NB does not take in to account resolution. Cells should be at the same input resolution.
    :param region_one: a list of strings representing cell suids
    :param region_two: a list of strings representing cell suids
    :return: boolean
    """
    if isinstance(region_one, str):
        region_one = [region_one]
    if isinstance(region_two, str):
        region_two = [region_two]
    for cell in region_one:
        if cell in region_two:
            return True
    return False


