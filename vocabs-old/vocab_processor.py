from rdflib import Graph, Namespace

voc = "landform_0.ttl"
voc = "soil-prof_0.ttl"

g = Graph().parse(voc, format="ttl")
g.bind("sp", Namespace("http://registry.it.csiro.au/def/soil/au/asls/soil-prof/"))
g.bind("lnd", Namespace("http://registry.it.csiro.au/def/soil/au/asls/landform/"))

print(len(g))

# remove duplicate RDFS & DCTERMS properties
q = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

DELETE {
    ?c dcterms:description ?d .
    ?c rdfs:comment ?d .
} 
INSERT {
    ?c skos:definition ?d .
}
WHERE {
    ?c dcterms:description|rdfs:comment ?d .
}"""
g.update(q)

q = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

DELETE {
    ?c rdfs:label ?x
} WHERE {
    ?c rdfs:label ?x .
}"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>

DELETE {
    ?c dct:identifier ?x
} WHERE {
    ?c dct:identifier ?x .
}"""
g.update(q)

print("duplicate properties removal complete")

# g.serialize(destination=voc.replace("_0", "_1"), format="ttl")

# build ConceptScheme
q = """
PREFIX ldp: <http://www.w3.org/ns/ldp#>

INSERT {
    ?cs a skos:ConceptScheme .
}
WHERE {
    ?cs a ldp:Container .
}  
"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

# DELETE {
#     ?x a skos:Collection .
# }
INSERT {
    ?x a skos:Concept .
}
WHERE {
    ?x a skos:Collection .
}"""
g.update(q)

q = """PREFIX ui: <http://purl.org/linked-data/registry-ui#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX skos-ext: <http://linked.data.gov.au/def/skos-ext#>

DELETE {
    ?x ui:topMemberOf ?y .
    ?x skos-ext:topMemberOf ?y .
}
INSERT {
    ?x skos:topConceptOf ?cs .
}
WHERE {
    ?x ui:topMemberOf|skos-ext:topMemberOf ?y .
    ?cs a skos:ConceptScheme .
}"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT {
    ?cs skos:hasTopConcept ?x .
}
WHERE {
    ?x skos:topConceptOf ?cs .
}"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT {
    ?x skos:inScheme ?cs .
}
WHERE {
    ?cs a skos:ConceptScheme .
    ?x a skos:Concept .
}"""
g.update(q)

print("ConceptScheme built")

# g.serialize(destination=voc.replace("_0", "_2"), format="ttl")

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX skos-ext: <http://linked.data.gov.au/def/skos-ext#>

DELETE {
    ?x skos-ext:isMemberOf ?y .
}
INSERT {
    ?x skos:broader ?y .
}
WHERE {
    ?x skos-ext:isMemberOf ?y .
}
"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

DELETE {
    ?x skos:member ?y .
}
INSERT {
    ?x skos:narrower ?y .
}
WHERE {
    ?x skos:member ?y .
}
"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT {
    ?x skos:narrower ?y .
}
WHERE {
    ?y skos:broader ?x .
}
"""
g.update(q)

q = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

INSERT {
    ?x skos:broader ?y .
}
WHERE {
    ?y skos:narrower ?x .
}
"""
g.update(q)

print("Concept hierarchy replaced Collection hierarchy")

# g.serialize(destination=voc.replace("_0", "_3"), format="ttl")

# remove unused Reg properties
q = """PREFIX reg: <http://purl.org/linked-data/registry#>

DELETE { ?c ?p ?o }
WHERE {
    ?c a reg:RegisterItem .
    ?c ?p ?o .
}"""
g.update(q)

q = """PREFIX reg: <http://purl.org/linked-data/registry#>

DELETE {
    ?x ?p ?o 
} 
WHERE {
    ?x reg:entity ?y .
	?x ?p ?o .
}"""
g.update(q)

q = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>

DELETE {
    ?s ?p ?o .
}
WHERE {
    ?s foaf:accountName|foaf:name ?o .
    ?s ?p ?o .
}
"""
g.update(q)

print("Reg properties removal complete")

g.serialize(destination=voc.replace("_0", "_4"), format="ttl")
