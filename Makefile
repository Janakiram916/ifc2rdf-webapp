SRC_PATH := ./ifc2rdf-webapp

.PHONEY: install
install:
	poetry install

.PHONEY: ifc-viewer
ifc-viewer:
	poetry run streamlit run ifc2rdf_webapp/Homepage.py

.PHONEY: test
test:
	poetry run pytest -vv -s .\tests

.PHONY: requirements.txt
requirements.txt: ## Creates requirements.txt file
	poetry export -f requirements.txt --output requirements.txt

.PHONY: auto-format
auto-format: ## Automatically formats the code
	poetry run black ./tests
	poetry run isort ./tests

.PHONY: lint
lint: ## Execute lint script located in the bin folder of the dt/config repo
	poetry run ruff check ./tests --fix
	poetry run ruff check ./ifc2rdf_webapp/tools --fix

.PHONY: check
check: auto-format lint test ## Runs all code checks and tests