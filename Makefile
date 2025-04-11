# Default goal when no target is specified
.DEFAULT_GOAL := help

############################################################################
# Help Command
############################################################################
help:
	@echo "Usage:"
	@echo "Basic Commands:"

############################################################################
# Environment Setup and Dependencies
############################################################################

.PHONY: bootstrap
bootstrap:
	python3.9 -m venv sandbox

setup:
	@poetry config virtualenvs.create false
	@poetry install --no-root

############################################################################
# Build & Install
############################################################################

.PHONY: build
build:
	poetry install

############################################################################
# Benchmark
############################################################################

.PHONY: bench 
bench:
	@quark --bench $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))

############################################################################
# Testing & Validation
############################################################################

.PHONY: test
test: build
	@cd tests && ./run_pytest.sh

