from rdflib import Literal
from rhealsf import (
    sfOverlaps,
    sfEquals,
    sfTouches,
    sfWithin,
    sfContains,
    sfDisjoint,
    sfIntersects,
)


def validate_and_clean(cell_or_cellcollection_literal):
    if cell_or_cellcollection_literal.startswith("CELLLIST (("):
        cells_list = (
            cell_or_cellcollection_literal.replace("CELLLIST ((", "")
            .replace("))", "")
            .split(" ")
        )
    elif cell_or_cellcollection_literal.startswith("CELL ("):
        cells_list = (
            cell_or_cellcollection_literal.replace("CELL (", "")
            .replace(")", "")
            .split(" ")
        )
    else:
        raise ValueError(
            "DGGS strings must be formatted as DGGS Literals, e.g. the format: "
            "'CELL (R012)' or "
            "'CELLLIST ((R0 S1 Q2))'"
        )
    return cells_list


def contains(a, b) -> Literal:
    """SPARQL dggs:sfContains

    Returns Literal(true) if the first geometry contains the second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfContains(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfContains(a, b):
        return Literal(True)
    return Literal(False)


def within(a, b) -> Literal:
    """SPARQL dggs:sfWithin

    Returns Literal(true) if the first geometry is within the second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfWithin(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfWithin(a, b):
        return Literal(True)
    return Literal(False)


def disjoint(a, b) -> Literal:
    """SPARQL dggs:sfDisjoint

    Returns Literal(true) if the first geometry is disjoint with the second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfDisjoint(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfDisjoint(a, b):
        return Literal(True)
    return Literal(False)


def intersects(a, b) -> Literal:
    """SPARQL dggs:sfIntersects

    Returns Literal(true) if the first geometry intersects (i.e. has any spatial relation other than disjoint) the
    second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfIntersects(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfIntersects(a, b):
        return Literal(True)
    return Literal(False)


def touches(a, b) -> Literal:
    """SPARQL dggs:sfTouches

    Returns Literal(true) if the first geometry touches the second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfTouches(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfTouches(a, b):
        return Literal(True)
    return Literal(False)


def overlaps(a, b) -> Literal:
    """SPARQL dggs:sfOverlaps

    Returns Literal(true) if the first geometry overlaps the second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfOverlaps(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfOverlaps(a, b):
        return Literal(True)
    return Literal(False)


def equals(a, b) -> Literal:
    """SPARQL dggs:sfEquals

    Returns Literal(true) if the first geometry is equal to the second geometry.

    Example:
    SELECT ?a ?b
    WHERE {
        ?x a geo:Geometry ;
           geo:asDGGS ?a .
        ?y a geo:Geometry ;
           geo:asDGGS ?b .
        FILTER dggs:sfEquals+(?a, ?b)
    }
    """
    a, b = validate_and_clean(a), validate_and_clean(b)
    if sfEquals(a, b):
        return Literal(True)
    return Literal(False)
