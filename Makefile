# Makefile


python_package := pmpc
pip_requirements := requirements.txt
python_test_modules := $(wildcard tests/*.py)
pylint_packages := setup.py,$(python_package),$(python_test_modules)


.PHONY: run
run:
	python -m pmpc.script


.PHONY: develop
develop:
	pip install --requirement $(pip_requirements) --editable .


.PHONY: pep8
pep8:
	python setup.py pep8


.PHONY: pylint
pylint:
	python setup.py lint --lint-packages=$(pylint_packages)


.PHONY: lint
lint: pep8 pylint


.PHONY: test
test:
	python setup.py pytest --addopts=-v


# EOF
