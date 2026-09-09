.DEFAULT_GOAL := help
EXAMPLE ?= examples/01_first_agent.py
LIVE_CORE := examples/01_first_agent.py examples/02_function_tool.py \
	examples/04_conditional_router.py examples/12_handoff.py \
	examples/13_agent_as_tool.py
LIVE_ORCHESTRATION := examples/08_fan_out.py examples/10_evaluator_refiner.py \
	examples/11_plan_execute.py examples/25_manager_worker.py \
	examples/42_partial_failure.py examples/43_dependency_scheduling.py \
	examples/44_replanning.py
LIVE_ALL := $(filter-out examples/16_graph_topology.py examples/18_cycle_detection.py \
	examples/35_failure_modes.py examples/37_eval_matrix.py examples/41_sandbox_boundary.py \
	examples/45_approval_resume.py,$(wildcard examples/[0-9][0-9]_*.py))

.PHONY: help install format lint typecheck test run live-core live-orchestration live-all check-all clean

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

typecheck: ## Run strict mypy checks
	uv run mypy examples tests

test: ## Run offline workflow tests
	uv run python -m pytest -v

run: ## Run one example offline (append --live in EXAMPLE for API calls)
	uv run python $(EXAMPLE)

live-core: ## Run a small live Agents SDK subset (uses API credits)
	@for example in $(LIVE_CORE); do uv run python $$example --live || exit $$?; done

live-orchestration: ## Run seven orchestration lessons with real API calls
	@for example in $(LIVE_ORCHESTRATION); do uv run python $$example --live || exit $$?; done

live-all: ## Run all model lessons except the hosted sandbox (uses API credits)
	@for example in $(LIVE_ALL); do uv run python $$example --live || exit $$?; done

check-all: lint typecheck test ## Run the safe quality gate

clean: ## Remove local caches and outputs
	rm -rf .pytest_cache .ruff_cache out
	find . -type d -name __pycache__ -exec rm -rf {} +
