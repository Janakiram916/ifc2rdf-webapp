.PHONEY: install
install:
	poetry install

.PHONEY: ifc-viewer
ifc-viewer:
	poetry run streamlit run ifc2rdf_webapp/Homepage.py