# Makefile


python_package := pmpc
pip_requirements := requirements.txt
pylint_packages := setup.py $(python_package) tests/*.py


# join with commas
comma := ,
empty :=
space := $(empty) $(empty)
joinwithcommas = $(subst $(space),$(comma),$(wildcard $(1)))


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
	python setup.py lint --lint-reports=no \
		--lint-packages=$(call joinwithcommas,$(pylint_packages))


.PHONY: lint
lint: pep8 pylint


.PHONY: test
test:
	python setup.py pytest --addopts=-v


# EOF
