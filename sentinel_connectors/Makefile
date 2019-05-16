.PHONY: clean lint requirements tests

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = sentinel_connectors
PYTHON_INTERPRETER = python3.6
VENV_NAME = .env

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies
requirements: 
	$(PYTHON_INTERPRETER) setup.py install
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache

## Lint using flake8 nad check types using mypy
lint:
	flake8 sentinel_connectors
	mypy sentinel_connectors --ignore-missing-imports

## Create virtual environment:
create_environment:
	$(PYTHON_INTERPRETER) -m venv $(VENV_NAME)

## Run tests
tests:
	$(PYTHON_INTERPRETER) -m pytest tests

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

SINK ?= kafka
all:;: '$(SINK)'

reddit_sample:
	$(PYTHON_INTERPRETER) run_connector.py stream --source reddit --sink $(SINK)

reddit_historical_sample:
	$(PYTHON_INTERPRETER) run_connector.py historical --source reddit --keywords madagascar --since 2019-04-19 --until 2019-04-20 --sink $(SINK)

hn_sample:
	$(PYTHON_INTERPRETER) run_connector.py stream --source hacker-news --sink $(SINK)

hn_historical_sample:
	$(PYTHON_INTERPRETER) run_connector.py historical --source hacker-news --keywords microsoft --since 2019-04-19 --until 2019-04-20 --sink $(SINK)

gn_sample:
	$(PYTHON_INTERPRETER) run_connector.py stream --source google-news --sink $(SINK)

gn_historical_sample:
	$(PYTHON_INTERPRETER) run_connector.py historical --source google-news --keywords microsoft --since $(shell date +'%Y-%m-%d' --date='-1 day') --until $(shell date +'%Y-%m-%d') --sink $(SINK)

twitter_sample:
	$(PYTHON_INTERPRETER) run_connector.py stream  --source twitter --sink $(SINK)

twitter_historical_sample:
	$(PYTHON_INTERPRETER) run_connector.py historical --source twitter --keywords nike --since $(shell date +'%Y-%m-%d' --date='-1 day') --until $(shell date +'%Y-%m-%d') --sink $(SINK)

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
