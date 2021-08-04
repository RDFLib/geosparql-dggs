"""
This Python 3.8 code tests the ``dggs_geosparql.sf_functions`` module.
Beware, these tests cover only some functions and only some scenarios.
Keep adding tests!
CHANGELOG:
- 2021-08-04:   David Habgood (DH): Initial version
"""

from gsdggs import contains
from rdflib import Literal, Graph, Namespace, URIRef
from gsdggs import DGGS

contains(Literal('R1'), Literal('R2'))
contains(Literal('R1'), Literal('R12'))
contains('R1', 'R11')

GEO = Namespace("http://www.opengis.net/ont/geosparql#")

g = Graph()
g.add((URIRef('https://geom-one'), GEO.hasGeometry, Literal('R1')))
g.add((URIRef('https://geom-two'), GEO.hasGeometry, Literal('R11')))
g.add((URIRef('https://geom-three'), GEO.hasGeometry, Literal('R2')))
g.add((URIRef('https://geom-four'), GEO.hasGeometry, Literal('R111')))

result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX dggs: <https://placeholder.com/dggsfuncs/>
SELECT * {?a geo:hasGeometry ?a_geom .
            ?b geo:hasGeometry ?b_geom .
            FILTER dggs:sfContains(?a_geom, ?b_geom) }""")
result = [{str(k): v for k, v in i.items()} for i in result.bindings]