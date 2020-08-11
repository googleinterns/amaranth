.PHONY: setup run-interactive run-train test-python lint-python lint-js

setup:
	pip install -r requirements.txt

# Amaranth ML commands
run-interactive:
	python -m amaranth.ml.interactive

run-train:
	python -m amaranth.ml.train

test-python:
	python -m unittest

lint-python:
	pylint amaranth/

# Amaranth Chrome Extension commands
lint-js:
	node_modules/.bin/eslint amaranth-chrome-ext/src/