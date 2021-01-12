from rdflib import Graph

g = Graph().parse("landform_orig.ttl", format="ttl")
print(len(g))


# remove duplicate RDFS & DCTERMS properties
q = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

DELETE {
    ?c rdfs:comment ?x
} WHERE {
    ?c rdfs:comment ?x .
    { ?c a skos:Concept . }
    UNION
    { ?c a skos:Collection . }
}"""


q = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

DELETE {
    ?c rdfs:label ?x
} WHERE {
    ?c rdfs:label ?x .
    { ?c a skos:Concept . }
    UNION
    { ?c a skos:Collection . }
}"""


q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>

DELETE {
    ?c dct:identifier ?x
} WHERE {
    ?c dct:identifier ?x .
    { ?c a skos:Concept . }
    UNION
    { ?c a skos:Collection . }
}"""


q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>

DELETE {
    ?c dct:description ?x
} WHERE {
    ?c dct:description ?x .
    { ?c a skos:Concept . }
    UNION
    { ?c a skos:Collection . }
}"""

# remove unused Reg properties
q = """PREFIX reg: <http://purl.org/linked-data/registry#>

DELETE { ?c ?p ?o }
WHERE {
    ?c a reg:RegisterItem .
    ?c ?p ?o .
}"""

q = """PREFIX reg: <http://purl.org/linked-data/registry#>

DELETE {
    ?x ?p ?o 
} 
WHERE {
    ?x reg:entity ?y .
	?x ?p ?o .
}"""


# build ConceptScheme
q = """PREFIX ui: <http://purl.org/linked-data/registry-ui#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX skos-ext: <http://linked.data.gov.au/def/skos-ext#>

INSERT {
    ?x skos:topConceptOf ?y .
    ?y a skos:ConceptScheme .
}
WHERE {
    ?x ui:topMemberOf|skos-ext:topMemberOf ?y .
}"""

