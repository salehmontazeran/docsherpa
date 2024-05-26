SHELL=/bin/sh
VENV=venv
VEN_PYTHON=$(VENV)/bin/python3.10
SYSTEM_PYTHON=$(or $(shell which python3.10), $(shell which python3))
REQUIREMENTS_FILE=requirements.txt

.PHONY: help build run tests clean lint

deps.venv:
	$(SYSTEM_PYTHON) -m venv $(VENV)

deps.require:
	$(VEN_PYTHON) -m pip install --upgrade pip
	$(VEN_PYTHON) -m pip install pip-tools wheel setuptools

deps.compile:
	$(VEN_PYTHON) -m piptools compile --upgrade --allow-unsafe -o $(REQUIREMENTS_FILE)

deps.sync:
	$(VEN_PYTHON) -m piptools sync $(REQUIREMENTS_FILE)

install:
	make deps.venv && make deps.require && make deps.sync

app.run:
	export PYTHONPATH=$(pwd)
	$(VEN_PYTHON) -m streamlit run src/main.py

milvus.up:
	bash standalone_embed.sh start

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache

lint:
	$(VEN_PYTHON) -m ruff check src
	$(VEN_PYTHON) -m mypy --check-untyped-defs src

# build:
# 	$(DOCKER_COMPOSE) build --no-cache

# up:
# 	$(DOCKER_COMPOSE) up --remove-orphans -d

# down:
# 	$(DOCKER_COMPOSE) down

# logs:
# 	$(DOCKER_COMPOSE) logs -f

# exec:
# 	$(DOCKER_EXEC) bash


# lint:
# 	flake8

# test:
# 	$(DOCKER_EXEC) pytest $(arg)
