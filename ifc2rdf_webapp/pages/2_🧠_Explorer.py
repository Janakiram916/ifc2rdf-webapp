import streamlit as st

from tools.rdf_helper import get_rdf_entities
from tools.rdf_helper import get_instances_of_rdf_resource
from tools.rdf_helper import get_triples_based_on_instance_name
from tools.rdf_helper import get_instance_id_from_rdf_resource
from tools.rdf_helper import get_triples_based_on_instance_uri



def execute():
    st.header(" 🧠 Explorer ")
    tab1, tab2, tab3 = st.tabs(["Data_visualize", "DICL", "DICM"])
    with tab1:
        if "rdf_data" in session:
            col1, col2 = st.columns([1, 1])
            col1.selectbox(
                ":orange[Pick select an items from class overview]",
                get_rdf_entities(session.rdf_graph),
                placeholder="",
                key="class_selection",
            )
            col1.selectbox(
                ":blue[Pick an items from instance name overview]",
                get_instances_of_rdf_resource(session.rdf_graph, session.class_selection),
                placeholder="",
                key="instance_selection",
            )
            col2.code(
                get_triples_based_on_instance_name(
                    session.rdf_graph, session.instance_selection, session.class_selection
                ),
                language="turtle",
                line_numbers=True,
            )
            col1.selectbox(
                ":green[Pick an items from instance global id overview]",
                get_instance_id_from_rdf_resource(
                    session.rdf_graph, session.instance_selection
                ),
                placeholder="",
                key="instance_id_selection",
            )
            if not session.instance_id_selection == " Please Select":
                code = get_triples_based_on_instance_uri(
                    session.rdf_graph, session.instance_id_selection
                )
                col1.code(code, language="turtle", line_numbers=True)

        else:
            st.header("Step 1: Load a file from the Home Page")
            st.header("Step 2: Convert IFC file to RDF using converter from the Home Page")
    with tab2:
        st.header("Lifecycle Ontology")
        tab2.markdown(
            f'<iframe src="https://digitalconstruction.github.io/Lifecycle/v/0.5/" width="900" height="900"></iframe>',
            unsafe_allow_html=True,
        )
    with tab3:
        st.header("Material Ontology")
        tab2.write(
            f'<iframe src="https://digitalconstruction.github.io/Materials/v/0.5/" width="900" height="900"></iframe>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    session = st.session_state
    execute()
