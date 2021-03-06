.PHONY: setup run-interactive run-train test-python lint-python test-js lint-js

setup:
	pip install -r requirements.txt
	npm install --prefix amaranth-chrome-ext/

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
test-js:
	npm run test --prefix amaranth-chrome-ext/

lint-js:
	npm run lint --prefix amaranth-chrome-ext/