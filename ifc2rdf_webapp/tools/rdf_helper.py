from icecream import ic
from ifc2rdftool.ifc2rdf_tool import initialize_graph
from rdflib import Graph, URIRef

_INSTANCE_NAME = "$INSTANCE_NAME"
_CLASS_URI = URIRef("$CLASS_URI")
_INSTANCE_URI = URIRef("$INSTANCE_URI")
_CLASS_QUERY = """
    SELECT ?instance ?resource ?inst_name ?inst_id
    WHERE
    {
    ?instance a ?resource .
    optional{?instance core:hasLabel ?inst_name .}
    optional{?instance core:hasGlobalID ?inst_id .}
    }
"""

_GET_INSTANCE_GRAPH_BASED_ON_NAME_QUERY = f"""
    CONSTRUCT
    {{
        ?instance ?p ?o .
    }}
    WHERE
    {{
        ?instance a <{_CLASS_URI}> .
        ?instance core:hasLabel ?inst_name .
        FILTER(str(?inst_name) = "{_INSTANCE_NAME}")
        
        ?instance ?p ?o .
        
    }}
"""

_GET_INSTANCE_GRAPH_BASED_ON_URI_QUERY = f"""
    CONSTRUCT
    {{
        ?instance ?p ?o .
    }}
    WHERE
    {{
        ?instance ?p ?o .
        FILTER(?instance = <{_INSTANCE_URI}>)
    }}
"""


def get_rdf_entities(rdf_graph: Graph):
    query_result = rdf_graph.query(_CLASS_QUERY)
    items_set = set()
    for row in query_result:
        items_set.add(row.resource.fragment)
    return sorted(items_set)


def get_instances_of_rdf_resource(rdf_graph: Graph, resource_type: str):
    query_result = rdf_graph.query(_CLASS_QUERY)
    items_data = {}
    for row in query_result:
        element = row.resource.fragment
        if element in items_data:
            items_data[element].add(str(row.inst_name))
        else:
            items_data[element] = {str(row.inst_name)}
    if resource_type in items_data:
        return sorted(items_data[resource_type])


def get_instance_id_from_rdf_resource(rdf_graph: Graph, resource_name: str):
    query_result = rdf_graph.query(_CLASS_QUERY)
    items_data = {}
    for row in query_result:
        element_name = str(row.inst_name)
        if element_name in items_data:
            items_data[element_name].add(str(row.inst_id))
        else:
            items_data[element_name] = {" Please Select "}
            items_data[element_name].add(str(row.inst_id))
    if resource_name in items_data:
        return sorted(items_data[resource_name])


def get_triples_based_on_instance_name(rdf_graph: Graph, instance_label: str, rdf_resource: str):
    query_result = rdf_graph.query(_CLASS_QUERY)
    resource = URIRef('')
    for row in query_result:
        if row.resource.fragment == rdf_resource:
            resource = row.resource
    instance_rule_query = _GET_INSTANCE_GRAPH_BASED_ON_NAME_QUERY.replace(_INSTANCE_NAME, instance_label).replace(
        _CLASS_URI, resource)
    graph = initialize_graph()
    construct_query_result = rdf_graph.query(instance_rule_query)
    for triple in construct_query_result:
        graph.add(triple)
    constructed_graph_data = graph.serialize()
    return constructed_graph_data


def get_triples_based_on_instance_uri(rdf_graph: Graph, instance_id: str):
    query_result = rdf_graph.query(_CLASS_QUERY)
    instance_uri = URIRef('')
    for row in query_result:
        if row.instance.fragment == instance_id:
            instance_uri = row.instance
    instance_rule_query = _GET_INSTANCE_GRAPH_BASED_ON_URI_QUERY.replace(_INSTANCE_URI, instance_uri)
    graph = initialize_graph()
    construct_query_result = rdf_graph.query(instance_rule_query)
    for triple in construct_query_result:
        graph.add(triple)
    constructed_graph_data = graph.serialize()
    return constructed_graph_data
