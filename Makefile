.DEFAULT_GOAL := help

help:
	@echo ""
	@echo "PowerXRD Development Commands"
	@echo "-----------------------------"
	@echo "make setup    → Install project + dev dependencies (uv sync)"
	@echo "make venv     → Create virtual environment"
	@echo "make lint     → Run ruff lint (auto-fix)"
	@echo "make format   → Format code with ruff"
	@echo "make type     → Run mypy type checking"
	@echo "make test     → Run pytest"
	@echo "make run      → Run hello_rietveld_long.py"
	@echo "make build    → Build package (wheel/sdist)"
	@echo ""

setup:
	uv sync

venv:
	uv venv

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

type:
	uv run mypy powerxrd

test:
	uv run pytest

run:
	uv run python hello_rietveld_long.py

build:
	uv build