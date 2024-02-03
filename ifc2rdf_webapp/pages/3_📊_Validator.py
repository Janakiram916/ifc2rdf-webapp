import streamlit as st


def initialize_session_state():
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}


def execute():
    st.set_page_config(
        layout="wide",
        page_title="RDF Validator ©karlapudi",
        page_icon="📊",
        menu_items={
            'Get Help': 'mailto:janakiramkarlapudi841@gmail.com',
            'Report a bug': "https://github.com/Janakiram916/ifc2rdf-webapp/issues",
            'About': "## RDF Data validator. Developed to validate RDF data!"
        }
    )
    st.header(" 📊 Validator ")

    if "rdf_data" in session:
        pass
    else:
        st.header("Step 1: Load a file from the Home Page")
        st.header("Step 2: Convert IFC file to RDF using converter from the Home Page")


if __name__ == "__main__":
    session = st.session_state
    execute()
