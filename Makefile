# Variables
PYTHON ?= python
POETRY ?= poetry

# Phony targets
.PHONY: help fix check tests build init pre-commit

help:
	@echo "Available commands:"
	@echo "  make fix    - Format the code using black and fix issues with ruff"
	@echo "  make check  - Run linters (ruff, black)"
	@echo "  make tests  - Run all unit tests using pytest"
	@echo "  make build  - Build the package using poetry"
	@echo "  make init   - Initialize the environment (install dependencies)"
	@echo "  make pre-commit   - Run pre-commit hooks manually on all files"

fix:
	@echo "Running black and ruff (fix mode)..."
	$(POETRY) run black .
	$(POETRY) run ruff check . --fix

check:
	@echo "Running black and ruff (check mode)..."
	$(POETRY) run black --check .
	$(POETRY) run ruff check .

tests:
	@echo "Running pytest..."
	$(POETRY) run pytest tests/

build:
	@echo "Building the package..."
	$(POETRY) build

init:
	@echo "Initializing the project..."
	$(POETRY) install --all-extras

pre-commit:
	@echo "Running pre-commit hooks on all files..."
	$(POETRY) run pre-commit run --all-files
