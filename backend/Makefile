# Variables Configuration
PYTHON = python
APP_DIR = app
TEST_DIR = tests

.PHONY: help install migrate migrations rollback history current test test-v lint format type-check check-all clean

help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


## --- SETUP ---
add: ## Add a production dependency (e.g., make add p=requests)
	uv add $(p)

add-dev: ## Add a development dependency (e.g., make add-dev p=pytest)
	uv add --group dev $(p)


## --- DATABASE (ALEMBIC) ---
migrations: ## Generate a new migration script (usage: make migrations m="migration_name")
	alembic revision --autogenerate -m "$(m)"

migrate: ## Apply all pending migrations to the latest version
	alembic upgrade head

rollback: ## Revert the last migration version
	alembic downgrade -1

history: ## Show migration lineage and scripts
	alembic history --verbose

current: ## Show the current revision of the database
	alembic current


## --- QUALITY CONTROL & TESTING ---
test: ## Run tests with coverage report
	pytest

test-v: ## Run tests with log visibility (loguru)
	pytest -s

lint: ## Check for logical errors and style violations (Ruff)
	ruff check .

format: ## Automatically format code (Ruff)
	ruff format .

type-check: ## Run static type analysis (Mypy)
	mypy .

check-all: format lint type-check test ## Run all quality tools in sequence


## --- CLEANUP ---
clean: ## Remove temporary cache files, coverage data, and directories
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf .cache