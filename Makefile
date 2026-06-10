.DEFAULT_GOAL := help

# Every command assumes an activated virtualenv. If none is active, fail loudly
# instead of touching the global Python.
ifndef VIRTUAL_ENV
$(error No virtualenv active. Create and activate one first: python -m venv .venv && source .venv/bin/activate   (Windows: .venv\Scripts\activate))
endif

PY := python

###############################################################################
# Development
###############################################################################

.SECTION: Development

.PHONY: install
install: ## Install dependencies
	@$(PY) -m pip install -r requirements.txt

.PHONY: run
run: ## Run the API in dev mode with auto-reload (http://localhost:8000)
	@$(PY) -m uvicorn app.main:app --reload

.PHONY: seed
seed: ## Fill the local database with demo data
	@$(PY) -m app.seed

###############################################################################
# Student
###############################################################################

.SECTION: Student

.PHONY: test
test: ## Run the whole test suite
	@$(PY) -m pytest

.PHONY: black
black: ## Format app/ with Black
	@$(PY) -m black app

.PHONY: criteria
criteria: ## Show the graded criteria (the spec to satisfy)
	@$(PY) -m grader.show_criteria

.PHONY: grade
grade: ## Run automated grading and write the score report
	@$(PY) -m grader.engine.run

###############################################################################
# Instructor
###############################################################################

.SECTION: Instructor - ⚠️ DON'T RUN THESE COMMANDS
.PHONY: sync
sync: ## (Instructor) Refresh criteria totals + protected-file hashes
	@$(PY) -m grader.sync

###############################################################################
# Help
###############################################################################

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} \
		/^\.SECTION:/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 11) } \
		/^[a-zA-Z0-9_-]+:.*?## / { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' \
		$(MAKEFILE_LIST)
