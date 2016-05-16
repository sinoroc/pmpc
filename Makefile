# Makefile


pip_requirements := requirements.txt
lint_packages := setup.py,pmpc


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
	python setup.py lint --lint-packages=$(lint_packages)


.PHONY: lint
lint: pep8 pylint


# EOF
