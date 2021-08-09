from .sf_functions import (
    contains,
    overlaps,
    equals,
    touches,
    within,
    disjoint,
    intersects,
)
from rdflib import Namespace
from rdflib.plugins.sparql.operators import register_custom_function

__version__ = "0.1"
DGGS = Namespace("https://placeholder.com/dggsfuncs/")

register_custom_function(DGGS.sfContains, contains)
register_custom_function(DGGS.sfEquals, equals)
register_custom_function(DGGS.sfOverlaps, overlaps)
register_custom_function(DGGS.sfDisjoint, disjoint)
register_custom_function(DGGS.sfWithin, within)
register_custom_function(DGGS.sfTouches, touches)
register_custom_function(DGGS.sfIntersects, intersects)
