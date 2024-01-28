from icecream import ic
from rdflib import Graph
from rdflib.compare import isomorphic

from ifc2rdf_webapp.tools.rdf_helper import get_rdf_entities, get_instances_of_rdf_resource, \
    get_triples_based_on_instance_name, get_instance_id_from_rdf_resource, get_triples_based_on_instance_uri

test_query ="""
    SELECT ?instance
    WHERE
    {{
        ?instance core:hasLabel ?inst_name .
        FILTER(str(?inst_name) = "CIB")
    }}
    """


def test_should_return_ontology_resources() -> None:
    test_graph_path = "tests/resources/test_graph.ttl"
    test_graph = Graph().parse(source=test_graph_path, format='turtle')
    actual_list = get_rdf_entities(test_graph)
    expected_item = ['Building',
                     'Constituent',
                     'ConstituentSet',
                     'Door',
                     'Layer',
                     'LayerSet',
                     'Material',
                     'Project',
                     'Property',
                     'Roof',
                     'Site',
                     'Slab',
                     'Space',
                     'Storey',
                     'Wall',
                     'Window']
    assert actual_list == expected_item


def test_should_return_list_of_ontology_resource() -> None:
    resource_type = 'Building'
    test_graph_path = "tests/resources/test_graph.ttl"
    test_graph = Graph().parse(source=test_graph_path, format='turtle')
    actual_list = get_instances_of_rdf_resource(test_graph, resource_type)
    expected_list = ['CIB']
    assert actual_list == expected_list


def test_should_return_resource_id_when_given_resource_name():
    resource_name = 'CIB'
    test_graph_path = "tests/resources/test_graph.ttl"
    test_graph = Graph().parse(source=test_graph_path, format='turtle')
    actual_list = get_instance_id_from_rdf_resource(test_graph, resource_name)
    expected_list = [' Please Select ', '04XCdhzWXDtBhVSPPuhCyY']
    assert actual_list == expected_list


def test_should_return_triples_based_on_instance_name() -> None:
    instance_type = 'CIB'
    test_graph_path = "tests/resources/test_graph.ttl"
    test_graph = Graph().parse(source=test_graph_path, format='turtle')
    actually_constructed_graph = get_triples_based_on_instance_name(test_graph, instance_type, "Building")
    actual_graph = Graph().parse(data=actually_constructed_graph)
    expected_triples = """
    @prefix bot: <https://w3id.org/bot#> .
    @prefix core: <https://w3id.org/digitalconstruction/core#> .
    @prefix inst: <https://w3id.org/digitalconstruction/instance#> .

    inst:04XCdhzWXDtBhVSPPuhCyY a bot:Building ;
        bot:hasStorey inst:04XCdhzWXDtBhVSPQ7KoGO,
            inst:04XCdhzWXDtBhVSPQ7KoGx,
            inst:04XCdhzWXDtBhVSPQ7KoNL,
            inst:04XCdhzWXDtBhVSPQ7KoNt,
            inst:04XCdhzWXDtBhVSPQ7KpcK ;
        core:hasGlobalID "04XCdhzWXDtBhVSPPuhCyY" ;
        core:hasLabel "CIB" ;
        core:hasName "CIB" .
        """
    expected_graph = Graph().parse(data=expected_triples)
    assert isomorphic(actual_graph, expected_graph)


def test_should_return_triples_based_on_instance_uri() -> None:
    test_graph_path = "tests/resources/test_graph.ttl"
    test_graph = Graph().parse(source=test_graph_path, format='turtle')
    actually_constructed_graph = get_triples_based_on_instance_uri(test_graph, "04XCdhzWXDtBhVSPPuhCyY")
    actual_graph = Graph().parse(data=actually_constructed_graph)
    expected_triples = """
    @prefix bot: <https://w3id.org/bot#> .
    @prefix core: <https://w3id.org/digitalconstruction/core#> .
    @prefix inst: <https://w3id.org/digitalconstruction/instance#> .

    inst:04XCdhzWXDtBhVSPPuhCyY a bot:Building ;
        bot:hasStorey inst:04XCdhzWXDtBhVSPQ7KoGO,
            inst:04XCdhzWXDtBhVSPQ7KoGx,
            inst:04XCdhzWXDtBhVSPQ7KoNL,
            inst:04XCdhzWXDtBhVSPQ7KoNt,
            inst:04XCdhzWXDtBhVSPQ7KpcK ;
        core:hasGlobalID "04XCdhzWXDtBhVSPPuhCyY" ;
        core:hasLabel "CIB" ;
        core:hasName "CIB" .
        """
    expected_graph = Graph().parse(data=expected_triples)
    assert isomorphic(actual_graph, expected_graph)
