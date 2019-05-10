all: run

clean:
	rm -rf *.egg-info && rm -rf dist && rm -rf *.log* && rm -rf venv

venv:
	virtualenv --python=python3.6 venv  && venv/bin/pip install -r requirements.txt

run: venv
	FLASK_APP=sentinel_backend FLASK_DEBUG=1 SENTINEL_BACKEND_SETTINGS=../settings.cfg venv/bin/flask run

test: venv
	SENTINEL_BACKEND_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
