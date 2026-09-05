.DEFAULT_GOAL := help
EXAMPLE ?= examples/01_first_agent.py
LIVE_CORE := examples/01_first_agent.py examples/02_function_tool.py \
	examples/04_conditional_router.py examples/12_handoff.py \
	examples/13_agent_as_tool.py

.PHONY: help install format lint test run live-core check-all clean

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*## "}; {printf "  %-14s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --all-groups

format: ## Format examples and tests
	uv run ruff format examples tests
	uv run ruff check --fix examples tests

lint: ## Check formatting and linting
	uv run ruff format --check examples tests
	uv run ruff check examples tests

test: ## Run offline workflow tests
	uv run python -m pytest -v

run: ## Run one example (SDK calls require OPENAI_API_KEY)
	uv run python $(EXAMPLE)

live-core: ## Run a small live Agents SDK subset (uses API credits)
	@for example in $(LIVE_CORE); do uv run python $$example || exit $$?; done

check-all: lint test ## Run the safe quality gate

clean: ## Remove local caches and outputs
	rm -rf .pytest_cache .ruff_cache out
	find . -type d -name __pycache__ -exec rm -rf {} +
