lint:
	uv run flake8 .
	uv run mypy .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".cache" -exec rm -rf {} +