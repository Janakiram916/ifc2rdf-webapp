import streamlit as st


def initialize_session_state():
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    
def execute():
    st.header(" 📊 Validator ")

    if "rdf_data" in session:
        pass
    else:
        st.header("Step 1: Load a file from the Home Page")
        st.header("Step 2: Convert IFC file to RDF using converter from the Home Page")


if __name__ == "__main__":
    session = st.session_state
    execute()
