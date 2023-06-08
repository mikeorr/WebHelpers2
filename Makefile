# isort . && black . && bandit -r . && pylint && pre-commit run --all-files
# Get changed files

FILES := $(wildcard **/*.py)

# if you wrap everything in poetry run, it runs slower.
ifeq ($(origin VIRTUAL_ENV),undefined)
    VENV := poetry run
else
    VENV :=
endif

poetry.lock: pyproject.toml
	@echo "Installing dependencies"
	@poetry install --with dev

clean-pyc:
	@echo "Removing compiled files"
	@find . -name '*.pyc' -exec rm -f {} + || true
	@find . -name '*.pyo' -exec rm -f {} + || true
	@find . -name '__pycache__' -exec rm -fr {} + || true

clean-test:
	@echo "Removing coverage data"
	@rm -f .coverage || true
	@rm -f .coverage.* || true

clean: clean-pyc clean-test

# tests can't be expected to pass if dependencies aren't installed.
# tests are often slow and linting is fast, so run tests on linted code.
test: clean poetry.lock
	@echo "Running unit tests"
	$(VENV) pytest webhelpers2
	 #--doctest-modules
	# $(VENV) py.test test --cov=webhelpers2 --cov-report=html --cov-fail-under 50

tox:
	@echo "Running tox tests"
	$(VENV) tox

.build_history:
	@mkdir -p .build_history

check: test

.PHONY: publish
build: check
	rm -rf dist && poetry build

# Better to not do this and use trusted publisher with github actions
.PHONY: publish
publish_test:
	rm -rf dist && poetry version minor && poetry build && twine upload -r testpypi dist/*

# Better to not do this and use trusted publisher with github actions
.PHONY: publish
publish_pypi: test
	rm -rf dist && poetry version minor && poetry build && twine upload dist/*
