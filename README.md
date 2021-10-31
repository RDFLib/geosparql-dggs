# RDFlib GeoSPARQL Functions for DGGS

This library provides support for the [GeoSPARQL 1.1 Simple Features Relation Family](https://opengeospatial.github.io/ogc-geosparql/geosparql11/spec.html#_simple_features_relation_family_relation_familysimple_features)
for geometries expressed as [DGGS Literals](https://opengeospatial.github.io/ogc-geosparql/geosparql11/spec.html#_rdfs_datatype_geodggsliteral).
Currently, [rHEALPix DGGS](https://iopscience.iop.org/article/10.1088/1755-1315/34/1/012012/pdf) Grids are supported.  

## Installation
From the python package index, PyPi: https://pypi.org/project/geosparql-dggs/  
`pip install geosparql-dggs`

This package depends on to support the functions' use against graphs [RDFlib](https://pypi.org/project/rdflib/). The functions themselves depend on the [rHEAL-sf](https://github.com/surroundaustralia/rhealpix-sf/) 
library, which in turn depends on the [rHEAL-geo](https://github.com/surroundaustralia/rhealpix-geo/) library for the base classes
which represent DGGS Cells and collections of Cells. 
## Use
These functions are implemented in RDFlib Python in the file `gsdggs/sf_functions.py` and are imported into `gsdggs/__init__.py` and registered there in RDFlib as SPARQL extension functions with their IRIs.

This means they can be used like this (full working script):

```python
from rdflib import Literal, Graph, Namespace, URIRef
from gsdggs import DGGS

EX = Namespace("http://example.com/")
GEO = Namespace("http://www.opengis.net/ont/geosparql#")

# Define the DGGS Geometries, add them to an in-memory RDF graph
g = Graph()
g.add((URIRef('https://geom-a'), GEO.asDGGS, Literal('CELLLIST ((R0 R10 R13 R16 R30 R31 R32 R40))', EX.ausPixLiteral)))
g.add((URIRef('https://geom-b'), GEO.asDGGS, Literal('CELLLIST ((R06 R07 R30 R31))', EX.ausPixLiteral)))
g.add((URIRef('https://geom-c'), GEO.asDGGS, Literal('CELLLIST ((R11 R12 R14 R15))', EX.ausPixLiteral)))

# Query the in-memory graph
q = """
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX dggs: <https://placeholder.com/dggsfuncs/>
    
    SELECT ?a ?b 
    WHERE {
        ?a geo:asDGGS ?a_geom .
        ?b geo:asDGGS ?b_geom .
        
        FILTER dggs:sfWithin(?a_geom, ?b_geom)
    }"""
# Interate through and print results
for r in g.query(q):
    print(f"{r['a']} is within {r['b']}")
```
The above stript outputs:

```bash
https://geom-b is within https://geom-a
```

The functions can also be used directly (without RDFLib) by direct import from _source, for example:
```python
from _source import sfEquals

sfEquals("R1", "R1")
```
The above stript outputs:

```bash
True
```
## Function Definitions
The Simple Feature relations have been interpreted in the following way for the context of a nested square DGGS grid (such as rHEALPix grids).  

* **dggs:sfEqual:** Two sets of cells are equal if they have the same identifier.  
* **dggs:sfWithin:** One set of cells (A) is within some other set of cells (B) if the addition of A's cells to B results in a set of cells equal to B, where A is not equal to B.  
* **dggs:sfContains:** One set of cells (A) is contains some other set of cells (B) if the addition of A's cells to B results in a set of cells equal to A, where A is not equal to B.  
* **dggs:sfIntersects:** One set of cells (A) intersects some other set of cells (B) where they share any two cells, or any cell in A is the parent or child of a cell in B, or any cell in A or B touches.  
* **dggs:sfTouches:** One set of cells (A) touches some other set of cells (B) where the cells meet at an edge, or vertex.  
* **dggs:sfDisjoint:** One set of cells (A) is disjoint with some other set of cells (B) where they do not share any two cells, no cell in A is the parent or child of a cell in B, and no cells in A and B touch.  
* **dggs:sfOverlaps:** One set of cells (A) overlaps some other set of cells (B) where the addition of A's cells to B results in a set of cells different from A and B, and A and B are not disjoint and do not touch.

## Testing
All tests are in `tests/` and implemented using [pytest](https://docs.pytest.org/en/6.2.x/index.html).

There are individual tests for each function, along with more granular tests for supporting Python classes (Cells and CellCollections), as well as application of the functions without RDF. 

## Contributing
Via GitHub, Issues & Pull Requests: 

* <https://github.com/rdflib/geosparql-dggs>

## License
This code is licensed with the BSD 3-clause license as per [LICENSE](LICENSE) which is the same license as used for [rdflib](https://pypi.org/project/rdflib/).

## Citation
```bibtex
@software{https://github.com/rdflib/geosparql-dggs,
  author = {{David Habgood}},
  title = {RDFlib GeoSPARQL Functions for DGGS},
  version = {0.0.1},
  date = {2021},
  url = {https://github.com/rdflib/geosparql-dggs}
}
```

## Contact
_Creator & maintainer:_  
**David Habgood**  
_Application Architect_  
[SURROUND Australia Pty Ltd](https://surroundaustralia.com)  
<david.habgood@surroundaustrlaia.com>  

https://orcid.org/0000-0002-3322-1868
