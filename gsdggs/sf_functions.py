from rdflib import Literal
from _source import sfOverlaps, sfEquals, sfTouches, sfWithin, sfContains, sfDisjoint


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
    # TODO consider checking types etc.
    if sfContains(a, b):
        return Literal(True)
    return Literal(False)
