from .sf_functions import contains
from rdflib import Namespace
from rdflib.plugins.sparql.operators import register_custom_function

__version__ = "0.1"
DGGS = Namespace("https://placeholder.com/dggsfuncs/")

register_custom_function(DGGS.sfContains, contains)
