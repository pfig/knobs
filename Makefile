.PHONY: clean clean-build clean-pyc clean-test docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
    from urllib import pathname2url
except:
    from urllib.request import pathname2url

webbrowser.open('file://' + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print('%-20s %s' % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all development artefacts

clean-build: ## remove build artefacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -type f -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python compiled artefacts
	find . -type f -name '*.pyc' -exec rm -f {} +
	find . -type f -name '*.pyo' -exec rm -f {} +
	find . -type f -name '*~' -exec rm -f {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +

clean-test: ## remove test and coverage artefacts
	rm -rf .pytest_cache/
	rm -rf .coverage coverage.xml
	rm -rf htmlcov/

venv: ## create isolated environment
	python -m venv --prompt knobs ./.venv

install-dev: ## install for development
	python -m pip install --editable '.[dev]'

lint: ## check style with black and flake8
	black --line-length 99 --check --diff src/ tests/
	flake8 src tests --builtins='ModuleNotFoundError'

black: ## format code with black
	black --line-length 99 src/ tests/

test: ## run tests
	SQLALCHEMY_SILENCE_UBER_WARNING=1 python -m pytest

coverage: ## check test coverage
	python -m pytest --cov=src tests

install: clean ## install package and script
	python -m pip install .
