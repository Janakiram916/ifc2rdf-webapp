import ifcopenshell
import streamlit as st
from ifc2rdftool.ifc2rdf_tool import get_all_entity_types_from_project_decomposition

from ifc2rdf_webapp.tools.rdf_helper import get_rdf_entities, get_instances_of_rdf_resource, \
    get_triples_based_on_instance_name, get_instance_id_from_rdf_resource, get_triples_based_on_instance_uri


def initialize_session_state():
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}


def get_element_data(placement):
    placement.subheader('Change log')
    placement.write(f"you changed to {session.class_selection}")
    code = """
        SELECT ?resource
        {
        ?instance a ?resource .
        }
    """
    placement.code(code, language="turtle", line_numbers=True)


def execute():
    st.header(" 🧠 Explorer ")

    if "rdf_data" in session:
        col1, col2 = st.columns([1, 1])
        col1.selectbox(":orange[Pick select an items from class overview]", get_rdf_entities(session.rdf_graph),
                       placeholder='', key="class_selection", )
        col1.selectbox(":blue[Pick an items from instance name overview]", get_instances_of_rdf_resource(session.rdf_graph, session.class_selection),
                       placeholder='', key="instance_selection",)
        col2.code(get_triples_based_on_instance_name(session.rdf_graph, session.instance_selection, session.class_selection), language="turtle", line_numbers=True)
        col1.selectbox(":green[Pick an items from instance global id overview]",
                       get_instance_id_from_rdf_resource(session.rdf_graph, session.instance_selection),
                       placeholder='', key="instance_id_selection",)
        if not session.instance_id_selection == " Please Select":
            code = get_triples_based_on_instance_uri(session.rdf_graph, session.instance_id_selection)
            col1.code(code, language="turtle", line_numbers=True)

    else:
        st.header("Step 1: Load a file from the Home Page")
        st.header("Step 2: Convert IFC file to RDF using converter from the Home Page")


if __name__ == "__main__":
    session = st.session_state
    execute()
