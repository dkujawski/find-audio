PROJECT_NAME = find-audio
PYTHON = python3
POETRY = poetry

# Default target
.DEFAULT_GOAL := help

## Install dependencies
install:
	$(POETRY) install

## Run the application
run:
	$(POETRY) run $(PROJECT_NAME)

## Run linting (flake8 and black)
lint:
	$(POETRY) run flake8 $(PROJECT_NAME)
	$(POETRY) run black --check $(PROJECT_NAME)

## Format code using black
format:
	$(POETRY) run black $(PROJECT_NAME)

## Run tests
 test:
	$(POETRY) run pytest tests

## Clean up cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm ./downloads/*

## Show help
help:
	@echo "Available commands:"
	@grep -E '^##' Makefile | sed -e 's/^## //'

