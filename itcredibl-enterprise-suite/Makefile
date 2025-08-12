SHELL := /bin/bash

.PHONY: setup demos test clean

setup:
	python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

demos:
	source .venv/bin/activate && python demos/01_basic_chat.py

test:
	source .venv/bin/activate && pytest -q

clean:
	rm -rf .venv **/__pycache__ **/*.pyc