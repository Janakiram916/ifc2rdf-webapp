
import ifcopenshell
import streamlit as st
from ifc2rdftool.ifc2rdf_tool import create_rdf_graph_from_ifc


def callback_upload():
    if session["uploaded_file"] is not None:
        session["file_name"] = session["uploaded_file"].name
        session["array_buffer"] = session["uploaded_file"].getvalue()
        session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
        session["is_file_loaded"] = True

    # Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    # Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

    # Emptying generation session
    session["is_rdf_data_generated"] = False


def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name


# def change_project_name():
#     if session.project_name_input:
#         session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
#         st.balloons()


def generate_rdf_data():
    generated_rdf = create_rdf_graph_from_ifc(session.ifc_file)
    session["rdf_graph"] = generated_rdf
    if generated_rdf:
        session["rdf_data"] = generated_rdf.serialize(format='turtle')
        session["is_rdf_data_generated"] = True


def main():
    st.set_page_config(
        layout="wide",
        page_title="IFC Processor ©karlapudi",
        page_icon="✍️",
    )
    st.title("IFC Processor")
    st.markdown(
        """ 
    ## A tool to visualize BIM data and convert it to RDF.
    
    ###  📁 Click on `Browse File` in the Side Bar to start
    """
    )

    # Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    # Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success('Project successfully loaded')
        st.sidebar.write("🔃 You can reload a new file  ")

        col1, col2 = st.columns([2, 1])
        col1.subheader(f'Start Exploring "{get_project_name()}"')

        col2.subheader("IFC2RDF convertor")
        col2.write("IFC2RDF convertor converty your IFC data to RDF based on the library "
                   "🐙 [ifc2rdfTool](https://github.com/Janakiram916/ifc2rdfTool).")
        col2.button("🔃 Start Conversion", key="generated_file", on_click=generate_rdf_data)
        if "is_rdf_data_generated" in session and session["is_rdf_data_generated"]:
            col2.success('Data conversion is successful')
            col2.write("You can now ⬇️ Download rdf file ")
            col2.download_button('⬇️ Download RDF', key="download_rdf", data=session.rdf_data,
                                 file_name=f"{session.file_name.split('.')[0]}.ttl", on_click=generate_rdf_data)

    st.sidebar.write("""
    --------------
    ### Credits:
    #### Sigma Dimensions (TM)
    #### Janakiram Karlapudi
    License: MIT
    
    """)
    st.write("")
    st.sidebar.write("")


if __name__ == "__main__":
    session = st.session_state
    main()
