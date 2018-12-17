# Makefile for the 'watchman' package.
#
# Author: Tuomas Isola

PACKAGE_NAME = watchman
SHELL = bash

default:
	@echo "Makefile for $(PACKAGE_NAME)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make run          run the package'
	@echo '    make build        install requirements'
	@echo '    make clean        cleanup all temporary files'
	@echo

.PHONY: run
run:
	. bin/activate && \
	python watchman/watch.py

.PHONY: build
build:
	python3 -m venv . && \
	. bin/activate && \
	python3 -m pip install --upgrade pip && \
	pip install -r requirements.txt

.PHONY: clean
clean:
	rm -Rf bin include lib *.cfg pip-selfcheck.json && \
	find . -name __pycache__ -exec rm -rf {} \;
