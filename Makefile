.PHONY: all test run lint clean

### Default target(s)
all: test

### Perform static analysis
lint:
	uv run ruff check --select I --fix .
	uv run ruff format .
	uv run ruff check . --fix

### Run the project
run: lint
	uv run pastebin-cli ls
	uv run pastebin-cli get DM8weHEd

### Run unit tests
test: lint
	uv run pytest -s -v

### Clean up generated files
clean:
	uv clean
	rm -fr .ruff_cache .venv

### Install this tool locally
install:
	uv tool install --upgrade .

### Start the notebook server
notebook:
	uv run jupyter lab --notebook-dir=pastebin-api

