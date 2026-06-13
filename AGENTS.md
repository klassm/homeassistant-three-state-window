# AGENTS.md

## Commands

- **Format & lint:** `uv run ruff check --fix . && uv run ruff format .`
- **Run tests:** `uv run pytest -v`
- **Install dependencies:** `uv sync --group test --group lint`

## Rules

After every code change, you MUST:

1. Run the formatter and linter: `uv run ruff check --fix . && uv run ruff format .`
2. Run the unit tests: `uv run pytest -v`
3. Fix any issues before considering the task complete.
