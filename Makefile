PY=python

.PHONY: setup lint test format

setup:
	$(PY) -m pip install -r requirements.txt

lint:
	ruff check .

format:
	ruff format .

test:
	pytest -q
