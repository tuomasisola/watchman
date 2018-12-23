# Makefile for the 'watchman' package.
#
# Author: Tuomas Isola

PACKAGE_NAME = watchman
SHELL = bash

SSH_USER = pi
SSH_IP = raspberrypi.local

default:
	@echo "Makefile for $(PACKAGE_NAME)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make run          run the package'
	@echo '    make build        install requirements'
	@echo '    make clean        cleanup all temporary files'
	@echo
	@echo '    make init-pi      set-up Raspberry Pi ('$(SSH_IP)')'
	@echo '    make publish      deploy package to the Pi'
	@echo '    make run-pi       run package at the Pi'
	@echo

.PHONY: run
run:
	source venv/bin/activate && \
	python watchman/watch.py

.PHONY: build
build:
	python3 -m venv ./venv && \
	source venv/bin/activate && \
	python3 -m pip install --upgrade pip && \
	python3 -m pip install -r requirements.txt

.PHONY: clean
clean:
	rm -Rf venv pip-selfcheck.json && \
	find . -name __pycache__ -exec rm -rf {} \+

.PHONY: init-pi
init-pi:
	ssh $(SSH_USER)@$(SSH_IP) 'sudo apt-get install python3-pip && \
		sudo apt-get install python3-venv && \
		sudo apt-get install python3-lxml python-lxml && \
		mkdir watchman && \
		cd watchman && \
		virtualenv venv'

.PHONY: run-pi
run-pi:
	ssh $(SSH_USER)@$(SSH_IP) 'make -C watchman run'

.PHONY: publish
publish:
	rsync -vzrc --exclude '__pycache__' -e ssh watchman Makefile requirements.txt cronfile $(SSH_USER)@$(SSH_IP):watchman/ && \
	ssh $(SSH_USER)@$(SSH_IP) 'cd watchman && \
	source venv/bin/activate && \
	pip3 install -r requirements.txt && \
	crontab cronfile'
