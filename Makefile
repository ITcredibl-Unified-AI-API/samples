SHELL := /bin/bash

.PHONY: setup py.setup ts.setup build test demo clean

setup: py.setup ts.setup

py.setup:
	cd python_sdk && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

ts.setup:
	cd ts_sdk && npm install

build:
	cd ts_sdk && npm run build

test:
	cd ts_sdk && npm test -- --passWithNoTests

demo:
	cd python_sdk && source .venv/bin/activate && \	python -m examples.cli_demo && \	python -m examples.stream_demo

clean:
	rm -rf **/__pycache__ **/*.pyc ts_sdk/dist python_sdk/.venv