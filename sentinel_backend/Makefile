SHELL := /bin/bash

all: run

clean:
	rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -rf venv

venv:
	python3 -m venv venv && venv/bin/pip install -r requirements.txt

run: venv
	FLASK_APP=sentinel_backend SENTINEL_BACKEND_SETTINGS=../settings.cfg venv/bin/flask run

prod:
	FLASK_APP=sentinel_backend SENTINEL_BACKEND_SETTINGS=../settings.cfg flask run --host=0.0.0.0 

test: venv
	SENTINEL_BACKEND_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist

lint: 
	venv/bin/flake8 sentinel_backend
	venv/bin/mypy sentinel_backend --ignore-missing-imports