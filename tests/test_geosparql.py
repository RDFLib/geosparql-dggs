import unittest
from rdflib import Literal, Graph, Namespace, URIRef
from gsdggs import DGGS

GEO = Namespace("http://www.opengis.net/ont/geosparql#")

# use image from geosparql 1.1 spec, recreate this as a set of cells,
# then create a truth table, then for each geometry apply the functions
g = Graph()
geom_a = URIRef('https://geom-a')
geom_b = URIRef('https://geom-b')
geom_c = URIRef('https://geom-c')
geom_d = URIRef('https://geom-d')
geom_g = URIRef('https://geom-g')
g.add((geom_a, GEO.hasGeometry, Literal('CELLLIST ((R0 R10 R13 R16 R30 R31 R32 R40))')))
g.add((geom_b, GEO.hasGeometry, Literal('CELLLIST ((R06 R07 R30 R31))')))
g.add((geom_c, GEO.hasGeometry, Literal('CELLLIST ((R11 R12 R14 R15))')))
g.add((geom_d, GEO.hasGeometry, Literal('CELLLIST ((R40 R41 R43 R44))')))
g.add((geom_g, GEO.hasGeometry, Literal('CELLLIST ((R40 R41 R43 R44))')))


class SfRelationships(unittest.TestCase):
    def test_contains(self):
        # A contains B
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfContains(?a_geom, ?b_geom) }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 1
        self.assertTrue(result[0]["a"] == geom_a and result[0]["b"] == geom_b)

    def test_within(self):
        # B is within A
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfWithin(?a_geom, ?b_geom) }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 1
        self.assertTrue(result[0]["a"] == geom_b and result[0]["b"] == geom_a)

    def test_intersects(self):
        # A intersects B
        # A intersects C
        # A intersects D
        # A intersects G
        # B intersects A
        # C intersects A
        # D intersects A
        # D intersects G
        # G intersects A
        # G intersects D
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfIntersects(?a_geom, ?b_geom)
                    FILTER (?a!=?b)
                    }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 10
        assert {'a': geom_a, 'b': geom_b} in result
        assert {'a': geom_a, 'b': geom_c} in result
        assert {'a': geom_a, 'b': geom_d} in result
        assert {'a': geom_a, 'b': geom_g} in result
        assert {'a': geom_b, 'b': geom_a} in result
        assert {'a': geom_c, 'b': geom_a} in result
        assert {'a': geom_d, 'b': geom_a} in result
        assert {'a': geom_d, 'b': geom_g} in result
        assert {'a': geom_g, 'b': geom_a} in result
        assert {'a': geom_g, 'b': geom_d} in result

    def test_touches(self):
        # A touches C
        # C touches A
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfTouches(?a_geom, ?b_geom)
                    }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 2
        assert {'a': geom_a, 'b': geom_c} in result
        assert {'a': geom_c, 'b': geom_a} in result


    def test_equals(self):
        # D equals G
        # G equals D
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfEquals(?a_geom, ?b_geom)
                    FILTER(?a!=?b)
                    }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 2
        assert {'a': geom_d, 'b': geom_g} in result
        assert {'a': geom_g, 'b': geom_d} in result

    def test_overlaps(self):
        # D overlaps A
        # A overlaps D
        # G overlaps A
        # A overlaps G
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfOverlaps(?a_geom, ?b_geom) }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 4
        assert {'a': geom_a, 'b': geom_d} in result
        assert {'a': geom_d, 'b': geom_a} in result
        assert {'a': geom_a, 'b': geom_g} in result
        assert {'a': geom_g, 'b': geom_a} in result

    def test_disjoint(self):
        # B disjoint C
        # C disjoint B
        # B disjoint D
        # D disjoint B
        # B disjoint G
        # G disjoint B
        # D disjoint C
        # C disjoint D
        # G disjoint C
        # C disjoint G
        result = g.query("""PREFIX geo: <http://www.opengis.net/ont/geosparql#>
        PREFIX dggs: <https://placeholder.com/dggsfuncs/>
        SELECT ?a ?b {?a geo:hasGeometry ?a_geom .
                    ?b geo:hasGeometry ?b_geom .
                    FILTER dggs:sfDisjoint(?a_geom, ?b_geom) }""")
        result = [{str(k): v for k, v in i.items()} for i in result.bindings]
        assert len(result) == 10
        assert {'a': geom_b, 'b': geom_c} in result
        assert {'a': geom_c, 'b': geom_b} in result
        assert {'a': geom_b, 'b': geom_d} in result
        assert {'a': geom_d, 'b': geom_b} in result
        assert {'a': geom_b, 'b': geom_g} in result
        assert {'a': geom_g, 'b': geom_b} in result
        assert {'a': geom_d, 'b': geom_c} in result
        assert {'a': geom_c, 'b': geom_d} in result
        assert {'a': geom_g, 'b': geom_c} in result
        assert {'a': geom_c, 'b': geom_g} in result

if __name__ == '__main__':
    unittest.main()
