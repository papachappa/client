.PHONY: clean-pyc lint help install upgrade
.DEFAULT_GOAL := help
SHELL := /bin/bash


PY_VERSION ?= 3.5
PIP ?= pip$(PY_VERSION)
PYVENV ?= pyvenv-$(PY_VERSION)
REQUIREMENTS ?= requirements_dev.txt

mkfile_path = $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_PATH ?= $(patsubst %/,%,$(dir $(mkfile_path)))
VAR_PATH ?= "$(PROJECT_PATH)/var"
VENV_PATH ?= "$(PROJECT_PATH)/venv"
CELERY_DIR ?= $(VAR_PATH)/celery
CLIENT_DIR ?= $(PROJECT_PATH)/client
CLIENT_SETTINGS_DIR ?= $(CLIENT_DIR)/settings/

FIND_NOT_IN_VENV = find -not -path "$(VENV_PATH)/*"
ACTIVATE_VENV = . $(VENV_PATH)/bin/activate


help:
	@echo "install"
	@echo "    Install test_portal client application and its python dependencies"
	@echo "upgrade"
	@echo "     Upgrade python dependencies, scripts"
	@echo "install-scripts"
	@echo "    Install scripts for start/stop workers into virtual environment"
	@echo "clean"
	@echo "    Remove artifacts."
	@echo "clean-pyc"
	@echo "    Remove python artifacts."
	@echo "clean-celery-logs"
	@echo "    Remove celery logs."
	@echo "lint"
	@echo "    Run static code analyser."


upgrade: install-py-deps install-scripts


install: | make-dirs install-py-deps install-scripts


make-dirs:
	mkdir $(CELERY_DIR)/{logs,pid} -p
	$(PYVENV) $(VENV_PATH)


install-py-deps:
	$(ACTIVATE_VENV) ; \
	$(PIP) install --upgrade pip ; \
	$(PIP) install -r $(REQUIREMENTS) ; \
	deactivate ; 


install-scripts: | add-scripts-to-env enhance-scripts


add-scripts-to-env:
	@cp "$(PROJECT_PATH)/scripts/start_workers.sh" "$(VENV_PATH)/bin/start_workers"
	@cp "$(PROJECT_PATH)/scripts/stop_workers.sh" "$(VENV_PATH)/bin/stop_workers"


enhance-scripts:
	@sed -E -e "s|^(VAR_CELERY_DIR=).*|\1\"$(CELERY_DIR)\"|" \
		 -e "s|^(CLIENT_SETTINGS_DIR=).*|\1\"$(CLIENT_SETTINGS_DIR)\"|" \
		 -i "$(VENV_PATH)/bin/"start_workers
	@sed -i -E "s|^(CELERY_DIR=).*|\1\"$(CELERY_DIR)\"|" "$(VENV_PATH)/bin/"stop_workers


clean: clean-pyc
	rm -rf $(VAR_PATH)
	rm -rf $(VENV_PATH)


clean-celery-logs:
	rm -f $(CELERY_DIR)/logs/*


clean-pyc:
	$(FIND_NOT_IN_VENV) -type d -and -not -path '__pycache__/*' \
						-name '__pycache__' -exec rm -rf {} +
	$(FIND_NOT_IN_VENV) -type f -name '*.pyc' -or -name '*.pyo' -exec rm -f {} +


lint:
	$(ACTIVATE_VENV) ; \
	pylint client ; \
	deactivate
