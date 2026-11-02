VENV := .venv
UV_EXIST := $(shell command -v uv 2> /dev/null)


all: ensure install

install:
	@if [ ! -d ".venv" ]; then \
		uv sync; \
	else \
		echo "Everything is installed"; \
	fi

ensure:
ifdef UV_EXIST
	@echo "UV is installed"
else
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@. $(HOME)/.local/bin/env
	@echo "Uv sucessful installed"
endif

re: fclean install

test:
	uv run pytest

lint:
	uv run flake8 .
	uv run mypy .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

fclean: clean
	rm -rf .venv